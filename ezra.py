from ClientChat import ClientChat
from M2Crypto import RSA 
from ServerConnection import ServerConnection
from random import randint

rsa = RSA.load_pub_key('keys/key.pem')
c=ClientChat(ServerConnection('127.0.0.1',5000,None,rsa))
username='ezra'
c.connect(username)
c.serverRecv()
c.waitForChat()