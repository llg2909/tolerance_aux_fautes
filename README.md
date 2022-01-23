# tolerance_aux_fautes

Pour lancer le projet :

Se placer dans le répertoire du projet, ouvrir 4 terminaux et lancer les 4 commandes suivantes :

python ./launch_server1.py

python ./launch_server2.py

python ./launch_watchdog.py

python ./launch_sensor.py

Par défaut l'injection de fautes est activée. Celle-ci est désactivable dans le fichier serverComputing.py en fixant le booléen en paramètre de la fonction 

def data_processing(self,fault_Injection = True)

à False.

Pour simuler un crash server, il y a la possibilité de stopper le script python dans le terminal.
