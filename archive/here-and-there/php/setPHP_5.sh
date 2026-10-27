# Copyright @ 2016 darkframexue
# date: 2016/9/13
# version: 0.0.1

echo "set up PHP with apache and MySQL..."

# install basic options
echo "install php apache and mysql..."
sudo apt-get update
sudo apt-get install php5 php5-mysql
sudo apt-get install apache2 libapache2-mod-php5
sudo apt-get install mysql-server

# check the installations
clear
echo "check the installations:"
apache2 -v
php -v
mysql -V
sleep 5

# install extensions of php
# These extensions is required by Magento2
echo "install extensions of php..."
sudo apt-get install php5-fpm \
php5-intl \
php5-zip \
php5-gd \
php5-dom \
php5-curl \
php5-mbstring \
php5-mcrypt \
php5-soap \
php5-xml \
php5-xsl \
php5-json \
php5-iconv

# restart apache2
echo "restart server..."
sudo service apache2 restart
