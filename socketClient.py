#!/usr/bin/env python
# encoding: UTF-8

import socket
import sys,getopt
import xmlReader
import CondorTools

chirp = CondorTools.CondorChirp()
class Client:

	def __init__(self,config):
		self.config = config
		print ("client init")

	def get_constant(self, prefix):
		"""Create a dictionary mapping socket module constants to their names."""
		return dict( (getattr(socket, n), n)
						for n in dir(socket) if n.startswith(prefix)
					)

	def get_constants(self, sock):
		families = self.get_constant('AF_')
		types = self.get_constant('SOCK_')
		protocols = self.get_constant('IPPROTO_')		
		
		print >>sys.stderr, 'Family  :', families[sock.family]
		print >>sys.stderr, 'Type    :', types[sock.type]
		print >>sys.stderr, 'Protocol:', protocols[sock.proto]
		print >>sys.stderr

	
		 
	def demand(self):
		
		print ("client demand")
		try:
			xmlHandler = xmlReader.XmlHandler(self.config)
		except:
			print "xml read error"
			sys.exit()
		host, port, path, timestamp, offset = xmlHandler.read()
		print "five vals:"
		print host, port, path, timestamp, offset
			
		interval = 5
		maxtries = 12*3
		serverInfo = chirp.getJobAttrWait("IperfServer",None,interval, maxtries)	
		print "serverInfo is:" + serverInfo
		#hostFromCondor,portFromCondor = serverInfo.strip("'").split()
		#print hostFromCondor, portFromCondor
		# Create a TCP/IP socket
		sock = socket.create_connection((host, int(port)))
		self.get_constants(sock)
		
		print host, port, path, timestamp, offset

		try:
			# Send data
			message = timestamp + ',' + offset
			sock.sendall(message)
			amount_received = 0			
			amount = sock.recv(8)
			print amount
			if amount:
				sock.sendall("kunBegin")
			else:
				sock.sendall("kunStop")
    			
			dataComp = ""
			while amount_received < int(amount):
				print (amount_received, amount)
				data = sock.recv(128)
				dataComp += data
				amount_received += len(data)
			
			strAdded, timestamp, offset = dataComp.split("KUNSIGN")
			
			print strAdded
			
			with open(path, "a") as output:
				output.write(strAdded)
			print "time is " + timestamp
			if timestamp and offset:
				xmlHandler.write(timestamp, offset, self.config)
		
		finally:
			print >>sys.stderr, 'closing socket'
			sock.close()
			print("dadada")

if __name__ == '__main__':
	client = Client()
	client.demand()
