apt-get -y update
apt-get -y install build-essential
apt-get -y install dh-autoreconf
apt-get -y install git
apt-get -y install cmake
apt-get -y install libqt4-dev
apt-get -y install libphonon-dev
apt-get -y install python2.7-dev
apt-get -y install libxml2-dev
apt-get -y install libxslt1-dev
apt-get -y install qtmobility-dev
apt-get -y install libqtwebkit-dev
apt-get -y install qt4-dev-tools
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
echo "python /home/pi/FanControl/main.py" >> /home/pi/StartupScript.sh
chmod 777 /home/pi/StartupScript.sh
echo "SETUP COMPLETE!"
python /home/pi/FanControl/main.py