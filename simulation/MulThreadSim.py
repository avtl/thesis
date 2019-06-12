#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 14:27:16 2019
@author: avtl
Applying scripts authored by Katrine Sofie Tjell
The protocol is developed by Niek J. Bouman & Niels de Vreede
"""


import numpy as np 
from scipy import linalg
from scipy.linalg import toeplitz
from numpy.linalg import inv
import random 
from numpy.linalg import matrix_rank
from threading import Thread
import FFArithmetic as field
import shamir_scheme as ss
import time
import proc


# script simulates multiparty computation 
# consists of 3 cloudparties and 1 data owner (the autonomous vehicle)

# autonomous vehicle produces:
    # Beaver's Triplets (not how it shall be done in real life implementation
    # with multiple vehicles)
    # random variable for equality tests
    # shares of A, b, I_n matrices securely
    # generates random Toeplitz matrices U and L openly


# parties computes Pivo-free Gaussian Elimination 
# according to Niek J. Bouman & Niels de Vreede protocol

# parties distribute shares of the result to the vehicle
# the vehicle reconstructs the result, only the vehicle can know the result
# the result is the solution to the linear system, Ax= b    

# F = IntegerModP
# n= number of parties
# t= shamir degree
    
    
    
#time_start = time.clock()
for abe in range (0,1):
    class server:
        securecom = {}
        broadcasts = {}
        def __init__(self,F, n, t, numTrip): 
            self.b = ss.share(F,np.random.choice([-1,1]), t, n)
            self.triplets = [proc.triplet(F,n,t) for i in range(numTrip)]
         
    class part(Thread):
            
        def __init__(self, F, n, t, i, s):  
            Thread.__init__(self)
            self.c = 0
            self.comr = 0
            self.F = F
            self.n = n
            self.t = t
            self.i = i
            self.server = s
            self.comtime = 0
    
               
        def distribute_shares(self,var, name):
            shares = ss.share(self.F, var, self.t, self.n)  # create shares
            
            s = name                                        # identify share
            self.server.securecom[s] = shares        
            
        def get_share(self, name):
            st = time.time()
            while True:
                try:
                    res =  (self.server.securecom[name][self.i])
                    break
                except:
                    continue
            sl = time.time()
            self.comtime +=(sl-st)
            return res
        
        def add_shares(self,a,b):
            return a+b
        
        def mult_shares(self, a, b):
            r = self.server.triplets[self.c][self.i]
            self.c += 1
            
            d_local = a - r[0]
            self.broadcast('d' + str(self.comr), d_local)
            d_pub = self.reconstruct_secret('d' + str(self.comr))
            self.comr +=1
            e_local = b - r[1]
            self.broadcast('e' + str(self.comr), e_local)
            e_pub = self.reconstruct_secret('e' + str(self.comr))
            self.comr+=1
            return d_pub * e_pub + d_pub*r[1] + e_pub*r[0] + r[2]
        
           
        def reconstruct_secret(self, c):
            res = []
            for i in range(self.n):
                res.append(self.get_broadcast(c + str(i)))
            return ss.rec(self.F, res)
        
        
        def broadcast(self, name, c):
            st = time.time()
            self.server.broadcasts[name + str(self.i)] = c
            sl = time.time()
            self.comtime += sl-st
        
        
        
        def get_broadcast(self, c):
            st = time.time()
            while True:
                try:
                    res = self.server.broadcasts[c]
                    break
                except:
                    continue
            sl = time.time()
            self.comtime += (sl-st)
            return res
        
        def run(self):
        
            # recieve shares for A, b, I_n, h, t, random variable
                 
            input_sharesa00=self.get_share('a00').n        
            input_sharesa01=self.get_share('a01').n
            input_sharesa10=self.get_share('a10').n
            input_sharesa11=self.get_share('a11').n
            input_sharesb0=self.get_share('b0').n
            input_sharesb1=self.get_share('b1').n
            
            input_sharesI00=self.get_share('iden00').n      
            input_sharesI01=self.get_share('iden01').n
            input_sharesI10=self.get_share('iden10').n
            input_sharesI11=self.get_share('iden11').n
            
            h_share=self.get_share('h_shares').n
            t_share=self.get_share('t_shares').n
            ra_share=self.get_share('ran_shares').n   # shares of random variable 
                                                      # for equality test
        
            # arrange arrays corresponding to original input
            AA=np.array([[input_sharesa00, input_sharesa01],[input_sharesa10, input_sharesa11]]) 
            bb= np.array([[input_sharesb0],[input_sharesb1]])
            I_n=np.array([[input_sharesI00, input_sharesI01],[input_sharesI10, input_sharesI11]])
                    
            e11= np.array(U@AA@L) 
            e12=np.array(U@bb)         
            e21= np.array(I_n)
            
    
            C_shares=np.array(([e11[0,0], e11[0,1], e12[0,0]],[e11[1,0], e11[1,1], e12[1,0]], [e21[0,0], e21[0,1], 0],[ e21[1,0], e21[1,1], 0]))
            C_shares=C_shares.astype(int)
     
            f = []
            r_temp = []
            r = []
            

            for k in range(0, mu):
                
                broad_ckk= self.mult_shares(ra_share,C_shares[k,k]).n
                self.broadcast('c_kk' + str(self.comr), broad_ckk)
                
                r_temp.append(self.reconstruct_secret('c_kk'+str(self.comr))) 
             
              
                if r_temp[k] == 0:
                    r.append(0)
                elif r_temp[k] != 0:
                    r.append(1)
                else: 
                    print('error message')
           
                C_shares[mu+k,k] = h_share
            
                
                f.append(h_share)
         
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
            
            s_w_inv= w_inv*10E10
            s_w_inv=s_w_inv+0.5
            s_w_inv=int(s_w_inv) 
            
            
            if self.i ==0:
                self.distribute_shares(s_w_inv,'inv_y')
               
            sw_inv_share=self.get_share('inv_y').n 
          
            
            g=self.mult_shares(sw_inv_share, ra_share).n
            
          
            gt_temp=self.mult_shares(g,t_share).n
          
         
            gtL=gt_temp * L
          
       
            fx=np.zeros(2, dtype=int)  
        
           
            for k in range(0, mu):
                fx[k] = self.mult_shares(f[k], X[k]).n
       
 
            fx=fx.astype(int)
                    
            [ra,ca]=gtL.shape    
            [rb]=fx.shape
            cb=1
            
            for ii in range(0,ra):
                for jj in range(0,cb):
                    for kk in range(0,ca):
                        X[ii]=X[ii]+self.mult_shares(gtL[ii,kk],fx[kk]).n
           
         
            X=np.reshape(X, (2, 1))
   

            self.X = X
        
    class ground:
    
        def __init__(self,F, A, b, hh, tt, iden, ran, n, t,s): 
            self.A = A 
            self.b = b      
            self.server = s
            self.F = F
            self.t = t
            self.n = n
            self.hh=hh
            self.tt=tt
            self.iden= iden
            self.ran= ran
        
        def distribute_shares(self,var, name):
            shares = ss.share(self.F, var, self.t, self.n) 
            
            s = name                                  
            self.server.securecom[s] = shares
               
        def reconstruct_secret1(self, c):
            res = []
            for i in range(self.n):
                res.append(self.get_broadcast(c + str(i)))
            return ss.rec(self.F, res)
        
        
        @staticmethod   
        def reconstruct_secret(F, c):
             return ss.rec(F, c)
            
    
    ##############################################################################
    # Define field, number of parties, polynomial order, input matrices and more #
    ##############################################################################
             
    F = field.GF(792606555396977)   # prime
                                 
                                  
                                    
                     
    n = 3
    t = 1
    serv = server(F, n, t, 1500) 
    
    # Matrix dimensions
    m = 2   # number of A rows
    nn = 2  # number of A coloums
    l = 1   # number of b rows
    mu=min(nn,m)
    
    # Protocol inputs 
    A= 0 # initialize
    b= 0 # initialize
    
    tt = 1      # secret
    hh = 1      # secret
    
    # Secret matrices, input
    #sys 0
    H= np.array([[2, 3], [4 , 9]])      # A, secret
    G= np.array([[6],[15]])             # b, secret
    #sys 1
    #H= np.array([[5, 2], [6 , 3]])     
    #G= np.array([[2],[12]])
    #sys 2
    #H= np.array([[2, 3], [2 , 4]])
    #G= np.array([[80],[84]])              
    iden_n=np.identity(nn)
    
    AB=np.hstack((H,G))
    
    rankAB=np.array(matrix_rank(AB))
    rankA= np.array(matrix_rank(H))

    if rankA==rankAB:
         print('System is solvable')
    else:
         print('Preconditioning fails, system not solvable')

    # Generate Upper/Lower Toeplitz matrices (open)
    # OBS: random variables small range due to overfloat caused by scaling  
    # to avoid faulty output when inverting
    
    L = toeplitz([1,random.randint(1,10)])  
    U = toeplitz([1,random.randint(1,10)])
    
    L= np.array(np.tril(L) )               # remove upper triangular entries
    U= np.array(np.triu(U) )               # remove lower triangular entires
    
    #ran=7
    ran= random.randint(1,501)

    iden= 0
    
    
    #L= np.array(([1, 0],[11, 1]))
    #U= np.array(([1, 8],[0, 1]))
 
    
    # create shares of each matrix entry
    gr=ground(F, A, b, hh, tt, iden, ran, n, t, serv) # hh, tt)
    
    for p in range(0, m):
        b=G[p]
        b=int(b)
    
        gr.distribute_shares(b,'b'+str(p))
    
        
        for q in range(0, nn):
            A=H[p,q]
            A=int(A)
            iden_ny=iden_n[p,q]
            iden_ny=int(iden_ny)
    
            gr.distribute_shares(A,'a'+str(p)+str(q))
            gr.distribute_shares(iden_ny,'iden'+str(p)+str(q)) 
            
    gr.distribute_shares(gr.hh,'h_shares') 
    gr.distribute_shares(gr.tt,'t_shares') 
    gr.distribute_shares(gr.ran,'ran_shares') 
    

   
    part1 = part(F,n,t,0, serv)
    part2 = part(F,n,t,1, serv)
    part3 = part(F,n,t,2, serv)
    
    part1.start()
    part2.start()
    part3.start()
    
    part1.join()  # syncronizing
    part2.join()
    part3.join()
    
    a_p=part1.X
    b_p=part2.X
    c_p=part3.X
    
    
    # reconstruct solution
    X_fi1=gr.reconstruct_secret(F,[a_p[0,0],b_p[0,0],c_p[0,0]])
    X_fi2=gr.reconstruct_secret(F,[a_p[1,0],b_p[1,0],c_p[1,0]])
    

    res1=int(str(X_fi1))
    res2 = int(str(X_fi2))
    
    dummy =10E13
    
    # differentiate between positive and negativ numbers
    if res1 > dummy:
        res1 = res1 -792606555396977      # subtracting field due to wrap around 
                                          # caused by negative value
    
    if res2 > dummy:
        res2= res2 -792606555396977
    
    # final result
    finalX1=res1/10E10
    finalX2 =res2/10E10
    #time_elapsed = (time.clock() - time_start)
    print(finalX1, finalX2)
    #print('Solution, X= [',finalX1, finalX2, ']')
