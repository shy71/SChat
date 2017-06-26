from Connection import Connection
from AESCipher import AESCipher
from SChatError import SChatError
class P2PConnection(Connection):
	def __init__(self,ip_address,port,key):
		Connection.__init__(self,ip_address,port)
		self.key=key
		self.aes=AESCipher(key)
	def sendChat(self,msg):
		self.send(self.aes.encrypt(msg))
	def recvChat(self):
		try:
			return self.aes.decrypt(self.recv())
		except Exception as er:
			raise SChatError('Problem with decryption of the recived data - '+str(er))			
	def tryRecvChat(self):
		if self.isNewMsg():
			return self.recvChat()
	def startChat(self):
		self.settimeout(None)