## uninstall mysql
sudo rm /var/lib/mysql -R
sudo rm /etc/mysql -R

## remove the version you installed
sudo apt-get --purge autoremove mysql-server-5.7 mysql-common mysql-workbench
sudo apt-get remove apparmor

