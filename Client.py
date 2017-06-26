from SChat import ClientServer
from SChat import ServerConnection
from random import randint
from SChat import P2PChat
import time

username='shy'+str(randint(1,65555))
server=raw_input('Server: ')
c=ClientServer(ServerConnection(server,5000,None,'keys/key.pem'),username,False)
dIp,sharedkey, nounce,token= c.getInfo('ezra')
p=P2PChat(username)
p.startChat('ezra',dIp,5002,sharedkey,nounce,token)
p.LoadChat()
p.output('1')
print p.input()
p.output('2')
print p.input()
p.output('3')
print p.input()
print p.input()
print p.input()

