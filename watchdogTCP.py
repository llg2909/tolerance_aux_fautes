import time
import os
from clientTCP import TCPClient
import threading
import socket
import sys
TEMPO_WD = 5

#Cette classe permet la gestion de la comunication entre le watchdog et les serveurs
class WatchdogTCP(TCPClient) :
    def __init__(self,priority = "primary"):
        TCPClient.__init__(self)
        self.priority = priority

    #Permet l envoi de message au serveur pour verifier si il est toujours en bon etat de marche
    def send(self):
        while True :
            if self.isConnected() == 0 and self.isDisconnected() == False:
                message = 'Toujours OK?'
                try:              
                    print('envoi du message : {!r}, a {}'.format(message,self.port))
                    self.sock.sendall(message.encode())                    
                    self.start_timer()                    
                except:
                    pass
    
    #Permet la temporisation et de lancer le switch de serveur en cas d erreur sur les donnees transmises
    def start_timer(self):
        time.sleep(TEMPO_WD)
        if self.data != 'OK':            
            self.server_Error_Timeout()
        else:
            self.data = ''

    #Permet de changer de serveur en cas d'erreur
    def server_Error_Timeout(self):
        self._opened = -1
        print('\n')
        print('Le serveur primaire a crash')
        self.priority = "backup"
        print('deconnexion du serveur')
        print('\n')
        self.disconnectionOfServer()
        print('Changement de connexion vers le serveur backup')
        print('Lancement du serveur backup')
        print('\n')

    #Getter sur la priorite actuelle
    def getPriority(self):
        return self.priority

    #Setter pour changer la priorite actuelle
    def setPriority(self,priority):
        self.priority = priority