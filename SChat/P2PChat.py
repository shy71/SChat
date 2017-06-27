from UserChat import UserChat
from P2PConnection import P2PConnection
from Connection import Connection
import threading
from ClientChat import loadKey
from SChatError import SChatError
class P2PChat:
	def __init__(self,sUser):#,username,ip,sharedKey,nounce,token
		self.suser=sUser
		self.inputlist=[]
	def startChat(self,duser,ip,port,sharedKey,nounce,token):#why need username?
		self.socket=P2PConnection(ip,port,sharedKey)
		self.help=UserChat('lead')
		self.help.sendSyn(self.socket,nounce,token)
		responded,resp=self.socket.tryRecv()
		if not responded:
			raise SChatError('Peer didn\'t responded in the start of setting up the chat(Hi msg) - '+str(resp)) 
		self.help.handleMsg(resp)
		self.userinput=[]
		self.duser=duser
		self.socket.startChat()
		self.open=True
	def gotChatRequest(self,ip,port,msg):
		self.help=UserChat('wait')
		self.duser,sharedKey,nounce=self.help.handleSynReq(msg,loadKey(self.suser))
		self.socket=P2PConnection(ip,port,sharedKey)
		self.help.sendOkMsg(self.socket,nounce)
		responded,resp=self.socket.tryRecv()
		if not responded:
			raise SChatError('Peer didn\'t responded in the middle of setting up the chat(Ok msg) - '+str(resp))
		self.help.handleMsg(resp)
		self.socket.startChat()
		self.open=True
		print 'Chat Up'
	def waitForRequest(self):
		inCon=Connection('0.0.0.0',0)
		inCon.bind(5002,None)
		while not inCon.isNewMsg():
			pass
		msg,addr=inCon.recvfrom()
		inCon.close()
		self.gotChatRequest(addr[0],addr[1],msg)
	def startActiveChatCMD(self):
		while self.open:
			data = self.socket.tryRecvChat()
			if not data:
				continue
			if data:
				print '\r'+self.duser+': '+data
				print self.suser+': ',
			if data.startswith('!'):
				if data=='!exit':
					self.closeChat()
					print 'Press enter to continue'
	def LoadChatCMD(self):
		print 'Secure Chat with ' +self.duser
		recv_thread = threading.Thread(target=self.startActiveChatCMD)
		recv_thread.setDaemon(True)
		recv_thread.start()
		while self.open:
			inp= raw_input('\r'+self.suser+': ')
			if not self.open:
				return
			self.socket.sendChat(inp)
			if inp.startswith('!'):
				if inp=='!exit':
					self.closeChat()
	def startActiveChat(self):
		while self.open:
			data = self.socket.tryRecvChat()
			if not data:
				continue
			self.inputlist.append(data)
			if data.startswith('!'):
				if data=='!exit':
					self.closeChat()
	def LoadChat(self):
		recv_thread = threading.Thread(target=self.startActiveChat)
		recv_thread.setDaemon(True)
		recv_thread.start()
	def input(self):
		if self.inputlist:
			msg=self.inputlist[0]
			self.inputlist.remove(msg)
			return msg
	def output(self,msg):
		if not self.open:
			return
		self.socket.sendChat(msg)
		if msg.startswith('!'):
				if msg=='!exit':
					self.closeChat()
	def closeChat(self):
		self.open=False
		self.socket.close()
		#raise SChatError('Chat has been closed!')

	
		
