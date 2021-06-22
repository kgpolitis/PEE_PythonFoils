% Initialise workspace
global WagKT WagKQ RV
WagKT=importdata('WagKT.txt');
WagKQ=importdata('WagKQ.txt');
RV=importdata('resistance.txt');
display('Velocity Limits')
V_min=min(RV.data(:,1))
V_max=max(RV.data(:,1))
RV.data(:,2)=RV.data(:,2)*9.807