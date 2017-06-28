from UserChat import UserChat
from random import randint
from AESCipher import AESCipher
from time import time
from SChatError import SChatError,toSChatError
import re
import binascii
import os

LOCAL_USERS_FILE_PATH='localusers.data'
def loadKey(username):
	with open(LOCAL_USERS_FILE_PATH,'a+') as f:
		return re.search('{'+username+';([a-z|0-9]+)}\n',f.read()).group(1)
def isRegister(username):
		with open(LOCAL_USERS_FILE_PATH,'a+') as f:
			return re.search('{'+username+';([a-z|0-9]+)}\n',f.read()) != None
class ClientChat:
	def __init__(self,server):
		self.server=server
		self.state='start'
		self.chats={}
	def register(self,username):
		if self.state!='start':
			raise SChatError('Can\'t send register request in the middle of a diffrent request')
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
			raise toSChatError(resp.split(';')[1])
		if self.state=='regReq':
			self.handleRegReq(resp)
		if self.state=='conReq':
			self.handleConReq(resp)
		if self.state=='infoReqSent':
			return self.handleInfoResp(resp)
	def handleConReq(self,resp):
		header=resp.split(';')[0]
		if header!='s':
			raise SChatError('Got invalid msg(header) while in \'conReq\' state!')
		plainData = binascii.unhexlify(str(self.server.aes.decrypt(resp.split(';')[1])))
		subHeader=plainData.split(';')[0]
		if subHeader != 'c':
			raise SChatError('Got invalid msg(subHeader) while in \'conReq\' state!')
		timestamp=plainData.split(';')[1]
		if abs(time()-int(timestamp))>300:
			raise SChatError('Received timestamp of the connect response from the server has expired, please try again')
		self.ctime=time()
		self.state = 'connected'
	def handleRegReq(self,resp):
		header=resp.split(';')[0]
		if header!='s':
			raise SChatError('Got invalid msg(header) while in \'regReq\' state!')
		plainData = binascii.unhexlify(str(self.server.aes.decrypt(resp.split(';')[1])))
		subHeader=plainData.split(';')[0]
		if subHeader != 'r':
			raise SChatError('Got invalid msg(subHeader) while in \'regReq\' state!')
		if int(plainData.split(';')[1]) != (self.nounce - 1):
			raise SChatError('Received nounce sent back by the server isn\'t compatible with the\n nounce number sent originally by you... \nYou may be under attack if this error continue to apper!')
		self.addUsername(self.username,self.random_key)
		del self.username
		del self.random_key
		del self.nounce
		self.state='start'
	def connect(self,username):
		if self.state!='start':
			raise SChatError('Can\'t send CONNECT request in the middle of a diffrent request')
		key=loadKey(username)
		self.server.aes = AESCipher(key)
		self.username=username
		self.server.send('c;' + username + ';' + self.server.aes.encrypt(binascii.hexlify(username+';' + str(int(time())))))
		self.state='conReq'
	
	def addUsername(self,username,key):
		with open(LOCAL_USERS_FILE_PATH,'a+') as f:
			f.write('{'+username+';'+key+'}\n')

	def sendInfoReq(self,username):
		requestInfoMsg =self._buildInfoMsg(username)		
		self.server.send(requestInfoMsg)
		self.state='infoReqSent'
		
	def handleInfoResp(self,resp):
		header=resp.split(';')[0]
		if header!='s':
			raise SChatError('Got invalid msg(header) while in \'infoReqSent\' state!')
		data=binascii.unhexlify(self.server.aes.decrypt(resp.split(';')[1]))
		subHeader=data.split(';')[0]
		if subHeader!='m':
			raise SChatError('Got invalid msg(subHeader) while in \'infoReqSent\' state!')
		nounce = data.split(';')[3]
		if nounce!=self.nounce:
			raise SChatError('Received nounce sent back by the server isn\'t compatible with the\n nounce number sent originally by you... \nYou may be under attack if this error continue to apper!')
		del self.nounce
		self.state = 'connected'
		return data.split(';')[1:]

	def isConnected(self):
		if time()-self.ctime<21600:
			return True#6 Hourse
		self.state='start'
		return False
	
	def _buildInfoMsg(self,username):
		self.nounce = str(randint(1, 65536))
		return 'm;' + self.username + ';'+self.server.aes.encrypt(binascii.hexlify(username + ';' + self.nounce))
