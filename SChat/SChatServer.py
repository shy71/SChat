import re
from SChat import AESCipher
from M2Crypto import RSA
from time import time
import binascii
import os
from SChat import ServerError
from SChat import Connection


class SChatServer:
	def __init__(self,path_to_rsa,passphrase,userfilepath):
		self.usersIp={}
		self.usersConnectTime={}
		self.userfilepath=userfilepath
		self.rsa=RSA.load_key(path_to_rsa,lambda x: passphrase)
		self.users=self.getUsers()
		self.con=Connection('0.0.0.0',0)
		self.con.bind(5000,None)
		print 'Server Ready'
	def runServer(self):
		while True:
				data,addr=self.con.recvfrom()
				self.handleMsg(addr,data)
	#def getPassprashe(num):
	#	return 'shy71' 
	def registerUsername(self,addr,userName,symtric_key):
		if userName in self.users:
			self.sendError(addr,'11')
		if not self.isUserNameValid(userName):
			self.sendError(addr,'12')
		self.users[userName]=symtric_key
		self.addToUsersFile(userName,symtric_key)
	def isUserNameValid(self,userName):
		for let in userName:
			if not (let.isdigit() or let.islower()):
				return False
		return True
	def addToUsersFile(self,userName,symtric_key):
		with open(self.userfilepath,'a') as f:
			f.write('{'+userName+';'+symtric_key+'}\n')

	def getUsers(self):
		with open(self.userfilepath,'r') as f:
			return {self.parseName(line):self.parseKey(line) for line in f}

	def parseName(self,line):
		return re.search('^{([a-z|0-9]+);([a-z|0-9]+)}$',line).group(1)
	def parseKey(self,line):
		return re.search('^{([a-z|0-9]+);([a-z|0-9]+)}$',line).group(2)
	def sendError(self,addr,error):
		self.sendRespToIp(addr,'e;'+error)
		raise ServerError(error)
	def sendConfirmation(self,addr,userName,nounce):
		self.sendRespToIp(addr,'s;'+self.encrypForUser(userName,'r;'+str(int(nounce)-1)))
	def sendSucess(self,addr,userName,msg):
		self.sendRespToIp(addr,'s;'+self.encrypForUser(userName,msg))
	def sendRespToIp(self,addr,msg):
		self.con.sendto(msg,addr)
	def encrypForUser(self,userName,msg):
		return self.encryptAES(self.users[userName],msg)
	def decrypForUser(self,userName,msg):
		return self.decryptAES(self.users[userName],msg)
	def encryptAES(self,key,msg):
		return AESCipher.AESCipher(key).encrypt(binascii.hexlify(msg))
	def decryptAES(self,key,msg):
		return binascii.unhexlify(AESCipher.AESCipher(key).decrypt(msg))
	def handleMsg(self,addr,msg):
		try:
			dMsg=self.rsa.private_decrypt(msg,RSA.pkcs1_oaep_padding)
			header=dMsg.split(';')[0]
			if header=='r': #r;UserName;symtric_key;Nounce
				userName,symtric_key,nounce=dMsg.split(';')[1:] 
				print 'Got register Msg - ' + userName
				self.registerUsername(addr,userName,symtric_key)
				#userOnline(userName,addr)
				self.sendConfirmation(addr,userName,nounce)
			elif header=='m':
				srcUser,desUser,nounce=dMsg.split(';')[1:]
				print 'Got Requset for details - ' + srcUser+ ' -> '+ desUser
				if srcUser not in self.usersIp:
					self.sendError(addr,'31')
				newKey=self.genAes()
				self.sendInfo(addr,srcUser,desUser,nounce,newKey)
			elif header=='c':
				srcUser,token=dMsg.split(';')[1:]
				print 'Got connect Requset - '+srcUser
				tokenStatus=self.connectTokenValid(addr,srcUser,token)
				if tokenStatus!=1:
					self.sendError(addr,str(tokenStatus))
		except ServerError as er:
			print 'Error - ' + er
			
	def connectTokenValid(self,addr,srcUser,token):
		decToken=self.decrypForUser(srcUser,token)
		tokUser,tokTime=decToken.split(';')
		if tokUser!=srcUser:
			return 21
		if abs(time()-int(tokTime))>300:
			return 22
		self.usersIp[srcUser]=addr[0]
		self.usersConnectTime[srcUser]=time()
		self.sendSucess(addr,srcUser,'c;'+tokTime)
		return 1
	def sendInfo(self,addr,srcUser,desUser,nounce,sharedKey):
		if desUser not in self.users:
			self.sendError(addr,'32')
		if desUser not in self.usersIp:
			self.sendError(addr,'33')
		if time()-self.usersConnectTime[srcUser]>21600:
			del self.usersIp[desUser]
			del self.usersConnectTime[desUser]
		token=srcUser+';'+sharedKey+';'+str(nounce)
		encToken=self.encrypForUser(desUser,token) 
			#raise Exception(encrypForUser(userName,'Error - User '+desUser+' not connected'))
		self.sendSucess(addr,srcUser,'m;'+self.usersIp[desUser]+';'+sharedKey+';'+nounce+';'+encToken)
		
	def genAes(self):
		return binascii.hexlify(os.urandom(32))
