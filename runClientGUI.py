from SChat import SChatMainGUI

serverIp='127.0.0.1' #<- Enter static server Ip (Hardcoded))
#This is relese way of runing, for testing use python MainWindow.py <ServerIP>
main=SChatMainGUI(serverIp)
main.startGui()