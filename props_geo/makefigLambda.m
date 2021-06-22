syms J r real
syms a real
assume(J>0)
assume(a>0)
syms x
int(sqrt(1+a^2*x^2/J^2)*(- 8.6e+02*x^{7} + 3.3e+03*x^{6} - 5.3e+03*x^{5} + 4.6e+03*x^{4} - 2.3e+03*x^{3} + 6.5e+02*x^{2} - 96*x +7.2),x,0.16,1)
subs(ans,a,pi)
Iv=matlabFunction(ans)
x=linspace(0.4,1.5,200)
Ivvals=Iv(x)
plot(x,Ivvals)
grid on
xlabel('$$J$$','interpreter','latex')
ylabel('$$\Lambda(J)$$','interpreter','latex','rotation',0,'Position',[-0.1 80])
set(gca,'fontsize',14)
% change ticks manually!!!!
%print('-bestfit','Mean Reynolds Corr','-dpdf')