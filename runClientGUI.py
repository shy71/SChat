from SChat import SChatMainGUI

serverIp='127.0.0.1' #<- Enter static server Ip (Hardcoded))
#This is release way of runing, for testing you can also use "python SChatMainGUI.py <ServerIP>", but it may need some adapting in order to run successfully
main=SChatMainGUI(serverIp)
main.startGui()