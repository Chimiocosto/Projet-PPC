import random
import time
import sysv_ipc
import signal
import concurrent.futures
import os
from multiprocessing import *

key = 10
INFINI = 9999999


class Marche (Process):
	def __init__(self):
		super().__init__()
		self.prix_energie = 10
		self.energie_stock = INFINI
		
	def vente_maison(self, m, mq):
		m_tmp = str(m.decode())
		message = m_tmp.split("/")
		pid = int(message[1])
		
		mq.send(str(self.prix_energie*int(message[0])).encode(), type = pid)
		
	def achat_maison(self, m, mq):
		m_tmp = str(m.decode())
		message = m_tmp.split("/")
		pid = int(message[1])
		
		mq.send(str(self.prix_energie*int(message[0])).encode(), type = pid)
		
	
	def handler(self, sig, frame):
		if (sig == signal.SIGUSR1):
			print("Une météorite frappe la terre, le prix de l'énergie augmente de 20 € ")
			self.prix_energie += 20 
		elif (sig == signal.SIGUSR2):
			print("Une grave crise économique surgit, les prix grimpent en flêche \(+30€\)")
			self.prix_energie += 30
	
	def external(self):
		while True:
			aleatoire = random.randint(1,2)
			
			if (aleatoire == 1):
				os.kill(os.getpid(), signal.SIGUSR1)
			elif(aleatoire == 2):
				os.kill(os.getpid(), signal.SIGUSR2)
			
			time.sleep(5)
					
	def run(self):
		print("C'est le matin, le marché ouvre")
		
		signal.signal(signal.SIGUSR1, Marche.handler)
		signal.signal(signal.SIGUSR2, Marche.handler)
		
		event = Process(target = self.external, args=())
		
		event.start()

		
		mq = sysv_ipc.MessageQueue(key, sysv_ipc.IPC_CREX)
		
		with concurrent.futures.ThreadPoolExecutor(max_workers = 4) as executor:
			while True:
				m, t = mq.receive(type = -10)
				if t == 1:
					#print("Je suis bien dans la condition t = 1 ")
					executor.submit(Marche.vente_maison,self, m, mq)
					
				if t == 2:
					#print("Je suis bien dans la condition t = 2 ")
					executor.submit(Marche.achat_maison,self, m, mq) 
					
				if t == 3:
					#print("Je suis bien dans la condition t = 3 ")
					mq.remove()
					
					print("Le marché ferme, fin de la simulation")  
					break
				
		event.terminate()	
		event.join()	
			     
		
