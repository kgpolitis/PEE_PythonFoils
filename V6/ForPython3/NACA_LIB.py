### PART OF FOIL LIBRARY
# 
# Author: Konstantinos POLITIS
# 
#   Defines a Specific Instance of Foil : NACA
#   
#  To do list : 
#    - Add other NACA constructors (series 6)
# 
###
from FOIL import afoil as foil
from abc import ABC, abstractmethod

def NACA(code,TE_closed=1):
    """ NACA Picker """
    if (len(code) == 5):
        return None # not yet implemented
    elif (len(code) == 4):
        return Series4(code,TE_closed) 

class NACArep(foil):
    
    @abstractmethod
    def yc(self,x):
        pass
    
    @abstractmethod
    def dyc(self,x):
        pass
    
    @abstractmethod
    def curv(self,x):
        pass
    
    @abstractmethod
    def yt(self,x):
        pass
    
    @abstractmethod
    def dyt(self,x):
        pass
    
    def Xs(self,x):
        """ Suction side (X/c above coordinate)"""
        from numpy import sqrt
        val=x-self.dyc(x)/sqrt(1+self.dyc(x)**2)*self.yt(x)
        return val
    
    def Ys(self,x):
        """ Suction side (Y/c above coordinate)"""
        from numpy import sqrt
        val=self.yc(x)+1/sqrt(1+self.dyc(x)**2)*self.yt(x)
        return val
    
    
    def Xp(self,x):
        """ Pressure side (X/c below coordinate)"""
        from numpy import sqrt
        val=x+self.dyc(x)/sqrt(1+self.dyc(x)**2)*self.yt(x)
        return val
    
    def Yp(self,x):
        """ Pressure side (Y/c below coordinate)"""
        from numpy import sqrt
        val=self.yc(x)-1/sqrt(1+self.dyc(x)**2)*self.yt(x)
        return val
    
    def vecS_TE(self):
        """ Tangent at TE at pressure and suction (orientation from pressure to suction - towards LE and back to TE towards wake) """
        from numpy import sqrt
        v=self.curv(1)*self.yt(1)
        dyc=self.dyc(1)
        dyt=self.dyt(1)
        nR2=1+dyc**2
        nR=sqrt(1+dyc**2)
        vecNx=-dyc/nR
        vecNy=   1/nR
        vecRx=1
        vecRy=dyc
        vec_SuctSide_TEtoWkx= ((1-v)*vecRx+dyt*vecNx)/sqrt((1-v)**2*nR2+dyt**2) # above TE
        vec_SuctSide_TEtoWky= ((1-v)*vecRy+dyt*vecNy)/sqrt((1-v)**2*nR2+dyt**2) # above TE
        vec_PresSide_TEtoLEx=-((1+v)*vecRx-dyt*vecNx)/sqrt((1+v)**2*nR2+dyt**2) # below TE
        vec_PresSide_TEtoLEy=-((1+v)*vecRy-dyt*vecNy)/sqrt((1+v)**2*nR2+dyt**2) # below TE
        A=[vec_PresSide_TEtoLEx, vec_PresSide_TEtoLEy, vec_SuctSide_TEtoWkx, vec_SuctSide_TEtoWky]
        return A 

    def vecS_LE(self):
        """ Tangent at LE (orientation from pressure to suction) """
        from numpy import sqrt
        dyc=self.dyc(0)
        lv=sqrt(1+dyc**2)
        vx=-dyc/lv
        vy=1./lv
        A=[vx,vy,vx,vy]
        return A
        
    
    def plot_ct(self,npoints=100):
        """ Returns a plt handle for the camber and thickness distributions """
        import matplotlib.pyplot as plt
        from numpy import linspace
        x=linspace(0,1,npoints)
        plt.plot(x,self.yc(x),'r',label='Camber')
        plt.plot(x,self.yt(x),'g',label='Thickness')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.title(self.name())
        plt.legend()
        plt.grid(1)
        return plt

    
### Definitions of local foil geometries

class Series4(NACArep):
    """ NACA Series 4 """
    
    ### Declaration of Constants
    # Do not modify if not sure

    # Constants for 4 digit thickness
    __A0  = 0.2969       # multiplies sqrt
    __A1  =-0.126        # multiplies x
    __A2  =-0.3516       # multiplies x^2
    __A3  = 0.2843       # multiplies x^3
    __A4c =-0.1036       # multiplies x^4 (closed trailing edge)
    __A4o =-0.1015       # multiplies x^4 (open trailing edge)

###>End of Declaration of Constants
    
    ### Definition of methods  
    
    #Initialiser
    def __init__(self,MPTT,TE_closed=True):
        """ Initialiser : Parameters, and closed trailing edge specifier """
        # Find digits
        self.code=int(MPTT,10)
        self.m=self.code//1000
        self.p=(self.code-self.m*1000)//100
        self.closed(TE_closed)
        # Find actual values
        self.t=(self.code-self.m*1000-self.p*100)/100
        self.p=self.p/10
        self.m=self.m/100
    
    # Visual Verifier of parameters
    def show_parameters(self):
        print("NACA 4 digits : ",self.code)
        print("m=",self.m)
        print("p=",self.p)
        print("t=",self.t)
        if (self.TE_closed):
            print("Closed Trailing Edge")
        else:
            print("Open Trailing Edge")

    # Name
    def name(self):
        """ Get the foils name """
        n="NACA"+"_{:d}".format(self.code)
        return n
    
    # definition of camber line
    def yc(self,x):
        from numpy import where
        """ Compute y=Y/c values of the camber line """
        # input argument is x (non-dimensional X coordinate x=X/c
        #        where this condition happens            then do this              if not do this
        if (self.p==0):
            return 0
        y =where(x<=self.p                    ,self.m/self.p**2*(-x**2+2*self.p*x),self.m/(1-self.p)**2*(-x**2+2*self.p*x+1-2*self.p))         
        return y
    
    # definition of camber line derivative
    def dyc(self,x):
        """ Compute dy/dx(=dY/dX) values of the camber line (0<x<1) """
        from numpy import where
        if (self.p==0):
            return 0
        dy=(-2*x+2*self.p)*where(x<=self.p,self.m/self.p**2,self.m/(1-self.p)**2)
        return dy
    
    # definition of thickness 
    def yt(self,x):
        from numpy import sqrt
        y=self.__A0*sqrt(x)+self.__A1*x+self.__A2*x**2+self.__A3*x**3
        if (self.TE_closed):
            y+=self.__A4c*x**4
        else:
            y+=self.__A4o*x**4
        y*=self.t/0.2
        return y

    # definition of thickness derivative 
    def dyt(self,x):
        from numpy import sqrt
        dy=self.__A0/2./sqrt(x)+self.__A1+self.__A2*x*2+self.__A3*x**2*3
        if (self.TE_closed):
            dy+=self.__A4c*x**3*4
        else:
            dy+=self.__A4o*x**3*4
        dy*=self.t/0.2
        return dy
    
    # definition of camber line curvature (ddyc/sqrt(1+dyc**2))
    def curv(self,x):
        """ Compute d2y/dx2 values of the camber line (0<x<1) """
        from numpy import where, sqrt
        if (self.p==0):
            return 0
        curv=-2*where(x<=self.p,self.m/self.p**2,self.m/(1-self.p)**2)/sqrt(1+self.dyc(x)**2)**3
        return curv
    
