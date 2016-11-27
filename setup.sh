apt-get update
apt-get install build-essential
apt-get install git
apt-get install cmake
apt-get install libqt4-dev
apt-get install libphonon-dev
apt-get install python2.7-dev
apt-get install libxml2-dev
apt-get install libxslt1-dev
apt-get install qtmobility-dev
apt-get install libqtwebkit-dev
apt-get install qt4-dev-tools
pip install -U PySide
cd /home/pi
git clone https://github.com/ThomasMcVay/FanControl.git
cd ./FanControl
git submodule init
git submodule update
cd ./pi-blaster
./autogen.sh
./configure
make install
pi-blaster
echo "@/home/pi/StartupScript.sh" >> /home/pi/.config/lxsession/LXDE-pi/autostart
touch /home/pi/StartupScript.sh
echo "python /usr/src/FanControl/main.py" >> /home/pi/StartupScript.sh
chmod 777 /home/pi/StartupScript.sh
echo "SETUP COMPLETE!"