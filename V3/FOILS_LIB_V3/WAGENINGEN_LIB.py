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
from FOIL  import afoil as foil
from scipy import interpolate

def WAGENINGEN(Z,EAR,rR,TE_closed=1):
    """ WAGENINGEN Picker """
    return BseriesFoil(D,Z,EAR,rR,TE_closed) 

class BseriesFoil(foil):
    
    # K(r) for B series
    __Kr=[1.662, 1.882, 2.05, 2.152, 2.187, 2.144, 1.970, 1.582] 
    
    # Provided at r/R=
    __rR_Kr=[0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    
    # Kr function
    __KrSp = interpolate.InterpolatedUnivariateSpline(self.__rR_Kr,self.__Kr)
    
    # Percentages (NOT in %) of Maximum thickness for a given r/R and given position from maximum thickness 
    # Note : Lines   denote radius :                                                          :                 r/R = 0.15, 0.20, 0.25, 0.3, 0.4, 0.5, 0.6, 0.7 
    #        Columns denote percentage of distance from location of maximum thickness, x_tmax :   For the j-th column we have the following
    #<------------                     X/c=(1+a(j))*x_tmax/c     --------------------------------->  X/c=x_tmax <-------------------------      X/c=(1-a(j))*x_tmax/c+a  ------------------------------->
    # LE                                                                                                                                                                                         TE
    #with:j=1    2       3    ....
    #a(j)=-1   -0.95   -0.9    -0.85        -0.8       -0.7       -0.6      -0.5      -0.4      -0.2     0        0.2     0.4        0.5      0.6       0.7       0.8        0.9       0.95      1       
    __V1=[ 
    [ 0.3860 ,  0.3150 , 0.2642 , 0.2230  ,  0.1870 ,   0.1320 ,   0.0920 ,  0.0615 ,  0.0384 ,  0.0096 ,  0 ,   0.0365 ,  0.0955 ,  0.1280 ,   0.1610 ,  0.1950 ,  0.2300 ,  0.2650 ,  0.2824 , 0.3000],
    [ 0.3560 ,  0.2821 , 0.2353 , 0.2000  ,  0.1685 ,   0.1180 ,   0.0804 ,  0.0520 ,  0.0304 ,  0.0049 ,  0 ,   0.0172 ,  0.0592 ,  0.0880 ,   0.1207 ,  0.1570 ,  0.1967 ,  0.2400 ,  0.2630 , 0.2826], 
    [ 0.3256 ,  0.2513 , 0.2068 , 0.1747  ,  0.1465 ,   0.1008 ,   0.0669 ,  0.0417 ,  0.0224 ,  0.0031 ,  0 ,   0.0084 ,  0.0350 ,  0.0579 ,   0.0899 ,  0.1246 ,  0.1651 ,  0.2115 ,  0.2372 , 0.2598],
    [ 0.2923 ,  0.2186 , 0.1760 , 0.1445  ,  0.1191 ,   0.0790 ,   0.0503 ,  0.0300 ,  0.0148 ,  0.0027 ,  0 ,   0.0033 ,  0.0202 ,  0.0376 ,   0.0623 ,  0.0943 ,  0.1333 ,  0.1790 ,  0.2040 , 0.2306],
    [ 0.2181 ,  0.1467 , 0.1088 , 0.0833  ,  0.0637 ,   0.0357 ,   0.0189 ,  0.0090 ,  0.0033 ,  0      ,  0 ,   0      ,  0.0044 ,  0.0116 ,   0.0214 ,  0.0395 ,  0.0630 ,  0.0972 ,  0.1200 , 0.1467],
    [ 0.1278 ,  0.0778 , 0.0500 , 0.0328  ,  0.0211 ,   0.0085 ,   0.0034 ,  0.0008 ,  0      ,  0      ,  0 ,   0      ,  0      ,  0.0012 ,   0.0040 ,  0.0100 ,  0.0190 ,  0.0330 ,  0.0420 , 0.0522], 
    [ 0.0382 ,  0.0169 , 0.0067 , 0.0022  ,  0.0006 ,   0      ,   0      ,  0      ,  0      ,  0      ,  0 ,   0      ,  0      ,  0      ,   0      ,  0      ,  0      ,  0      ,  0      , 0     ], 
    [ 0      ,  0      , 0      , 0       ,  0      ,   0      ,   0      ,  0      ,  0      ,  0      ,  0 ,   0      ,  0      ,  0      ,   0      ,  0      ,  0      ,  0      ,  0      , 0     ] ]
    
    __rR_V1=[0.15, 0.20, 0.25, 0.3, 0.4, 0.5, 0.6, 0.7]
    __a_V1 =[-1  ,-0.95, -0.9, -0.85, -0.8, -0.7, -0.6, -0.5, -0.4, -0.2,  0 , 0.2, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95, 1 ]  
    
    # Data for Thickness : 
    # Note : Lines   denote radius :                                                          :                 r/R = 0.15, 0.20, 0.25, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.85, 0.9 
    #        Columns denote percentage of distance from location of maximum thickness, x_tmax :   For the j-th column we have the following
    #<------------                     X/c=(1+a(j))*x_tmax/c     --------------------------------->  X/c=x_tmax <-------------------------      X/c=(1-a(j))*x_tmax/c+a  ------------------------------->
    # LE                                                                                                                                                                                                TE
    #with:j=1    2       3    ....
    #a(j)=-1   -0.9    -0.8    -0.7        -0.6       -0.5       -0.4      -0.3      -0.2      -0.1     0        0.2     0.4        0.5      0.6       0.7       0.8        0.9       0.95      1       
    __V2=[
    [ 0   ,   0.1300    , 0.2600  ,  0.3665  ,  0.4520  ,  0.5995  , 0.7105  ,   0.8055  ,  0.8825  ,  0.9760 ,  1 ,  0.9360 ,  0.7805  ,  0.6770   , 0.5585  , 0.4280  , 0.2870   ,  0.1325  ,  0.0540 ,  0 ],  
    [ 0   ,   0.1560    , 0.2840  ,  0.3905  ,  0.4777  ,  0.6190  , 0.7277  ,   0.8170  ,  0.8875  ,  0.9750 ,  1 ,  0.9446 ,  0.7984  ,  0.6995   , 0.5842  , 0.4535  , 0.3060   ,  0.1455  ,  0.0640 ,  0 ],   
    [ 0   ,   0.1758    , 0.3042  ,  0.4108  ,  0.4982  ,  0.6359  , 0.7415  ,   0.8259  ,  0.8899  ,  0.9751 ,  1 ,  0.9519 ,  0.8139  ,  0.7184   , 0.6050  , 0.4740  , 0.3228   ,  0.1567  ,  0.0725 ,  0 ],   
    [ 0   ,   0.1890    , 0.3197  ,  0.4265  ,  0.5130  ,  0.6505  , 0.7520  ,   0.8315  ,  0.8920  ,  0.9750 ,  1 ,  0.9583 ,  0.8265  ,  0.7335   , 0.6195  , 0.4885  , 0.3360   ,  0.1670  ,  0.0800 ,  0 ],   
    [ 0   ,   0.1935    , 0.3235  ,  0.4335  ,  0.5220  ,  0.6590  , 0.7593  ,   0.8345  ,  0.8933  ,  0.9725 ,  1 ,  0.9645 ,  0.8415  ,  0.7525   , 0.6353  , 0.5040  , 0.3500   ,  0.1810  ,  0.0905 ,  0 ],   
    [ 0   ,   0.1750    , 0.3056  ,  0.4135  ,  0.5039  ,  0.6430  , 0.7478  ,   0.8275  ,  0.8880  ,  0.9710 ,  1 ,  0.9639 ,  0.8456  ,  0.7580   , 0.6439  , 0.5140  , 0.3569   ,  0.1865  ,  0.0950 ,  0 ],   
    [ 0   ,   0.1485    , 0.2720  ,  0.3775  ,  0.4620  ,  0.6060  , 0.7200  ,   0.8090  ,  0.8790  ,  0.9690 ,  1 ,  0.9613 ,  0.8426  ,  0.7530   , 0.6415  , 0.5110  , 0.3585   ,  0.1885  ,  0.0965 ,  0 ],   
    [ 0   ,   0.1240    , 0.2337  ,  0.3300  ,  0.4140  ,  0.5615  , 0.6840  ,   0.7850  ,  0.8660  ,  0.9675 ,  1 ,  0.96   ,  0.84    ,  0.75     , 0.64    , 0.51    , 0.36     ,  0.19    ,  0.0975 ,  0 ],   
    [ 0   ,   0.1050    , 0.2028  ,  0.2925  ,  0.3765  ,  0.5265  , 0.6545  ,   0.7635  ,  0.8520  ,  0.9635 ,  1 ,  0.96   ,  0.84    ,  0.75     , 0.64    , 0.51    , 0.36     ,  0.19    ,  0.0975 ,  0 ],   
    [ 0   ,   0.1000    , 0.1950  ,  0.2830  ,  0.3660  ,  0.5160  , 0.6455  ,   0.7550  ,  0.8450  ,  0.9615 ,  1 ,  0.96   ,  0.84    ,  0.75     , 0.64    , 0.51    , 0.36     ,  0.19    ,  0.0975 ,  0 ],   
    [ 0   ,   0.0975    , 0.1900  ,  0.2775  ,  0.3600  ,  0.51    , 0.6400  ,   0.75    ,  0.8400  ,  0.9600 ,  1 ,  0.96   ,  0.84    ,  0.75     , 0.64    , 0.51    , 0.36     ,  0.19    ,  0.0975 ,  0 ]]  
    
    __rR_V2=[0.15, 0.20, 0.25, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.85, 0.9]
    __a_V1 =[-1  ,-0.95, -0.9, -0.85, -0.8, -0.7, -0.6, -0.5, -0.4, -0.2,  0 , 0.2, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95, 1 ]  
    
    
    
    
    #Initialiser
    def __init__(self,Z,EAR,rR,TE_closed):
        """ Initialiser : Parameters, and closed LEADING edge specifier """
        # NOTE : Here TE_Closed refers to the LEADING EDGE
        self.closed(TE_closed)
        self.D=D
        self.EAR=EAR
        self.Z=Z
        self.rR=rR
    
    # Complete exemple
    def chord(self,r):
        from scipy import interp1d
        """ Chord for the requested radius """
        self.chord=2*self.__KrSp*self.EAR 
        
    # A completer
    def x_tmax(self,r):
        """ Location of maximum thickness for the requested radius """
        # Last column of table 4.11
        # Attention : these tables are actually function and interpolations
        # are required
        pass
    
    # A completer
    def yt(self,x):
        """ Thickness for the requested radius """
        # Add equation 4.4 (use table 4.9 for Ar,Br) 
        # Attention : these tables are actually function and interpolations
        # are required
        pass
    
    def Xs(self,x):
        """ Suction side (X above coordinate)"""
        return x
        
    def Xp(self,x):
        """ Pressure side (X below coordinate)"""
        return x
    
    # A completer
    def Yp(self,x):
        """ Pressure side (Y below coordinate)"""
        # Add equation 4.2 (use table 4.9 for Ar,Br) 
        # Attention : these tables are actually function and interpolations
        # are required
        return x
    
    # A completer
    def Ys(self,x):
        """ Suction side (Y above coordinate)"""
        
    
  
    
    def vecS_TE(self):
        """ Tangent at TE at pressure and suction (orientation from pressure to suction - towards LE and back to TE towards wake) """
        vec_SuctSide_TEtoWkx=  1 # above TE
        vec_SuctSide_TEtoWky=  0 # above TE
        vec_PresSide_TEtoLEx= -1 # below TE
        vec_PresSide_TEtoLEy=  0 # below TE
        return [vec_PresSide_TEtoLEx, vec_PresSide_TEtoLEy, vec_SuctSide_TEtoWkx, vec_SuctSide_TEtoWky]

    def vecS_LE(self):
        v=[0,1]
        return v
        
    
    def plot_chord(self,npoints=100):
        """ Returns a plt handle for the chord/R distribution """
        import matplotlib.pyplot as plt
        from numpy import linspace
        x=linspace(0,1,npoints)
        plt.plot(x,self.chord(x),'r',label='Camber')
        plt.xlabel('r/R')
        plt.ylabel('c/R')
        plt.legend()
        plt.grid(1)
        return plt

    # Visual Verifier of parameters
    def show_parameters(self):
        print("WAGENINGEN : ")
        print("EAR=",self.EAR)
        print("Z=",self.Z)
        print("rE=",self.rR)
        if (self.TE_closed):
            print("Closed Leading Edge")
        else:
            print("Open Leading Edge")

