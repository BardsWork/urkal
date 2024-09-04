<!-- PROJECT LOGO -->
# Urkal
<div align="center">
  <a href="https://github.com/BardsWork/bsm-sheets">
    <img src="docs/img/logo.png" alt="Logo" width="512" height="512">
  </a>
  <p>An eInk calendar/planner written for raspberry pi zero &amp; waveshare 800x480 display.</p>
</div>



## Hardware Required

- [Raspberry Pi Zero WH](https://www.raspberrypi.org/blog/zero-wh/) - Header pins are needed to connect to the E-Ink display
- [Waveshare 7.5" Tri-color E-Ink Display](https://www.waveshare.com/product/raspberry-pi/displays/e-paper/7.5inch-e-paper-hat-b.htm?___SID=U) - Black & white display is sufficient but newer displays are tri-colored.


## Setting Up Raspberry Pi Zero

1. Start by flashing [Raspberrypi OS Lite](https://www.raspberrypi.org/software/operating-systems/) to a MicroSD Card. (March 2023 Edit: If you're still using the original Raspberry Pi Zero, there are [known issues](https://forums.raspberrypi.com/viewtopic.php?t=323478) between the latest RPiOS "bullseye" release and chromium-browser, which is required to run this code. As such, I would recommend that you keep to the legacy "buster" OS if you're still running this on older RPiO hardware.)

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

5. Run the following commands in the RPi Terminal to install the web interface for PiSugar2 display. See [this page](https://github.com/PiSugar/PiSugar/wiki/PiSugar2) for more details. After running the command, you would be able to access the web interface at http://your_raspberry_ip:8421 in your browser. From there you should be able to specify when you wish to schedule the PiSugar2 boot up your RPi.
```bash
curl http://cdn.pisugar.com/release/Pisugar-power-manager.sh | sudo bash
```

6. Download the over the files in this repo to a folder in your PC first. 

7. In order for you to access your Google Calendar events, it's necessary to first grant the access. Follow the [instructions here](https://developers.google.com/calendar/api/quickstart/python) on your PC to get the credentials.json file from your Google API. Don't worry, take your time. I'll be waiting here.

8. Once done, copy the credentials.json file to the "gcal" folder in this project. Run the following command on your PC. A web browser should appear, asking you to grant access to your calendar. Once done, you should see a "token.pickle" file in your "gcal" folder.

```bash
python3 auth.py
```

9. Copy all the files over to your RPi using your preferred means. 

10. Run the following command in the RPi Terminal to open crontab.
```bash
crontab -e
```
11. Specifically, add the following command to crontab so that the MagInkCal Python script runs each time the RPi is booted up.
```bash
@reboot cd /location/to/your/maginkcal && python3 maginkcal.py
```

12. That's all! Your Magic Calendar should now be refreshed at the time interval that you specified in the PiSugar2 web interface! 

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)