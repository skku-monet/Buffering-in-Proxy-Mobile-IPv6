from socket import *
import string
import time
import sys
import datetime
import struct
import binascii

if len(sys.argv) != 2:
	sys.exit("Usage: python client_test.py <packetrate>")

host = "cnode" 	# servername
port = 9079
bandwidth = 128		# kbytes per second

UDPSock = socket(AF_INET6,SOCK_DGRAM)
print "server running on %s port %s" % (host, port)

try:        
	bandwidth = int(sys.argv[1])
	numpacket = 5000 
	s = struct.Struct('Q 1016s')	# 2048 bytes
	info = struct.Struct('I I')     # (number packets, bandwidth)
except:
	numpacket = None
	s = None
	print "Invalid number of kbytes for sending"
				
if not s:
	pass
else:
	try:
		sequence = 0
		totalsend = 0
		pkgsend = 0
		elapse = 0
        
		print "client will send %s packets in sending rate %s numpacket/s" % (numpacket, bandwidth)
		while (totalsend < numpacket):
			sequence += 1
			values = (sequence, 'X'*1016)			# 2048 bytes
			packed_data = s.pack(*values)
			
			if (UDPSock.sendto(packed_data,(host,port))):
				pkgsend += 1
				totalsend += 1
			else:
				print "Send error!"
				
			elapse += 1000 / bandwidth 	
			time.sleep(1.0 / bandwidth) # 5ms send 1 packet or packetrate=200		

			if (totalsend >= numpacket or elapse >= 1000):
				now = datetime.datetime.now()
				print "%s Send: %s packets, %s total packets" % (now.time(), pkgsend, totalsend)
				pkgsend = 0
				elapse = 0.0
		print "elapse: %s" % (elapse)
		UDPSock.sendto("FINISH",(host,port)) # send to server to notify finish
		print "Done. Total send: %s packets" % (totalsend)

	except:
		print "Send failed"
UDPSock.close()
