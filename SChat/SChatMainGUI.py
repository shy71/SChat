import sys
import time
import re
from appJar import gui
from openChatWindowGUI import openChatWindowGUI

from SChat import ClientServer
from SChat import ServerConnection
from SChat import isRegister
from SChat import SChatError
import sys


class SChatMainGUI:
	def __init__(self,serveIp):
		self.serverIp=serveIp
	def checkUsername(self,username):	
		isregistered = isRegister(username)
		if not isregistered:
			if(self.app.yesNoBox("Register", "The username you chose isn't registered. \nWould you like to register it?") == False):
				return False,None
		return True,ClientServer(ServerConnection(self.serverIp,5000,None,'keys/key.pem'),username)

	def press(self,button):
		try:
			if button == "Cancel":
				self.app.stop()
			else:
				usr = self.app.getEntry("Username")
				self.app.clearEntry("Username", False)
				check,c = self.checkUsername(usr)
				if check:
					window = openChatWindowGUI(c,usr)
					window.openWindow()
					self.app.stop()
		except SChatError as er:
			self.app.errorBox('Error!', er)

	def startGui(self):
		self.app = gui("Login Window", "500x200")
		self.app.setBg("lightGreen")
		self.app.setFont(18)
		self.app.addLabel("Choose","Enter username you want to use to join:")
		self.app.addEntry("Username")
		self.app.addButtons(["Log in", "Cancel"], self.press)
		self.app.enableEnter(self.press)
		self.app.go()
	
if __name__=='__main__':
	print '##This is test and development way of runing'
	print '##For release purposes Hardcode static Server Ip into runClientGui.py and have the users run that file'
	if len(sys.argv)<2:
		print 'Usage MainWindow.py <serverIp>'
	main=SChatMainGUI(sys.argv[1])
	main.startGui()


	
