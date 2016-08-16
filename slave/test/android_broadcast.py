import time
import socket
try:
    import androidhelper as android
except:
    import android

droid = android.Android()
ACTION="android.net.conn.CONNECTIVITY_CHANGE"
droid.eventRegisterForBroadcast(ACTION, False)

droid.eventRegisterForBroadcast("android.intent.action.SCREEN_ON",False)
droid.eventRegisterForBroadcast("android.intent.action.SCREEN_OFF",False)
port=54321
droid.startEventDispatcher(port)

print(droid.eventGetBrodcastCategories())
# droid.eventPost('Some Event', "123456")
# print("some event posted")

print("Dispatcher listening on port %s" % port)
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(('localhost',port))
print("Connected to listener")
try:
    while True:
        print(s.recv(1024))
except:
  print("Socket interrupted.")
print( "Listening Done.")


