'''
Description: CMPT-371 Assignment2 - Q1(Client)
Author: Sen Lin, Mingjian Tang
Last Modified Date: June 24th, 2018
'''
import random
import time
from socket import *
#server info from sample
serverName = 'localhost'
serverPort = 50007
clientSocket = socket(AF_INET, SOCK_DGRAM)

#user input
seeds = int(input("Please provide me a random seed: "))
total_packets = int(input("How many packets do you want to send: "))
ackSeed = int(input("Please provide me seed for determining ACKs and NACKs has been corrupted: "))
probability = float(input("Please enter a propability between 0.0 to 1.0: "))


random.seed(ackSeed)
state1 = random.getstate() #random.uniform(0.0,1.0)
#random.seed(ackSeed)
random.seed(seeds)
state2 = random.getstate()

class packet:
	data = 0 #field 1
	sequence_number = 0
	ack	= 0
	nack = 0


currentPacket = packet()
currentPacket.data = random.randint(0,4294967295)
packetstr=str(currentPacket.data)+" "+str(currentPacket.sequence_number)+" "+str(currentPacket.ack)+" "+str(currentPacket.nack)
clientSocket.sendto( packetstr.encode(), (serverName, serverPort) )
expectedTime = time.time()
print("")
print("")
print("A packet with sequence number ", currentPacket.sequence_number," is about to be sent")
print("The sender is moving to state WAIT FOR ACK OR NACK")
print("Packet to send contains: data=",currentPacket.data," seq=",currentPacket.sequence_number," ack=",currentPacket.ack," nack=",currentPacket.nack)
print("")
currentPacketNumber = 0
modifiedMessage, severAddress = clientSocket.recvfrom(2048)
packetReceivedArray = modifiedMessage.decode().split(' ') #check if can be decoded
#print(probability_array)
message = None
waitingMessage = None

while currentPacketNumber < total_packets:
#check returning packet
	if time.time() >= expectedTime:
		random.setstate(state1)
		prob = random.uniform(0.0,1.0)
		state1 = random.getstate()
		if prob > probability and int(packetReceivedArray[2])==1:
			currentPacketNumber+=1

		if currentPacketNumber == total_packets:
			print("An ACK packet has just been received") 
			print("All packages have been sent successfully. Byebye :) ")
			break
		if int (packetReceivedArray[2])==1 and currentPacket.sequence_number == 0 and prob>probability: #ack received and not corrupted, original sqnumber = 0
			currentPacket = packet()
			currentPacket.data = random.randint(0,4294967295)
			currentPacket.sequence_number = 1
			print("An ACK packet has just been received") 
			print("A packet with sequence number ", currentPacket.sequence_number," is about to be sent")
			message = "The sender is moving to state WAIT FOR CALL 1 FROM ABOVE "
			waitingMessage = "The sender is moving to state WAIT FOR ACK OR NACK "
			#currentPacketNumber += 1	
		elif int (packetReceivedArray[2])==1 and currentPacket.sequence_number == 1 and prob > probability: #ack received and not corrupted, original sqnumber = 1
			currentPacket = packet()
			currentPacket.data = random.randint(0,4294967295)
			currentPacket.sequence_number = 0
			print("An ACK packet has just been received")
			print("A packet with sequence number ", currentPacket.sequence_number," is about to be sent")
			message = "The sender is moving to state WAIT FOR CALL 0 FROM ABOVE "
			waitingMessage = "The sender is moving to state WAIT FOR ACK OR NACK "
			#currentPacketNumber += 1
	
		elif prob < probability: 										#corrupted
			print("A Corrupted ACK or NACK packet has just been received")
			if int(packetReceivedArray[2])==1:						#Ack and corrupted
				print("An ACK packet has just been received") 
			else: 													#NACK and corrupted
				print("A NACK packet has just been received") 
			if currentPacket.sequence_number == 1:
				message = "The sender is moving back to state WAIT FOR CALL 1 FROM ABOVE"
			else:
				message = "The sender is moving back to state WAIT FOR CALL 0 FROM ABOVE"
			waitingMessage = "The sender is moving back to state WAIT FOR ACK OR NACK"
			print("A packet with sequence number ", currentPacket.sequence_number," is about to be resent")

		elif int (packetReceivedArray[3])==1 and (prob > probability): 						#Nack and not corrupted					
			if currentPacket.sequence_number == 1:
				message = "The sender is moving back to state WAIT FOR CALL 1 FROM ABOVE"
			else:
				message = "The sender is moving back to state WAIT FOR CALL 0 FROM ABOVE"
			waitingMessage = "The sender is moving back to state WAIT FOR ACK OR NACK"
			print("A NACK packet has just been received") 
			print("A packet with sequence number ", currentPacket.sequence_number," is about to be resent")
							
		print("Packet to send contains: data=",currentPacket.data," seq=",currentPacket.sequence_number," ack=",currentPacket.ack," nack=",currentPacket.nack)
		random.setstate(state2)
		sleepTime = round(random.uniform(1.0,5.0))
		state2 = random.getstate()
		expectedTime+= sleepTime
		#time.sleep(sleepTime)
		print(message)
    	#send
		packetstr=str(currentPacket.data)+" "+str(currentPacket.sequence_number)+" "+str(currentPacket.ack)+" "+str(currentPacket.nack)
		clientSocket.sendto( packetstr.encode(), (serverName, serverPort))
		print(waitingMessage)
		#receive
		modifiedMessage, severAddress = clientSocket.recvfrom(2048)
		packetReceivedArray = modifiedMessage.decode().split(' ')
		print("")
		print("")

clientSocket.close()