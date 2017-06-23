from ClientServer import ClientServer
from M2Crypto import RSA 
from ServerConnection import ServerConnection
from random import randint
from P2PChat import P2PChat

rsa = RSA.load_pub_key('keys/key.pem')
username='shy'+str(randint(1,65555))
c=ClientServer(ServerConnection('127.0.0.1',5000,None,rsa),username,False)
dIp,sharedkey, nounce,token= c.getInfo('ezra')
p=P2PChat()
p.startChat(username,dIp,5002,sharedkey,nounce,token)
