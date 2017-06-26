from SChat import ClientServer
from SChat import ServerConnection
from SChat import Connection
from socket import socket,gethostbyname, AF_INET, SOCK_DGRAM

from random import randint
from SChat import P2PChat
import time

username='ezra'
server=raw_input('Server: ')
c=ClientServer(ServerConnection(server,5000,None,'keys/key.pem'),username,True)
c.close()
p=P2PChat(username)
p.waitForRequest()
p.LoadChat()
p.output('1')
print p.input()
p.output('2')
print p.input()
p.output('3')
print p.input()
print p.input()
print p.input()


