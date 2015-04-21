#! /usr/bin/env python
import os
import sys
import socketClient
import socketServer
import socket
import TimedExec
from IDPLException import *


## *****************************
## main routine
## *****************************

serverTimeout = 120
clientTimeout = 30
server = "./socketServer.py"
client = "./socketClient.py"

if len(sys.argv) < 3:
	print ("val number error")
for string in sys.argv:
	print string

path = sys.argv[1]
host = ""
port = sys.argv[2]
config = sys.argv[3]

print path, host, port, config
if int(os.environ['_CONDOR_PROCNO']) == 0:
	#client = socketClient.Client(config)
	print ("client start")
	print socket.gethostname(), socket.gethostbyname(socket.gethostname()) 
	resultcode,output,err=TimedExec.runTimedCmd(clientTimeout,[client, config])
	if resultcode < 0:
                print("Timeout! Result code: %d" % resultcode)
                raise TimeOutException("client")
	#client.demand()		
else:
	print("server start")
	#server = socketServer.Server(path, host, port)
	resultcode,output,err=TimedExec.runTimedCmd(serverTimeout, [server, path, host, port])
	if resultcode < 0:
		print("Result code: %d" % resultcode)
		raise TimeOutException("server")
	#server.serve()

