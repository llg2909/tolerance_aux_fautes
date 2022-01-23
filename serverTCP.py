import threading
import socket
import sys
import os
import time

#Cette classe permet de receptionner les donnees des capteur envoye par le client
#Architecture client serveur, communication socket TCP
class TCPServer :
    #taille de la fenetre coulissante sur laquelle est effectuee le calcul (utilise dans le fichier serverMachine.py)
    SLIDING_WINDOW_LENGHT = 5

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = []
        self.data = ''
    
    #Permet de lancer le serveur sur le port et l ip voulus
    def startServer(self, IP, port, receiveFunc):        
        self.server_address = (IP, port)
        print('lancement sur {} port {}'.format(*self.server_address))
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(self.server_address)        
        self.sock.listen(3)        
        print('en attente de la connexion')
        while True:            
            thread_Server = threading.Thread(target=receiveFunc,args=self.sock.accept())
            thread_Server.start()
            if port == 2700:                
                break
    #Comme precedemment mais utilise lors d une update de serveur dans la classe VirtualSensor
    def startServer1(self, IP, port):        
        os.system('fuser -k '+ str(port)+'/tcp')
        server_address = (IP, port)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(server_address)        
        self.sock.listen(2)
        conn, addr = self.sock.accept()
        return conn
       
    #Permet la reception des donnees
    def receive(self,conn):
        #while(True):         
        currentServer = (conn.recv(32)).decode("utf-8") 
        self.data = currentServer
        return currentServer

    





