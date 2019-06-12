#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 16 13:33:06 2019

@author: avtl
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
import os



class party(Thread):
    def __init__(self, F, x, n, t, i, q, q2,q3, party_addr, server_addr):
        Thread.__init__(self)
        self.c = 0
        self.comr = 0
        self.recv = {}
        self.F = F
        self.x = x
        self.n = n
        self.t = t
        self.i = i
        self.q = q
        self.q2 = q2
        self.q3 = q3
        self.party_addr = party_addr
        self.server_addr = server_addr
        
    
    def distribute_shares(self, sec):
        shares = ss.share(self.F, sec, self.t, self.n)
        for i in range(self.n):
            #print('input dist ID', i)
            sock.TCPclient(self.party_addr[i][0], self.party_addr[i][1], ['input' + str(self.i) , int(str(shares[i]))])
    
    def distribute_shares_car(self, sec):
        shares = ss.share(self.F, sec, self.t, self.n)
        for i in range(self.n):
           
            sock.TCPclient(self.party_addr[3][0], self.party_addr[3][1], ['car' + str(self.i), int(str(shares[i]))])    
    def broadcast(self, name, s):
        for i in range(self.n):
            sock.TCPclient(self.party_addr[i][0], self.party_addr[i][1], [name + str(self.i) , int(str(s))])
                    
    def readQueue(self):
        while not self.q.empty():
            b = self.q.get()[1]
            self.recv[b[0]] = b[1]
            self.q3.put([b[0][-1], b[1]])
    
    def get_shares(self, name):
        
        res = []
        
        for i in range(self.n):
         #   print('def ping 2', i)
            while name + str(i) not in self.recv:
                self.readQueue()    
            res.append(self.F(self.recv[name+str(i)]))
            del self.recv[name + str(i)]
        return res
        
            
    def reconstruct_secret(self, name):
        
        return ss.rec(self.F, self.get_shares(name))
    
    def get_share(self, name):
       # print('ping share 1')
        while name not in self.recv:
            self.readQueue()
        a = self.F(self.recv[name])
        del self.recv[name]
        return a
        
    def get_triplets(self):
        while 'triplets' not in self.recv:
            self.readQueue()
        b = self.recv['triplets']
        res = []
        for i in b:
            res.append([self.F(j) for j in i])
        self.triplets = res
    
    def mult_shares(self, a, b):
        r = self.triplets[self.c]
        self.c += 1
        
        d_local = a - r[0]
        #print('BT operation 1')
        self.broadcast('d' + str(self.comr), d_local)
        #print('BT operation 2')
        d_pub = self.reconstruct_secret('d' + str(self.comr))
        #print('BT operation 3')
        self.comr +=1
        
        e_local = b - r[1]
        #print('BT operation 4')
        self.broadcast('e' + str(self.comr), e_local)
        #print('BT operation 5')
        e_pub = self.reconstruct_secret('e' + str(self.comr))
        #print('BT operation 6')
        self.comr+=1
        #print('BT operation 7')
        return d_pub * e_pub + d_pub*r[1] + e_pub*r[0] + r[2]
    

    
    def run(self):
        #print('starting party ', self.i)
        self.get_triplets()

        
        m = 2   # number of A rows
        nn = 2  # number of A coloums
        l = 1   # number of b rows
        mu=min(nn,m)
        
        #
        L=np.array(([1,0],[11,1]))
        U=np.array(([1,8],[0,1]))
        

        input_sharesa00=self.get_share('A00'+str(self.i)).n 
        input_sharesa01=self.get_share('A01'+str(self.i)).n
        input_sharesa10=self.get_share('A10'+str(self.i)).n
        input_sharesa11=self.get_share('A11'+str(self.i)).n
        input_sharesb0=self.get_share('b0'+str(self.i)).n
        input_sharesb1=self.get_share('b1'+str(self.i)).n
        h_share=self.get_share('hh'+str(self.i)).n
        t_share=self.get_share('tt'+str(self.i)).n
        ra_share=self.get_share('ran'+str(self.i)).n   
        input_sharesI00=self.get_share('I00'+str(self.i)).n  
        input_sharesI01=self.get_share('I01'+str(self.i)).n
        input_sharesI10=self.get_share('I10'+str(self.i)).n
        input_sharesI11=self.get_share('I11'+str(self.i)).n

        print('Shares from data owner have been recieved')
        print(' ')
        print('Computing secure Gaussian elimination')
        print('...')
        print('...')

        
        # Gaussian Elimination without pivoting
        
        AA=np.array([[input_sharesa00, input_sharesa01],[input_sharesa10, input_sharesa11]]) 
        bb= np.array([[input_sharesb0],[input_sharesb1]])
        I_n=np.array([[input_sharesI00, input_sharesI01],[input_sharesI10, input_sharesI11]])
        
        e11= np.array(U@AA@L)
        e12=np.array(U@bb)         
        e21= np.array(I_n)
        e22= np.array(np.zeros((nn,l)))
        

        
        C_shares=np.array(([e11[0,0], e11[0,1], e12[0,0]],[e11[1,0], e11[1,1], e12[1,0]], [e21[0,0], e21[0,1], 0],[ e21[1,0], e21[1,1], 0]))
       
        f = []
        r_temp = []
        r = []
        
        for k in range(mu):
              
            broad_ckk= self.mult_shares(ra_share,C_shares[k,k]).n
            self.broadcast('c_kk' + str(self.comr), broad_ckk)
            
            r_temp.append(self.reconstruct_secret('c_kk'+str(self.comr)))
            self.comr=+1
            
           
            if r_temp[k] == 0:
                r.append(0)
            elif r_temp[k] != 0:
                r.append(1)
            else: 
                print('error message')

  
            
            C_shares[mu+k,k] = h_share
    
            f.append(h_share)
            print(' ')

            t_share = self.mult_shares(t_share,h_share).n    
          


            c_kk = (C_shares[k,k]+1-r[k])   
                                                 
            
            h_share = self.mult_shares(h_share,c_kk).n 
    
              
            for i in range(0, mu+k):
                for j in range(k+1, nn+l):
                    if i!= k and (i<= mu or j <= nn-1):
                       
                        dummy=np.matrix( np.vstack((C_shares[i,j],-(C_shares[i,k]))))
                        temp= np.matrix(np.hstack(((C_shares[k,k]+1-r[k]), C_shares[k,j])))
                        temp_C1=self.mult_shares(temp[0,0],dummy[0,0]).n
                        temp_C2=self.mult_shares(temp[0,1],dummy[1,0]).n
                        C_shares[i,j]=temp_C1 +temp_C2 


       
        g = []               
        ss = []


        X = np.asarray(C_shares[(0,1), -1]) 
        
     
        inv_temp=self.mult_shares(t_share,h_share).n
    
        test_in=self.mult_shares(ra_share,inv_temp).n
        
        self.broadcast('yinv' + str(self.comr), test_in)
        ww= self.reconstruct_secret('yinv'+str(self.comr)).n

        w_inv=1/ww
        
        s_w_inv= w_inv*10E10 +0.5
        s_w_inv=int(s_w_inv)

        if self.i ==0:
            self.distribute_shares(s_w_inv)

        
        sw_inv_share=self.get_share('input0')  
        self.broadcast('test_1' + str(self.comr), sw_inv_share)
        test_11= self.reconstruct_secret('test_1'+str(self.comr))
        

        g=self.mult_shares(sw_inv_share, ra_share).n
        f_diag=np.diag(f)
        
        gt_temp=self.mult_shares(g,t_share).n # ook
        
        gtL=gt_temp * L #ook
        
        
        fx=np.zeros(2) 
       
        for k in range(mu):
            fx[k] = self.mult_shares(f[k], X[k]).n

  
        fx=fx.astype(np.int64)

        [ra,ca]=gtL.shape    
        [rb]=fx.shape
        cb=1
        
        for ii in range(0,ra):
            for jj in range(0,cb):
                for kk in range(0,ca):
                    X[ii]=X[ii]+self.mult_shares(gtL[ii,kk],fx[kk]).n
             
         

        X=np.reshape(X, (2, 1))
        print('Resulting shares are:')
        print(X)
        print(' ')
        
        for i in range(self.n):
           
            sock.TCPclient(self.party_addr[3][0], self.party_addr[3][1], ['x1' + str(self.i) , int(str(X[0,0]))])
            sock.TCPclient(self.party_addr[3][0], self.party_addr[3][1], ['x2' + str(self.i) , int(str(X[1,0]))])
        
        print('Shares of result have been send to data owner') 
        
