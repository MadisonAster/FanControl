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


### Installation

sudo apt-get update
sudo apt-get install build-essential
sudo apt-get install git
sudo apt-get install cmake
sudo apt-get install libqt4-dev
sudo apt-get install libphonon-dev
sudo apt-get install python2.7-dev
sudo apt-get install libxml2-dev
sudo apt-get install libxslt1-dev
sudo apt-get install qtmobility-dev
sudo apt-get install libqtwebkit-dev
sudo apt-get install qt4-dev-tools
sudo pip install -U PySide
cd /home/pi
git clone https://github.com/ThomasMcVay/FanControl.git
cd ./FanControl
git submodule init
git submodule update
cd ./pi-blaster
./autogen.sh
./configure
sudo make install

sudo pi-blaster
sudo echo "@/home/pi/StartupScript.sh" >> /home/pi/.config/lxsession/LXDE-pi/autostart
sudo touch /home/pi/StartupScript.sh
sudo echo "python /usr/src/FanControl/main.py" >> /home/pi/StartupScript.sh
sudo chmod 777 /home/pi/StartupScript.sh