import sys
from socket import socket, AF_INET, SOCK_DGRAM,gethostbyname
from Crypto import Random
import base64
import hashlib
from time import time
from Crypto.Cipher import AES
from M2Crypto import RSA
from random import randint
from AESCipher import AESCipher
import os
import binascii
from P2PConnection import P2PConnection,Connection
errorStr={11:'The username is already registered',
      12:'Username isn\'t valid, only lowercase letters and numbers',
      21:'Authentication token isn\'t valid, wrong username',
      22:'Authentication token isn\'t valid, timestamp expired',
      31:'You are not connected!',
      32:'Desired user isn\'t connected'}

SIZE = 1024
SERVER_IP   = '127.0.0.1'
PORT_NUMBER = 5000
server=Connection(SERVER_IP,PORT_NUMBER)


random=Random.new()
#make it send to the server the username chosen
nounce = randint(1, 65536)
random_key = binascii.hexlify(os.urandom(32)) #random_key = '8d043c91e350a170562b51fe91dbabd04a965b1908c97ca9ce24a40826f23684'

connected = 0




temp_user='shy'+str(randint(1,65555)) #'ezra'
def openSession():
	bob_username ='ezra'# raw_input('Enter the username of the account you want to send a message to:')
	msg = createMsg(bob_username)
	
	rsa = RSA.load_pub_key('keys/key.pem')
	enc = rsa.public_encrypt(msg,RSA.pkcs1_oaep_padding)
	print 'Encrypted message with rsa public key'
	
	server.send(enc)
	print 'Sent message to server'
	
	print 'Receiving data from server'
	received_data = server.recv()
	print 'Received data'
	
	handleHeader(received_data,bob_username,0);

	
def createMsg(bob_username):
	#make it send to the server the username chosen
	username =temp_user# raw_input('Enter your username:')
	token = randint(1, 65536)
	msg = 'm;' + username + ';' + bob_username + ';' + str(token)
	print 'Finished building message'
	return msg

def connectToServer():
	#make it send to the server the username chosen
	username = temp_user# raw_input('Enter your username:')
	nounce = randint(1, 65536)
	aeslifier = AESCipher(random_key)
	msg = 'c;' + username + ';' + aeslifier.encrypt(binascii.hexlify(username+';' + str(int(time()))))
	rsa = RSA.load_pub_key('keys/key.pem')
	
	server.send(rsa.public_encrypt(msg,RSA.pkcs1_oaep_padding))
	received_data = server.recv()
	
	handleHeader(received_data,'',0)
    
def Register():
	SIZE = 1024
	print ("Test client sending packets to IP {0}, via port {1}\n".format(SERVER_IP, PORT_NUMBER))
	
	#make it send to the server the username chosen
	username =temp_user#  raw_input('Enter your username:')
	nounce = randint(1, 65536)
	msg = 'r;' + username + ';' + random_key + ';' + str(nounce)
	print 'Finished building message'
	
	rsa = RSA.load_pub_key('keys/key.pem')
	enc = rsa.public_encrypt(msg,RSA.pkcs1_oaep_padding)
	print 'Encrypted message with rsa public key'
	server.send(enc)
	print 'Sent message to server'
	
	print 'Receiving data from server'
	received_data = server.recv()
	
	handleHeader(received_data,'',nounce)
	
usersSockets={}
def handleHeader(data,bob_username,nounce):
	header = data.split(';')[0]
	actualData = data.split(';')[1]
	if header == 's': # success
		print 'Received data'
		aeslifier = AESCipher(random_key)
		plainData = binascii.unhexlify(str(aeslifier.decrypt(actualData)))
		subHeader = plainData.split(';')[0]
		if subHeader == 'r':
			rcvNounce = plainData.split(';')[1]
			if not (int(rcvNounce) == (nounce - 1)):
				print 'Error! The nounce number sent back by the server isn\'t compatible with the\n nounce number sent originally by you... \nYou may be under attack! (You probably are)'
			else:
				print 'The registration has been completed successfully!'
		elif subHeader == 'c':
			timestamp=plainData.split(';')[1]
			if abs(time()-int(timestamp))>300:
				print 'Error! The timestamp has expired.'
			else:
				connected = 1
				print 'Connection completed successfully'
		elif subHeader == 'm':# success message sending
			#the message is built
			#s;m;bobip;newkey;nounce;(alice,newkey,nounce)kAlice
			bobip,newkey,nounce,token = plainData.split(';')[1:]
			usersSockets[bob_username]=P2PConnection(bobip,-1,newkey,temp_user,bob_username)
			sendSynMessage(bob_username,token,nounce)
			print 'chat setup completed'
		else:
			print 'Error in message format'
	elif header == 'e':#error
		print errorStr[int(actualData)]
	else:
		print 'Error in message format'
	#add the syn message receive
	
def getSynHiMessageToken(hiMessage,aliceip,aliceport):
	header = hiMessage.split(';')[0]
	if(header == 'h'):
		token =binascii.unhexlify(AESCipher(random_key).decrypt(hiMessage[2:]))						   
		alice_username,newkey,nounce = token.split(';')
		return alice_username,newkey,nounce
def checkGMessageNounceCompatability(GMessage,chat_aeslifier,nounce):
	header = GMessage.split(';')[0]
	if (header == 'g'):
		incremented_nounce = chat_aeslifier.decrypt(GMessage[2:])
		if int(incremented_nounce) == int(nounce) + 1:																
			return True
	return False
	
def checkOkMessageNounce(OkMessage,nounce,key):
	header = OkMessage.split(';')[0]
	if (header == 'o'):
		rcvnounce = AESCipher(key).decrypt(OkMessage[2:])
		if rcvnounce == nounce:
			return True
	return False

def receiveSynMessage(addr,hiMessage):
	print 'Got Syn Request'					
	aliceip,aliceport=addr
	alice_username,newkey,nounce = getSynHiMessageToken(hiMessage,aliceip,aliceport)
	usersSockets[alice_username]=P2PConnection(aliceip,aliceport,newkey,temp_user,alice_username)
	chat_aeslifier = AESCipher(newkey)
	usersSockets[alice_username].send('o;' + chat_aeslifier.encrypt(nounce))
	
	#expect the next message (g - ack)
	GMessage = usersSockets[alice_username].recv()
	nounceCompataible = checkGMessageNounceCompatability(GMessage,chat_aeslifier,nounce)
	if not nounceCompataible:
		print 'The G message is not compatible'
	print 'done with the sync proccess. The session has been opened successfully'
	return alice_username
CHAT_SYN_PORT=5001
def sendSynMessage(username,token,nounce):
	
    #send the last part -
	usersSockets[username].send('h;' + token)
	print 'sent Syn Request - '+username
	#receive the ok message from the other side
	OkMessage,addr = usersSockets[username].recvfrom()
	usersSockets[username].port=addr[1]
	nounceCompataible = checkOkMessageNounce(OkMessage,nounce,usersSockets[username].key)
	if not nounceCompataible:
		print 'The ok message isn\'t comatible'
	else:
		#send g message to complete the sync process
		usersSockets[username].send('g;' + AESCipher(usersSockets[username].key).encrypt(str(int(nounce) + 1)))
		print 'The session sync has been completed'

def waitForConnection():
	con=Connection(gethostbyname( '0.0.0.0' ),CHAT_SYN_PORT)
	con.bind()
	data,addr=con.recvfrom()
	if data.startswith('h;'):
		return receiveSynMessage(addr,data)
		
def startChat(username,starter):
	print 'Started Secured Chat - '+username
	if starter:
		usersSockets[username].sendChat(raw_input(temp_user+': '))
	while True:
		print username+': '+usersSockets[username].recvChat()
		usersSockets[username].sendChat(raw_input(temp_user+': '))
	
if __name__=='__main__':
	Register()
	connectToServer()
	openSession()
	startChat('ezra',True) #	startChat(waitForConnection(),False)










