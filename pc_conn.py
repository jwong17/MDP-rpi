import socket
import sys
import time

class PCSocketAPI(object):

	def __init__(self):
		self.tcp_ip = "192.168.12.21" # Connecting to IP address of MDPGrp12
		self.port = 5182
		self.conn = None
		self.client = None
		self.addr = None
		self.pc_is_connect = False

	def close_pc_socket(self):
		"""
		Close socket connections
		"""
		if self.conn:
			self.conn.close()
			print("Closing server socket")
		if self.client:
			self.client.close()
			print ("Closing client socket")
		self.pc_is_connect = False

	def pc_is_connected(self):
		"""
		Check status of connection to PC
		"""
		return self.pc_is_connect

	def init_pc_conn(self):
		"""
		Initiate PC connection over TCP
		"""
		# Create a TCP/IP socket
		try:
			self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.conn.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			self.conn.bind((self.tcp_ip, self.port))
			self.conn.listen(1)		#Listen for incoming connections
			print ("Listening for incoming connections from PC...")
			self.client, self.addr = self.conn.accept()
			print ("Connected! Connection address: ", self.addr)
			self.pc_is_connect = True
			return 1
		except Exception as e: 	#socket.error:
			print ("=================Error: %s" % str(e))
			print ("~~~~~~~~~~~~~~~~~Trying again in a few seconds")
			self.pc_is_connect = False
			return 0

	def write_to_PC(self, message):
		"""
		Write message to PC
		"""
		try:
			self.client.sendto(message, self.addr)
			print (">>>>>>>>>>>>>>>>Sent [%s] to PC" % message)
		except Exception as e:
			print (">===============Error: %s" %str(e))
			self.close_pc_socket()
			time.sleep(0.5)
			#Reestablish connection with pc client
			self.init_pc_conn()


	def read_from_PC(self):
		"""
		Read incoming message from PC
		"""
		try:
			pc_data = self.client.recv(46080)
			print ("<<<<<<<<<<<<<<<<<Read [%s] from PC" %pc_data)
			if (pc_data == 'quit'):
				self.close_pc_socket()
			return pc_data
		except Exception as e:
			print (">================Error: %s " % str(e))
			self.close_pc_socket()
			time.sleep(0.5)
			#Reestablish connection with pc client
			self.init_pc_conn()

#if __name__ == "__main__":
# 	print ("main")
 #	pc = PCSocketAPI()
 #	pc.init_pc_conn()

#	while True:
#		send_msg = raw_input()
#		if(send_msg =="quit"):
#			break
#		print "write_to_PC(): %s " % send_msg
 #		pc.write_to_PC(send_msg)

#		msg = pc.read_from_PC()
#		if (msg==-1):
#			break
 #		print("data received: %s " % msg)

# 	print("closing sockets")
 #	pc.close_pc_socket()
