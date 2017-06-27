import sys
import time
from appJar import gui
import threading

class chatWin:
	def __init__(self,pchat):#,username,ip,sharedKey,nounce,token
		self.app2 = gui("Chat Window","400x400")
		self.pchat = pchat
		self.messages = []
		self.username = self.pchat.suser
		self.peerUsername = self.pchat.duser
		self.msgCounter = 0
		self.msgChanged=False
		self.exit=False
	def setMsgLabel(self,msgText,local):
		self.msgCounter = self.msgCounter + 1
		self.messages.append(msgText)
		if self.msgCounter == 9:
			msgList = self.messages[len(self.messages)-8:]
			self.msgCounter = 8
		else:
			msgList = self.messages
		msg=''
		for message in msgList:
			if local:
				msg += '\n' +self.username+': '+ message
			else:
				msg +='\n' + self.peerUsername+': ' + message #+ ' '*(400 - 12*len(message))
		self.msg=msg
		self.msgChanged=True
		self.exit=True

	def chatf(self,button):
		cht = self.app2.getEntry("chat")
		#msgText = self.app2.getLabel("chattext") + '\n' + cht
		self.pchat.output(cht)
		self.setMsgLabel(cht,True)
		#make it change the stream and update the label here too
		print cht
	def updateChatPolling(self):
		while True:
			msg = self.pchat.input()
			if not msg == None:
				self.setMsgLabel(msg,False)
			#if msg=='!exit':
					
			 #get updated stream from method which shy will implement
			#update the label 	
	def sendExitMsg(self):
		self.pchat.output('!exit')
	def updateMsg(self):
		if self.msgChanged:
			self.app2.setLabel("chattext",self.msg)	
			self.msgChanged=False
		if self.exit:
			self.app2.whenClose=None
			self.app2.close()
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
		self.app2.setPollTime(200)
		self.app2.registerEvent(self.updateMsg)
		self.app2.go(None,None,self.sendExitMsg)
