import sys
import time
import re
from appJar import gui
from chatWindow import chatWin
from openChatWindow import openChatWindow

from SChat import ClientServer
from M2Crypto import RSA 
from SChat import ServerConnection
from random import randint
from SChat import P2PChat


app = gui("Login Window", "500x200")
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
	return True,ClientServer(ServerConnection('127.0.0.1',5000,None,'keys/key.pem'),username,not notRegistered)

def press(button):
	if button == "Cancel":
		app.stop()
	else:
		usr = app.getEntry("Username")
		check,c = checkUsername(usr)
		if check:
			window = openChatWindow(c,usr)
			window.openWindow()
			app.stop()

app.addLabel("Choose","Enter username you want to use to join:")
app.addEntry("Username")
app.addButtons(["Log in", "Cancel"], press)
app.go()
