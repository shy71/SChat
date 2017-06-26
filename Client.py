from ClientServer import ClientServer
from ServerConnection import ServerConnection
from random import randint
from P2PChat import P2PChat
import time

username='shy'+str(randint(1,65555))
c=ClientServer(ServerConnection('127.0.0.1',5000,None,'keys/key.pem'),username,False)
time.sleep(25)
dIp,sharedkey, nounce,token= c.getInfo('ezra')
p=P2PChat(username)
p.startChat('ezra',dIp,5002,sharedkey,nounce,token)
p.LoadChat()
