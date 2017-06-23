from UserChat import UserChat
from P2PConnection import P2PConnection
from AESCipher import AESCipher
class P2PChat:
	def __init__(self):#,username,ip,sharedKey,nounce,token
		pass
	def startChat(self,username,ip,port,sharedKey,nounce,token):#why need username?
		self.socket=P2PConnection(ip,port,sharedKey)
		self.help=UserChat('lead')
		self.help.sendSyn(self.socket,nounce,token)
		responded,resp=self.socket.tryRecv()
		if not responded:
			print 'Peer didn\'t responded! - Syn'
			raise resp 
		self.help.handleMsg(resp)
		print 'Chat Up'
	def gotChatRequest(self,ip,port,msg,serverKey):
		self.help=UserChat('wait')
		username,sharedKey,nounce=self.help.handleSynReq(msg,serverKey)
		self.socket=P2PConnection(ip,port,sharedKey)
		self.socket.bind()
		self.help.sendOkMsg(self.socket,nounce)
		responded,resp=self.socket.tryRecv()
		if not responded:
			print 'Peer didn\'t responded! - Ok'
			raise resp
		self.help.handleMsg(resp)
		print 'Chat Up'