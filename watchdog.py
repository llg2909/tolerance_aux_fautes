from watchdogTCP import WatchdogTCP
from clientTCP import TCPClient
import os
import threading
import time

#Cette classe permet la gestion du watchdog, c est a dire le changement de serveur en cas de crash et 
#l envoi d une notification d erreur au sensor pour lui indiquer que le serveur a change
class WatchDog:
    def __init__(self):        
        self.client1 = WatchdogTCP("primary")
        self.client2 = WatchdogTCP("backup")
        self.client3 = TCPClient()
        self.primary_server = 'server1'
        self.backup_server = 'server2'
        self.thread_client1 = threading.Thread(target=self.client1.connectionToServer,args=['localhost',2500])
        self.thread_send1 = threading.Thread(target=self.client1.send)
        self.thread_receive1 = threading.Thread(target=self.client1.receive) 
        self.thread_client3 = threading.Thread(target=self.client3.connectionToServer,args=['localhost',2700])  
        self.thread_updateServer = threading.Thread(target=self.updateServer) 

    #Permet d inverser la priorite dans les attributs de classe Watchdog
    def invertPriority(self):
        self.primary_server, self.backup_server = self.backup_server, self.primary_server
    
    #Permet de swap entre les 2 serveur lors d un crash
    def updateServer(self):
        while True:
            if self.primary_server == "server1" and self.client1.getPriority() == "backup":               
                threads = self.reinitialisation_client2_threads()
                self.invertPriority()
                self.send_Sensor_ErrorServer(self.primary_server)
                self.client2.setPriority("primary")
                threads[0].start()
                threads[1].start()
                threads[2].start()
            elif self.primary_server == "server2" and self.client2.getPriority() == "backup":                
                threads = self.reinitialisation_client1_threads()
                self.invertPriority()
                self.send_Sensor_ErrorServer(self.primary_server)
                self.client1.setPriority("primary")
                threads[0].start() 
                threads[1].start()
                threads[2].start() 

    #Permet de relancer les threads lors de crash du serveur 2
    def reinitialisation_client1_threads(self):
        self.client1 = WatchdogTCP("primary")
        thread_client1 = threading.Thread(target=self.client1.connectionToServer,args=['localhost',2500])
        thread_send1 = threading.Thread(target=self.client1.send)
        thread_receive1 = threading.Thread(target=self.client1.receive) 
        return thread_client1, thread_send1, thread_receive1
    
    #Permet de relancer les threads lors de crash du serveur 1
    def reinitialisation_client2_threads(self):
        self.client2 = WatchdogTCP("primary")
        thread_client2 = threading.Thread(target=self.client2.connectionToServer,args=['localhost',3000])
        thread_send2 = threading.Thread(target=self.client2.send)
        thread_receive2 = threading.Thread(target=self.client2.receive) 
        return thread_client2, thread_send2, thread_receive2

    #Permet d indiquer au sensor qu il y a eu un crash et donc changement de serveur
    def send_Sensor_ErrorServer(self, newPrimaryServer): 
        self.client3.send(newPrimaryServer)

    #Permet de lancer les threads
    def start_all_threads(self):
        self.thread_client1.start()
        self.thread_send1.start()
        self.thread_receive1.start()
        self.thread_client3.start()
        self.thread_updateServer.start()
