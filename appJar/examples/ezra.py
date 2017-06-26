from ClientServer import ClientServer
from M2Crypto import RSA 
from ServerConnection import ServerConnection
from Connection import Connection
from socket import socket,gethostbyname, AF_INET, SOCK_DGRAM

from random import randint
from P2PChat import P2PChat

rsa = RSA.load_pub_key('keys/key.pem')
username='ezra'
c=ClientServer(ServerConnection('127.0.0.1',5000,None,rsa),username,True)
c.close()
mySocket = socket( AF_INET, SOCK_DGRAM )
hostName = gethostbyname( '0.0.0.0' )
mySocket.bind( (hostName, 5002) )
msg,addr=mySocket.recvfrom(2048)
mySocket.close()
p=P2PChat()
p.gotChatRequest(addr[0],addr[1],msg,c.getKey())
p.LoadChat()


