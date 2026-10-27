# Copyright @ 2016 darkframexue
# date: 2016/9/13
# version: 0.0.1

echo "set up PHP with apache and MySQL..."

# install basic options
echo "install php apache and mysql..."
sudo apt-get update
# if you are using ubuntu 15.* or older enable the next line of code.  
#sudo add-apt-repository ppa:ondrej/php
sudo apt-get install php7.0 php7.0-mysql
sudo apt-get install apache2.0 libapache2-mod-php7.0
sudo apt-get mysql-server

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
sudo apt-get install php7.0-fpm \
php7.0-intl \
php7.0-zip \
php7.0-gd \
php7.0-dom \
php7.0-curl \
php7.0-mbstring \
php7.0-mcrypt \
php7.0-soap \
php7.0-xml \
php7.0-xsl \
php7.0-json \
php7.0-iconv

# restart apache2
echo "restart server..."
sudo /etc/init.d/apache2 restart
