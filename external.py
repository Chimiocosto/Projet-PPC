from main import *
import signal

class External (Process):
		def __init__(self):
			super().__init__()
			
		def envoi_signal(self):
			
			rand = random.randint(1,2)
			
			if (rand == 1):
				signal.signal(signal.SIGUSR1,handler)
			elif(rand == 2):
				signal.signal(signal.SIGUSR2,handler)
				
		
