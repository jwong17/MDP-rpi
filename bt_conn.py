from bluetooth import *
import time

class BluetoothAPI(object):
	
	def __init__(self):
		"""
		Connect to Nexus 7
		RFCOMM port: 4
		Nexus 7 MAC Address: 08:60:6E:A5:BD:82
		"""
		self.server_socket = None
		self.client_socket = None
		self.bt_is_connected = False
	
	def close_bt_socket(self):
		"""
		Close socket connections
		"""
		if self.client_socket:
			self.client_socket.close()
			print ("Closing client socket")
		if self.server_socket:
			self.server_socket.close()
			print ("Closing server socket")
		self.bt_is_connected = False

	def bt_is_connect(self):
		"""
		check status of BT Connection
		"""
		return self.bt_is_connected

	def init_bluetooth(self):
		"""
		Connect to nexus 7 device
		"""
		# Creating the server socket and bind to the port 
		btport = 3
		try:
			self.server_socket = BluetoothSocket(RFCOMM)
			self.server_socket.bind(("",btport))
			self.server_socket.listen(1)
			self.port = self.server_socket.getsockname()[1]
			uuid ="00001101-0000-1000-8000-00805F9B34FB"
			
			
			advertise_service(self.server_socket, "SampleServer",
					  service_id = uuid,
					  service_classes = [uuid, SERIAL_PORT_CLASS],
					  profiles = [SERIAL_PORT_PROFILE],
					  )
			print ("Waiting for BT connection on RFCOMM channel %d" % self.port)
			#Accept requests
			self.client_socket, client_address = self.server_socket.accept()
			print ("Accepted connection from ", client_address)
			self.bt_is_connected = True
			return 1
		except Exception as e:
			print ("Connection Error: %s" %str(e))
			self.close_bt_socket()
			init_bluetooth()
			return 0


	def write_to_bt(self,message):
		"""
		Write message to nexus 7
		"""
		try:
			print(">>>>>>>>>>>>>>>>>>Sending to Nexus 7 [%s]<<<<<<<<<<<<<<<<<<<<"  %message)
			self.client_socket.send(str(message))
		except BluetoothError:
			print ("Bluetooth Error. Connection reset by peer")
			self.close_bt_socket()
			time.sleep(0.5)
			self.connect_bluetooth() #Reestablish connection


	def read_from_bt(self):
		"""
		Read incoming message from Nexus
		"""
		try:
			msg=self.client_socket.recv(2048)
			print (">>>>>>>>>>>>>>>>>>>>>>Receive[%s] from Nexus 7 <<<<<<<<<<<<<<<<<<<<<<< " % msg)
			return msg
		except BluetoothError:
			print ("Bluetooth Error. Connection reset by peer. Trying to connect...")
			self.close_bt_socket()
			time.sleep(0.5)
			self.connect_bluetooth() # Reestablish connection

if __name__ == "__main__":
	print ("Running Main")
	bt = BluetoothAPI()
	bt.init_bluetooth()


	send_msg = raw_input()
	while not(send_msg =='quit'): 
		print("Write(): %s " %send_msg)
		bt.write_to_bt(send_msg)
		send_msg = raw_input()

#	print("read")
#	print("data received: %s " %bt.read_from_bt())

	print("closing bluetooth connection")
	bt.close_bt_socket()

