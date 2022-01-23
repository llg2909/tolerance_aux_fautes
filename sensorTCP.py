import time
import os
from random import uniform
import threading
import socket
import sys
from clientTCP import TCPClient

#Parametre de temporisation sur acquisation et publication des donnees
TEMPO = 5

#Classe permettant l acquisition de donnee du capteur et l envoi (avec temporisation : variable TEMPO)
class Sensor(TCPClient) : 
    def __init__(self,priority = "primary"):
        TCPClient.__init__(self)

    #Permet l envoi des donnees capteur 
    def send(self):
        while True :
            self.data =''
            if self.isConnected() == 0 and self.isDisconnected() == False:
                try:                
                    data = str(Sensor.sensor_Data_Acquisition())
                    print('envoi de {!r} vers {}'.format(data,self.port))
                    self.sock.sendall(data.encode())                    
                except:
                    pass
            self.start_timer()

    #Permet la temporisation (generation et envoi des donnees toutes les TEMPO secondes)
    def start_timer(self):
        time.sleep(TEMPO)

    #Permet l acquisition des donnees
    @staticmethod
    def sensor_Data_Acquisition():
        data = uniform(-1000,1000)
        return data
