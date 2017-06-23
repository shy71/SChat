from socket import socket, AF_INET, SOCK_DGRAM

class Connection:
	def __init__(self,sport,ip_address,port):
		self.ip=ip_address
		self.port=port
		self.socket = socket( AF_INET, SOCK_DGRAM )
		self.socket.settimeout(30)

	def send(self,msg):
		self.socket.sendto(msg,(self.ip,self.port))
		
	def recv(self):
		a=self.socket.recv(2048)
		print "R - "+a
		return a
	def tryRecv(self):
		try:
			return True,self.recv()
		except Exception as er:
			return False,er
	def recvfrom(self):
		return self.socket.recvfrom(2048)
		
	def bind(self):
		self.socket.bind((self.ip,self.port))
	def getaddr(self):
		return (self.ip,self.port)
	def close(self):
		return self.socket.close()