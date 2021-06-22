%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Plot Wageningen Blade Sections
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Provide desired r/R > 0.15, tle_D, tte_D, number of blades (Z>=3), expanded
% area ration AEA0, pitch over diameter P/D
r_R=0.2
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

% Interpolate tmax_D at requested rR
tmax_D_r_R=interp1(Wag.data(:,1),tmax_D,r_R,'spline');

% Get chord distribution
c_D=Wag.data(:,2)*AEA0/Z;

% find chord at r/R
c_D_r_R=interp1(Wag.data(:,1),c_D,r_R,'spline');
c_D_r_R
% get distribution of 1-x(tmax)/c
b=Wag.data(:,4);

% find 1-x(tmax)/c at r/R
b_r_R=interp1(Wag.data(:,1),b,r_R,'spline');

% get distribution of 1-xd/c
a=Wag.data(:,3);

% find 1-xd/c at r/R
a_r_R=interp1(Wag.data(:,1),a,r_R,'spline');

% Evaluate blade section at N points P points
N=61;
Ps=linspace(-1,1,N);

% yface_c and yback_c (i.e. divided by chord)
yface_c(1:N)=0;
yback_c(1:N)=0;
x_c(1:N)=0;
for i=1:N
    iV1=interp2(mP,mrR,V1,Ps(i),r_R,'spline');
    iV2=interp2(mP,mrR,V2,Ps(i),r_R,'spline');
    if (Ps(i)<=0)
        x_c(i)=(Ps(i)+1)*(1-b_r_R)-0.5; % displaced to directrix
        yface_c(i)=iV1*(tmax_D_r_R-tte_D)/c_D_r_R;
        yback_c(i)=((iV1+iV2)*(tmax_D_r_R-tte_D)+tte_D)/c_D_r_R;
    else
        x_c(i)=1+(Ps(i)-1)*b_r_R-0.5; % displaced to directrix
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

% make figures
%figure
plot(xface_c_rot,yface_c_rot,'LineWidth',2)
% plot no rotation
%plot(x_c,yface_c,'LineWidth',2)
% plot vs Ps
%plot(Ps,yface_c,'LineWidth',2)
%hold
plot(xback_c_rot,yback_c_rot,'LineWidth',2)
% plot no rotation
% plot(x_c,yback_c,'LineWidth',2)
% plot vs Ps
%plot(Ps,yback_c,'LineWidth',2)
%axis equal      
%legend('face','back')
%grid on
%xlabel('x/c')
%ylabel('y/c')