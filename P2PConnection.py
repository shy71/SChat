from Connection import Connection
from AESCipher import AESCipher
class P2PConnection(Connection):
	def __init__(self,ip_address,port,key):
		Connection.__init__(self,ip_address,port)
		self.key=key
		self.aes=AESCipher(key)
	def sendChat(self,msg):
		self.send(self.aes.encrypt(msg))
	def recvChat(self):
		return self.aes.decrypt(self.recv())