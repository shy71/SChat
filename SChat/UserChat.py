from AESCipher import AESCipher
from SChatError import SChatError
import binascii
class UserChat:
	def __init__(self,state):
		self.state=state
	def handleMsg(self,resp):
		header=resp.split(';')[0]
		if header=='e':
			self.state='lead'
			raise SChatError.toSChatError(resp.split(';')[1])
		if self.state=='syn':
			self.handleOkResp(resp)
		if self.state=='wait':
			self.handleSynReq(resp)
		if self.state=='okSent':
			self.handleGrResp(resp)
	def handleSynReq(self,resp,serverKey):
		header=resp.split(';')[0]
		if header!='h':
			raise SChatError('Got invalid msg(header) while in \'wait\' state!')
		try:
			return binascii.unhexlify(AESCipher(serverKey).decrypt(resp.split(';')[1])).split(';') #username,sharedKey,nounce
		except Exception as err:
			raise SChatError('Invalid content in Hi request, problem with decryption! - '+str(er))
	def sendOkMsg(self,peer,nounce):
		self.peer=peer
		self.nounce=nounce
		self.peer.send('o;' + self.peer.aes.encrypt(nounce+';'+str(peer.sport)))
		self.state='okSent'	
	def handleGrResp(self,resp):
		#expect the next message (g - ack)
		header=resp.split(';')[0]
		if header!='g':
			raise SChatError('Got invalid msg(header) while in \'okSent\' state!')
		recvNounce=int(self.decryptAes(resp.split(';')[1]))
		if recvNounce!= int(self.nounce)+1:	
			raise SChatError('Received nounce sent back by the server isn\'t compatible with the\n nounce number sent originally by you... \nYou may be under attack if this error continue to apper!')
		self.state='ready'
	def decryptAes(self,msg):
		try:
			return self.peer.aes.decrypt(msg)
		except Exception as er:
			raise SChatError('Invalid msg, can\'t decrypt the data, maybe wrong key or unauthorized source! - '+str(er))
	def handleOkResp(self,resp):
		header=resp.split(';')[0]
		if header!='o':
			raise SChatError('Got invalid msg(header) while in \'syn\' state!')
		nounce,port=self.decryptAes(resp.split(';')[1]).split(';')
		self.peer.changePort(int(port))
		self.peer.port=int(port)
		if nounce != self.nounce:
			raise SChatError('Received nounce sent back by the server isn\'t compatible with the\n nounce number sent originally by you... \nYou may be under attack if this error continue to apper!')
		self.peer.send('g;' + self.peer.aes.encrypt(str(int(self.nounce) + 1)))
		self.state='ready'


	def sendSyn(self,peer,nounce,token):
		self.peer=peer
		if self.state!='lead':
			raise SChatError('Can\'t start chat without getting info from the server about the unknown user!')
		self.peer.send('h;'+token)
		self.nounce=nounce
		self.state='syn'
	