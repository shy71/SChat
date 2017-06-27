import sys
import time
from appJar import gui
import threading

class chatWin:
	def __init__(self,pchat,username,peerUsername):#,username,ip,sharedKey,nounce,token
		self.app2 = gui("Chat Window","400x400")
		self.pchat = pchat
		self.messages = []
		self.username = username
		self.peerUsername = peerUsername
		self.msgCounter = 0
		
	def setMsgLabel(self,msgText,username):
		self.msgCounter = self.msgCounter + 1
		if self.msgCounter == 9:
			msgList = messages[len(messages)-8:]
			self.msgCounter = 8
		else:
			msgText = messages
		for message in msgList:
			if self.username == username:
				msg = msg + '\n' + message
			else:
				msg = msg + '\n' + ' '*(400 - 12*len(message)) + message
		self.app2.setLabel("chattext",msg)	

	def chatf(self,button):
		cht = self.app2.getEntry("chat")
		#msgText = self.app2.getLabel("chattext") + '\n' + cht
		self.pchat.output(self.username + ': ' +cht,self.username)
		self.setMsgLabel(msgText)
		#make it change the stream and update the label here too
		print cht
	def updateChatPolling(self):
		while True:
			msg = self.pchat.input()
			if not msg == None:
				self.setMsgLabel(self.peerUsername + ": " + msg,self.peerUsername)
			#if msg=='!exit':
					
			 #get updated stream from method which shy will implement
			#update the label 	
	def sendExitMsg(self):
		print 'exit'
		self.pchat('!exit')
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
		self.app2.go(None,None,self.sendExitMsg)
