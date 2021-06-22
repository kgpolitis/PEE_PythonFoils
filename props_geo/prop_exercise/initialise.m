% Initialise workspace
global WagKT WagKQ RV
WagKT=importdata('WagKT.txt');
WagKQ=importdata('WagKQ.txt');
RV=importdata('resistance.txt');
display('Velocity Limits')
V_min=min(RV.data(:,1))
V_max=max(RV.data(:,1))

% 
% Check the file resistance. 
% Modify the values of RV.data(:,1) to SI units.
% How we can obtain the RV values of this file ?