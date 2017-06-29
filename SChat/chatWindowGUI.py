import time
from SChat import SChatError
import threading

class chatWindowGUI:
	def __init__(self,pchat,app):
		self.app2=app
		self.app2.startSubWindow(pchat.duser)
		self.app2.setGeometry("400x400")

		self.pchat = pchat
		self.username = pchat.suser
		self.peerUsername = pchat.duser
	def chatf(self,button):
		cht=self.chatbox.get()
		#How can i clear the chatbox?? maybe you will find a way...I didn't
		#1 Devloper give up on this problem, when you will give up, please bump the counter for future reference 
		self.pchat.output(cht)
		self.app2.addListItem(self.peerUsername+"."+"list",time.strftime("%H:%M") + " " + self.username + ": " + cht)
	def updateChatPolling(self):
		while True:
			msg = self.pchat.input()
			if not msg == None:
				self.app2.addListItem(self.peerUsername+"."+"list",time.strftime("%H:%M") + " " + self.peerUsername + ": " + msg)
			if msg=='!exit':
				self.app2.topLevel.after(0,self.chatClose)
	def chatClose(self):
		self.app2.errorBox('Chat close!', 'Chat has been closed by the other side!')
		self.app2.hideWidget(self.app2.BUTTON,"Send "+self.peerUsername)
		self.app2.hideWidget(self.app2.ENTRY,self.peerUsername+"."+"chatbox")
	def sendExitMsg(self):
		self.pchat.output('!exit')
	def openWindow(self):
		try:
			self.app2.setBg("lightGreen")
			self.app2.setFont(10)
			self.app2.setSticky("sew")
			self.app2.setExpand("both")
			self.app2.addListBox(self.peerUsername+"."+"list","")
			self.app2.setExpand("s")
			outList=[]
			self.app2.addEntry(self.peerUsername+"."+"chatbox",list=outList)
			self.chatbox=outList[0]
			self.app2.addButton("Send "+self.peerUsername,self.chatf)
			self.app2.enableEnter(self.chatf)
			recv_thread = threading.Thread(target=self.updateChatPolling)
			recv_thread.setDaemon(True)
			recv_thread.start()
			self.app2.setPollTime(1000)
			self.app2.showSubWindow(self.peerUsername)
		except SChatError as er:
			self.app2.errorBox('Error!', er)
