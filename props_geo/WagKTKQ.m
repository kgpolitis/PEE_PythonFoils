% Evaluation of Wageningen Polynomials
WagKT=importdata('WagKT.txt');
WagKQ=importdata('WagKQ.txt');

% inputs
P_D=0.6
AEA0=0.5
Z=4

% Evaluate for these J values
N=100
J=linspace(0,1.3,N)
KT=zeros(1,N);

%KT values
Zvn=Z.^WagKT.data(:,6);
AEA0un=AEA0.^WagKT.data(:,5);
PDtn=P_D.^WagKT.data(:,4);
CoefT=WagKT.data(:,2).*Zvn.*AEA0un.*PDtn
for i=1:N
       KT(i)=sum(CoefT.*J(i).^WagKT.data(:,3))
end

%KQ values
Zvn=Z.^WagKQ.data(:,6);
AEA0un=AEA0.^WagKQ.data(:,5);
PDtn=P_D.^WagKQ.data(:,4);
CoefQ=WagKQ.data(:,2).*Zvn.*AEA0un.*PDtn
for i=1:N
       KQ(i)=sum(CoefQ.*J(i).^WagKQ.data(:,3))
end

%trim negative values
i0=find(KT<0)

J=J(1:i0(1)-1);
KT=KT(1:i0(1)-1);
KQ=KQ(1:i0(1)-1);
eta=KT.*J./(KQ*2*pi)

figure
plot(J,KT,'LineWidth',2)
hold
plot(J,KQ*10,'--','LineWidth',2)
plot(J,eta,'LineWidth',2)
legend('K_T','10K_Q','\eta')
grid on