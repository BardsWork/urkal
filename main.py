from __future__ import print_function
from PIL import Image, ImageDraw, ImageFont
from lib.gcal.main import get_calendar_events

import os
import json
import datetime
import calendar


def main():
    """Main function to render calendar and events on an e-ink display."""

    # Load configuration settings
    with open('config.json') as config_file:
        config = json.load(config_file)
    
    # Configuration variables
    screen_width = config['screenWidth']  # E-Ink display width (landscape)
    screen_height = config['screenHeight']  # E-Ink display height (landscape)
    week_start_day = config['weekStartDay']  # Monday = 0, Sunday = 6
    development_mode = config['development']  # Development mode disables the e-ink display

    # Waveshare library initialization & setup.
    if not development_mode:
        from lib.waveshare import epd7in5_V2
        epd = epd7in5_V2.EPD()
        epd.init()
        epd.Clear()

    # Configure fonts
    font_path = os.path.join(os.path.dirname(__file__), 'lib', 'fonts', 'font.ttc')
    text_font = ImageFont.truetype(font_path, 18)
    heading_font = ImageFont.truetype(font_path, 36)

    # Date variables
    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)
    todays_event_count = 0
    tomorrows_events = []
    day_after_events = []

    # PIL setup for image buffer
    Himage = Image.new('1', (screen_width, screen_height), 255)
    draw = ImageDraw.Draw(Himage)

    # Calendar configuration
    calendar.setfirstweekday(week_start_day)
    calendar_days = calendar.monthcalendar(today.year, today.month)

    # Draw mini monthly calendar on the left side
    draw.text(
        xy=(130, 40),
        text=today.strftime("%B"),
        font=heading_font,
        anchor="mm",
        align="center"
    )

    # The positioning for abreviations of the days of the week for the mini cal.
    x = 12
    y = 100

    # Display days of the week
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

    # Display monthly calendar days (1 - 31)
    for row in calendar_days:
        x = 12
        y += 30
        for day in row:
            x += 30
            if day == 0:
                continue
            if int(today.strftime("%d")) == day:
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

    # Daily events section (right hand side)
    draw.text(
        xy=(510, 40),
        text=today.strftime("%A"),
        font=heading_font,
        anchor="mm",
        align="center"
    )

    x = 400  # X-axis start position for the event panel
    y = 50  # Y-axis start position for the event panel

    # Retrieve and display events
    events = get_calendar_events()
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        end = event['end'].get('dateTime', event['end'].get('date'))

        if len(start) == 10:  # Whole-day events
            start_date = datetime.datetime.strptime(start, "%Y-%m-%d")
            end_date = datetime.datetime.strptime(end, "%Y-%m-%d")
            time = ''
        elif len(start) == 25:  # Timed events
            start_date = datetime.datetime.strptime(start, "%Y-%m-%dT%H:%M:%S%z")
            end_date = datetime.datetime.strptime(end, "%Y-%m-%dT%H:%M:%S%z")
            time = start_date.strftime("%I:%M-") + end_date.strftime("%I:%M %p")

            if start_date.date() == today:
                todays_event_count += 1
                y += 40
                draw.text((x - 120, y), time, font=text_font)
                draw.text((x + 25, y), event['summary'], font=text_font)
            elif start_date.date() == tomorrow:
                tomorrows_events.append(event)

    # Handle case when there are fewer than two events today
    if todays_event_count < 2:
        if todays_event_count == 0:
            draw.text((325, 75), "There are no more events scheduled for today.", font=text_font)

        if tomorrows_events:
            _x = 400  # X-axis start for tomorrow's events
            _y = 150  # Y-axis start for tomorrow's events
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                end = event['end'].get('dateTime', event['end'].get('date'))

                if len(start) == 10:
                    start_date = datetime.datetime.strptime(start, "%Y-%m-%d")
                    end_date = datetime.datetime.strptime(end, "%Y-%m-%d")
                    time = ''
                elif len(start) == 25:
                    start_date = datetime.datetime.strptime(start, "%Y-%m-%dT%H:%M:%S%z")
                    end_date = datetime.datetime.strptime(end, "%Y-%m-%dT%H:%M:%S%z")
                    time = start_date.strftime("%I:%M-") + end_date.strftime("%I:%M %p")

                    if start_date.date() == tomorrow:
                        # Display tomorrow's day name
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

    # Display buffer on the screen
    if not development_mode:
        epd.display(epd.getbuffer(Himage))
        epd.sleep() # sleep MUST be used to prevent physically damaging e-ink display.
    else:
        Himage.show()


if __name__ == '__main__':
    main()
