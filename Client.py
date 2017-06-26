from SChat import ClientServer
from SChat import ServerConnection
from random import randint
from SChat import P2PChat
import time
import threading

username='shy'+str(randint(1,65555))
server=raw_input('Server: ')
c=ClientServer(ServerConnection(server,5000,None,'keys/key.pem'),username,False)
dIp,sharedkey, nounce,token= c.getInfo('ezra')
p=P2PChat(username)
p.startChat('ezra',dIp,5002,sharedkey,nounce,token)
p.LoadChat()

def run():
	while True:
		data=p.input()
		if data:
			print 'Input: ' + data
			data=None
		
recv_thread = threading.Thread(target=run)
recv_thread.setDaemon(True)
recv_thread.start()
while True:
	inp=raw_input('Output: ')
	p.output(inp)



