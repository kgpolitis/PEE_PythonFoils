### PART OF FOIL LIBRARY
# 
# Author: Konstantinos POLITIS
# 
#   Defines a Specific Instance of Foil : Wageningen 
#   
#  To do list : 
#         1. Seperate propeller parts from foil parts 
#         2. Rework interpolation (for now linear) for V1, V2 values 
#         3. Add "smoothing" option (or extend option) for squared trailing edges
#         4. Remove Use_Original Option : Create variants for Bseries propellers 
#            using modified distributions of K(z)
# 
# Note : To define a Wageningen Foil we have to specify 
#        the geometry of the whole propeller:
#        Z   : number of blades
#        EAR : extended area ratio
#        rR  : radial location
#        
#   If we do not provide all the above then we cannot 
#   define the basic characteristics of the foil.
#   
#   Therefore, we actually define the propeller to define 
#   the foil ... this is a bit too much... but that's life 
#   
#   
#        
###
from FOIL  import afoil as foil
from numpy import array as nparr

def WAGENINGEN(Z,EAR,rR,tLE_tmax=0.,tTE_tmax=0,Use_Original=1,Use_Smooth=0,s=0,Smooth_LE=0,x0s=0.1,x0p=0.1,ks=0.5,kp=0.5):
    """ WAGENINGEN Picker 
    Inputs :
      Z                  : number of blades 
      EAR                : expanded area ratio
      rR                 : non dimensional reference radius (r/R)
      tLE_tmax, tTE_tmax : ratio of LE/TE thickness with respect to maximum thickness, default = 0
      Use_Original       : use the original distributions of K(r)=c(r)/D*Z/EAR 
                            default =  1 : use the original distribution (different for propellers with Z=4 and Z=3)
                                    =  0 : use a modified distribution that produces the values of EAR very close to the expected
                                    = -1 : use a modified distribution resulting directly from Wageningen Drawings
      Use_Smooth         : construct bivariate smoothing splines for the data used for thickness and pressure side calculations
                            default = False 
      s                  : smoothing factor, active for the procedure related to Use_Smooth 
                            default = 0 : interpolate 
                                  s > 0 : smooth, the larger the s the larger the smoothing
      Smooth_LE          : enable the LE smoothing procedure 
                            default = False
      x0s,x0p            : smoothing lengths suction and pressure side, the smoothing is mostly active for 
                            x<x0s for the suction  side and
                            x<x0p for the pressure side
                            default = 0.1
      ks, kp             : shape parameter 0<k<1 of the Weibull distribution used for smoothing. For k near zero the smoothing is 
                           close to a smoothed heaviside step function. k=1 closer to a ramp function (actually an exponential).
                           Note: the smoothing affects the suction/pressure side of whole foil.  
      """
    return BseriesFoil(Z,EAR,rR,tLE_tmax,tTE_tmax,Use_Original,Use_Smooth,s,Smooth_LE,x0s,x0p,ks,kp) 
    
class BseriesFoil(foil):
    
    # Splines Check
    # The code sets the following variable to True when the splines for a given propeller are constructed
    __splines_constructed=False
    
    # Hub Radius 
    __rR_Hub=0.167
    
    ####################### K(r) : function used for chord distribution
    #### Use_Original = 1
    #### NOTE : these values will be used if Use_Original is 1
    # (Original) Values of distributions are provided at r/R=
    __rR=nparr([0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1])
    
    # K(r) (4 blades +)  > Original Data from Oosterveld 1975 = Data from Kuiper 1992 
    __Kr_4=nparr([1.662, 1.882, 2.05, 2.152, 2.187, 2.144, 1.970, 1.582, 0.68]) 
    
    # K(r) (3 blades) > Data from Oosterveld 1975
    __Kr_3=nparr([1.633, 1.832, 2.0, 2.12, 2.186, 2.168, 2.127, 1.657, 0]) 
    
    #### Use_Original = 0
    #### NOTE : these values will be used if Use_Original is 0
    # K(r) > if used for all cases these values generate the exact EAR when interpolated 
    #        the dataset commes from Kr_3 with a modified rR=0.6 value to match EAR                            
    __Kr0=nparr([1.633, 1.832, 2.0, 2.12, 2.176, 2.168, 2.127, 1.657, 0]) 
    
    
    #### Use_Original = -1
    #### NOTE : these values will be used if Use_Original is -1
    # Values of distributions are provided at r/R=
    __rR2=nparr([0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95, 1])
    
    ## K(r) > obtained by mean values from drawings of B4-100/B5-105/B4-55/B5-75
    #__Kr_dr=nparr([ 1.630860093322964e+00,
    #                1.834640509520060e+00,
    #                2.004486224599534e+00,
    #                2.120805579441116e+00,
    #                2.176620735204807e+00,
    #                2.127005486463469e+00,
    #                1.950603483933783e+00,
    #                1.586311948351957e+00,
    #                1.194496769953584e+00,
    #                0])
    # error ~  -1.581670669767310e-02
    __Kr=nparr([1.633, 1.832, 2.0, 2.12, 2.186, 2.199, 2.127, 1.657, 0]) 
    #######################  END OF K(r)
        
    ####################### xtmax(r) : Function used for the Location of maximum thickness
    # x_tmax=X_tmax/c (4 blades +) > Data from Kuiper 1992
    __xtmax_Kuiper=nparr([0.35, 0.35, 0.351, 0.355, 0.389, 0.443, 0.486, 0.5, 0.5])
    
    # x_tmax=X_tmax/c (4 blades +) > Data from Oosterveld 1975
    __xtmax_Oosterveld4=nparr([0.35, 0.35, 0.351, 0.355, 0.389, 0.443, 0.479, 0.5, 0.])
    
    # x_tmax=X_tmax/c (3 blades) 
    __xtmax_Oosterveld3=nparr([0.35, 0.35, 0.351, 0.355, 0.389, 0.442, 0.478, 0.5, 0.])
    
    # Note : Differences for 3, and 4+ blades do not seem significant
    # Kuiper values will be used. The 0.5 for r/R=1 indicates that the decreament of Xtmax=xtmax*c
    # will follow the decreament of the chord and shall not decrease independently
    
    # x_tmax=X_tmax/c (4 blades +) > Data from Kuiper 1992
    __xtmax_mod=nparr([0.35, 0.35, 0.35, 0.355, 0.389, 0.443, 0.486, 0.5, 0.5])
    __xtmax=__xtmax_mod
    
    ## xtmax > obtained by mean values from drawings of B4-100/B5-105/B4-55/B5-75
    #__xtmax_dr=nparr([3.472068514029757e-01,
    #                  3.465972752014425e-01,
    #                  3.473695167447711e-01,
    #                  3.521592139805451e-01,
    #                  3.912068836783953e-01,
    #                  4.426962965048316e-01,
    #                  4.725832276101920e-01,
    #                  5.270663671102803e-01,
    #                  5.869021976445969e-01,
    #                  0])
    #
    # These values suggest that a linear increase is present for xtmax for r/R>0.7
    # The values for r/R<0.4 are almost constant and if we take into account the error
    # from the capturing procedure we can say that are equal to 0.35 as suggested.
    # In order to perform a better smoothing the values that we shall use a sligtly
    # smaller value for r/R=0.4 : 0.35 instead of 0.351 and enforce a zero first order
    # derivative there. 
    ####################### END OF xtmax(r) 
    
    
    ####################### A(r), B(r) : Functions used to define maximum thickness 
    __A=nparr([0.0526, 0.0464, 0.0402, 0.0340, 0.0278, 0.0216, 0.0154, 0.0092, 0.003])
    __B=nparr([0.0040, 0.0035, 0.0030, 0.0025, 0.0020, 0.0015, 0.0010, 0.0005, 0.000])
    ####################### END OF xtmax(r) 
   
    ####################### V1 and V2 : functions used to define pressure side and thickness 
    # Percentages (NOT in %) of Maximum thickness for a given r/R and given position from maximum thickness 
    # Note : Lines   denote radius :                                                          :                 r/R = 0.15, 0.20, 0.25, 0.3, 0.4, 0.5, 0.6, 0.7 
    #        Columns denote percentage of distance from location of maximum thickness, x_tmax :   For the j-th column we have the following
    #<------------                     X/c=(1+a(j))*x_tmax/c     --------------------------------->  X/c=x_tmax <-------------------------      X/c=(1-a(j))*x_tmax/c+a  ------------------------------->
    # LE                                                                                                                                                                                         TE
    #with:j=1    2       3    ....
    #a(j)=-1    -0.95     -0.9    -0.85       -0.8      -0.7       -0.6      -0.5     - 0.4      -0.2      0        0.2     0.4        0.5      0.6       0.7       0.8        0.9       0.95      1       
    __V1=nparr([ 
    [ 0.3860 ,  0.3150 , 0.2642 , 0.2230  ,  0.1870 ,   0.1320 ,   0.0920 ,  0.0615 ,  0.0384 ,  0.0096 ,  0 ,   0.0365 ,  0.0955 ,  0.1280 ,   0.1610 ,  0.1950 ,  0.2300 ,  0.2650 ,  0.2824 , 0.3000],
    [ 0.3560 ,  0.2821 , 0.2353 , 0.2000  ,  0.1685 ,   0.1180 ,   0.0804 ,  0.0520 ,  0.0304 ,  0.0049 ,  0 ,   0.0172 ,  0.0592 ,  0.0880 ,   0.1207 ,  0.1570 ,  0.1967 ,  0.2400 ,  0.2630 , 0.2826], 
    [ 0.3256 ,  0.2513 , 0.2068 , 0.1747  ,  0.1465 ,   0.1008 ,   0.0669 ,  0.0417 ,  0.0224 ,  0.0031 ,  0 ,   0.0084 ,  0.0350 ,  0.0579 ,   0.0899 ,  0.1246 ,  0.1651 ,  0.2115 ,  0.2372 , 0.2598],
    [ 0.2923 ,  0.2186 , 0.1760 , 0.1445  ,  0.1191 ,   0.0790 ,   0.0503 ,  0.0300 ,  0.0148 ,  0.0027 ,  0 ,   0.0033 ,  0.0202 ,  0.0376 ,   0.0623 ,  0.0943 ,  0.1333 ,  0.1790 ,  0.2040 , 0.2306],
    [ 0.2181 ,  0.1467 , 0.1088 , 0.0833  ,  0.0637 ,   0.0357 ,   0.0189 ,  0.0090 ,  0.0033 ,  0      ,  0 ,   0      ,  0.0044 ,  0.0116 ,   0.0214 ,  0.0395 ,  0.0630 ,  0.0972 ,  0.1200 , 0.1467],
    [ 0.1278 ,  0.0778 , 0.0500 , 0.0328  ,  0.0211 ,   0.0085 ,   0.0034 ,  0.0008 ,  0      ,  0      ,  0 ,   0      ,  0      ,  0.0012 ,   0.0040 ,  0.0100 ,  0.0190 ,  0.0330 ,  0.0420 , 0.0522], 
    [ 0.0382 ,  0.0169 , 0.0067 , 0.0022  ,  0.0006 ,   0      ,   0      ,  0      ,  0      ,  0      ,  0 ,   0      ,  0      ,  0      ,   0      ,  0      ,  0      ,  0      ,  0      , 0     ], 
    [ 0      ,  0      , 0      , 0       ,  0      ,   0      ,   0      ,  0      ,  0      ,  0      ,  0 ,   0      ,  0      ,  0      ,   0      ,  0      ,  0      ,  0      ,  0      , 0     ],
    [ 0      ,  0      , 0      , 0       ,  0      ,   0      ,   0      ,  0      ,  0      ,  0      ,  0 ,   0      ,  0      ,  0      ,   0      ,  0      ,  0      ,  0      ,  0      , 0     ],
    [ 0      ,  0      , 0      , 0       ,  0      ,   0      ,   0      ,  0      ,  0      ,  0      ,  0 ,   0      ,  0      ,  0      ,   0      ,  0      ,  0      ,  0      ,  0      , 0     ], 
    [ 0      ,  0      , 0      , 0       ,  0      ,   0      ,   0      ,  0      ,  0      ,  0      ,  0 ,   0      ,  0      ,  0      ,   0      ,  0      ,  0      ,  0      ,  0      , 0     ],
    [ 0      ,  0      , 0      , 0       ,  0      ,   0      ,   0      ,  0      ,  0      ,  0      ,  0 ,   0      ,  0      ,  0      ,   0      ,  0      ,  0      ,  0      ,  0      , 0     ] ])
    
    __rR_V=nparr([0.15, 0.20, 0.25, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.85, 0.9, 1])
    __a =nparr([-1  ,-0.95, -0.9, -0.85, -0.8, -0.7, -0.6, -0.5, -0.4, -0.2,  0 , 0.2, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95, 1 ])  
     
    # Data for Thickness : 
    # Note : Lines   denote radius :                                                          :                 r/R = 0.15, 0.20, 0.25, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.85, 0.9, 1
    #        Columns denote percentage of distance from location of maximum thickness, x_tmax :   For the j-th column we have the following
    #<------------                     X/c=(1+a(j))*x_tmax/c     --------------------------------->  X/c=x_tmax <-------------------------      X/c=(1-a(j))*x_tmax/c+a  ------------------------------->
    # LE                                                                                                                                                                                                TE
    #with:j=1    2       3    ....
    #a(j)=-1   - 0.9     -0.95       -0.85      -0.8       -0.7      -0.6         -0.5      -0.4       -0.2     0      0.2     0.4        0.5        0.6       0.7       0.8         0.9        0.95      1   
    # NOTE : Modified Values for the following a,rR
    #         rR= 0.15 : a =-0.9; a=0.9; a=0.95
    #         rR=  0.2 :                 a=0.95
    #         a = -0.4 : rR=0.3
    #         
    __V2=nparr([
    [ 0   ,   0.1380    , 0.2600  ,  0.3665  ,  0.4520  ,  0.5995  , 0.7105  ,   0.8055  ,  0.8825  ,  0.9749 ,  1 ,  0.9360 ,  0.7805  ,  0.6770   , 0.5585  , 0.4280  , 0.2870   ,  0.1432  ,  0.0700 ,  0 ],  
    [ 0   ,   0.1560    , 0.2840  ,  0.3905  ,  0.4777  ,  0.6190  , 0.7277  ,   0.8170  ,  0.8875  ,  0.9750 ,  1 ,  0.9446 ,  0.7984  ,  0.6995   , 0.5842  , 0.4535  , 0.3060   ,  0.1455  ,  0.0700 ,  0 ],   
    [ 0   ,   0.1758    , 0.3042  ,  0.4108  ,  0.4982  ,  0.6359  , 0.7415  ,   0.8259  ,  0.8899  ,  0.9751 ,  1 ,  0.9519 ,  0.8139  ,  0.7184   , 0.6050  , 0.4740  , 0.3228   ,  0.1567  ,  0.0725 ,  0 ],   
    [ 0   ,   0.1890    , 0.3197  ,  0.4265  ,  0.5130  ,  0.6505  , 0.7520  ,   0.8315  ,  0.8923  ,  0.9750 ,  1 ,  0.9583 ,  0.8265  ,  0.7335   , 0.6195  , 0.4885  , 0.3360   ,  0.1670  ,  0.0800 ,  0 ],   
    [ 0   ,   0.1935    , 0.3235  ,  0.4335  ,  0.5220  ,  0.6590  , 0.7593  ,   0.8345  ,  0.8933  ,  0.9725 ,  1 ,  0.9645 ,  0.8415  ,  0.7525   , 0.6353  , 0.5040  , 0.3500   ,  0.1810  ,  0.0905 ,  0 ],   
    [ 0   ,   0.1750    , 0.3056  ,  0.4135  ,  0.5039  ,  0.6430  , 0.7478  ,   0.8275  ,  0.8880  ,  0.9710 ,  1 ,  0.9639 ,  0.8456  ,  0.7580   , 0.6439  , 0.5140  , 0.3569   ,  0.1865  ,  0.0950 ,  0 ],   
    [ 0   ,   0.1485    , 0.2720  ,  0.3775  ,  0.4620  ,  0.6060  , 0.7200  ,   0.8090  ,  0.8790  ,  0.9690 ,  1 ,  0.9613 ,  0.8426  ,  0.7530   , 0.6415  , 0.5110  , 0.3585   ,  0.1885  ,  0.0965 ,  0 ],   
    [ 0   ,   0.1240    , 0.2337  ,  0.3300  ,  0.4140  ,  0.5615  , 0.6840  ,   0.7850  ,  0.8660  ,  0.9675 ,  1 ,  0.96   ,  0.84    ,  0.75     , 0.64    , 0.51    , 0.36     ,  0.19    ,  0.0975 ,  0 ],   
    [ 0   ,   0.1050    , 0.2028  ,  0.2925  ,  0.3765  ,  0.5265  , 0.6545  ,   0.7635  ,  0.8520  ,  0.9635 ,  1 ,  0.96   ,  0.84    ,  0.75     , 0.64    , 0.51    , 0.36     ,  0.19    ,  0.0975 ,  0 ],   
    [ 0   ,   0.1000    , 0.1950  ,  0.2830  ,  0.3660  ,  0.5160  , 0.6455  ,   0.7550  ,  0.8450  ,  0.9615 ,  1 ,  0.96   ,  0.84    ,  0.75     , 0.64    , 0.51    , 0.36     ,  0.19    ,  0.0975 ,  0 ],   
    [ 0   ,   0.0975    , 0.1900  ,  0.2775  ,  0.3600  ,  0.51    , 0.6400  ,   0.75    ,  0.8400  ,  0.9600 ,  1 ,  0.96   ,  0.84    ,  0.75     , 0.64    , 0.51    , 0.36     ,  0.19    ,  0.0975 ,  0 ],
    [ 0   ,   0.0975    , 0.1900  ,  0.2775  ,  0.3600  ,  0.51    , 0.6400  ,   0.75    ,  0.8400  ,  0.9600 ,  1 ,  0.96   ,  0.84    ,  0.75     , 0.64    , 0.51    , 0.36     ,  0.19    ,  0.0975 ,  0                                                                                                                                                                                                               ]])  
    
    
    # Initialiser
    def __init__(self,Z,EAR,rR,tLE_tmax=0.2,tTE_tmax=0,Use_Original=1,Use_Smooth=0,s=0,Smooth_LE=0,x0s=0.1,x0p=0.1,ks=0.8,kp=0.8):
        """ Initialiser : Parameters, and closed LEADING edge specifier """
        # NOTE : Here TE_Closed refers to the LEADING EDGE
        self.EAR=EAR
        self.Z=Z
        self.rR=rR
        self.Use_Original=Use_Original
        self.tLE_tmax=tLE_tmax
        if (tTE_tmax>0):
            self.closed(TE_closed=0)
        else:
            self.closed(TE_closed=1)
        self.tTE_tmax=tTE_tmax
        self.Use_Smooth=Use_Smooth
        # note if Use_Smooth is false then s has no effect
        self.s=s
        self.Smooth_LE=Smooth_LE
        self.construct_splines()
        if (self.Use_Smooth):
            self.construct_pres_suct_rR_representation() 
        else:
            self.construct_pres_suct_rR_representation2() 
            # setup smoothing parameters
            self.smooth_at_LE_WeibParams(x0s,ks,x0p,kp)
    
    # Construct the required splines for c(r)/D, tmax/D, Xtmax/D ...
    def construct_splines(self):
        from scipy import interpolate
        from numpy import zeros_like, ones_like, meshgrid, delete
        if (self.__splines_constructed):
            pass
        self.construct_cRspl()
        self.construct_xtmaxspl()
        self.construct_tmaxRspl()
        # note : the subroutine below only prepares data for visualisation using the plot_V2 function
        #        as long as Use_Smooth is false
        self.construct_pres_suct_smoothing()
        if (not self.Use_Smooth):
            self.construct_pres_suct_smoothing2()
        self.__splines_constructed=True
        
        
    def construct_cRspl(self):
        from scipy import interpolate
        # Construction of chord/R spline
        if (self.Use_Original==1):
            if (self.Z<=3):
                self.cR = interpolate.UnivariateSpline(self.__rR,self.__Kr_3*2*self.EAR/self.Z,k=5,s=0)
            else:
                self.cR = interpolate.UnivariateSpline(self.__rR,self.__Kr_4*2*self.EAR/self.Z,k=5,s=0)
        elif (self.Use_Original==-1):
                self.cR = interpolate.UnivariateSpline(self.__rR2,self.__Kr_dr*2*self.EAR/self.Z,k=5,s=0)
        else:
            self.cR = interpolate.UnivariateSpline(self.__rR,self.__Kr*2*self.EAR/self.Z,k=5,s=0)
    
    def construct_xtmaxspl(self):
        from scipy import interpolate
        # Construction of xtmax=Xtmax/c spline
        self.xtmaxSp=interpolate.make_interp_spline(self.__rR[2:len(self.__rR)-1],self.__xtmax[2:len(self.__rR)-1],bc_type=([(1,0)],[(1,0)]))

    def construct_tmaxRspl(self):
        from scipy import interpolate
        # Construction of tmax/R spline
        self.tmaxR=interpolate.UnivariateSpline(self.__rR,(self.__A*self.Z-self.__B)/2,k=5,s=0)

    # Note : Bad subroutine name 
    # The subroutine construct_pres_suct_smoothing prepares the Wageningen Data given as t/tmax and yp/tmax 
    # to obtain the same ! data but as t/c and yp/c. It is clear that t/c=t/tmax * tmax/c
    #                                                                yp/c=yp/tmax * tmax/c
    # 
    def construct_pres_suct_smoothing(self):
        from scipy import interpolate
        from numpy import zeros_like, ones_like, meshgrid, delete
        # Contruction of V2 spline
        #self.V2=interpolate.SmoothBivariateSpline(tile(self.__a.,len(self.__rR_V)),tile(self.__rR_V,len(self.__a)),self.__V2,s=0)
        #a,r=meshgrid(self.a2x(self.__a),self.__rR_V)
        #self.__X=self.a2x(self.__a,self.__rR_V)
        # Physical Internal Locations (X/c) where V2 and V1 data are defined
        a,r=meshgrid(self.__a,self.__rR_V)
        self.__Xc=self.a2x(a,r)
        self.__r=r.copy()
        #print(self.__Xc)
        # Physical Internal thickness (yt/c), pressure side and suction side
        # Prepare data
        self.__ytc=zeros_like(self.__V2)
        self.__ytc[:,0:11] =self.__V2[:,0:11]*(1-self.tLE_tmax)+self.tLE_tmax
        self.__ytc[:,11:20]=self.__V2[:,11:20]*(1-self.tTE_tmax)+self.tTE_tmax
        self.__ypc=ones_like(self.__V1)
        self.__ypc[:,0:11]  =self.__V1[:,0:11]*(1-self.tLE_tmax)  
        self.__ypc[:,11:20]=self.__V1[:,11:20]*(1-self.tTE_tmax)
        # Finalise data
        for i in range(len(self.__rR_V)):
            self.__ytc[i,:]*=self.tmaxR(self.__rR_V[i])/self.cR(self.__rR_V[i])
            self.__ypc[i,:]*=self.tmaxR(self.__rR_V[i])/self.cR(self.__rR_V[i])
        self.__ysc=self.__ytc+self.__ypc
        if (self.Use_Smooth):
            # Prepare Actual Pressure and Suction Sides with round LE
            self.__yscu=self.__ysc.copy()
            self.__yscu[:,0]=(self.__ysc[:,0]+self.__ypc[:,0])*0.5
            #print(self.__yscu[:,1])
            #print(self.__yscu.ravel())
            #self.yscSp=interpolate.SmoothBivariateSpline(delete(self.__Xc,[1],1).ravel(),delete(r,[1],1).ravel(),delete(self.__yscu,[1],1).ravel(),kx=5,ky=3,s=1e-2)
            self.yscSp=interpolate.SmoothBivariateSpline(self.__Xc.ravel(),r.ravel(),self.__ysc.ravel(),kx=3,ky=3,s=self.s)
            #self.yscSp=interpolate.SmoothBivariateSpline(a.ravel(),r.ravel(),self.__yscu.ravel(),kx=5,ky=3,s=0)
            self.__ypcu=self.__ypc.copy()
            #self.__ypcu=delete(self.__ypc,[1,2],1)
            self.__ypcu[:,0]=(self.__ysc[:,0]+self.__ypc[:,0])*0.5
            #print(self.__ypcu[:,1])
            #print(self.__yscu.ravel())
            #self.ypcSp=interpolate.SmoothBivariateSpline(delete(self.__Xc,[1],1).ravel(),delete(r,[1],1).ravel(),delete(self.__ypcu,[1],1).ravel(),kx=5,ky=3,s=1e-2)
            self.ypcSp=interpolate.SmoothBivariateSpline(self.__Xc.ravel(),r.ravel(),self.__ypc.ravel(),kx=3,ky=3,s=self.s)
    
        
    def construct_pres_suct_rR_representation(self):
        from scipy import interpolate
        from numpy import linspace, exp, sqrt, where
        # For the specified radius construct the representation of the foil that will be
        # used to obtain points
        # For rR : evaluate yp yc for npoints points
        npoints=100
        x=linspace(0,1,npoints)
        x=x.reshape(-1,1)
        yp=self.ypcSp(x,self.rR)
        #ys=self.yscSp(x,self.rR)
        m=(self.yscSp(0,self.rR)+self.ypcSp(0,self.rR))*0.5
        asuc=(m-self.yscSp(0.2,self.rR))/sqrt(0.2)
        yp[0]=m
        ys=where(x<=0.2,m-asuc*sqrt(x),self.yscSp(x,self.rR))
        ys[npoints-1]=yp[npoints-1]
        # create a nice interpolating spline 
        self.ypsp=interpolate.UnivariateSpline(x,yp,k=5,s=0)
        self.yssp=interpolate.UnivariateSpline(x,ys,k=5,s=0)
    
    def construct_pres_suct_smoothing2(self):
        from scipy import interpolate
        # Specify how we interpolate the values of the tables V1 and V2 : here simple linear interpolations
        self.V1int=interpolate.interp2d(self.__a,self.__rR_V,self.__V1, kind='linear')
        self.V2int=interpolate.interp2d(self.__a,self.__rR_V,self.__V2, kind='linear')
    
    def construct_pres_suct_rR_representation2(self):
        from numpy import where
        from scipy import interpolate
        # Get values V values for thickness and yp for the given rR
        V1=self.V1int(self.__a,self.rR)
        V2=self.V2int(self.__a,self.rR)
        # Get values of x/c that correspond to these a and the given rR
        x=self.a2x(self.__a,self.rR)
        # Construct the values of pressure side and thickness
        yp=where(self.__a<0,V1*(1-self.tLE_tmax),V1*(1-self.tTE_tmax))
        yt=where(self.__a<0,V2*(1-self.tLE_tmax)+self.tLE_tmax,V2*(1-self.tTE_tmax)+self.tTE_tmax)
        # The above values of yp and yt are actually yp/tmax and yt/tmax, transform them to yp/c, yt/c. 
        # The obtained values (given below) are transformed the values that correspond to yp/c, yt/c  
        yp*=self.tmaxR(self.rR)/self.cR(self.rR)
        yt*=self.tmaxR(self.rR)/self.cR(self.rR)
        # find values for suction
        ys=yp+yt
        # find values for the camber (mean) line
        yc=yp+yt*0.5
        # create interpolating splines(or not, if s is eventually different than wero) 
        # for pressure and suction side :
        self.ypsp=interpolate.UnivariateSpline(x,yp,k=5,s=0)
        self.yssp=interpolate.UnivariateSpline(x,ys,k=5,s=0)
        # create interpolating splines(or not, if s is eventually different than wero) 
        # for the (half)thickness and the camber (mean) line
        self.ytsp=interpolate.UnivariateSpline(x,yt*0.5,k=5,s=0)
        self.ycsp=interpolate.UnivariateSpline(x,yc,k=5,s=0)
        
        
        
    def smooth_at_LE_WeibParams(self,x0_s,k_s,x0_p,k_p):
        from numpy import log
        # Create a smooth transition at LE
        # x0_p and x0_p are the smoothing lengths 
        # k_s  and k_p  are the transition parameter for the smoothing
        # The closest these values are to one the smoother the transition  
        if (not self.Smooth_LE):
            pass
        # Mollifier for the pressure side 
        self.l_p=x0_p/(-log(0.05))**(1./k_p)
        self.k_p=k_p
        self.l_s=x0_s/(-log(0.05))**(1./k_s)
        self.k_s=k_s
        
    def Weibulp(self,x):
        from numpy import exp
        v=1-exp(-(x/self.l_p)**self.k_p)
        return v
    
    def Weibuls(self,x):
        from numpy import exp
        v=1-exp(-(x/self.l_s)**self.k_s)
        return v
    
    # Name
    def name(self):
        """ Get the foils name """
        n="B"+"{:d}".format(self.Z)+"_"+"{:.0f}".format(self.EAR*100)+"_rR="+"{:.2f}".format(self.rR)
        return n    
    
    # Location of maximum thickness for the requested radius
    # Value of xtmax
    def xtmax(self,rR):
        """ Location of maximum thickness for the requested radius """
        from numpy import where
        lnrR=len(self.__rR)-1
        v=where(rR<self.__rR[2],self.__xtmax[2],where(rR>self.__rR[lnrR-1],self.__xtmax[lnrR-1], self.xtmaxSp(rR)))
        return v
    

    def x2a(self,x,rR):
        from numpy import where
        """ Transform function : from local variable x/c to a """
        xt=self.xtmax(rR)
        a=where(x<=xt,x/xt-1.,(x-xt)/(1-xt))
        return a
    
    def a2x(self,a,rR):
        from numpy import where
        """ Transform function : from local variable x/c to a """
        x=where(a<0,(1+a)*self.xtmax(rR), (1-a)*self.xtmax(rR)+a)
        return x 
    
    # A completer
    def yt(self,x):
        """ Thickness for the requested radius """
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
        from numpy import where
        #y=where(x<=1e-4,(self.ypsp(x)+self.yssp(x))*0.5,self.ypsp(x))
        if (self.Smooth_LE):
            y=self.ycsp(x)-self.ytsp(x)*self.Weibulp(x)
        else:
            y=self.ypsp(x)
        return y
    
    # A completer
    def Ys(self,x):
        """ Suction side (Y above coordinate)"""
        from numpy import where
        #y=where(x<=1e-4,self.ypcSp(x,self.rR),where(x>=1-1e-4,self.ypcSp(x,self.rR),self.yscSp(x,self.rR)))
        #y=where(x<=1e-4,(self.ypsp(x)+self.yssp(x))*0.5,self.yssp(x))
        if (self.Smooth_LE):
            y=self.ycsp(x)+self.ytsp(x)*self.Weibuls(x)
        else:
            y=self.yssp(x)
        return y
    
    def vecS_TE(self):
        """ Tangent at TE at pressure and suction (orientation from pressure to suction - towards LE and back to TE towards wake) """
        from numpy import sqrt
        derS=self.yssp.derivatives(1)
        derP=self.ypsp.derivatives(1)
        vec_SuctSide_TEtoWkx=  1/(sqrt(1+derS[1]**2)) # above TE
        vec_SuctSide_TEtoWky=  derS[1]/(sqrt(1+derS[1]**2)) # above TE
        vec_PresSide_TEtoLEx=  -1/(sqrt(1+derP[1]**2)) # below TE
        vec_PresSide_TEtoLEy=  -derP[1]/(sqrt(1+derP[1]**2)) # below TE
        return [vec_PresSide_TEtoLEx, vec_PresSide_TEtoLEy, vec_SuctSide_TEtoWkx, vec_SuctSide_TEtoWky]

    def vecS_LE(self):
        from numpy import sqrt
        if (not self.Smooth_LE):
            derS=self.yssp.derivatives(0)
            derP=self.ypsp.derivatives(0)
            vec_SuctSide_TEtoWkx=  1/(sqrt(1+derS[1]**2)) # above TE
            vec_SuctSide_TEtoWky=  derS[1]/(sqrt(1+derS[1]**2)) # above TE
            vec_PresSide_TEtoLEx=  -1/(sqrt(1+derP[1]**2)) # below TE
            vec_PresSide_TEtoLEy=  -derP[1]/(sqrt(1+derP[1]**2)) # below TE
        else:
            vec_SuctSide_TEtoWkx=  0 # above TE
            vec_SuctSide_TEtoWky=  1 # above TE
            vec_PresSide_TEtoLEx=  0 # below TE
            vec_PresSide_TEtoLEy=  1 # below TE
        return [vec_PresSide_TEtoLEx, vec_PresSide_TEtoLEy, vec_SuctSide_TEtoWkx, vec_SuctSide_TEtoWky]
        
    
    def plot_cR(self,npoints=100):
        """ Returns a plt handle for the c/R=chord/R distribution """
        import matplotlib.pyplot as plt
        from numpy import linspace, pi, cos
        x=linspace(self.__rR_Hub,1,npoints)
        plt.plot(x,self.cR(x),'r',label='Spline Interpolation')
        if (self.Use_Original==1):
            if (self.Z <=3):
                plt.plot(self.__rR,2*self.__Kr_3*self.EAR/self.Z ,'bo',label='B Series Data')
            else:
                plt.plot(self.__rR,2*self.__Kr_4*self.EAR/self.Z ,'bo',label='B Series Data')
        elif (self.Use_Original==-1):
                plt.plot(self.__rR2,2*self.__Kr_dr*self.EAR/self.Z ,'bo',label='B Series Data')
        else:
            plt.plot(self.__rR,2*self.__Kr*self.EAR/self.Z ,'bo',label='B Series Data')
        plt.plot(x[0],self.cR(x[0]),'go',label='Hub Radius')
        plt.xlabel('r/R')
        plt.ylabel('c/R')
        plt.legend()
        EAR_app=self.Z*self.cR.integral(self.__rR[0],1)/pi/cos(15*pi/180)
        EAR_err=abs(self.EAR-EAR_app)/self.EAR
        plt.text(0.54, self.cR(x[2])/3, r'Relative Error(EAR)='+"{:.4f}".format(EAR_err*100)+"%")
        print('EAR Err=',EAR_err)
        print('EAR_App=',EAR_app)
        plt.grid(1)
        return plt
    
    def plot_xtmax(self,npoints=100):
        """ Returns a plt handle for the xtmax=Xtmax/c distribution """
        import matplotlib.pyplot as plt
        from numpy import linspace
        x=linspace(self.__rR_Hub,1,npoints)
        plt.plot(x,self.xtmax(x),'r',label='Spline Interpolation')
        plt.plot(self.__rR,self.__xtmax,'bo',label='B Series Data')
        plt.plot(x[0],self.xtmax(x[0]),'go',label='Hub Radius')
        plt.xlabel('r/R')
        plt.ylabel('Xtmax/c')
        plt.legend()
        plt.grid(1)
        return plt

    def plot_tmax(self,npoints=100):
        """ Returns a plt handle for the tmax/c distribution """
        import matplotlib.pyplot as plt
        from numpy import linspace
        x=linspace(self.__rR_Hub,1,npoints)
        plt.plot(x,self.tmaxR(x)/self.cR(x),'r',label='Spline Interpolation')
        plt.plot(self.__rR,(self.__A*self.Z-self.__B)/2/(2*self.__Kr_4*self.EAR/self.Z),'bo',label='B Series Data')
        plt.plot(x[0],self.tmaxR(x[0])/self.cR(x[0]),'go',label='Hub Radius')
        plt.xlabel('r/R')
        plt.ylabel('tmax/c')
        plt.legend()
        plt.grid(1)
        return plt

    def plot_V2(self,npoints=10,mpoints=10):
        """ Returns a plt handle to visualise the V2 distribution (thickness) at physical space """
        import matplotlib.pyplot as plt
        from mpl_toolkits.mplot3d import Axes3D
        from numpy import linspace, meshgrid
        x=linspace(0,1,npoints)
        #a=linspace(-1,1,npoints)
        #a=linspace(0,1,npoints)
        r=linspace(0.15,1,mpoints)
        X,R=meshgrid(x,r)
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_wireframe(self.__Xc,self.__r,self.__ypc,color='k')
        ax.plot_wireframe(self.__Xc,self.__r,self.__ysc,color='k')
        #print(self.yscSp(x,r))
        #X=self.a2x(A,R)
        if (self.Use_Smooth):
            ax.plot_surface(X,R,self.yscSp(x,r).T,color='r')
            ax.plot_surface(X,R,self.ypcSp(x,r).T,color='b')
        #ax.plot_surface(x,r,self.V2(a,r))
        ax.set_zlim(0, 0.3)
        return plt

    # Visual Verifier of parameters
    def show_parameters(self):
        print("WAGENINGEN : ")
        print("EAR=",self.EAR)
        print("Z=",self.Z)
        print("rR=",self.rR)
        if (self.TE_closed):
            print("Closed Leading Edge")
        else:
            print("Open Leading Edge")

