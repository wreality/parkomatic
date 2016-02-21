# Parkomatic
![alt text](https://github.com/wreality/parkomatic/raw/master/pass-example-small.png "Example Parking Pass")

## Background
Parkomatic was created to allow members at [our makerspace](https://www.lansingmakersnetwork.org) to print tags to attach to their belongings that didn't fit in their member storage area.   It's probably pretty specific to LMN and how we do things, but the basic code could be useful to someone else, so enjoy.

## How it works

1. The member scans their card at the reader attached to a Raspberry PI
2. A python script pings an URL on our member management server which returns an image of the label to be printed. (expiration dates, name, etc)
3. A print job is sent to CUPs which sends the image to the Brother QL-700 label printer.

## Prerequisites
### Printer
Its probably best to get printing from CUPS working on your Raspberry PI first.  In our case, a brother QL-700 label printer was used.  Install the ptouch driver to get it working under cups. There's a lot of tutorials and walkthroughs for installing CUPS on a PI.  We'll leave that as an exercise for the reader.

### RFID Reader
We used a pretty standard (read: cheap) USB RFID reader from Amazon.  It attaches as a HID device and then we use evdev to read keystrokes.

### Raspberry PI
Step-by-step installation instructions are here: https://github.com/wreality/parkomatic/blob/master/INSTALLATION.md
## Installation
There's an installation script included which should copy everything to where it needs to be:
```
chmod +x ./install.sh 
sudo ./install.sh
```

Then modify /etc/parkomatic/parkomatic.conf to suit your needs (it needs a URL to poke for images at the very least).
## Todo

1. Currently the script caches the downloaded images and refreshes them when the current date changes.  Eventually it would be nice for the PI to continue to notify the server of the print request, but not download the images if they're cached.  That way the server can log that a label was generated.
2. CUPS is SLOOOOOOW on a Raspberry PI B.  Ideally there's a way to fix that. (We'll be trying a PI 2 first)
3. Document the installation of dependencies.

### Inspiration / Implementation Help

 * [stickerbot9000](https://github.com/Denhac/Stickerbot9000) for basics of using a QL-700 on a PI
 * [Parsing evdev](https://gist.github.com/oliversalzburg/5111996) for parsing the evdev events from the wedge.
 
