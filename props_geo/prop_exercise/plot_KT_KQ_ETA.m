% Plot Wageningen Kt,Kq,eta
% Input 
P_D=
EAR=
Z=

% Set Jmax below JKT0
percentage=0.99;
Jmax=JKT0(P_D,EAR,Z)*percentage;

% number of points to plot from J=0 to Jmax
nval=100;
J=linspace(0,Jmax,nval);

Kt=KT(J,P_D,EAR,Z);
Kq=KQ(J,P_D,EAR,Z);

% Question : Calculate eta
eta=

% plot
figure
plot(J,KT(J,P_D,EAR,Z))

hold
plot(J,KQ(J,P_D,EAR,Z))

plot(J,eta)

grid on
title(['Wagenigen P/D=',num2str(P_D),' EAR=',num2str(EAR),' Z=',num2str(Z)])
legend('Kt','Kq','eta')