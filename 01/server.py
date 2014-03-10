from socket import *
import time
import datetime
import struct
import binascii
import csv

host = "::"		# want to bind on all IPv6 addr client
port = 9079
buffer = 102400
bandwidth = 128 	# default value, kbytes per sencond

# Create socket and bind to address
UDPSock = socket(AF_INET6,SOCK_DGRAM)
UDPSock.bind((host,port))

print "Starting UDP receive server...  control-C to exit."
print "Waiting for data..."

total = 0
s = struct.Struct('Q 1016s') #Q : unsigned long long = 8 bytes
info = struct.Struct('I I')
myfile = open("data.csv","w")
csvfile = csv.writer(myfile, delimiter=',')
num = 2000
ok = 0
while 1:
	data,addr = UDPSock.recvfrom(buffer)
	if not data:
		print "No data."
		break
	elif (len(data) == len("START")):
		print "START..."
		ok = 1
	elif (ok == 1):
		unpacked_info = info.unpack(data)
		print "Client will send total packets %s in bandwidth %s\n" % (unpacked_info[0], unpacked_info[1])
		header = ['Total packet send %d' % unpacked_info[0], 'Bandwidth send %d' % unpacked_info[1]]
		csvfile.writerow(header)
		header = ['Time', 'Sequence Number', 'Total Received Packets']
		csvfile.writerow(header)
		num = unpacked_info[0]
		ok = 0
	elif (len(data) == len("FINISH")):
		myfile.flush()
          	print "FINISH: RECEIVE %s packets,  LOST %s packets\n" % (total, num - total)
		total = 0;
	else:
		total += 1
		now = datetime.datetime.now()
		unpacked_data = s.unpack(data)
		out_data = [now.time(), unpacked_data[0], total]
		csvfile.writerow(out_data)
		print now.strftime("%Y-%m-%d %H:%M:%S") + " Sequence Number: %s, total package: %s \n" % (unpacked_data[0] , total)		
UDPSock.close()
