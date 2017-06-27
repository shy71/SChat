import sys
import time
from appJar import gui
from SChat import SChatError
import threading

class chatWin:
	def __init__(self,pchat):#,username,ip,sharedKey,nounce,token
		self.app2 = gui("Chat Window","400x400")
		self.pchat = pchat
		self.username = pchat.suser
		self.peerUsername = pchat.duser
		self.msgChanged=False
		self.exit=False
	def chatf(self,button):
		cht = self.app2.getEntry("chat")
		#msgText = self.app2.getLabel("chattext") + '\n' + cht
		self.pchat.output(cht)
		self.app2.addListItem("list",self.username + ": " + cht)
		#make it change the stream and update the label here too
		print cht
	def updateChatPolling(self):
		while True:
			msg = self.pchat.input()
			if not msg == None:
				self.app2.addListItem("list",self.peerUsername + ": " + msg)
			#get updated stream from method which shy will implement
			#update the label 
			if msg=='!exit':
				self.exit=True
					
			 #get updated stream from method which shy will implement
			#update the label 	
	def sendExitMsg(self):
		self.pchat.output('!exit')
	def openWindow(self):
		try:
			self.app2.setBg("lightGreen")
			self.app2.setFont(10)
			self.app2.setSticky("sew")
			self.app2.setExpand("both")
			self.app2.addListBox("list","")
			self.app2.setExpand("s")
			self.app2.addEntry("chat")
			self.app2.addButton("Print",self.chatf)
			recv_thread = threading.Thread(target=self.updateChatPolling)
			recv_thread.setDaemon(True)
			recv_thread.start()
			self.app2.go(None,None,self.sendExitMsg)
		except SChatError as er:
			app.errorBox('Error!', er)