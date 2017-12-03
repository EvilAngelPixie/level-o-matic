# level-o-matic
Python code for TOM Melbourne 2017 Team 8 "level-o-matic" liquid level sensor

### Raspberry Pi (3B) Bluetooth
If you are having bluetooth issues, this worked for us:
- update OS
- update bluetooth drivers
- turn on Pi bluetooth manager to assign serial port post pair
- use bluetooth_terminal to check receipt of sensor data

Useful links:
https://www.hackster.io/user16726/raspberry-pi-bluetooth-terminal-f7e9bd

### Other useful Raspberry Pi things
- sudo shutdown -P now
- Schematics: https://www.raspberrypi.org/documentation/hardware/raspberrypi/schematics/Raspberry-Pi-3B-V1.2-Schematics.pdf
- Button basics: https://www.cl.cam.ac.uk/projects/raspberrypi/tutorials/robot/buttons_and_switches/
- Text to speech basics: https://learn.adafruit.com/speech-synthesis-on-the-raspberry-pi/speak-easier-flite
