from ServerConnection import ServerConnection
CHAR_SYN_START=5001
from random import randint
from P2PConnection import P2PConnection
import binascii
class UserChat:
	def __init__(self,username,desUser):
		self.username=username
		if desUser==None:
			self.state='wait'
			return
		self.dUsername=desUser
		self.state='start'
	def sendInfoReq(self,server):
		if self.state!='start':
			raise Exception,'UserChat can\'t start chat when state is not \'start\''
		requestInfoMsg =self._buildInfoMsg()		
		server.send(requestInfoMsg)
		print 'Send info Req'
		self.state='infoReqSent'
		#received_data = server.recv()
		#handleHeader(received_data,bob_username,0);
	def handleMsg(self,resp,conn):
		header=resp.split(';')[0]
		if header=='e':
			self.state='start'
			raise ServerError(resp.split(';'[1]))
		if self.state=='infoReqSent':
			self.handleInfoResp(resp,conn)
		if self.state=='syn':
			self.handleSynResp(resp)
		if self.state=='wait':
			self.handleSynReq(resp,conn)
		if self.state=='okSent':
			self.handleGrResp(resp)
	def handleSynReq(resp,conn):
		header=resp.split(';')[0]
		if header!='h':
			Exception,'header not "h" in wait state - '+header
		username,sharedKey,self.nounce=binascii.unhexlify(conn.aes.decrypt(resp.split(';')[1]))	
		aliceip,aliceport=conn.aliceip,conn.aliceport
		self.conn=P2PConnection(aliceip,aliceport,sharedKey,self.username,dUsername)	
		self.conn.send('o;' + self.con.aes.encrypt(nounce))
		self.state='okSent'
		print 'Got syn Req'

		
	def handleGrResp(resp):
		#expect the next message (g - ack)
		header=resp.split(';')[0]
		if header!='g':
			Exception,'header not "g" in okSent state - '+header
		if int(self.con.aes.decrypt(resp.split(';')[1])) != int(nounce) + 1:																
			raise Exception, 'nounce isn\'t match the sended nounce! - '+nounce
		self.state='ready'
		print 'Got GR Resp'

	def handleSynResp(self,resp):
		header=resp.split(';')[0]
		if header!='o':
			raise Exception,'header not "o" in syn state - '+header
		if self.con.aes.decrypt(resp.split(';')[1]) != nounce:
			raise Exception, 'nounce isn\'t match the sended nounce! - '+nounce
		self.con.send('g;' + self.con.aes.encrypt(str(int(nounce) + 1)))
		self.state='ready'
		print 'Got syn Resp'

	def handleInfoResp(self,resp,conn):
		header=resp.split(';')[0]
		if header!='s':
			raise Exception,'header not "s" in infoReqSent state - '+header
		data=binascii.unhexlify(conn.aes.decrypt(resp.split(';')[1]))
		subHeader=data.split(';')[0]
		if subHeader!='m':
			raise Exception,'subHeader not "m" in infoReqSent state - '+subHeader
		dIp,sharedKey,nounce,token=data.split(';')[1:]
		if nounce!=self.nounce:
			raise Exception,'Nounce didn\'t match in InfoResp -'+nounce + '-'+self.nounce
		self.con=P2PConnection(dIp,CHAR_SYN_START,sharedKey,self.username,self.dUsername)
		self.token=token
		self.state='infoRecv'
		print 'Got Info Resp'

	def startChat(self):
		if self.state!='infoRecv':
			raise Exception,'Can\'t start chat without getting info from the server about the user!'
		self.con.send('h;'+self.token)
		self.state='syn'
		print 'Send Syn'
	def _buildInfoMsg(self):
		self.nounce = str(randint(1, 65536))
		return 'm;' + self.username + ';' + self.dUsername + ';' + self.nounce