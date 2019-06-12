#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 16 12:57:22 2019

@author: Avtl
"""

import socket
import numpy as np
from threading import Thread
import FFArithmetic as field
import shamir_scheme as ss
import proc
import TcpSocket5 as sock
import time
import queue as que
from car_party import party
import os


port = 62
party_addr = [
              ['192.168.100.4', 62], # cloud0
              ['192.168.100.3', 62], # cloud1
              ['192.168.100.2', 62], # cloud2
              ['192.168.100.1', 62], # car
              ['192.168.100.2', 62], #P1
              ['192.168.100.3', 62] #P2
              ]

ccu_adr = '192.168.100.246'

server_addr = [
               [ccu_adr, 4050], #cloud 1
               [ccu_adr, 4060], #cloud 2
               [ccu_adr, 4061], #cloud 3
               [ccu_adr, 4031], #car
               [ccu_adr, 4040], #P1
               [ccu_adr, 4041] #P2
              ]

class commsThread (Thread):
   stop = False  
   def __init__(self, threadID, name, server_info,q):
      Thread.__init__(self)
      self.q = q
      self.threadID = threadID
      self.name = name
      self.server_info = server_info  # (Tcp_ip, Tcp_port)
      self.Rx_packet = [] # tuple [[client_ip, client_port], [Rx_data[n]]]

   def run(self):      
      #Create TCP socket
      tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
      tcpsock.bind(tuple(self.server_info))
      #Communication loop - Wait->Receive->Put to queue
      while not self.stop:
         Rx_packet = sock.TCPserver(tcpsock)
         
         if not self.q.full():
            self.q.put(Rx_packet)
      print("Exiting " + self.name)

class dealer():
    def __init__(self,F, n, t, numTrip):
        self.n = n
        b = ss.share(F,np.random.choice([-1,1]), t, n)
        self.distribute_shares('b', b)
        triplets = [proc.triplet(F,n,t) for i in range(numTrip)]
        for i in range(n):
            l = []
            for j in range(numTrip):
                l.append(triplets[j][i])
            sock.TCPclient(party_addr[i][0], party_addr[i][1], ['triplets' , l])
        
    def distribute_shares(self, name, s):
        for i in range(self.n):
            sock.TCPclient(party_addr[i][0], party_addr[i][1], [name , int(str(s[i]))])
    

m =  792606555396977
F = field.GF(m)            
n = 3
t = 1
x = 5


ipv4 = os.popen('ip addr show eth0').read().split("inet ")[1].split("/")[0]
pnr = party_addr.index([ipv4, port])
q = que.Queue()
q2 = que.Queue()
q3 = que.Queue()

server_info = party_addr[pnr]#(TCP_IP, TCP_PORT)

t1_comms = commsThread(1, "Communication Thread", server_info,q)

p = party(F,int(x), n,t, pnr, q, q2, q3, party_addr, server_addr)

t1_comms.start()

for i in range(n):
    while True:
        try:
            sock.TCPclient(party_addr[i][0], party_addr[i][1], ['flag', 1])
            break
        except:
            time.sleep(1)
            continue
print('Data owner, autonomous vehicle')
print(' ')
print('Connection established')        
   
deal = dealer(F,n,t,50)
time_start=time.clock()
p.start()
p.join()

#time_elapsed=(time.clock()-time_start) #comment all print commands before timing
#print('time elapsed:', time_elapsed)
