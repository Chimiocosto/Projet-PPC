from main import *

NBR_JOURNEE = 5

class Meteo(Process):
	def __init__(self, temperature):
		super().__init__()
		self.temperature = temperature
		
		
	def run(self):
		current_day = 0
		
		while (current_day < NBR_JOURNEE):
			
			with self.temperature.get_lock():
				self.temperature[current_day] = random.randint(-10, 30)
			
			
			current_day += 1
		
		
