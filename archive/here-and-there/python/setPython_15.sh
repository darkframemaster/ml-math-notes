# Copyright @ 2016 darkframexue 
# date: 2016/9/13 
# version: 0.0.0

echo "set up python extensions..."

# Install Flask
echo "set up flask:"

sudo apt-get install python3-pip
sudo pip3 install Flask
sudo pip3 install Flask-SQLAlchemy \
Flask-WTF \
Flask-Login \
Flask-OpenID \
rauth # rauth is a module for authentication and authenrization

# check
clear
pip3 list | grep lask
sleep 3


# Install database surport
echo "Install MySQL and mongoDB..."
# install MySQL and check
sudo apt-get install mysql-server
clear
mysql -V
sleep 2
sudo pip3 install mysql-connector-python

# install mongoDB and check
sudo apt-get install mongodb
clear
mongo --version
sleep 2
sudo pip3 install pymongo


# Machine learning & Computer vision
echo "Install machine learning and computer vision extensions..."
sudo apt-get install python3-numpy \
python3-scipy \
python3-matplotlib
