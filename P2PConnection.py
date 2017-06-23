from Connection import Connection
from AESCipher import AESCipher
class P2PConnection(Connection):
	def __init__(self,ip_address,port,key,srcUser,desUser):
		Connection.__init__(self,ip_address,port)
		self.key=key
		self.aes=AESCipher(key)
		self.srcUser=srcUser
		self.desUser=desUser
	def sendChat(self,msg):
		self.send(self.aes.encrypt(msg))
	def recvChat(self):
		return self.aes.decrypt(self.recv())
	def handshake(self):	
		self.send('h;'+seld.token)
	def handleOkResp(self,resp,nounce)
		#receive the ok message from the other side
		nounceCompataible = checkOkMessageNounce(OkMessage,nounce,usersSockets[username].key)
		if not nounceCompataible:
			print 'The ok message isn\'t comatible'
		else:
			#send g message to complete the sync process
			usersSockets[username].send('g;' + AESCipher(usersSockets[username].key).encrypt(str(int(nounce) + 1)))
			print 'The session sync has been completed'
	
	def checkOkMessageNounce(OkMessage,nounce,key):
		header = OkMessage.split(';')[0]
		if (header == 'o'):
			rcvnounce = AESCipher(key).decrypt(OkMessage[2:])
			if rcvnounce == nounce:
				return True
		r