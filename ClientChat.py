from UserChat import UserChat
from random import randint
import binascii
import os
from AESCipher import AESCipher
import re
from time import time
from ServerError import ServerError
from Connection import Connection
from socket import socket, AF_INET, SOCK_DGRAM,gethostbyname
CHAT_SYN_PORT=5001
def loadKey(username):
		with open('users.d','r') as f:
			return re.search('{'+username+';([a-z|0-9]+)}\n',f.read()).group(1)
class ClientChat:
	def __init__(self,server):
		self.server=server
		self.state='start'
		self.chats={}
	def register(self,username):
		if self.state!='start':
			raise Exception,'Can\'t register if the state is not \'start\'!'
		self.nounce = randint(1, 65536)
		self.random_key=binascii.hexlify(os.urandom(32))
		self.server.aes=AESCipher(self.random_key)
		self.username=username
		self.server.send('r;' + self.username + ';' + self.random_key + ';' + str(self.nounce))
		self.state='regReq'
	def handleMsg(self,resp):
		header=resp.split(';')[0]
		if header=='e':
			self.state='start'
			raise ServerError(resp.split(';')[1])
		if self.state=='regReq':
			self.handleRegReq(resp)
		if self.state=='conReq':
			self.handleConReq(resp)
		if self.state=='infoReqSent':
			return self.handleInfoResp(resp)
	#def serverRecv(self):
	#	self.handleMsg(self.server.recv(),self.server)
		
	#def startChat(self,dUsername):
	#	self.chats[dUsername]=UserChat(self.username,dUsername)
	#	self.chats[dUsername].sendInfoReq(self.server)
	#	self.chats[dUsername].handleMsg(self.server.recv(),self.server)
	#	self.chats[dUsername].startChat()
	#	self.chats[dUsername].handleMsg(self.chats[dUsername].con.recv(),self.chats[dUsername].con)
	#	self.chats[dUsername].handleMsg(self.chats[dUsername].con.recv(),self.chats[dUsername].con)
	#def waitForChat(self):
	#	conn=UserChat(self.username,'')
	#	con=Connection(gethostbyname( '0.0.0.0' ),CHAT_SYN_PORT)
	#	con.bind()
	#	conn.handleMsg(con.recv(),con)
	#	conn.handleMsg(con.recv(),con)

	def handleConReq(self,resp):
		header=resp.split(';')[0]
		if header!='s':
			Exception,'header not "s" in conReq state - '+header
		plainData = binascii.unhexlify(str(self.server.aes.decrypt(resp.split(';')[1])))
		subHeader=plainData.split(';')[0]
		if subHeader != 'c':
			raise Exception,'subHeader not "c" in regReq state - '+subHeader 
		timestamp=plainData.split(';')[1]
		if abs(time()-int(timestamp))>300:
			raise Exception, 'Error! The timestamp has expired.'
		self.ctime=time()
		self.state = 'connected'
	def handleRegReq(self,resp):
		header=resp.split(';')[0]
		if header!='s':
			Exception,'header not "s" in regReq state - '+header
		plainData = binascii.unhexlify(str(self.server.aes.decrypt(resp.split(';')[1])))
		subHeader=plainData.split(';')[0]
		if subHeader != 'r':
			raise Exception,'subHeader not "r" in regReq state - '+subHeader 
		if int(plainData.split(';')[1]) != (self.nounce - 1):
			raise Exception, 'Error! The nounce number sent back by the server isn\'t compatible with the\n nounce number sent originally by you... \nYou may be under attack! (You probably are)'
		self.addUsername(self.username,self.random_key)
		del self.username
		del self.random_key
		del self.nounce
		self.state='start'
	def connect(self,username):
		if self.state!='start':
			raise Exception,'Can\'t connect if the state is not \'start\'!'
		#make it send to the server the username chosen
		self.nounce = randint(1, 65536)
		key=loadKey(username)
		self.server.aes = AESCipher(key)
		self.username=username
		self.server.send('c;' + username + ';' + self.server.aes.encrypt(binascii.hexlify(username+';' + str(int(time())))))
		self.state='conReq'
	
	def addUsername(self,username,key):
		with open('users.d','a+') as f:
			f.write('{'+username+';'+key+'}\n')
			
			
			
			
	def sendInfoReq(self,username):
		requestInfoMsg =self._buildInfoMsg(username)		
		self.server.send(requestInfoMsg)
		print 'Send info Req'
		self.state='infoReqSent'
		
	def handleInfoResp(self,resp):
		header=resp.split(';')[0]
		if header!='s':
			raise Exception,'header not "s" in infoReqSent state - '+header
		data=binascii.unhexlify(self.server.aes.decrypt(resp.split(';')[1]))
		subHeader=data.split(';')[0]
		if subHeader!='m':
			raise Exception,'subHeader not "m" in infoReqSent state - '+subHeader
		nounce = data.split(';')[3]
		if nounce!=self.nounce:
			raise Exception,'Nounce didn\'t match in InfoResp -'+nounce + '-'+self.nounce
		del self.nounce
		self.state = 'connected'
		print 'Got Info Resp'
		return data.split(';')[1:]

	def isConnected(self):
		if time()-self.ctime<20:
			return True#6 Hourse
		self.state='start'
		return False
	
	def _buildInfoMsg(self,username):
		self.nounce = str(randint(1, 65536))
		return 'm;' + self.username + ';' + username + ';' + self.nounce