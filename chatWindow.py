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
		#make it change the stream and update the label here too
		print cht
	def updateChatPolling():
		while True:
			print 1
			#get updated stream from method which shy will implement
			#update the label 	
	def openWindow(self):
		self.app2.setBg("orange")
		self.app2.setFont(10)
		self.app2.setSticky("sew")
		self.app2.setExpand("both")
		self.app2.addScrolledTextArea("chattext2")
		self.app2.addLabel("chattext","")
		self.app2.setExpand("s")
		self.app2.addEntry("chat")
		self.app2.addButton("Print",self.chatf)
		self.app2.go()
		

window = chatWin()
window.openWindow()
