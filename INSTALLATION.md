# Installing & Dependencies

### Update & Upgrade

```
sudo apt-get update
sudo apt-get upgrade
```

### Install cups
```
sudo apt-get install cups
sudo usermod -a -G lpadmin pi #(or whatever user you're using for setup/testing
sudo apt-get install printer-driver-ptouch #(For our QL-700... your driver is likely different)
```

### Configure cups & install printer
Follow: http://www.howtogeek.com/169679/how-to-add-a-printer-to-your-raspberry-pi-or-other-linux-computer/


### Install upstart (OPTIONAL)
```
sudo apt-get install upstart
```

### Install Python Dependencies
```
sudo apt-get install python-pycups
sudo apt-get install python-pip python-dev

sudo pip install evdev
```

### Install Parkomatic
```
sudo apt-get install git
git clone https://github.com/wreality/parkomatic.git
cd parkomatic
sudo ./install.sh
```

### Configure Parkomatic
```
sudo nano /etc/parkomatic/parkomatic.conf
```

### Test 
```
sudo parkomaticd
```
Swipe a card, and a label should print.  Error messages should help debug any problems.
Press Crtl-C to exit parkomaticd

### Start the actual daemon
```
sudo service parkomatic start
```



