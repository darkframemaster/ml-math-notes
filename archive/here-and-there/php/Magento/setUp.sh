# set up php lib
echo "install php and php-lib"

sudo apt-get update
sudo apt-get install -y php7.0
sudo apt-get install -y php7.0-fpm \
php7.0-mysql \
php7.0-intl \
php7.0-zip \
php7.0-gd \
php7.0-dom \
imagemagick \
php7.0-curl \
php7.0-mbstring \
php7.0-mcrypt \
php7.0-soap \
php7.0-xml \
php7.0-xsl \
php7.0-json \
php7.0-iconv

#setup magento2
echo "install magento2..."


MAGE_HOSTNAME=yourhostname
MAGE_MODE_APP=developer
MAGE_PATH=/path/to/your/magento2

mkdir $MAGE_PATH
cd $MAGE_PATH

# Install Magento 2
sudo git clone https://darkframexue@bitbucket.org/devwyingo/wyingo-magento2-extension.git $MAGE_PATH
composer install

# set permissions
sudo find var vendor pub/static pub/media app/etc -type f -exec chmod u+w {} \;
sudo find var vendor pub/static pub/media app/etc -type d -exec chmod u+w {} \;
sudo chown -R www-data:www-data .
sudo chmod u+x bin/magento


# setup database
MYSQL_DATABASE=your_db_name
MYSQL_USER=your_db_manager_name
MYSQL_PASSWORD=your_db_passwd

mysql -u root -p -e "CREATE USER '$MYSQL_USER'@'localhost' IDENTIFIED BY '$MYSQL_PASSWORD';"
mysql -u root -p -e "CREATE DATABASE $MYSQL_DATABASE;"
mysql -u root -p -e "GRANT ALL PRIVILEGES ON ${MYSQL_DATABASE}.* TO '$MYSQL_USER';"

mysql -u $MYSQL_DATABASE -p $MYSQL_PASSWORD

cd ./bin/
sudo ./magento setup:install \
  --db-host=localhost \
  --db-name=$MYSQL_DATABASE \
  --db-user=$MYSQL_USER\
  --db-password=$MYSQL_PASSWORD \
  --base-url=http://$MAGE_HOSTNAME/ \
  --admin-firstname=your_first_name \
  --admin-lastname=your_last_name \
  --admin-email=yourname@email.com \
  --admin-user=site_admin_user_name \
  --admin-password=passwd_for_site_admin_user \
  --backend-frontname=whatever \
  --language=zh_Hans_CN \
  --currency=JPY \
  --timezone=Asia/Tokyo \
  --sales-order-increment-prefix=WO \
  --use-rewrites=1
