### Purpose

A pwm control software for use with the 7inch official raspberry pi touch screen.
I put this together to control the speed of the fans in my server rack. The fans are on a 12v supply,
and I connected the individual signal inputs using an array of optocouplers I built.
![OptocouplerArray](OptocouplerArray.jpg)



### Main Screen
![MainScreen](MainScreen.png)

### Settings Screen
![SettingsScreen](SettingsScreen.png)

### Touch Keyboard
![KeyboardScreen](KeyboardScreen.png)


### Raspbian Installation

Simply download [setup.sh](https://raw.githubusercontent.com/ThomasMcVay/FanControl/master/setup.sh) and run it like so:

    sudo bash setup.sh
    
This script assumes only that you have installed the full version of raspbian, if git is missing it will install it.
    
this will clone the necessary repositories into /home/pi/FanControl, install qt, pyside, and my fork of pi-blaster. It will also create a shell script at /home/pi/StartupScript.sh that will run the program on start

The script should work on a fresh raspbian installation, qt installation on a raspberry pi can take upwards of an hour though, so be prepared to do some waiting.