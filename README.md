<!-- PROJECT LOGO -->
# Urkal - a simple e-ink display for Google Calendar
<div align="center">
  <a href="https://github.com/BardsWork/urkal">
    <img src="docs/img/calendar.jpeg" alt="Logo" width="425" height="512">
  </a>
  <p>An eInk calendar/planner written for raspberry pi zero &amp; waveshare 800x480 display.</p>
</div>



## Hardware Required

- [Raspberry Pi Zero WH](https://www.raspberrypi.org/blog/zero-wh/) - Header pins are needed to connect to the E-Ink display
- [Waveshare 7.5" Tri-color E-Ink Display](https://www.waveshare.com/7.5inch-e-paper-hat.htm) - 800×480, 7.5inch E-Ink display HAT for Raspberry Pi.
- [3d Printed Case](www.thingiverse.com/thing:4807262) - The specific case I've used. STL can be found in `./docs/stl`


## Setting Up Raspberry Pi Zero

1. Start by flashing [Raspberrypi OS Lite](https://www.raspberrypi.org/software/operating-systems/) to a MicroSD Card. 

2. After setting up the OS, run the following commmand in the RPi Terminal, and use the [raspi-config](https://www.raspberrypi.org/documentation/computers/configuration.html) interface to setup Wifi connection, enable SSH, I2C, SPI, and set the timezone to your location.

```bash
sudo raspi-config
```

3. Run the following commands in the RPi Terminal to setup the environment to run the Python scripts.

```bash
sudo apt update
sudo apt-get install python3-pip
sudo apt-get install chromium-chromedriver
sudo apt-get install libopenjp2-7-dev
pip3 install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
pip3 install pytz
pip3 install selenium
pip3 install Pillow
```

4. Run the following commands in the RPi Terminal to install the libraries needed to drive the E-Ink display. See [this page](https://www.waveshare.com/wiki/12.48inch_e-Paper_Module) for more details.
```bash
sudo apt-get install python3-pil
sudo pip3 install RPi.GPIO
sudo pip3 install spidev
sudo apt-get install wiringpi
```

## Generating `token.json` to access Google Calendar
1. `git clone`, or download, the project files to your computer.

2. In order for you to access your Google Calendar events, it's necessary to first grant access and generate a `token.json` file. Follow the [instructions here](https://developers.google.com/calendar/api/quickstart/python). The `quickstart.py` from the tutorial is duplicated as `./lib/gcal/auth.py` for your convenience.

3. Once you run `auth.py`, a `token.json` file will be generated that is used to authenticate the API requests and retrieve calendar events.

## Setup RPI to display calendar
1. Copy all the files over to your RPi using your preferred means. 

2. Run the following command in the RPi Terminal to open crontab.
```bash
crontab -e
```
3. Specifically, add the following command to crontab so that the MagInkCal Python script runs each time the RPi is booted up.
```bash
@reboot cd /location/to/your/directory && python3 main.py
```

That's all! Your calendar should now be refreshed at the time interval that you specified. 


## License

[MIT](https://choosealicense.com/licenses/mit/)