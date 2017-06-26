from ClientChat import ClientChat
from SChatError import SChatError
class ClientServer:
	def __init__(self,server,username,isRegister):
		self.server=server
		self.help=ClientChat(server)
		self.username=username
		if not isRegister:
			self._register()
		self._connect()
	def _register(self):
		self.help.register(self.username)
		responded,resp=self.server.tryRecv()
		if not responded:
			raise SChatError('Server didn\'t responded in the start of the Register request - '+str(resp)) 
		self.help.handleMsg(resp)
	def _connect(self):
		self.help.connect(self.username)
		responded,resp=self.server.tryRecv()
		if not responded:
			raise SChatError('Server didn\'t responded in the start of the Connect request - '+str(resp)) 
		self.help.handleMsg(resp)
	def getInfo(self,username):
		if not self.help.isConnected():
			self._connect()
		self.help.sendInfoReq(username)
		responded,resp=self.server.tryRecv()
		if not responded:
			raise SChatError('Server didn\'t responded in the start of the Get Info request - '+str(resp)) 
		return self.help.handleMsg(resp) #dIp,sharedkey, nounce,token
	def close(self):
		self.server.close()
	def getKey(self):
		return self.help.loadKey(self.username)