import sys
import time
from appJar import gui
import threading

class chatWin:
	def __init__(self,):#,username,ip,sharedKey,nounce,token
		self.app2 = gui("Chat Window","400x400")
		self.messages = []
		self.fromBottom = 0
		self.msgCounter = 0
	
	def chatf(self,button):
		s = self.app2.getEntry("chat")
		self.app2.addListItem("list",s)
	def press(self,btn):
		items = app.getListItems("list")
		if len(items)> 0:
			app.removeListItem("list", items[0])	
	def openWindow(self):
		self.app2.setBg("orange")
		self.app2.setFont(10)
		self.app2.addListBox("list", ["apple", "orange", "pear", "kiwi"])
		self.app2.addListItem("list",'shy')
		self.app2.addButton("press",  self.press)
		self.app2.addEntry("chat",2,0,2)
		self.app2.addButton("Print",self.chatf,3,0,2)
		#recv_thread = threading.Thread(target=self.updateChatPolling)
		#recv_thread.setDaemon(True)
		#recv_thread.start()
		self.app2.go()
		
		
win = chatWin()
win.openWindow()