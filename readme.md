Setup Instructions for kali linux
--------------------------
To use ProxyChain Manager you must have the following dependencies installed

open the terminal and type:

-sudo apt update

-sudo apt-get update

-sudo apt install tor

-sudo apt install proxychains

check to make sure you have the .conf file:
----------------------------------------------
-sudo vim /etc/proxychains.conf

if it's there just close out the tab.

Next Step
---------------
download the PCM.py file or drag and drop the code into your own file.

move the PCM.py file to your desktop

right click the PCM.py file and select open with terminal 

run the command -python PCM.py

Using the GUI
-------------------
press the start tor button to start tor

press the stop tor button to stop tor

press the edit proxychains config button to bring up the /etc/proxychains.conf file

where it says "Enter command to run through proxychains" type in a command you want to use (for example. type "firefox dnsleak.com") when the run command button is pressed it will take you to the site entered using proxychains

where it says "Enter URL to navigate using proxychains" type in a website you want to go to (for example. type in "dnsleak.com") when the the Navigate to URL button is pressed it will take you to the site entered using proxychains

select the proxychain type by clicking the chain type, tyhen click the update proxychain type button and it will update your settings in the /etc/proxychains.conf file

press the ping servers button to ping the servers listed in the /etc/proxychains.conf file

execute commands through the Terminal section and hit the Execute command button to run the command (for example. "sudo systemctl status tor")

press the clear log button to clear the log

Adding more proxies
------------------------------
press the edit proxychains config button to bring up the /etc/proxychains.conf file

scroll to the button and press "S" on your keyboard, this will allow you to type

add a new proxy by entering the type, ip and port (for example. "socks5  142.54.239.1  4145")

once you have typed in your new proxy hit the esc key on your keyboard

now press shift and : 

type wq and press enter

test the new proxie by presseing the ping servers button


XYZ
----------------------
i made this in like two days, i know its not very good and probably not useful to anyone but i thought id share it anyways lol if anyone wants to help make this better please do so, i would love the help making this project even more than what it is. But for now it kinda works so we'll just leave it at that haha. 

if the feds are seeing this, i did this for fun. no harm intended :)
