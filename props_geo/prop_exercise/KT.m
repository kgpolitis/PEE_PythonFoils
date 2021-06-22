function Kt=KT(J,P_D,EAR,Z)

global WagKT

Zvn=Z.^WagKT.data(:,6);
AEA0un=EAR.^WagKT.data(:,5);
PDtn=P_D.^WagKT.data(:,4);
CoefT=WagKT.data(:,2).*Zvn.*AEA0un.*PDtn;

Kt=sum(CoefT.*J.^WagKT.data(:,3));