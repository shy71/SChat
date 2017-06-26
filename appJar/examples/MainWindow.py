import sys
import time
import re
sys.path.append("../../")
from appJar import gui
from chatWindow import chatWin
from openChatWindow import openChatWindow

from ClientServer import ClientServer
from M2Crypto import RSA 
from ServerConnection import ServerConnection
from random import randint
from P2PChat import P2PChat


app = gui("Login Window", "400x200")
app.setBg("orange")
app.setFont(18)


def isNotRegistered(username):
	with open('users.d','r') as f:
		return re.search('{'+username+';([a-z|0-9]+)}\n',f.read()) == None

def checkUsername(username):	
	notRegistered = isNotRegistered(username)
	if(notRegistered == True):
		if(app.yesNoBox("Register", "The username you chose isn't registered. \nWould you like to register it?") == False):
			return False,None
	rsa = RSA.load_pub_key('keys/key.pem')
	return True,ClientServer(ServerConnection('127.0.0.1',5000,None,rsa),username,not notRegistered)

def press(button):
	if button == "Cancel":
		app.stop()
	else:
		usr = app.getEntry("Username")
		check,c = checkUsername(usr)
		if check:
			window = openChatWindow(c)
			window.openWindow()
			app.stop()
		
app.addEntry("Username")
app.addLabel("Choose","Choose one of the following choices:")
app.addButtons(["Submit", "Cancel"], press)
app.go()
