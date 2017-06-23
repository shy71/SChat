from ServerConnection import ServerConnection
CHAR_SYN_START=5001
class UserChat:
	def __init__(self,username,desUser)
		self.username=username
		self.dUsername=desUser
		self.state='start'
	def sendInfoReq(self,server):
		if self.state!='start':
			raise Exception,'UserChat can\'t start chat when state is not \'start\''
		requestInfoMsg =self._buildInfoMsg()		
		server.send(enc)
		self.state='infoReqSent'
		#received_data = server.recv()
		#handleHeader(received_data,bob_username,0);
	def gotResponse(self,resp,conn):
		header=resp.split(';')[0]
		if header=='e':
			self.state='start'
			raise ServerError(resp.split(';'[1])
		if self.state=='infoReqSent':
			self.handleInfoResp(resp,conn)
		if self.state=='syn':
			self.handleSynResp(resp)
	def handleSynResp(self,resp):
		self.con.handleOkResp(resp,self.nounce)
		self.state='ready'
	def handleInfoResp(self,resp,conn):
		header=resp.split(';')[0]
		if header!='s':
			raise Exception,'header not "s" in infoReqSent state - '+header
		data=conn.aes.decrypt(resp.split(';')[1:])
		subHeader=data.split(';')[0]
		if subHeader!='m':
			raise Exception,'subHeader not "m" in infoReqSent state - '+subHeader
		dIp,sharedKey,nounce,token=data.split(';')[1:]
		if nounce!=self.nounce:
			raise Exception,'Nounce didn\'t match in InfoResp'
		self.con=P2PConnection(dIp,CHAR_SYN_START,sharedKey,seld.username,self.dUsername)
		self.token=token
		self.state='infoRecv'
	def startChat(self):
		self.con.send('h;'+seld.token)
		self.state='syn'
	def _buildInfoMsg(self):
		self.nounce = randint(1, 65536)
		return 'm;' + self.username + ';' + self.dUsername + ';' + str(self.nounce)