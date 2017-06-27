import sys
import time
from appJar import gui
import threading

class chatWin:
	def __init__(self,pchat):#,username,ip,sharedKey,nounce,token
		self.app2 = gui("Chat Window","400x400")
		self.pchat = pchat
		self.messages = []
		self.fromBottom = 0
		self.username = self.pchat.suser
		self.peerUsername = self.pchat.duser
		self.msgCounter = 0
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
		self.pchat.output(cht)
		self.setMsgLabel(cht,True)
		#make it change the stream and update the label here too
	def updateChatPolling(self):
		while True:
			msg = self.pchat.input()
			if not msg == None:
				self.setMsgLabel(msg,False)
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
	def createShowedMessagesList(self):
		return self.messages[len(self.messages) - 8 - self.fromBottom : len(self.messages) - self.fromBottom]
		
	def goUp(self,button):		
		if self.fromBottom < len(self.messages):
			self.fromBottom += 1			
			self.showMessageListOnScreen(self.createShowedMessagesList())

	def goDown(self,button):
		if self.fromBottom > 0:
			self.fromBottom -= 1
			self.showMessageListOnScreen(self.createShowedMessagesList())

	def openWindow(self):
		self.app2.setBg("orange")
		self.app2.setFont(10)
		self.app2.setSticky("n")
		self.app2.addLabel("peername",self.peerUsername,0,0)
		self.app2.setSticky("sew")
		self.app2.setExpand("both")
		self.app2.addLabel("chattext1","",0,0)
		self.app2.addLabel("chattext2","",0,0)
		self.app2.setExpand("s")
		self.app2.addButton("up",self.goUp,1,0,2)
		self.app2.addButton("down",self.goDown,1,1,2)
		self.app2.addEntry("chat",2,0,2)
		self.app2.addButton("Print",self.chatf,3,0,2)
		recv_thread = threading.Thread(target=self.updateChatPolling)
		recv_thread.setDaemon(True)
		recv_thread.start()
		self.app2.setPollTime(200)
		self.app2.registerEvent(self.updateMsg)
		self.app2.go(None,None,self.sendExitMsg)
