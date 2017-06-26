import sys
import time
sys.path.append("../../")
from appJar import gui

class chatWin:
	def __init__(self):#,username,ip,sharedKey,nounce,token
		self.app2 = gui("Login Window","400x200")
		pass
	
	def chatf(self,button):
		cht = self.app2.getEntry("chat")
		self.app2.setLabel("chattext",self.app2.getLabel("chattext") + '\n' + cht)
		print cht
	
	def openWindow(self):
		self.app2.setBg("orange")
		self.app2.setFont(10)
		self.app2.setSticky("sew")
		self.app2.setExpand("both")
		self.app2.addLabel("chattext","")
		self.app2.setExpand("s")
		self.app2.addEntry("chat")
		self.app2.addButton("Print",self.chatf)
		self.app2.go()
		
		