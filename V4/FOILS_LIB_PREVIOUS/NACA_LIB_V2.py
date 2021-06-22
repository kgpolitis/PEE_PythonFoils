from abc import ABC, abstractmethod

def NACA(code,TE_closed=1):
    """ NACA Picker """
    if (code//10000 !=0):
        return None # not yet implemented
    elif (code//1000 !=0):
        return Series4(code,TE_closed) 

class NACArep(ABC):
    
    @abstractmethod
    def yc(self,x):
        pass
    
    @abstractmethod
    def yt(self,x):
        pass
    
    @abstractmethod
    def dyc(self,x):
        pass
    
    @abstractmethod
    def show_parameters(self):
        pass
    
    def Xs(self,x):
        """ Suction side (X/c above coordinate)"""
        from numpy import sqrt
        val=x-self.dyc(x)/sqrt(1+self.dyc(x)**2)*self.yt(x)
        return val
        
    def Ys(self,x):
        """ Suction side (Y/c above coordinate)"""
        from numpy import sqrt
        val=self.yc(x)+1.0/sqrt(1+self.dyc(x)**2)*self.yt(x)
        return val
  
    
    def Xp(self,x):
        """ Pressure side (X/c below coordinate)"""
        from numpy import sqrt
        val=x+self.dyc(x)/sqrt(1+self.dyc(x)**2)*self.yt(x)
        return val
  
    def Yp(self,x):
        """ Pressure side (Y/c below coordinate)"""
        from numpy import sqrt
        val=self.yc(x)-1.0/sqrt(1+self.dyc(x)**2)*self.yt(x)
        return val
  
    def plot_ct(self,npoints=100):
        """ Returns a plt handle for the camber and thickness distributions """
        import matplotlib.pyplot as plt
        from numpy import linspace
        x=linspace(0,1,npoints)
        plt.plot(x,self.yc(x),'r',label='Camber')
        plt.plot(x,self.yt(x),'g',label='Thickness')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.legend()
        plt.grid(1)
        return plt
        
    def plot_XY(self,npoints=100):
        """ Returns a plt handle for the XY coordinates """
        import matplotlib.pyplot as plt
        from numpy import linspace
        x=linspace(0,1,npoints)
        plt.plot(self.Xs(x),self.Ys(x),'b',label='Suction Side')
        plt.plot(self.Xp(x),self.Yp(x),'r',label='Pressure Side')
        plt.xlabel('X/c')
        plt.ylabel('Y/c')
        plt.legend()
        plt.grid(1)
        plt.axis('equal')
        return plt
    
    def closed(self,TE_closed=True):
        self.TE_closed=TE_closed
    
    
### Definition of local foil geometries

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
        self.code=MPTT
        self.m=MPTT//1000
        self.p=(MPTT-self.m*1000)//100
        self.closed(TE_closed)
        # Find actual values
        self.t=(MPTT-self.m*1000-self.p*100)/100
        self.p=self.p/10
        self.m=self.m/100

    
    # Visual Verifier of parameters
    def show_parameters(self):
        """ Print Foil Parameters """
        print("NACA 4 digits : ",self.code)
        print("m=",self.m)
        print("p=",self.p)
        print("t=",self.t)
        if (self.TE_closed):
            print("Closed Trailing Edge")
        else:
            print("Open Trailing Edge")

    
    # definition of camber line
    def yc(self,x):
        from numpy import where
        """ Compute y=Y/c values of the camber line """
        # input argument is x (non-dimensional X coordinate x=X/c
        #        where this condition happens            then do this              if not do this
        y =where(x<=self.p                    ,self.m/self.p**2*(-x**2+2*self.p*x),self.m/(1-self.p)**2*(-x**2+2*self.p*x+1-2*self.p))         
        return y
    
    # definition of camber line derivative
    def dyc(self,x):
        """ Compute dy/dx(=dY/dX) values of the camber line (0<x<1) """
        from numpy import where
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