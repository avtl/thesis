

t = 1;
h= 1;
l= 1;
n= 2;
m= 2;
mu= min(n,m);

A= [2 3; 3 2];
b= [1; 4];

L= [1 0; 11 1];
U= [1 8; 0 1];

C= [(eye(2)*U*A*L) (eye(2)*U*b);eye(2) zeros(2,1)]
r= zeros(2,1);
f= zeros(2,1);

for k = 1:mu
    if C(k,k)~= 0
        r(k)=1;
    elseif C(k,k)== 0
        r(k) = 0;
    end
 
C(mu+k,k) = h;

f(k) = h;

t=t*h;

h = h * (C(k,k)+1-r(k)) ;
 
for i = 1:(mu+k)
  
for j=(k+1):(n+l)
   
    if i ~= k && (i <= mu || j <= n)
        C(i,j)= [(C(k,k)+1-r(k)) C(k,j)]*[C(i,j);(-C(i,k))];
    end 
end
end 
end
disp(C)

x= C(1:2,3);

g= inv(t*h);


g=g*10E10;
g*t*L;

diag(f)*x;

x= g*t*L*eye(2)*diag(f)*x;

        