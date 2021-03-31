from main import *
from external import *

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
		
		mq.send(str(self.prix_energie).encode(), type = pid)
		
	def achat_maison(self, m, mq):
		m_tmp = str(m.decode())
		message = m_tmp.split("/")
		pid = int(message[1])
		
		mq.send(str(self.prix_energie*int(message[0])).encode(), type = pid)
		
	
	def handler(self, sig, frame):
		print("coucou je suis la fonction")
		if (sig == signal.SIGUSR1):
			print("Le signal fonctionne")
		elif (sig == signal.SIGUSR2):
			print("Le signal fonctionne")
			

	def run(self):
		print("C'est le matin, le marché ouvre")
		
		signal.signal(signal.SIGUSR1, Marche.handler)

		
		
		mq = sysv_ipc.MessageQueue(key, sysv_ipc.IPC_CREX)
		
		with concurrent.futures.ThreadPoolExecutor(max_workers = 4) as executor:
			while True:
				m, t = mq.receive(type = -10)
				if t == 1:
					#print("Je suis bien dans la condition t = 1 ")
					print("Le message d'achat reçu est:", m) 
					
					executor.submit(Marche.vente_maison,self, m, mq)
					
				if t == 2:
					#print("Je suis bien dans la condition t = 2 ")
					executor.submit(Marche.achat_maison,self, m, mq) 
					
				if t == 3:
					#print("Je suis bien dans la condition t = 3 ")
					mq.remove()
					print("Le marché ferme, fin de la simulation")  
					break 
					
		
					     
		
