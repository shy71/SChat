import sys
import time
from appJar import gui
import threading

class chatWin:
	def __init__(self,pchat):#,username,ip,sharedKey,nounce,token
		self.app2 = gui("Chat Window","400x200")
		self.pchat = pchat
		self.msgCounter = 0
	def setMsgLabel(self,msgText):
		self.msgCounter = self.msgCounter + 1
		if self.msgCounter == 9:
			msgText = msgText[msgText.findfirstindex('\n') + 1:]
			self.msgCounter = 8
		self.app2.setLabel("chattext",msgText)	

	def chatf(self,button):
		cht = self.app2.getEntry("chat")
		msgText = self.app2.getLabel("chattext") + '\n' + cht
		self.pchat.output(cht)
		self.setMsgLabel(msgText)
		#make it change the stream and update the label here too
		print cht
	def updateChatPolling(self):
		while True:
			msg = self.pchat.input()
			if not msg == None:
				self.setMsgLabel(self.app2.getLabel("chattext") + '\n' + msg)
			 #get updated stream from method which shy will implement
			#update the label 	
	def openWindow(self):
		self.app2.setBg("orange")
		self.app2.setFont(10)
		self.app2.setSticky("sew")
		self.app2.setExpand("both")
		self.app2.addLabel("chattext","")
		self.app2.setExpand("s")
		self.app2.addEntry("chat")
		self.app2.addButton("Print",self.chatf)
		recv_thread = threading.Thread(target=self.updateChatPolling)
		recv_thread.setDaemon(True)
		recv_thread.start()
		self.app2.go()
