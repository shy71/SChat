from SChat import ClientServer
from SChat import ServerConnection
from SChat import Connection
from socket import socket,gethostbyname, AF_INET, SOCK_DGRAM

from random import randint
from SChat import P2PChat

username='ezra'
server=raw_input('Server: ')
c=ClientServer(ServerConnection(server,5000,None,'keys/key.pem'),username,True)
c.close()
p=P2PChat(username)
p.waitForRequest()
p.LoadChat()


