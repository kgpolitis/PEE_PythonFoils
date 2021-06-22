function JKt0=JKT0(P_D,EAR,Z)

fun=@(J) KT(J,P_D,EAR,Z);

JKt0=fsolve(fun,0.5);