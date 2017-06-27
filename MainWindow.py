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
from SChat import isRegister
import sys
app = gui("Login Window", "500x200")
app.setBg("orange")
app.setFont(18)

def checkUsername(username):	
	isregistered = isRegister(username)
	if not isregistered:
		if(app.yesNoBox("Register", "The username you chose isn't registered. \nWould you like to register it?") == False):
			return False,None
	return True,ClientServer(ServerConnection(server,5000,None,'keys/key.pem'),username)

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
if len(sys.argv)<2:
	print 'Usage MainWindow.py <serverIp>'
server=sys.argv[1]
app.addLabel("Choose","Enter username you want to use to join:")
app.addEntry("Username")
app.addButtons(["Log in", "Cancel"], press)
app.go()
