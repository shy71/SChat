from Connection import Connection
from AESCipher import AESCipher
from M2Crypto import RSA 

class ServerConnection(Connection):
	def __init__(self,ip_address,port,aes,rsa):
		Connection.__init__(self,ip_address,port)
		self.aes=aes
		self.rsa=rsa
	def serverEncrypt(self,msg):
		return self.rsa.public_encrypt(msg,RSA.pkcs1_oaep_padding)
	def send(self,msg):
		Connection.send(self,self.serverEncrypt(msg))