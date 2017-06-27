import sys
import time
from appJar import gui
import threading

class chatWin:
	def __init__(self,pchat):#,username,ip,sharedKey,nounce,token
		self.app2 = gui("Chat Window","400x400")
		self.pchat = pchat
		self.username = username
		self.peerUsername = peerUsername
		self.msgChanged=False
		self.exit=False
	def showMessageListOnScreen(self,msgList):
		msg1=''
		msg2=''
		for message in msgList:
			if message.startswith(self.username):
				msg2 += '\n'
				msg1 += '\n' + message	
			else:
				msg2 += '\n' + message
				msg1 += '\n'
		self.msg1=msg1
		self.msg2=msg2
		self.msgChanged=True
	def setMsgLabel(self,msgText,local):
		self.msgCounter = self.msgCounter + 1
		if local:
			self.messages.append(self.username + ': ' + msgText)
		else:
			self.messages.append(self.peerUsername + ': ' + msgText)

		if self.msgCounter == 9:
			msgList = self.messages[len(self.messages)-8:]
			self.msgCounter = 8
		else:
			msgList = self.messages
		self.showMessageListOnScreen(msgList)
	def chatf(self,button):
		cht = self.app2.getEntry("chat")
		#msgText = self.app2.getLabel("chattext") + '\n' + cht
		self.pchat.output(self.username + ': ' +cht,self.username)
		self.addListItem("list",self.username + ": " + msg)
		#make it change the stream and update the label here too
		print cht
	def updateChatPolling(self):
		while True:
			msg = self.pchat.input()
			if not msg == None:
				self.addListItem("list",self.peerUsername + ": " + msg)
			#get updated stream from method which shy will implement
			#update the label 
			if msg=='!exit':
				self.exit=True
					
			 #get updated stream from method which shy will implement
			#update the label 	
	def sendExitMsg(self):
		self.pchat.output('!exit')
	def updateMsg(self):
		if self.msgChanged:
			self.app2.setLabel("chattext1",self.msg1)
			self.app2.setLabel("chattext2",self.msg2)	
			self.msgChanged=False
		if self.exit:
			self.app2.whenClose=None
			self.app2.hide()
	def openWindow(self):
		ef openWindow(self):
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
		self.app2.setPollTime(200)
		self.app2.registerEvent(self.updateMsg)
		self.app2.go(None,None,self.sendExitMsg)
