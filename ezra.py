from SChat import ClientServer
from SChat import ServerConnection
from random import randint
from SChat import P2PChat
import time
import threading

username='ezra'
server=raw_input('Server: ')
c=ClientServer(ServerConnection(server,5000,None,'keys/key.pem'),username,True)
c.close()
p=P2PChat(username)
p.waitForRequest()
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



