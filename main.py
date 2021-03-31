from multiprocessing import *
import random
import time
import sysv_ipc
import concurrent.futures
import os
from marche import *
from home import *
from weather import *


NBR_JOURNEE = 5

TAILLE_METEO = NBR_JOURNEE

if __name__ == "__main__":
	
	barriere = Barrier (1)
	
	#La température est en mémoire partagée
	temperature = Array("i", TAILLE_METEO)
	
	meteo = Meteo(temperature)
	meteo.start()
	
	market = Marche()
	market.start()
	
	lst_process = []
	
	for i in range(1):
		p_m = Maison(i, barriere, temperature, random.randint(1,3))
		p_m.start()
		lst_process.append(p_m)
	
	
		
	for p_m in lst_process :
		p_m.join()
	
	market.join()
	
	meteo.join()
