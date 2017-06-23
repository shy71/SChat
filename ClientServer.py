from ClientChat import ClientChat

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
			print 'Server didn\'t responded! - Register'
			raise resp 
		self.help.handleMsg(resp)
	def _connect(self):
		self.help.connect(self.username)
		responded,resp=self.server.tryRecv()
		if not responded:
			print 'Server didn\'t responded! - Connect'
			raise resp 
		self.help.handleMsg(resp)
	def getInfo(self,username):
		self.help.sendInfoReq(username)
		responded,resp=self.server.tryRecv()
		if not responded:
			print 'Server didn\'t responded! - GetInfo'
			raise resp 
		return self.help.handleMsg(resp) #dIp,sharedkey, nounce,token
	def close(self):
		self.server.close()
	def getKey(self):
		return self.help.loadKey(self.username)