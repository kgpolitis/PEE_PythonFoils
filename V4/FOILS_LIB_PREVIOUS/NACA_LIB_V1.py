



### Declaration of Constants
# Do not modify if not sure

# Constants for 4 digit thickness
__A0 = 0.2969       # multiplies sqrt
__A1 =-0.126        # multiplies x
__A2 =-0.3516       # multiplies x^2
__A3 = 0.2843       # multiplies x^3
__A4c =-0.1036       # multiplies x^4 (closed trailing edge)
__A4o =-0.1015       # multiplies x^4 (open trailing edge)

###>End of Declaration of Constants


### Definition of local foil geometries

class Series4:
    """ NACA Series 4 """
            
    ### Definition of methods  
    
    #Initialiser
    def __init__(self,MPTT,TE_closed=True):
        """ Initialiser : Parameters, and closed trailing edge specifier """
        # Find digits
        self.code=MPTT
        self.m=MPTT//1000
        self.p=(MPTT-self.m*1000)//100
        self.TE_closed=TE_closed
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
        """ Compute y=Y/c values of the camber line """
        # input argument is x (non-dimensional X coordinate x=X/c
        y=0
        if (0<x and x<=sefl.m):
            y=(-x**2+2*self.p*x)
        elif (x<1):
            y=(-x**2+2*self.p*x+1-2*p)
        y*=self.m/self.p**2
        return y
    
    def yt(self,x):
        from numpy import sqrt
        y=0
        if(0<x and x<1):
            y=__A0*sqrt(x)+__A1*x+__A2*x**2+__A3*x**3
            if (self.TE_closed):
                y+=__A4c*x**4
            else:
                y+=__A4o*x**4
        y*=self.t
        return y