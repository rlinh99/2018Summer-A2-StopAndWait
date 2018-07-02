'''
Description: CMPT-371 Assignment2 - Q1(Server)
Author: Sen Lin, Mingjian Tang
Last Modified Date: June 24th, 2018
'''
import sys
from socket import *
import random
serverHost = "127.0.0.1"
serverPort = 50007
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(( serverHost, serverPort))



corruptedSeed = int(input("Please provide me seed for determining ACKs and NACKs has been corrupted: "))
probability = float(input("Please enter a propability between 0.0 to 1.0: "))
print("")
print("")


random.seed(corruptedSeed)
class ackPKG:
	data = 0
	sequence_number = 0
	ack	= 1
	nack = 0
class nackPKG:
	data = 0
	sequence_number = 0
	ack	= 0
	nack = 1

class receivedPacket:
	data = 0 
	sequence_number = 0
	ack	= 0
	nack = 0

def isCorrupted():
	prob = random.uniform(0.0,1.0)
	if prob < probability:
		#print(prob)
		return 1
	else:
		#print(prob)
		return 0

outPacket = receivedPacket()
inPacket = receivedPacket()
packetMessage = ""
packetCounter = 0

while True:
	sentence,clientAddress = serverSocket.recvfrom(1024)
	messageReceivedArray = sentence.decode().split(' ')
	#packet corrupted
	if isCorrupted() == 1:
		outPacket = nackPKG()
		packetMessage = str(outPacket.data)+" "+str(outPacket.sequence_number)+" "+str(outPacket.ack)+" "+str(outPacket.nack)
		print("A Corrupted packet has just been received")
		print("A NACK is about to be sent ")
		serverSocket.sendto(packetMessage.encode(), clientAddress) #send nack

		if int(messageReceivedArray[1]) == 0:
			print("The receiver is moving back to state WAIT FOR 0 FROM BELOW")
		else:
			print("The receiver is moving back to state WAIT FOR 1 FROM BELOW")
	#packet is fine
	else:
		outPacket = ackPKG()
		packetMessage = str(outPacket.data)+" "+str(outPacket.sequence_number)+" "+str(outPacket.ack)+" "+str(outPacket.nack)
		print("An ACK is about to be sent ")
		serverSocket.sendto(packetMessage.encode(), clientAddress) #send ack
	
	print("Packet to send contains: data=",outPacket.data," seq=",outPacket.sequence_number," ack=",outPacket.ack," nack=",outPacket.nack)
	


	# first time packet
	if packetCounter == 0: 
		print("A packet with sequence number ",messageReceivedArray[1]," has been received ")
		inPacket.data = int (messageReceivedArray[0])
		inPacket.sequence_number = int (messageReceivedArray[1])
		inPacket.ack = int (messageReceivedArray[2])
		inPacket.nack = int (messageReceivedArray[3])
		packetCounter+=1
		if int(messageReceivedArray[1]) == 0:
			print("The receiver is moving to state WAIT FOR 1 FROM BELOW ")
		else:
			print("The receiver is moving to state WAIT FOR 0 FROM BELOW ")
	elif int(messageReceivedArray[1]) == inPacket.sequence_number:  #duplicate packet received
		print("A duplicate packet with sequence number",inPacket.sequence_number,"has been received")
		if inPacket.sequence_number == 1:
			print("The receiver is moving back to state WAIT FOR 0 FROM BELOW ")
		else:
			print("The receiver is moving back to state WAIT FOR 1 FROM BELOW ")

	else:															#brand new packet received
		print("A packet with sequence number ",messageReceivedArray[1]," has been received ")
		inPacket.data = int (messageReceivedArray[0])
		inPacket.sequence_number = int (messageReceivedArray[1])
		inPacket.ack = int (messageReceivedArray[2])
		inPacket.nack = int (messageReceivedArray[3])
		packetCounter+=1
		if inPacket.sequence_number == 0:
			print("The receiver is moving to state WAIT FOR 1 FROM BELOW")
		else:
			print("The receiver is moving to state WAIT FOR 1 FROM BELOW")

	print("Packet received contains: data ", int(messageReceivedArray[0]),"seq =", int(messageReceivedArray[1]), "ack = ", int(messageReceivedArray[2]), "nack = ", int(messageReceivedArray[3]))
	print("")
	print("")