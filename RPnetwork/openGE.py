#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 19 12:08:59 2019

@author: avtl
"""


import numpy as np 
from numpy.linalg import inv
import random 
from numpy.linalg import matrix_rank
from threading import Thread
import FFArithmetic as field
import shamir_scheme as ss
import time
import proc

time_start = time.clock()
t = 1
h= 1;
l= 1;
n= 2;
m= 2;
mu= min(n,m);

A=np.array( [[2 ,3],[ 4, 9]])

b= np.array([[6],[15]])

L= np.array([[1 ,0],[ 11 ,1]])
U= np.array([[1 ,8],[ 0 ,1]])
#L = toeplitz([1,random.randint(1,10)])  
#U = toeplitz([1,random.randint(1,10)])
    
#L= np.array(np.tril(L) )            
#U= np.array(np.triu(U) )              
    


e11= np.array(U@A@L) # OK
e12=np.array(U@b)         
e21= np.array(np.eye(2))
e22= np.array(np.zeros((2,1)))


C=np.array(([e11[0,0], e11[0,1], e12[0,0]],[e11[1,0], e11[1,1], e12[1,0]], [e21[0,0], e21[0,1], 0],[ e21[1,0], e21[1,1], 0]))
C=C.astype(int)

f = []
r_temp = []
r = []


for k in range(mu):
    if C[k,k]!= 0:
        r.append(1)
    elif C[k,k]== 0:
        r.append( 0)

    C[mu+k,k] = h;

    f.append(h)
    t=t*h
    h = h * (C[k,k]+1-r[k]) ;

    for i in range (mu+k):
        for j in range ((k+1),(n+l)):
            if i!= k and (i<= mu or j <= n-1):
                #C[i,j]= [(C[k,k]+1-r[k]), C[k,j]]*[[C[i,j]],[(-C[i,k])]];
                dummy=np.matrix( np.vstack((C[i,j],-(C[i,k]))))
                temp= np.matrix(np.hstack(((C[k,k]+1-r[k]), C[k,j])))
                temp_C1=temp[0,0]*dummy[0,0]
                temp_C2=temp[0,1]*dummy[1,0]
                C[i,j]=temp_C1 +temp_C2
                
                

x = np.asarray(C[(0,1), -1])

g= 1/(t*h)

g=g*10E10
gtL=g*t*L

fx= np.diag(f)@x

x=gtL@np.eye(2)@fx

x=x/10E10
time_elapsed = (time.clock() - time_start)
print('time_elapsed:', time_elapsed)
