from main import *

key = 10
NBR_JOURNEE = 5
INFINI = 99999


class Maison (Process):
	def __init__(self, id, b, temperature, m_type):
		super().__init__()
		self.id = id
		self.energie_cons = 60
		self.energie_prod = 60
		self.solde = INFINI
		self.b = b
		self.temperature = temperature
		self.m_type = m_type
	
	#Changer la valeur demandé en fonction de self.energie_cons et self.energie_prod
	def achat(self,mq):
		pid = str(os.getpid()).encode()
		message = str(self.energie_cons-self.energie_prod).encode()
		slash = "/".encode()
		m = message + slash + pid
		
		mq.send(m, type = 1)
		
		perte, t = mq.receive(type = os.getpid())
		if (t == os.getpid()):
			print("La maison", self.id,"a perdu", int(perte.decode()))
			
	def vente(self,mq):
		pid = str(os.getpid()).encode()
		message = str(self.energie_prod-self.energie_cons).encode()
		slash = "/".encode()
		m = message + slash + pid
		
		mq.send(m, type = 2)
		
		recette, t = mq.receive(type = os.getpid())
		if (t == os.getpid()):
			print("La maison", self.id,"a gagné", int(recette.decode()))
			
	#Le type 1 : maison à grosse consommation
	def type_1(self, current_day):
		if (current_day == 0):
			with self.temperature.get_lock():
				if (self.temperature[current_day] <= 5):
					self.energie_cons += 20
				elif(self.temperature[current_day] >= 25):
					self.energie_cons -= 20
		else:
			with self.temperature.get_lock():
				#Condition si la journée considérée à une température faible
				if (self.temperature[current_day] <= 5):
					if (self.temperature[current_day-1] >= 6 and self.temperature[current_day-1] <= 24):
						self.energie_cons += 20
					elif(self.temperature[current_day-1] >= 25):
						self.energie_cons += 40
				#Condition si la journée considérée à une température élevée
				elif(self.temperature[current_day] >= 25):
					if (self.temperature[current_day-1] >= 6 and self.temperature[current_day-1] <= 24):
						self.energie_cons -= 10
					elif (self.temperature[current_day-1] <= 5):
						self.energie_cons -= 20
				#Condition si la journée considérée à une température moyenne
				elif(self.temperature[current_day] >= 6 and self.temperature[current_day] <= 24):
					if (self.temperature[current_day-1] <= 5):
						self.energie_cons -= 10
					elif (self.temperature[current_day-1] >= 25):
						self.energie_cons += 20
					
		
	#Le type 2 : maison à la consommation modérée
	def type_2(self, current_day):
		if (current_day == 0):
			with self.temperature.get_lock():
				if (self.temperature[current_day] <= 0):
					self.energie_cons += 15
				elif(self.temperature[current_day] >= 20):
					self.energie_cons -= 15
		else:
			with self.temperature.get_lock():
				#Condition si la journée considérée à une température faible
				if (self.temperature[current_day] <= 0):
					if (self.temperature[current_day-1] >= 1 and self.temperature[current_day-1] <= 19):
						self.energie_cons += 15
					elif(self.temperature[current_day-1] >= 20):
						self.energie_cons += 30
				#Condition si la journée considérée à une température élevée
				elif(self.temperature[current_day] >= 20):
					if (self.temperature[current_day-1] >= 1 and self.temperature[current_day-1] <= 19):
						self.energie_cons -= 15
					elif (self.temperature[current_day-1] <= 0):
						self.energie_cons -= 30
				#Condition si la journée considérée à une température moyenne
				elif(self.temperature[current_day] >= 1 and self.temperature[current_day] <= 19):
					if (self.temperature[current_day-1] <= 0):
						self.energie_cons -= 15
					elif (self.temperature[current_day-1] >= 20):
						self.energie_cons += 15
					
	

	#Le type 3 : maison peu consommatrice
	def type_3(self, current_day):
		if (current_day == 0):
			with self.temperature.get_lock():
				if (self.temperature[current_day] <= -5):
					self.energie_cons += 10
				elif(self.temperature[current_day] >= 15):
					self.energie_cons -= 20
		else:
			with self.temperature.get_lock():
				#Condition si la journée considérée à une température faible
				if (self.temperature[current_day] <= -5):
					if (self.temperature[current_day-1] >= -4 and self.temperature[current_day-1] <= 14):
						self.energie_cons += 10
					elif(self.temperature[current_day-1] >= 15):
						self.energie_cons += 20
				#Condition si la journée considérée à une température élevée
				elif(self.temperature[current_day] >= 15):
					if (self.temperature[current_day-1] >= -4 and self.temperature[current_day-1] <= 14):
						self.energie_cons -= 20
					elif (self.temperature[current_day-1] <= -5):
						self.energie_cons -= 40
				#Condition si la journée considérée à une température moyenne
				elif(self.temperature[current_day] >= -4 and self.temperature[current_day] <= 14):
					if (self.temperature[current_day-1] <= -5):
						self.energie_cons -= 20
					elif (self.temperature[current_day-1] >= 15):
						self.energie_cons += 10
					
					
	def run(self):
		current_day = 0
		print("Mon ID est le", self.id, "et mon type de maison est:", self.m_type)
		print("Le nombre de journée pour cette simulation est",NBR_JOURNEE)
		
		while (current_day < NBR_JOURNEE):
			mq = sysv_ipc.MessageQueue(key)
			
			with self.temperature.get_lock():
				print("Aujourd'hui la temperature est de:", self.temperature[current_day])
				if (current_day > 0):
					print("La température le jour d'avant était de :", self.temperature[current_day-1])
				print(self.temperature[:])
				
			#Mis à jour de la consommation d'énergie quotidienne
			if (self.m_type == 1):
				self.type_1(current_day)
			elif (self.m_type == 2):
				self.type_2(current_day)
			elif (self.m_type == 3):
				self.type_3(current_day)
				
			print("Je consomme:",self.energie_cons,"d'énergie car je suis de type", self.m_type)
		
		
			#Vente du surplus d'énergie
			if (self.energie_cons < self.energie_prod):
				self.vente(mq)
			#Achat de l'énergie nécessaire
			elif (self.energie_cons > self.energie_prod):
				self.achat(mq)
			

			
			time.sleep(random.randint(2, 5))
			
			print("--------------\n\n")
			self.b.wait()
			print("Fin de la journée", current_day,"pour la maison",self.id)
			print("--------------\n\n")
			current_day +=1
		
		if (self.id == 0):
			mq.send(str(25).encode(), type = 3)
		
