close all 
clear 
clc

x = -1:0.1:4;
f1=1-1.5*x+0.5*x.^2;
f2=1-3*x + x.^2;
f3=1.5*x - 0.5*x.^2;
f1_test= -(2/3)*x + (1/3)*x.^2;
h=2-3*x + x.^2



p=plot(x,f1,'DisplayName','This one'); hold on;

p1= plot(x,f2, 'DisplayName', 'This two' );
 
p2= plot(x,f3, 'DisplayName', 'This three');
 
p3= plot(x,f1_test, ':', 'DisplayName', 'This four');
 
p4=plot(0,1,'k+');

p5=plot(0,0,'k');

p6=plot(1,-1,'k+');

p7=plot(1,0,'k+');


p8=plot(1,1,'k+');


p9=plot(2,-1,'k+');


p10=plot(2,0,'k+');


p11=plot(2,1,'k+');


p12=plot(3,0,'k+');


p13=plot(3,1,'k+');
p14=plot(0,0,'k*');

grid
ylim([-1.5 2.5]);
legend([p, p1, p2, p3],{'f_1(x)', 'f_2(x)' ,'f_3(x)', 'f_1´(x)'})


figure(2)
g=plot(x, h, 'DisplayName', 'This one'); hold on;
g1=plot(0,2, 'k+')
grid
ylim([-0.5 2.5]);
legend([g],{'f(x)'})
