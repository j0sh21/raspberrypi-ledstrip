# Raspberry Pi & LED-Strip
## Hardware setup
Use the following pins:
- GPIO17 for red
- GPIO27 for green
- GPIO22 for blue

Note: I used an external power supply for the LEDs 12v and ground connections.

## Software setup
```bash
apt install pigpio python3-pip
pip3 install pigpio
chmod u+x rgb-launcher.sh
./rgb-launcher.sh
```

### Set script to run on reboot (optional)
```bash
crontab -e
# insert the path to the script and save
@reboot /home/pi/repos/raspberrypi-ledstrip/rgb-launcher.sh
```

## Useful links
[Here](http://dordnung.de/raspberrypi-ledstrip/) you can find a tutorial about how to connect a Raspberry Pi to a LED-Strip
[Here](http://www.instructables.com/id/Raspberry-Pi-Launch-Python-script-on-startup/) is a tutorial for running **fading.py** on boot
