from ClientServer import ClientServer
from M2Crypto import RSA 
from ServerConnection import ServerConnection
from random import randint
from P2PChat import P2PChat


import sys
import time
sys.path.append("../../")
from appJar import gui

class openChatWindow:
	def __init__(self,server):#,username,ip,sharedKey,nounce,token
		self.app2 = gui("Login Window","400x200")
		self.server = server
		pass
	
	def chatf(self,button):
		cht = self.app2.getEntry("chat")
		dIp,sharedkey, nounce,token= self.server.getInfo(cht)
		p=P2PChat()
		p.startChat(cht,dIp,5002,sharedkey,nounce,token)
		p.LoadChat()
	def exit(self,button):
		self.app2.stop()
		
	def openWindow(self):
		self.app2.setBg("lightBlue")
		self.app2.setFont(14)
		self.app2.setSticky("sewn")
		self.app2.setExpand("both")
		self.app2.addLabel("l1","Chat with:",0,0)
		self.app2.addEntry("chat",1,0)
		self.app2.addLabel("l2","",2,0)
		self.app2.addButton("Open Chat",self.chatf,3,0)
		self.app2.addVerticalSeparator(0,1,1,4, colour="red")
		self.app2.addButton("Exit",self.exit,3,2)
		self.app2.go()
		