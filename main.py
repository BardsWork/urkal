from __future__ import print_function

from PIL import Image, ImageDraw, ImageFont

# from lib.waveshare import epd7in5_V2
from lib.gcal.main import get_events

import datetime
from datetime import date
import calendar

EPD_WIDTH = 800
EPD_HEIGHT = 480


def main():
    # E-paper part
    # epd = epd7in5_V2.EPD()
    # epd.init()
    # epd.Clear()

    font12 = ImageFont.truetype("./fonts/font.ttc", 12)
    font14 = ImageFont.truetype("./fonts/font.ttc", 14)
    font15 = ImageFont.truetype("./fonts/font.ttc", 15)
    font18 = ImageFont.truetype("./fonts/font.ttc", 18)
    font24 = ImageFont.truetype("./fonts/font.ttc", 30)
    font56 = ImageFont.truetype("./fonts/font.ttc", 72)

    Himage = Image.new('1', (EPD_WIDTH, EPD_HEIGHT), 255)
    draw = ImageDraw.Draw(Himage)

    # TODAY
    draw.text((20, 20), date.today().strftime("%d"), font=font56, fill=0)
    draw.text((110, 30), date.today().strftime("%B"), font=font24, fill=0)
    draw.text((110, 60), date.today().strftime("%A"), font=font24, fill=0)

    # CALENDAR SETUP
    events = get_events()  # retrieves events from google calendar API
    today = datetime.date.today()  # needed to filter elements
    calendar.setfirstweekday(6)  # formats the calendar to start on sunday
    calendar_days = calendar.monthcalendar(today.year, today.month)  # provides current year and month
    days_of_week = calendar.day_abbr[-1:] + calendar.day_abbr[:-1]  # calendar starts on Monday but we want Sunday

    # POSITIONING OF FIRST ELEMENT
    calendar_y = 0
    calendar_x = 150
    calendar_offset = 30

    # PRINT DAYS OF THE WEEK
    for day in days_of_week:
        calendar_y += calendar_offset
        draw.text((calendar_y, calendar_x), day[:2], font=font18)

    # PRINT CALENDAR MONTH DAYS IN CALENDAR FORMAT
    for row in calendar_days:
        calendar_y = 0  # resets starting position
        calendar_x += calendar_offset

        for day in row:
            calendar_y += calendar_offset
            if day > 0:  # zero means no date to draw
                draw.text((calendar_y, calendar_x), str(day), font=font18)

    # Loop trough calendar events and draw them to buffer
    x = 400  # start position on x-axis of events on e-ink screen
    y = 30  # start position on y-axis of events on e-ink screen
    current_week = ''  # variable for week of event
    current_day = ''  # variable for day of event

    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        end = event['end'].get('dateTime', event['end'].get('date'))
        summary = event['summary']
        start_date = None
        end_date = None

        if len(start) == 10:  # events that are 'whole day'-events
            start_date = datetime.datetime.strptime(start, "%Y-%m-%d")
            end_date = datetime.datetime.strptime(end, "%Y-%m-%d")
            time = ''
        if len(start) == 25:  # events that start at specific time
            start_date = datetime.datetime.strptime(start, "%Y-%m-%dT%H:%M:%S%z")
            end_date = datetime.datetime.strptime(end, "%Y-%m-%dT%H:%M:%S%z")
            time = start_date.strftime(" (%H:%M -")
            fin_time = end_date.strftime(" %H:%M) ")

            start_offset = abs(8 - int(start_date.strftime("%H")))
            end_offset = abs(8 - int(end_date.strftime("%H")))
            x1 = 380
            x2 = 540
            y1 = 102 + (start_offset * 60) + int(start_date.strftime("%M"))
            y2 = 98 + (end_offset * 60) + int(end_date.strftime("%M"))
            draw.rounded_rectangle((x1, y1, x2, y2), radius=4, fill=None, outline=None, width=1)
            draw.text((x1, y1), summary)

        startdate_date = start_date.date()
        if startdate_date < date.today():
            start_date = date.today()
            startdate_date = date.today()
        day = start_date.strftime("%a %m-%d")
        week = start_date.strftime("%V")

        if current_week != week and startdate_date != date.today():
            if week == date.today().strftime("%V"):
                x = 550
                y = 30
                draw.text((x, y), 'LATER THIS WEEK', font=font18, fill=0)
            # elif (int(week) == int(date.today().strftime("%V")) + 1):
            #    x = 530
            #    y = 25
            #    draw.text((x, y), 'NEXT WEEK', font=font18, fill=0)
            else:
                break
            current_week = week
            y = y + 25

        if current_day != day and startdate_date != date.today():
            draw.text((x, y + 4), day.upper(), font=font18, fill=0)
            current_day = day
            y = y + 20

        draw.text((x, y), ' ' + event['summary'] + time + fin_time, font=font15, fill=0)
        y = y + 20

    # REFRESH TIME
    now = datetime.datetime.now()
    draw.text((700, 465), 'Update: ' + now.strftime('%H:%M'), font=font14, fill=0)

    # Vertical line to split the calendar, each section is 200px wide
    draw.line((560, 100, 560, 460), width=3)

    # Horizontally, we have 420 pixels, having 7 sections, each hour is 60px tall
    text_start = 320
    draw.text((text_start, 92), '8am', font=font12)
    draw.text((text_start, 152), '9am', font=font12)
    draw.line((360, 100, 760, 100), width=2)
    draw.line((360, 160, 760, 160), width=1)

    draw.text((text_start, 212), '10am', font=font12)
    draw.text((text_start, 272), '11am', font=font12)
    draw.line((360, 220, 760, 220), width=2)
    draw.line((360, 280, 760, 280), width=1)

    draw.text((text_start, 332), 'noon', font=font12)
    draw.text((text_start, 392), '1pm', font=font12)
    draw.line((360, 340, 760, 340), width=2)
    draw.line((360, 400, 760, 400), width=1)

    # Display buffer on the screen
    # epd.display(epd.getbuffer(Himage))
    Himage.show()


if __name__ == '__main__':
    main()
