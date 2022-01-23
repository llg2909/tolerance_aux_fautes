from sensorTCP import Sensor
from serverTCP import TCPServer
import threading
import time
from clientTCP import TCPClient

#Classe simulant un capteur, ici capteur virtuel
#Recupere les donnees grace a la classe Sensor
#Envoi les donnees grace aux classe TCPClient et TCP server
class VirtualSensor:
    def __init__(self):
        self.client1 = Sensor()
        self.client2 = Sensor()
        self.primary_server = 'server1'
        self.backup_server = 'server2' 
        self.thread_client1 = threading.Thread(target=self.client1.connectionToServer,args=['localhost',2500])
        self.thread_send1 = threading.Thread(target=self.client1.send)
        self.thread_receive1 = threading.Thread(target=self.client1.receive)
        self.thread_updateServer = threading.Thread(target=self.updateServer)        
        
    #Permet de swap entre les 2 serveur lors d un crash
    def updateServer(self):        
        TCPClient.freeAddressServer(2700)
        server = TCPServer()
        conn = server.startServer1('localhost',2700)
        print(conn)
        currentServer = self.primary_server           
        while(True):
            print(currentServer)
            currentServer = server.receive(conn)
            if self.primary_server == 'server1' and currentServer == 'server2':
                print('Le serveur 1 a crash')
                print("\n")
                print('Deconnexion du serveur 1')
                self.client1.disconnectionOfServer()
                self.invertPriority()
                threads = self.reinitialisation_client2_threads()
                print('Connexion avec le serveur de backup (serveur 2)')
                threads[0].start()
                threads[1].start()
                threads[2].start()
            elif self.primary_server == 'server2' and currentServer == 'server1':
                print('Le serveur 2 a crash')
                print("\n")
                print('Deconnexion du serveur 2')
                self.client2.disconnectionOfServer
                self.invertPriority()
                threads = self.reinitialisation_client1_threads()
                print('Connexion avec le serveur de backup (serveur 1)')
                threads[0].start()
                threads[1].start()
                threads[2].start()                
    
    #Permet d inverser la priorite dans les attributs de classe sensor
    def invertPriority(self):
        self.primary_server, self.backup_server = self.backup_server, self.primary_server
    
    #Permet de relaner les threads lors de crash du serveur 2
    def reinitialisation_client1_threads(self):
        self.client1 = Sensor()
        thread_client1 = threading.Thread(target=self.client1.connectionToServer,args=['localhost',2500])
        thread_send1 = threading.Thread(target=self.client1.send)
        thread_receive1 = threading.Thread(target=self.client1.receive) 
        return thread_client1, thread_send1, thread_receive1
    
    #Permet de relaner les threads lors de crash du serveur 1
    def reinitialisation_client2_threads(self):
        self.client2 = Sensor()
        thread_client2 = threading.Thread(target=self.client2.connectionToServer,args=['localhost',3000])
        thread_send2 = threading.Thread(target=self.client2.send)
        thread_receive2 = threading.Thread(target=self.client2.receive) 
        return thread_client2, thread_send2, thread_receive2 

    #Lancer tout les threads (fonction appelee dans fichier python launch_sensor.py)
    def start_all_threads(self):
        self.thread_client1.start()
        self.thread_send1.start()
        self.thread_receive1.start()
        self.thread_updateServer.start()


