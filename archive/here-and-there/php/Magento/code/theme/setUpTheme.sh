# Copyright @ 2016 darkframexue 
# date: 2016/9/12
# version: 0.0.1

# Run this file under your theme directory,for example,if you want to 
# create a new theme `<Vendor>/<theme_name>`, then you should run this 
# file under directory:`<Your magento path>/app/design/webfront/Vendor`.

# Params: None
# Output: basic file-structure for a Magento  theme

THEME_NAME=$1

echo "create file structure for theme: $THEME_NAME"

# create root directory
mkdir $THEME_NAME
cd $THEME_NAME

touch composer.json registration.php theme.xml
mkdir etc/ i18n/ media/ web/

touch etc/view.xml
