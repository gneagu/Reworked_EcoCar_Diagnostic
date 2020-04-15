# ReworkedDash

> These instructions should help to install PyQt5.
> The library is great, but really finicky to install depending on Python Version, and OS.
> Instructions below are organized based on OS.
> This project utilizes Python3.8 and PyQt5.

***
### Install Instructions for PyQt5 (Nice easy way) - Windows 10
***

> Open up the Windows App Store
> Search for Python 3.8 and install it.
> Once installed, open up command line and type:

1. pip uninstall serial
2. pip install pyserial
3. pip install PyQt5

> This should hopefully be it. 


***
### Install Insctructions for PyQt5 (The easy way) - Ubuntu
***
> Please follow the below instructions. These need to be typed in the command line.

1. python3 -m venv env
2. source venv/bin/activate
3. pip3 install pyqt5

> If you have the newest version of your OS, and python3.8 installed, you should be fine. 
> If this doesn't work, follow the instructions below. 


***
### Install Insctructions for PyQt5 (The painful other way) - Ubuntu
***
> Please follow the below instructions. These need to be typed in the command line.

1. python3 -m venv env
2. source venv/bin/activate
3. pip3 install pyqt-builder

> Go to https://pypi.org/project/PyQt5/#files and download "PyQt5-5.14.2.tar.gz

> cd to the folder where you have downloaded the tar file.

4. tar -xvzf PyQt5-5.14.2.tar.gz
5. cd PyQt5-5.14.2
6. sip-install

> Be prepared to wait half a year for the PyQt5 to install.

7. pip3 install pyqt5-sip
8. pip3 install serial

**You should be done now.**
> To verify you have installed PyQt5 correctly, run:
- python3 coms_hub.py

# Original install instructions. 
https://www.riverbankcomputing.com/static/Docs/PyQt5/installation.html
