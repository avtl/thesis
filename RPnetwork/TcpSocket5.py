import socket
from threading import Thread
import pickle
import json
import struct  # Interpret bytes as packed binary data


""" TCP socket """


def TCPserver(tcpsock):
    """ Sends and receive the data.

    """
    class ClientThread(Thread):

        def __init__(self, ip, port):
            Thread.__init__(self)
            self.ip = ip
            self.port = port
            self.Rx_data = []
            #print("[+] New thread started for " + ip + ":" + str(port))

        def run(self):
            Rx_data_bytes = conn.recv(2048)
            if Rx_data_bytes:
                self.Rx_data = pickle.loads(Rx_data_bytes)#struct.unpack('>L',Rx_data_bytes)
                message_ack = ("Data succesfully received at server...")
                conn.send(message_ack.encode('utf-8'))  # echo 

    threads = []
    #Communication loop
    tcpsock.listen(4)
    #print("Waiting for incoming connections...")
    (conn, (ip, port)) = tcpsock.accept()
    newCommthread = ClientThread(ip, port)
    newCommthread.start()
    threads.append(newCommthread)
        
    #It exits the communication when returs the data packet....
    for t in threads:
        t.join()
    client_info = [newCommthread.ip, newCommthread.port]
    return client_info, newCommthread.Rx_data


def TCPclient(TCP_IP, TCP_PORT, data):

    BUFFER_SIZE = 1024
    #Connect the socket to the server address
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    #Data transfer
    Tx_data_bytes = pickle.dumps(data)
    s.send(Tx_data_bytes)
    Rx_data_bytes = s.recv(BUFFER_SIZE)
    Rx_data = Rx_data_bytes.decode('utf-8')
    s.close()
    return Rx_data

""" UDP socket """

def UDPserver(udpsock):

    Rx_data_bytes, addr = udpsock.recvfrom(1024)
    numOfValues = int(len(Rx_data_bytes) / 8)
    Rx_data = struct.unpack('>{}d'.format(numOfValues), Rx_data_bytes)
    #Rx_data = struct.unpack('>dddd', Rx_data_bytes)
#    print('Received from:' + str(addr) + " Message:" + str(Rx_data))
    return Rx_data

def UDPclient(UDP_IP, UDP_PORT, data):
    #Tx_data = struct.pack('>4d', data[0], data[1], data[2], data[3])
    #numOfValues = data.__len__()
    #Tx_data = struct.pack('>{}d'.format(numOfValues),     *data)
    
    Tx_data = struct.pack('>d', data)

    s = socket.socket(socket.AF_INET,  # Internet
                         socket.SOCK_DGRAM)  # UDP
    s.sendto(Tx_data, (UDP_IP, UDP_PORT))

    


#def UDPserver(udpsock):
#
#    Rx_data_bytes, addr = udpsock.recvfrom(1024)
#    numOfValues = int(len(Rx_data_bytes) / 8)
#    Rx_data = struct.unpack('>{}d'.format(numOfValues), Rx_data_bytes)
#    #Rx_data = struct.unpack('>dddd', Rx_data_bytes)
#    print('Received from:' + str(addr) + " Message:" + str(Rx_data))
#    return Rx_data
#
#def UDPclient(UDP_IP, UDP_PORT, data):
#    #Tx_data = struct.pack('>4d', data[0], data[1], data[2], data[3])
#    numOfValues = data.__len__()
#    #Tx_data = struct.pack('>{}d'.format(numOfValues),
#    #                      data[0], data[1], data[2], data[3], data[4], data[5])
#    Tx_data = struct.pack('>{}d'.format(numOfValues),
#                          *data)
#
#    s = socket.socket(socket.AF_INET,  # Internet
#                         socket.SOCK_DGRAM)  # UDP
#    s.sendto(Tx_data, (UDP_IP, UDP_PORT))

    