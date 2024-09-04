from __future__ import print_function

from PIL import Image, ImageDraw, ImageFont

#from lib.waveshare import epd7in5_V2
from lib.gcal.main import get_calendar_events

import datetime
import calendar
import json

def main():
    # Basic configuration settings (user replaceable)
    configFile = open('config.json')
    config = json.load(configFile)
    
    # Load configuration variables.
    screen_width = config['screenWidth']  # Width of E-Ink display. Default is landscape. 
    screen_height = config['screenHeight']  # Height of E-Ink display. Default is landscape. 
    week_start_day = config['weekStartDay']  # Monday = 0, Sunday = 6
    display_to_monitor = config['displayToMonitor']  # If TRUE, will display on dev machine instead of drawing on e-ink

    # E-paper part
    # if display_to_monitor == False:
    #     epd = epd7in5_V2.EPD()
    #     epd.init()
    #     epd.Clear()

    # Configure font
    text_font = ImageFont.truetype("font.ttc", 18)
    heading_font = ImageFont.truetype("font.ttc", 36)

    # Variables
    today = datetime.date.today()
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    todays_event_cnt = 0
    tomorrows_events = []
    day_after_events = []

    # PIL Setup
    Himage = Image.new('1', (screen_width, screen_height), 255)
    draw = ImageDraw.Draw(Himage)

    # Calendar configuration
    calendar.setfirstweekday(week_start_day)
    calendar_days = calendar.monthcalendar(today.year, today.month)

    # ----------------------------------------------------
    # Draw the mini monthly calendar on the left side.
    # ----------------------------------------------------
    draw.text(
        xy=(130, 40),
        text=today.strftime("%B"),
        font=heading_font,
        anchor="mm",
        align="center"
    )

    # POSITIONING OF FIRST ELEMENT
    x = 12
    y = 100

    days_of_week = calendar.day_abbr[-1:] + calendar.day_abbr[:-1]
    for day in days_of_week:
        x += 30
        draw.text(
            xy=(x, y),
            text=day[:1],
            font=text_font,
            anchor="mm",
            align="center"
        )

    # Print monthly calendar on the left hand side.
    for row in calendar_days:
        x = 12
        y += 30
        for day in row:
            x += 30
            if day == 0:
                continue
            if int(datetime.date.today().strftime("%d")) == day:
                draw.rounded_rectangle(((x - 16, y - 13), (x + 15, y + 12)), radius=4, fill=0)
                draw.text(
                    xy=(x, y),
                    text=str(day),
                    fill=1,
                    font=text_font,
                    anchor="mm",
                    align="center"
                )
            else:
                draw.text(
                    xy=(x, y),
                    text=str(day),
                    font=text_font,
                    anchor="mm",
                    align="center"
                )

    # ----------------------------------------------------
    # THIS IS THE START OF THE DAY-PLANNER (RIGHT) SECTION
    # ----------------------------------------------------

    # Current day     
    draw.text(
        xy=(510, 40),
        text=today.strftime("%A"),
        font=heading_font,
        anchor="mm",
        align="center"
    )

    x = 400  # start position on x-axis of event panel (right)
    y = 50  # start position on y-axis of event panel (right)
   
    # Loop trough calendar events and draw them to buffer
    events = get_calendar_events()  # retrieves events from google calendar API
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        end = event['end'].get('dateTime', event['end'].get('date'))

        if len(start) == 10:  # events that are 'whole day'-events
            startdate = datetime.datetime.strptime(start, "%Y-%m-%d")
            enddate = datetime.datetime.strptime(end, "%Y-%m-%d")
            time = ''
        if len(start) == 25:  # events that start at specific time
            startdate = datetime.datetime.strptime(start, "%Y-%m-%dT%H:%M:%S%z")
            enddate = datetime.datetime.strptime(end, "%Y-%m-%dT%H:%M:%S%z")
            time = startdate.strftime("%I:%M-") + enddate.strftime("%I:%M %p")

            if startdate.date() == today:
                todays_event_cnt += 1
                y += 40
                draw.text((x - 120, y), time, font=text_font)
                draw.text((x + 25, y), event['summary'], font=text_font)
            elif (startdate.date() == tomorrow):
                tomorrows_events.append(event)

    if (todays_event_cnt < 2):

        if (todays_event_cnt == 0):
            draw.text((325, 75), "There are no more events scheduled for today.", font=text_font)

        if (len(tomorrows_events) > 0):
            _x = 400  # start position on x-axis of events on e-ink screen
            _y = 150  # start position on y-axis of events on e-ink screen
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                end = event['end'].get('dateTime', event['end'].get('date'))

                if len(start) == 10:  # events that are 'whole day'-events
                    startdate = datetime.datetime.strptime(start, "%Y-%m-%d")
                    enddate = datetime.datetime.strptime(end, "%Y-%m-%d")
                    time = ''
                if len(start) == 25:  # events that start at specific time
                    startdate = datetime.datetime.strptime(start, "%Y-%m-%dT%H:%M:%S%z")
                    enddate = datetime.datetime.strptime(end, "%Y-%m-%dT%H:%M:%S%z")
                    time = startdate.strftime("%I:%M-") + enddate.strftime("%I:%M %p")

                    if startdate.date() == tomorrow:
                        # Tomorrow's day Name
                        draw.text(
                            xy=(510, 150),
                            text=tomorrow.strftime("%A"),
                            font=heading_font,
                            anchor="mm",
                            align="center"
                        )
                        _y += 40
                        draw.text((_x - 120, _y), time, font=text_font)
                        draw.text((_x + 25, _y), event['summary'][:100], font=text_font)
                    else:
                        day_after_events.append(event)

    Himage.show()
    
    # Display buffer on the screen
    # if display_to_monitor == False:
    #     epd.display(epd.getbuffer(Himage))
    #     epd.sleep()
    # else: 
    #     Himage.show()


if __name__ == '__main__':
    main()
