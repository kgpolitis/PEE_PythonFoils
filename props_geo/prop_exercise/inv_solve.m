% Input Prop Geometry Data
% Complete the code
D=
EAR=
Z=

% other
n_props=
F=0

% hull/propeller interactions
w=0;
t=0;

% water density
rho=1000;

% Velocity range
Nv=11;
V_min=
V_max=
Vs=linspace(V_min,V_max,Nv);

% Pitch range
Np=11;
P_D_min=
P_D_max=
P_Ds=linspace(P_D_min,P_D_max,Np);

% options of nonlinear solver
options = optimoptions('fsolve','Display','off');

n=zeros(Np,Nv);
for v=1:Nv
    for p=1:Np
        fun=@(N) RES(Vs(v))/(1-t)+F-n_props*KT(Vs(v)*(1-w)/N/D,P_Ds(p),EAR,Z).*rho.*N.^2*D.^4;
        n(p,v)=fsolve(fun,5,options);
    end
end

% Plot results
% NOTE: We need n in rpm, what is the required modification
[VV PP]=meshgrid(Vs,P_Ds);
figure
contour(VV,PP,n,'ShowText','on')
xlabel('V(m/s)')
ylabel('P/D')
grid on
title(['Wageningen D=',num2str(D),' EAR=',num2str(EAR),' Z=',num2str(Z)])