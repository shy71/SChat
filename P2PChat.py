from UserChat import UserChat
from P2PConnection import P2PConnection
from AESCipher import AESCipher
import select
import threading
class P2PChat:
	def __init__(self):#,username,ip,sharedKey,nounce,token
		pass
	def startChat(self,duser,ip,port,sharedKey,nounce,token):#why need username?
		self.socket=P2PConnection(ip,port,sharedKey)
		self.help=UserChat('lead')
		self.help.sendSyn(self.socket,nounce,token)
		responded,resp=self.socket.tryRecv()
		if not responded:
			print 'Peer didn\'t responded! - Syn'
			raise resp 
		self.help.handleMsg(resp)
		self.userinput=[]
		self.duser=duser
		print 'Chat Up'
	def gotChatRequest(self,ip,port,msg,serverKey):
		self.help=UserChat('wait')
		self.duser,sharedKey,nounce=self.help.handleSynReq(msg,serverKey)
		self.socket=P2PConnection(ip,port,sharedKey)
		self.help.sendOkMsg(self.socket,nounce)
		responded,resp=self.socket.tryRecv()
		if not responded:
			print 'Peer didn\'t responded! - Ok'
			raise resp
		self.help.handleMsg(resp)
		print 'Chat Up'
	def startActiveChat(self):
		while True:
			data = self.socket.tryRecvChat()
			if data:
				print '\r'+self.duser+': '+data
				print 'Self: ',
	def LoadChat(self):
		print 'Secure Chat with ' +self.duser
		recv_thread = threading.Thread(target=self.startActiveChat)
		recv_thread.setDaemon(True)
		recv_thread.start()
		while True:
			inp= raw_input('\rself: ')
			self.socket.sendChat(inp)
		
	
		