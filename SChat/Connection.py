from socket import socket,gethostbyname, AF_INET, SOCK_DGRAM
import select
class Connection:
	def __init__(self,ip_address,port):
		self.ip=ip_address
		self.port=port
		self._buildSocket((gethostbyname('0.0.0.0'),0),30)
	def _buildSocket(self,addr,timeout):
		self.socket = socket( AF_INET, SOCK_DGRAM )
		self.socket.settimeout(timeout)
		self.socket.bind(addr)
		self.sip=self.socket.getsockname()[0]
		self.sport=self.socket.getsockname()[1]
	def send(self,msg):
		#print 'S -'+msg
		self.sendto(msg,(self.ip,self.port))
	def sendto(self,msg,addr):
		self.socket.sendto(msg,addr)
	def bind(self,port,timeout):
		self.socket.close()
		self._buildSocket((self.sip,port),timeout)
	def recv(self):
		#a=self.socket.recv(2048)
		#print 'R -'+a
		return self.socket.recv(2048)
	def tryRecv(self):
		try:
			#a=self.recv()
			#print 'R -'+a
			return True,self.recv()
		except Exception as er:
			return False,er
	def recvfrom(self):
		return self.socket.recvfrom(2048)
	def changePort(self,port):
		self.port=port
	def getaddr(self):
		return (self.ip,self.port)
	def close(self):
		return self.socket.close()
	def isNewMsg(self):
		sok=select.select([self.socket],[],[],0)
		if not sok[0]:
			return True
	def settimeout(self,timeout):
		self.socket.settimeout(timeout)