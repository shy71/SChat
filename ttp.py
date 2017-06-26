from socket import socket, gethostbyname, AF_INET, SOCK_DGRAM
import re
import sys
from SChat import AESCipher
from M2Crypto import RSA
from time import time
import binascii
import os
from SChat import ServerError
PORT_NUMBER = 5000
SIZE = 256
mySocket = socket( AF_INET, SOCK_DGRAM )


def startServer():


	hostName = gethostbyname( '0.0.0.0' )
		
	mySocket.bind( (hostName, PORT_NUMBER) )
	print 'Server Up'
	while True:
		print 'Waiting for transmissions'
		data,addr=mySocket.recvfrom(SIZE)
		handleMsg(addr,data)



def registerUsername(addr,userName,symtric_key):
	if userName in users:
		sendError(addr,'11')
		#raise Exception(encryptAES(symtric_key,'Error - Username '+userName+' already registered'))
	if not isValid(userName):
		sendError(addr,'12')
	users[userName]=symtric_key
	addToUsersFile(userName,symtric_key)
def isValid(userName):
	for let in userName:
		if not (let.isdigit() or let.islower()):
			return False
	return True
def addToUsersFile(userName,symtric_key):
	with open('users.data','a') as f:
		f.write('{'+userName+';'+symtric_key+'}\n') #timestamp?

def getUsers():
	with open('users.data','r') as f:
		return {parseName(line):parseKey(line) for line in f}

def parseName(line):
	return re.search('^{([a-z|0-9]+);([a-z|0-9]+)}$',line).group(1)
def parseKey(line):
	return re.search('^{([a-z|0-9]+);([a-z|0-9]+)}$',line).group(2)
def sendError(addr,error):
	sendRespToIp(addr,'e;'+error)
	raise ServerError(error)
def sendConfirmation(addr,userName,nounce):
	sendRespToIp(addr,'s;'+encrypForUser(userName,'r;'+str(int(nounce)-1)))
def sendSucess(addr,userName,msg):
	sendRespToIp(addr,'s;'+encrypForUser(userName,msg))
def sendRespToIp(addr,msg):
	mySocket.sendto(msg,addr)
def encrypForUser(userName,msg):
	return encryptAES(users[userName],msg)
def encryptAES(key,msg):
	return AESCipher.AESCipher(key).encrypt(binascii.hexlify(msg))
def decryptAES(key,msg):
	return binascii.unhexlify(AESCipher.AESCipher(key).decrypt(msg))
def getPassprashe(num):
	return 'shy71' 
usersIp={'ezra':'127.0.0.1'}
users=getUsers()
rsa=RSA.load_key('keys/private.pem',getPassprashe)	
def handleMsg(addr,msg):
	try:
		dMsg=rsa.private_decrypt(msg,RSA.pkcs1_oaep_padding)
		header=dMsg.split(';')[0]
		if header=='r': #r;UserName;symtric_key;Nounce
			userName,symtric_key,nounce=dMsg.split(';')[1:] 
			print 'Got register Msg - ' + userName
			registerUsername(addr,userName,symtric_key)
			#userOnline(userName,addr)
			sendConfirmation(addr,userName,nounce)
		elif header=='m':
			srcUser,desUser,nounce=dMsg.split(';')[1:]
			print 'Got Requset for details - ' + srcUser+ ' -> '+ desUser
			if srcUser not in usersIp:
				sendError(addr,'31')
			newKey=genAes()
			sendInfo(addr,srcUser,desUser,nounce,newKey)
		elif header=='c':
			srcUser,token=dMsg.split(';')[1:]
			print 'Got connect Requset - '+srcUser
			tokenStatus=connectTokenValid(addr,srcUser,token)
			if tokenStatus!=1:
				sendError(addr,str(tokenStatus))
	except ServerError as er:
		print 'Error - ' + er
		
def connectTokenValid(addr,srcUser,token):
	decToken=decryptAES(users[srcUser],token)
	tokUser,tokTime=decToken.split(';')
	if tokUser!=srcUser:
		return 21
	if abs(time()-int(tokTime))>300:
		return 22
	usersIp[srcUser]=addr[0]
	sendSucess(addr,srcUser,'c;'+tokTime)
	return 1
	
def userOnline(userName,addr):
	usersIp[userName]=addr[0]
		
def sendInfo(addr,srcUser,desUser,nounce,sharedKey):
	if desUser not in users:
		sendError(addr,'32')
	if desUser not in usersIp:
		sendError(addr,'33')
	token=srcUser+';'+sharedKey+';'+str(nounce)
	encToken=encrypForUser(desUser,token) 
		#raise Exception(encrypForUser(userName,'Error - User '+desUser+' not connected'))
	sendSucess(addr,srcUser,'m;'+usersIp[desUser]+';'+sharedKey+';'+nounce+';'+encToken)
	
def genAes():
	return binascii.hexlify(os.urandom(32))
	
if __name__=='__main__':
	startServer()
