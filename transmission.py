#! /usr/bin/env python
import os
import sys
import socketClient
import socketServer
import socket


## *****************************
## main routine
## *****************************

if len(sys.argv) < 3:
	print ("val numbers error")
for string in sys.argv:
	print string

path = sys.argv[1]
host = ""
port = sys.argv[2]
config = sys.argv[3]
print "hello world"

print path, host, port, config
if int(os.environ['_CONDOR_PROCNO']) == 0:
	client = socketClient.Client(config)
	print ("client start")
	print socket.gethostname(), socket.gethostbyname(socket.gethostname()) 
	client.demand()		
else:
	print("server start")
	server = socketServer.Server(path, host, port)
	server.serve()

