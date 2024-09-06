# Urkal: An E-Ink Display for Google Calendar
<div align="center">
  <a href="https://github.com/BardsWork/urkal">
    <img src="docs/img/calendar.jpeg" alt="Logo" width="425" height="512">
  </a>
  <p>An eInk calendar/planner built for Raspberry Pi Zero &amp; Waveshare 800x480 display.</p>
</div>

## Overview
The inspiration for this project stemmed from my desire to have a simple, desk-mounted calendar that automatically updates and 
provides an overview of my upcoming events along with a small calendar. While there are other projects that offer more customization, 
my goal was simplicity. I wanted the device to blend into the background and "just work."

### What problem does it solve?
It helps me keep track of my upcoming events and avoid double bookings, providing a calendar view—nothing more, nothing less.

While other projects may opt for rechargeable batteries, I found that unnecessary for a device that remains plugged in on my desk. 
This choice simplifies the build process and allows the device to fade into the background without requiring regular charging.

## Installation Instructions

### Hardware
- [Raspberry Pi Zero WH](https://www.raspberrypi.org/blog/zero-wh/) - Header pins are necessary to connect to the E-Ink display.
- [Waveshare 7.5" Tri-color E-Ink Display](https://www.waveshare.com/7.5inch-e-paper-hat.htm) - 800×480, 7.5-inch E-Ink display HAT.
- [3D Printed Case](www.thingiverse.com/thing:4807262) - The specific case I've used is available in `./docs/stl`.
- RPi Power Supply
- SD Card

### Waveshare Display
The drivers for my particular display are included in the `./lib/waveshare` folder. I've simplified the code by removing non-RPi 
components from `./lib/waveshare/epdconfig.py` in compliance with Waveshare's license.

For updated drivers and additional supported devices, please refer to the [official wiki](https://www.waveshare.com/wiki/7.5inch_e-Paper_HAT). 
The included Waveshare code is for the 7.5-inch display sold prior to September 2023. For newer devices, visit the wiki for updated code and follow the official documentation.

### Printing the Waveshare Case
The case I've used is available on [Thingiverse](https://www.thingiverse.com/thing:4807262), created by [Cybernetic](https://www.thingiverse.com/cybernetic/designs). 
For convenience, the STL files are included in the `./docs/stl` folder along with the description and license. M2 screws and heated inserts secure the case. 
If you don't have access to a 3D printer, cases are available from Amazon, DigiKey, AliExpress, and eBay.

### Preparing the SD Card with Raspberry Pi OS
If your SD card doesn't already have the Raspberry Pi OS or if you want to reset your Raspberry Pi, you can easily install Raspberry Pi OS yourself. 
he official documentation is easy to follow for flashing the OS onto your SD card.

  > [Setting up your Raspberry Pi Official Documentation](https://projects.raspberrypi.org/en/projects/raspberry-pi-setting-up/2)

A Lite OS or Standard 32-bit are the best options for this installation. The Imager app provides configuration options for hostname, device username and password, 
WiFi credentials, SSH, etc., to simplify the installation process. You will need to SSH into the device to complete the installation process.

### Configuring the Raspberry Pi
Once the Raspberry Pi is powered on with an SD card containing the OS, you'll need to SSH into the device to update the software and install the necessary packages.

Once you've SSH'd into the device, run the following commands:

```bash
sudo apt update
sudo apt upgrade
sudo apt-get install python3-pip
sudo pip3 install spidev
sudo pip3 install RPi.GPIO
```

> `spidev` and `RPi.GPIO` are not part of the requirements.txt file and must be installed manually. They require a Linux environment, so the installation will fail under development mode in Windows or MacOS.


## Enabling Google Calendar Integration
1. `git clone https://github.com/BardsWork/urkal`, or download the project files to your computer.

2. To access your Google Calendar events, you need to grant access and generate a `token.json` file. Follow the 
[instructions here](https://developers.google.com/calendar/api/quickstart/python). The `quickstart.py` from the tutorial is duplicated as `./lib/gcal/auth.py` for your convenience. 

- If this is your first project, its best to follow the official documentation step-by-step.

- If you're comfortable creating API keys, update the path of your `credentials.json` file within `auth.py` to generate the
`token.json` file.

3. Once you run `auth.py`, a `token.json` file will be generated to authenticate the API requests and retrieve calendar events.
Place the `token.json` file in the `./lib/gcal` folder. 

> `./lib/gcal/token.json` and `./lib/gcal/credentials.json` paths have been added to `.gitignore`. If you change the location, 
update the file to avoid committing sensitive information to a public repository.



## Setup RPI to display calendar
1. Copy all the files over to your RPi using your preferred means. 

2. Create a cron job to update the calendar every hour within the RPi Terminal:
```bash
crontab -e
```

3. Within the crontab, add the following code to set the update frequency:
```bash
0 * * * * /usr/bin/python3 /path/to/your/python/script.py
```

This will run the script every hour at the 0th minute. To run the script every 15 minutes, the crontab entry would look like this:
```bash
*/15 * * * * /usr/bin/python3 /path/to/your/python/script.py
```

4. Save and exit the editor.

Make sure to replace `/path/to/your/python/script.py` with the actual path to your Python script. You may also need to replace 
`/usr/bin/python3` with the path to your Python interpreter if it's installed in a different location.

That's it! Your calendar should now refresh at the specified intervals.


## License

[MIT](https://choosealicense.com/licenses/mit/)