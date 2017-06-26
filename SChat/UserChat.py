from AESCipher import AESCipher
import binascii
class UserChat:
	def __init__(self,state):
		self.state=state
	def handleMsg(self,resp):
		header=resp.split(';')[0]
		if header=='e':
			self.state='lead'
			raise ServerError(resp.split(';')[1])
		if self.state=='syn':
			self.handleOkResp(resp)
		if self.state=='wait':
			self.handleSynReq(resp)
		if self.state=='okSent':
			self.handleGrResp(resp)
	def handleSynReq(self,resp,serverKey):
		header=resp.split(';')[0]
		if header!='h':
			Exception,'header not "h" in wait state - '+header
		print 'Got syn Req'
		return binascii.unhexlify(AESCipher(serverKey).decrypt(resp.split(';')[1])).split(';') #username,sharedKey,nounce
		
	def sendOkMsg(self,peer,nounce):
		self.peer=peer
		self.nounce=nounce
		self.peer.send('o;' + self.peer.aes.encrypt(nounce+';'+str(peer.sport)))
		self.state='okSent'
		

		
	def handleGrResp(self,resp):
		#expect the next message (g - ack)
		header=resp.split(';')[0]
		if header!='g':
			Exception,'header not "g" in okSent state - '+header
		if int(self.peer.aes.decrypt(resp.split(';')[1])) != int(self.nounce)+1:								
			raise Exception, 'nounce isn\'t match the sended nounce! - '+ self.peer.aes.decrypt(resp.split(';')[1])+' -'+self.nounce
		self.state='ready'
		print 'Got GR Resp'

	def handleOkResp(self,resp):
		header=resp.split(';')[0]
		if header!='o':
			raise Exception,'header not "o" in syn state - '+header
		nounce,port=self.peer.aes.decrypt(resp.split(';')[1]).split(';')
		self.peer.changePort(int(port))
		self.peer.port=int(port)
		if nounce != self.nounce:
			raise Exception, 'nounce isn\'t match the sended nounce! - '+self.nounce
		self.peer.send('g;' + self.peer.aes.encrypt(str(int(self.nounce) + 1)))
		self.state='ready'
		print 'Got syn Resp'


	def sendSyn(self,peer,nounce,token):
		self.peer=peer
		if self.state!='lead':
			raise Exception,'Can\'t start chat without getting info from the server about the user!'
		self.peer.send('h;'+token)
		self.nounce=nounce
		self.state='syn'
		print 'Send Syn'
	