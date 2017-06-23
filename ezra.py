from ClientServer import ClientServer
from M2Crypto import RSA 
from ServerConnection import ServerConnection
from Connection import Connection

from random import randint
from P2PChat import P2PChat

rsa = RSA.load_pub_key('keys/key.pem')
username='ezra'
c=ClientServer(ServerConnection('127.0.0.1',5000,None,rsa),username,True)
c.close()
con=Connection('127.0.0.1',5002)
con.bind()
msg,addr=con.recvfrom()
p=P2PChat()
p.gotChatRequest(addr[0],addr[1],msg,c.getKey())

