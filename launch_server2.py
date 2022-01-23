from serverComputing import ServerComputing
from clientTCP import TCPClient

print('\n')
print('Reinitilisation du port 3000')
TCPClient.freeAddressServer(3000)
print("\n")
server2 = ServerComputing('server2')
server2.startServer('localhost',3000,server2.receiveData)