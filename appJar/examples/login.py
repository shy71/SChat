import sys
import time
sys.path.append("../../")
from appJar import gui

app = gui("Login Window", "400x200")
app.setBg("orange")
app.setFont(18)


def press(button):
    if button == "Cancel":
        app.stop()
    else:
        usr = app.getEntry("Username")
        pwd = app.getEntry("Password")
        print ("User:", usr, "Pass:", pwd)
		
		

app.addLabel("title","Test")
app.addLabelEntry("Username")
app.addLabelSecretEntry("Password")
app.setLabelBg("title","red")
app.addButtons(["Submit", "Cancel"], press)
app.go()