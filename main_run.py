import time
import threading
import logging
import Queue
import os

from bt_conn import *
from sr_conn import *
from pc_conn import *
 

logging.basicConfig(level=logging.DEBUG,format='(%(threadName)-10s) %(message)s',)
class RPIMain(threading.Thread):

        
        def __init__(self):
                threading.Thread.__init__(self)
                
		#call the damn bluetooth
		os.system("sudo hciconfig hci0 piscan")
		
                #Initialize Objects
		self.bt = BluetoothAPI()
		self.pc = PCSocketAPI()
		self.sr = ArduinoAPI()
		
		#Initialize all the queues
		self.toNexus_q = Queue.Queue(maxsize=0)
		self.toAlgo_q = Queue.Queue(maxsize=0)
		self.toRobot_q = Queue.Queue(maxsize=0)
		self.toPC_q = Queue.Queue(maxsize=0)

		#Initialize all the damn connections
		self.bt.init_bluetooth()
		self.sr.init_serial()
		self.pc.init_pc_conn()
		time.sleep(1) #wait for one sec before start all threads
                
        def read_sr(self, nexus_q, pc_q):
                logging.debug('Starting')
                while True:
			msg = self.sr.read_from_serial()
			if msg is not None:
				#algo_q.put_nowait(msg)
				nexus_q.put_nowait(msg)
				pc_q.put_nowait(msg)

                logging.debug('Exiting')


        def write_sr(self, robot_q):
                logging.debug('Starting')
		while True:
			#check if queue is not empty
			#If contains something then write to robot
			if not robot_q.empty():
				
				msg_to_sr = robot_q.get_nowait()
               			self.sr.write_to_serial(msg_to_sr)
                logging.debug('Exiting')
          

        def read_bt(self,robot_q,pc_q):
                logging.debug('Starting')
                while True:
			msg_from_bt = self.bt.read_from_bt()
			print("Reading msg from Nexus 7: [%s]")
			if msg_from_bt is not None:
				#Wait for communication protocol to be set then edit this *****
				robot_q.put_nowait(msg_from_bt)
				#algo_q.put_nowait(msg_from_bt)
				pc_q.put_nowait(msg_from_bt)
                logging.debug('Exiting')
             

        def write_bt(self, nexus_q):
                logging.debug('Starting')
		while True:
			if not nexus_q.empty():
				msg_to_bt = nexus_q.get_nowait()
               			self.bt.write_to_bt(msg_to_bt)
                logging.debug('Exiting')
              

        def read_pc(self, robot_q,nexus_q):
                logging.debug('Starting')
                while True:
			msg_from_pc = self.pc.read_from_PC()
			if msg_from_pc is not None:
				if (msg_from_pc[:3].lower() == 'mdp'):
					nexus_q.put_nowait(msg_from_pc)
				else:
					robot_q.put_nowait(msg_from_pc)

                logging.debug('Exiting')
             

        def write_pc(self, pc_q):
                logging.debug('Starting')
		while True:
			if not pc_q.empty():
				msg_to_pc = pc_q.get_nowait()
               			self.pc.write_to_PC(msg_to_pc)
                logging.debug('Exiting')

	     

        def create_thread(self):

                print("=========Initizaling threads========")
                
                rbt = threading.Thread(name='Read from BT', target =self.read_bt,args=(self.toRobot_q, self.toPC_q,) )
                wbt = threading.Thread(name='Write to BT', target =self.write_bt, args=(self.toNexus_q,))
                rsr = threading.Thread(name='Read from Serial', target =self.read_sr, args=( self.toNexus_q, self.toPC_q,))
                wsr = threading.Thread(name='Write to Serial', target =self.write_sr, args=(self.toRobot_q,))
                rpc = threading.Thread(name='Read from PC Socket', target =self.read_pc, args=(self.toRobot_q,self.toNexus_q,))
                wpc = threading.Thread(name='Write to PC Socket', target =self.write_pc, args=(self.toPC_q,))

                print("...........Created threads...........")
		rbt.daemon = True                
		wbt.daemon = True
		rsr.daemon = True
		wsr.daemon = True
		rpc.daemon = True
		wpc.daemon = True

                rbt.start()
                wbt.start()
                rsr.start()
                wsr.start()
                rpc.start()
                wpc.start()

                
        
if __name__ == '__main__':
        rpiserver = RPIMain()
        rpiserver.create_thread()
        
