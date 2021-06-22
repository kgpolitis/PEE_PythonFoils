function Kq=KQ(J,P_D,EAR,Z)

global WagKQ

Zvn=Z.^WagKQ.data(:,6);
AEA0un=EAR.^WagKQ.data(:,5);
PDtn=P_D.^WagKQ.data(:,4);
CoefQ=WagKQ.data(:,2).*Zvn.*AEA0un.*PDtn
Kq=sum(CoefQ.*J.^WagKQ.data(:,3))
