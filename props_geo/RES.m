function Res=RES(V)

global RV

Res=interp1(RV.data(:,1),RV.data(:,2),V);