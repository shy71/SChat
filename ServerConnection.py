from Connection import Connection
from AESCipher import AESCipher
class ServerConnection(Connection):
	def __init__(self,ip_address,port,aes,rsa):
		Connection.__init__(self,ip_address,port)
		self.aes=aes
		self.rsa=rsa
	def serverEncrypt(self,msg):
		return self.public_encrypt(msg)
	def send(self,msg):
		Connection.send(self,serverEncrypt(msg))