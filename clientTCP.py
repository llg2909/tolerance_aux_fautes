import os
import socket
import threading
import sys
import time

#Classe jouant le role de client pour le capteur dans l architecture client server, connexion TCP socket
class TCPClient :
    def __init__(self):        
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.opened = -1 
        self.port = 0
        self.data = ''

    #Permet de se connecter au serveur    
    def connectionToServer(self,IP,port):        
        print('connexion a {} au port {}'.format(IP,port))
        while(True):
            server_address = (IP, port)
            self.port = port
            self.opened = self.sock.connect_ex(server_address)
            if (self.opened == 0):
                print('connexion a {}  au port {} etablie'.format(IP,port))
                break
               
    #Permet de se deconnecter du serveur  
    def disconnectionOfServer(self):
        self.opened = -1
        self.sock.close()
        TCPClient.freeAddressServer(self.port)
       
    #Getter sur l etat de connexion
    def isDisconnected(self):
        return self.sock._closed

    #Getter sur l etat de connexion
    def isConnected(self):
        return self.opened

    #Permet la reception des donnees
    def receive(self):
        while True:
            if self.isConnected() == 0 and self.isDisconnected() == False:
                self.data = self.sock.recv(16).decode("utf-8")
                if(self.data != ''):   
                    print('donnees recues :  {!r} de {}'.format(self.data,self.port))    

    #Permet l envoi des donnees
    def send(self,msg):
        if self.isConnected() == 0 and self.isDisconnected() == False:
            data = msg  
            try: 
                self.sock.sendall(data.encode())
            except:
                pass
    
    #Permet de libere le port utilise par le serveur
    @staticmethod
    def freeAddressServer(port):
        os.system('fuser -k '+ str(port)+'/tcp')
                
