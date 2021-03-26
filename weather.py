from home import *
from main import *
import random
from multiprocessing import *

NBR_JOURNEE = 5

class Meteo(Process):
	def __init__(self, temperature, b):
		super().__init__()
		self.temperature = temperature
		self.b = b
		
		
	def run(self):
		current_day = 0
		
		while (current_day < NBR_JOURNEE):
			print("Le nombre de journée pour la météo est de", NBR_JOURNEE)
			
			with self.temperature.get_lock():
				self.temperature[current_day] = random.randint(-10, 30)
			
			self.b.wait()
			
			current_day += 1
		
		
