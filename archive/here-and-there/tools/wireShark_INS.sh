sudo apt-get update
sudo apt-get install wireshark

# add group for wireshark
sudo groupadd wireshark
sudo chgrp wireshark /usr/bin/dumpcap
sudo chmod 4755 /usr/bin/dumpcap

# add user to wireshark group
sudo gpasswd -a darkframexue wireshark
