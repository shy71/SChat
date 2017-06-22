from socket import socket, AF_INET, SOCK_DGRAM

class Connection:
	def __init__(self,ip_address,port):
		self.ip=ip_address
		self.port=port
		self.socket = socket( AF_INET, SOCK_DGRAM )

	def send(self,msg):
		self.socket.sendto(msg,(self.ip,self.port))
		
	def recv(self):
		return self.socket.recv(2048)
		
	def recvfrom(self):
		return self.socket.recvfrom(2048)
		
	def bind(self):
		self.socket.bind((self.ip,self.port))
	def getaddr(self):
		return (self.ip,self.port)