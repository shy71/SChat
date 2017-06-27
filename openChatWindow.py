from SChat import ClientServer
from M2Crypto import RSA 
from SChat import ServerConnection
from SChat import SChatError
from random import randint
from SChat import P2PChat
from chatWindow import chatWin
import threading
import sys
import time
from appJar import gui

class openChatWindow:
	def __init__(self,server,username):#,username,ip,sharedKey,nounce,token
		self.app2 = gui("Options Window","400x200")
		self.server = server
		self.username = username
		self.incom=[]
	def waitForChatPolling(self):
		try:
			while True:
				p = P2PChat(self.username)
				p.waitForRequest()
				p.LoadChat()
				while self.openingWin:
					pass
				self.incom.append(p)				
				#recv_thread = threading.Thread(target=cwindow.openWindow)
				#recv_thread.setDaemon(True)
				#recv_thread.start()
				#openchatwindow with that user
		except SChatError as er:
			app.errorBox('Error!', er)
	def chatf(self,button):
		cht = self.app2.getEntry("chat")
		dIp,sharedkey, nounce,token= self.server.getInfo(cht)
		p=P2PChat(self.username) #<-need username
		p.startChat(cht,dIp,5002,sharedkey,nounce,token)
		p.LoadChat()
		cwindow = chatWin(p)
		cwindow.openWindow()
	def exit(self,button):
		self.app2.stop()
	
	def checkRequests(self):
		self.openingWin=True
		for item in self.incom:
			cwindow = chatWin(item)
			cwindow.openWindow()
		self.incom=[]
		self.openingWin=False

	
	def openWindow(self):
		try:
			self.app2.setBg("lightGreen")
			self.app2.setFont(14)
			self.app2.setSticky("sewn")
			self.app2.setExpand("both")
			self.app2.addLabel("l1","Chat with:",0,0)
			self.app2.addEntry("chat",1,0)
			self.app2.addLabel("l2","",2,0)
			self.app2.addButton("Open Chat",self.chatf,3,0)
			self.app2.addVerticalSeparator(0,1,1,4, colour="red")
			self.app2.addButton("Exit",self.exit,3,2)
			recv_thread = threading.Thread(target=self.waitForChatPolling)
			recv_thread.setDaemon(True)
			recv_thread.start()
			self.app2.setPollTime(1000)
			self.app2.registerEvent(self.checkRequests)
			self.app2.go()
		except SChatError as er:
			app.errorBox('Error!', er)
	
		
