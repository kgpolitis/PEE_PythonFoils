%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Plot Wageningen Blade Sections Wrapped in Cylinder in diff r/R
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

tle_D=0
tte_D=0
Z=4
AEA0=0.4
P_D=0.6
% Import V1 and V2
V1=importdata('V1.txt');
V2=importdata('V2.txt');
% V1 and V2 values are provided for :
P=[-1 -0.95 -0.9 -0.8 -0.7 -0.6 -0.5 -0.4 -0.2 0 0.2 0.4 0.5 0.6 0.7 0.8 0.85 0.9 0.95 1];
rR=[1 0.9 0.85 0.8 0.7 0.6 0.5 0.4 0.3 0.25 0.2 0.15];
% where P=(x-x(tmax))/x(tmax) where x is the length along the chord, and
% rR=r/R
% Generate meshgrid to interpolate V1,V2 values 
[mP,mrR]=meshgrid(P,rR);

% tmax is a function of number of blades, and Ar,Br (Wageningen data)
if (Z==3)
    Wag=importdata('Wageningen3.txt');
else
    Wag=importdata('Wageningen4+.txt');
end
tmax_D=Wag.data(:,5)-Wag.data(:,6)*Z; % this is a function of r/R

% number of blade sections
NrR=20;
Ar_R=linspace(0.2,0.99,NrR);

% Number of points per section
N=61;

% store points here

figure     
hold
grid on
xlabel('x/R')
ylabel('y/R')
zlabel('z/R')
axis equal

for i=1:NrR

r_R=Ar_R(i);
% Interpolate tmax_D at requested rR
tmax_D_r_R=interp1(Wag.data(:,1),tmax_D,r_R,'spline');

% Get chord distribution
c_D=Wag.data(:,2)*AEA0/Z;

% find chord at r/R
c_D_r_R=interp1(Wag.data(:,1),c_D,r_R,'spline');

% get distribution of 1-x(tmax)/c
b=Wag.data(:,4);

% find 1-x(tmax)/c at r/R
b_r_R=interp1(Wag.data(:,1),b,r_R,'spline');

% get distribution of 1-xd/c
a=Wag.data(:,3);

% find 1-xd/c at r/R
a_r_R=interp1(Wag.data(:,1),a,r_R,'spline');

% Evaluate blade section at N points P points
Ps=linspace(-1,1,N);

% yface_c and yback_c (i.e. divided by chord)
yface_c(1:N)=0;
yback_c(1:N)=0;
x_c(1:N)=0;
for i=1:N
    iV1=interp2(mP,mrR,V1,Ps(i),r_R,'spline');
    iV2=interp2(mP,mrR,V2,Ps(i),r_R,'spline');
    if (Ps(i)<=0)
        %x_c(i)=(Ps(i)+1)*(1-b_r_R)-1+a_r_R; % displaced to generator
        x_c(i)=(Ps(i)+1)*(1-b_r_R)-0.5; % displaced to directrix
        yface_c(i)=iV1*(tmax_D_r_R-tte_D)/c_D_r_R;
        yback_c(i)=((iV1+iV2)*(tmax_D_r_R-tte_D)+tte_D)/c_D_r_R;
    else
        %x_c(i)=1+(Ps(i)-1)*b_r_R-1+a_r_R ; % displaced to generator
        x_c(i)=1+(Ps(i)-1)*b_r_R-0.5 ; % displaced to directrix
        yface_c(i)=iV1*(tmax_D_r_R-tle_D)/c_D_r_R;
        yback_c(i)=((iV1+iV2)*(tmax_D_r_R-tle_D)+tle_D)/c_D_r_R;
    end
end

% displace to centerline
ydisp=(yface_c(1)+yface_c(N))/2;
yface_c=yface_c-ydisp;
yback_c=yback_c-ydisp;

% rotate over pitch
theta=atan(P_D/(pi*r_R));
xface_c_rot=x_c*cos(theta)-yface_c*sin(theta);
yface_c_rot=x_c*sin(theta)+yface_c*cos(theta);
xback_c_rot=x_c*cos(theta)-yback_c*sin(theta);
yback_c_rot=x_c*sin(theta)+yback_c*cos(theta);

% add skew
xface_c_rot=xface_c_rot+(a_r_R-0.5)*cos(theta);
xback_c_rot=xback_c_rot+(a_r_R-0.5)*cos(theta);

% find w
phi=2*xface_c_rot*c_D_r_R/r_R;
xfacew_R=r_R*sin(phi);
zfacew_R=-r_R*(1-cos(phi))+r_R;
phi=2*xback_c_rot*c_D_r_R/r_R;
xbackw_R=r_R*sin(phi);
zbackw_R=-r_R*(1-cos(phi))+r_R;

% make figures
%plot3(2*xface_c_rot*c_D_r_R,2*yface_c_rot*c_D_r_R,r_R*ones(1,N),'b')
%plot3(2*xback_c_rot*c_D_r_R,2*yback_c_rot*c_D_r_R,r_R*ones(1,N),'r')
plot3(xfacew_R,2*yface_c_rot*c_D_r_R,zfacew_R,'b','LineWidth',2)
plot3(xbackw_R,2*yback_c_rot*c_D_r_R,zbackw_R,'r','LineWidth',2)

end
