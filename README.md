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

simply download and run

    sudo setup.sh
    
this will install the qt library, pyside, and my fork of pi-blaster. It will also create a shell script at /home/pi/StartupScript.sh that will run the program on start
