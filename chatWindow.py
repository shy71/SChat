import sys
import time
from appJar import gui
from SChat import SChatError
import threading

class chatWin:
	def __init__(self,pchat):
		self.app2 = gui("Chat Window","400x400")
		self.pchat = pchat
		self.username = pchat.suser
		self.peerUsername = pchat.duser
	def chatf(self,button):
		cht = self.app2.getEntry("chat")
		self.app2.clearEntry("chat", False)
		self.pchat.output(cht)
		self.app2.addListItem("list",time.strftime("%H:%M") + " " + self.username + ": " + cht)
	def updateChatPolling(self):
		while True:
			msg = self.pchat.input()
			if not msg == None:
				self.app2.addListItem("list",time.strftime("%H:%M") + " " + self.peerUsername + ": " + msg)
			if msg=='!exit':
				self.app2.topLevel.after(0,self.chatClose)
	def chatClose(self):
		print num
		self.app2.errorBox('Chat close!', 'Chat has been closed by the other side!')
		self.app2.hideWidget(self.app2.BUTTON,"Send")
		self.app2.hideWidget(self.app2.ENTRY,"chat")

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
			self.app2.addButton("Send",self.chatf)
			self.app2.enableEnter(self.chatf)
			recv_thread = threading.Thread(target=self.updateChatPolling)
			recv_thread.setDaemon(True)
			recv_thread.start()
			self.app2.setPollTime(1000)
			self.app2.go(None,None,self.sendExitMsg)
		except SChatError as er:
			self.app2.errorBox('Error!', er)
			
			
#if len(sys.argv)<4:
#	print 'Usage chatWindow.py <serverIp> <SUserName> <DUserName>'
#username=sys.argv[2]
#dusername=sys.argv[3]
#server=ClientServer(ServerConnection(sys.argv[1],5000,None,'keys/key.pem'),username)
#dIp,sharedkey, nounce,token= self.server.getInfo(dusername)
#p=P2PChat(username) #<-need username
#p.startChat(cht,dIp,5002,sharedkey,nounce,token)
#p.LoadChat()
#cwindow = chatWin(p)
#cwindow.openWindow()
