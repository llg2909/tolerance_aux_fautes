from memory import loadJsonFile, saveData
from serverTCP import TCPServer
import threading
from clientTCP import TCPClient 
import numpy as np
PATH_MEMORY = "./memoire.json"

#Classe permettant cote server le traitement des donnees (calucl de moyenne)
#Redondance avec vote majoritaire
#Le stockage des donnees en memoire (fichier json)
#Communication avec le watchdog
#L injection de fautes
class ServerComputing(TCPServer):
    def __init__(self, server_ID):
        TCPServer.__init__(self)
        self.server_ID = server_ID
        self.priority = ''  
        self.recover_data_memory()        

    #Permet la gestion du calcul de moyenne sur la fenetre glissante + le vote majoritaire
    def data_processing(self,fault_Injection = True):        
        if len(self.data) == TCPServer.SLIDING_WINDOW_LENGHT:                     
            print('\n')
            print('Calcul numero 1')
            mean_1 = self.mean_Computing(self.data,fault_Injection)
            print('\n')            
            if fault_Injection == False:
                print('La moyenne des {} valeurs est {} :'.format(TCPServer.SLIDING_WINDOW_LENGHT,mean_1))
                self.store_data_memory(PATH_MEMORY, self.data, mean_1)
            else:
                print('\n')
                print('Calcul numero 2')
                mean_2 = self.mean_Computing(self.data,fault_Injection)                
                print('\n')
                if mean_1 == mean_2:
                    print('La moyenne des {} valeurs est {} :'.format(TCPServer.SLIDING_WINDOW_LENGHT,mean_1))
                    self.store_data_memory(PATH_MEMORY, self.data, mean_1)
                else: 
                    print('\n')
                    print('Calcul numero 3')
                    mean_3 = self.mean_Computing(self.data,fault_Injection)                    
                    print('\n')
                    #Gestion du vote par majorite
                    print('Vote par majorite en cours')
                    if mean_3 == mean_1:
                        print('La moyenne des {} valeurs est {} :'.format(TCPServer.SLIDING_WINDOW_LENGHT,mean_1))
                        self.store_data_memory(PATH_MEMORY, self.data, mean_1)
                    elif mean_3 == mean_2:
                        print('La moyenne des {} valeurs est {} :'.format(TCPServer.SLIDING_WINDOW_LENGHT,mean_2))
                        self.store_data_memory(PATH_MEMORY, self.data, mean_2)
                    else:
                        print('Impossibilite de vote par majorite, les 3 valeurs sont differentes')
                        print("Echec du service, " + self.server_ID + " besoin de reparation, fermeture de "+ self.server_ID + " en cours")
                        self.sock.close()
                        TCPClient.freeAddressServer(self.server_address[1])    
            
    
    #Permet d enregister les donnees en memoire
    def store_data_memory(self, path, newDataVector, mean):
        saveData(path, newDataVector, mean)

    #Permet d inverser la priorite    
    def set_priority(self, priority):
        self.priority = priority

    #Permet de recuperer a partir des donnees memoire
    def recover_data_memory(self):
        memory = loadJsonFile(PATH_MEMORY)
        if len(memory) > 0: 
            self.data = memory[len(memory)-1][0]
            self.data.pop(0)

    #Permet la reception des donnees du watchdog ou du sensor
    def receiveData(self,connection,client_address):
        try:
            print('Connexion de ', client_address)            
            while True:  
                temp = (connection.recv(32)).decode("utf-8")                 
                try:  
                    data = float(temp)
                except:
                    data = temp
                if(data!= None):
                    if data.__class__ == str:
                        print('\n')
                        print('Donnees du watchdog')
                        print('recue de {} , donnees : {}'.format(client_address,data))
                        print('\n')
                        if data == 'Toujours OK?':
                            response = 'OK'
                            print('envoi {!r}'.format(response))
                            connection.sendall(response.encode())                        
                        print('\n')
                    else:
                        print('\n')
                        print('Donnes du sensor')
                        print('recue de {} , donnees : {}'.format(client_address,data))
                        response = 'donnees recues'
                        print('envoi {!r}'.format(response))
                        connection.sendall(response.encode())
                        self.data.append(data)                        
                        print('\n')
                        if len(self.data) >= TCPServer.SLIDING_WINDOW_LENGHT: 
                            self.data_processing()
                            self.data.pop(0)      
        except:
            pass
    
    #Calcul de la moyenne des valeurs du capteur sur la fenetre glissante
    def mean_Computing(self,data,fault_Injection):
        if fault_Injection == True:
            data_With_Fault = self.fault_Injector(data)
           
            print('valeur pour le calcul {}'.format(data_With_Fault))
            mean = np.mean(data_With_Fault)
            print('moyenne {}'.format(mean))
            return mean
        else:
            print('valeur pour le calcul {}'.format(data))
            mean = np.mean(data)
            print('moyenne {}'.format(mean))
        return mean

    #Permet l injection de faute dans les donnees a traiter, peut etre active ou desactive dans la fonction data_processing
    def fault_Injector(self, receivedData):     
        from random import randint
        new_Data = self.data.copy()
        print('liste avant injection de fautes {}'.format(new_Data))
        new_Data[1] += randint(0,2)
        print('liste apres injection de fautes {}'.format(new_Data))
        return new_Data

    
     
