import serial
import time

class ArduinoAPI(object):
	def __init__(self):
		self.port ='/dev/ttyACM0'
		self.baud_rate = 9600
		self.ser = None
	
	def init_serial(self):
		"""
		initialize serial socket connection
		"""
		try:
			self.ser = serial.Serial(self.port,self.baud_rate)
			if(self.ser!= None):
				print ("Serial Connection to Arduino Successful")
				
		except Exception as e:
			print ("error (Serial): %s " % str(e))
			#print ("Error: Serial connection fail. Try reconnecting the serial cable or restart the pi")
			self.init_serial()
			
			
	def close_sr_socket(self):
		if(self.ser):
			self.ser.close()
			print ("Closing serial connection")	

	def write_to_serial(self,msg):
		"""
		Write to arduino
		"""
		print msg
		try:
			self.ser.write(msg)
			print ("*****************Write to arduino: [%s] **********************" %msg)
		except AttributeError:
			print ("Error in serial communication. No value to be written, check connection!!")
	
	def read_from_serial(self):
		"""
		read from arduino
		Wait until data is received from arduino
		"""	
		try:
			received_data = self.ser.readline()
			print ("*****************Received from arduino: [%s] ************************" %received_data)
			return received_data
		except AttributeError:
			print ("Error in serial connection. No value received, check connection!")


#if __name__ =="__main__":
#	print("running main")
#	sr = ArduinoAPI()
#	sr.init_serial()
#	print("Serial connection established")
#	while True:
#		#send_msg = raw_input()
#		#print("Writing [%s] to arduino " %send_msg)
		#sr.write_to_serial(send_msg)
	
#		print("read")
#		print("data received from serial %s" %sr.read_from_serial)

#	print("closing sockets")
#	sr.close_sr_socket()
