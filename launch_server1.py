from clientTCP import TCPClient
from serverComputing import ServerComputing

print('\n')
print('Reinitilisation du port 2500')
TCPClient.freeAddressServer(2500)
print("\n")
server1 = ServerComputing('server1')
server1.startServer('localhost',2500,server1.receiveData)