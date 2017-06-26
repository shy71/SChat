from socket import socket,gethostbyname, AF_INET, SOCK_DGRAM

class Connection:
	def __init__(self,ip_address,port):
		self.sip=gethostbyname('0.0.0.0')
		self.ip=ip_address
		self.port=port
		self.socket = socket( AF_INET, SOCK_DGRAM )
		self.socket.settimeout(30)
		self.socket.bind((self.sip,0))
		self.sport=self.socket.getsockname()[1]
	#	s.connect((self.ip,self.port))

	def send(self,msg):
		self.socket.sendto(msg,(self.ip,self.port))
		
	def recv(self):
		return self.socket.recv(2048)
	def tryRecv(self):
		try:
			return True,self.recv()
		except Exception as er:
			return False,er
	def recvfrom(self):
		return self.socket.recvfrom(2048)
	def changePort(self,port):
		self.port=port
	#	self.port=port
	#	self.socket.close()
	#	self.socket.connect((self.ip,self.port))
	#def bind(self,port):
	#	self.socket.bind((self.sip,port))
	#	self.sport=port
	def getaddr(self):
		return (self.ip,self.port)
	def close(self):
		return self.socket.close()