### PART OF FOIL LIBRARY
# Python 2.7 Version 
# (note: files without the above specifier are actually
#        the same as those of the Python 3 version)
# 
# Author: Konstantinos POLITIS
# 
#   Defines the abstract class of a Foil 
#   
#   Any "Foil" generates a set of points in some manner that is 
#   not specified here. 
#   
#   A specific implementation of a foil is the NACA foil (see NACA_LIB)
#   
#  To do list : 
#    - Add other family of foils :
#                 1. Foils read from file 
#                 
#    - Provide extensions for complicated 3D foil geometries (more FreeCAD interaction) 
#    - Initially the subroutine that generate points for FreeCAD used 20 points. Some ugly
#      splines (with cusps) were generated by FreeCAD so I modified it to 30. Check other
#      options foir generating splines. 
#    
###
####Features of 3.7 that do not work with Python 2.7 : 
# 1. from abc import ABC, abstractmethod : requires six
import abc


class afoil(abc.ABC):
    
    @abc.abstractmethod
    def Xs(self,x):
        """ Suction side (X/c above coordinate)"""
        pass
    
    @abc.abstractmethod
    def Ys(self,x):
        """ Suction side (Y/c above coordinate)"""
        pass
    
    @abc.abstractmethod
    def Zs(self,x):
        """ Suction side (Z/c above coordinate)"""
        pass
    
    @abc.abstractmethod
    def Xp(self,x):
        """ Pressure side (X/c below coordinate)"""
        pass
    
    @abc.abstractmethod
    def Yp(self,x):
        """ Pressure side (Y/c below coordinate)"""
        pass
    
    @abc.abstractmethod
    def Zp(self,x):
        """ Pressure side (Z/c below coordinate)"""
        pass
    
    @abc.abstractmethod
    def vecS_TE(self):
        """ Tangent at TE at pressure and suction (orientation from pressure to suction - towards LE and back to TE towards wake) """
        # NOTE : Should return the two vectors in the following list format
        #                     [v_PressureSide_from TE_to_LE  _x , v_PressureSide_from TE_to_LE  _y 
        #                      v_SuctionSide _from LE_to_wake_x , v_SuctionSide _from LE_to_wake_y]
        pass
    
    @abc.abstractmethod
    def vecS_LE(self):
        """ Tangent at LE (orientation from pressure to suction) """
        # NOTE : Should return the two vectors in the following list format
        #                     [v_PressureSide_from TE_to_LE_x , v_PressureSide_from TE_to_LE_y 
        #                      v_SuctionSide _from LE_to_TE_x , v_SuctionSide _from LE_to_TE_y]
        pass
    
    @abc.abstractmethod
    def show_parameters(self):
        """ Print Foil Parameters """
        pass
    
    @abc.abstractmethod
    def name(self):
        """ Get the foils name """
        pass
        
    def closed(self,TE_closed=True,LE_closed=True):
        """ Set Closed Parameter for the foil """
        self.TE_closed=TE_closed
        self.LE_closed=LE_closed
    
    def isclosed(self):
        """ Checks if the foil was defined as closed """
        return (self.TE_closed and self.LE_closed)
    
    def printclosed(self):
        if ( self.isclosed() ): 
            print ("Closed Foil")
        else:   
            print ("Open Foil : ")
            if (self.LE_closed):
                print("Closed Leading Edge")
            else:
                print("Open Leading Edge")
            if (self.TE_closed):
                print("Closed Trailing Edge")
            else:
                print("Open Trailing Edge")
    
    def SuctionSide_FCAD(self,npoints=30,LE2TE=True,spacing='linear'):
        """ Generates lists of npoints (default=20) as X,Y coordinates to define FreeCAD base vectors for the suction side (oriented from LE to TE) """
        from numpy import linspace,cos,pi
        if (LE2TE):
            ts,te=0,1
        else:
            ts,te=1,0
        t=linspace(ts,te,npoints)
        if (spacing=='linear'):
            x=t
        elif (spacing=='cos'):
            x=1-cos(pi*t/2)
        if (LE2TE):
            params=x
        else:
            params=1-x
        return self.Xs(x), self.Ys(x), self.Zs(x), params
        
    
    def PressureSide_FCAD(self,npoints=30,LE2TE=False,spacing='linear'):
        """ Generates lists of npoints (default=20) as X,Y coordinates to define FreeCAD base vectors for the suction side (oriented from LE to TE) """
        from numpy import linspace,cos,pi
        if (LE2TE):
            ts,te=0,1
        else:
            ts,te=1,0
        t=linspace(ts,te,npoints)
        if (spacing=='linear'):
            x=t
        elif (spacing=='cos'):
            x=1-cos(pi*t/2)
        if (LE2TE):
            params=x
        else:
            params=1-x
        return self.Xp(x), self.Yp(x), self.Zp(x), params
    
        
    def plot_XY(self,show_vecS=True,npoints=20,spacing='linear'):
        """ Returns a plt handle for the XY coordinates """
        import matplotlib.pyplot as plt
        from numpy import linspace, cos, sqrt, pi
        t=linspace(0,1,npoints)
        if (spacing=='linear'):
            x=t
        elif (spacing=='cos'):
            x=1-cos(pi*t/2)
        elif (spacing=='sqrt'):
            x=1-sqrt(t)
        #plt.plot(self.Xs(x),self.Ys(x),'bo',markersize=1.5,label='Suction Side')
        #plt.plot(self.Xp(x),self.Yp(x),'ro',markersize=1.5,label='Pressure Side')
        plt.plot(self.Xs(x),self.Ys(x),'b-o',label='Suction Side')
        plt.plot(self.Xp(x),self.Yp(x),'r-o',label='Pressure Side')
        print("Distance from Suction to Pressure at LE = ",self.Ys(0)-self.Yp(0))
        print("Distance from Suction to Pressure at TE = ",self.Ys(1)-self.Yp(1))
        plt.xlabel('X/c')
        plt.ylabel('Y/c')
        plt.title("Foil "+self.name())
        plt.legend()
        plt.grid(1)
        plt.axis('equal')
        if (show_vecS):
            vTE=self.vecS_TE()
            vLE=self.vecS_LE()
            Xs=[self.Xp(1),self.Xp(0),self.Xs(0),self.Xs(1)]
        #   NOTE :          ^^^ Xp(0)=Xs(0)
            Ys=[self.Yp(1),self.Yp(0),self.Ys(0),self.Ys(1)]
        #   NOTE :          ^^^ Yp(0)=Ys(0) but Ys(1)=Yp(1) only if TE closed is true 
            Us=[vTE[0],vLE[0],vLE[2],vTE[2]]
            Vs=[vTE[1],vLE[1],vLE[3],vTE[3]]
            plt.quiver(Xs,Ys,Us,Vs,width=0.002)
        return plt
    
    def write4Xfoil(self,npoints=20,spacing='cos'):
        from numpy import linspace, concatenate, savetxt, stack, pi, cos, sqrt
        t=linspace(1,0,npoints)
        if (spacing=='linear'):
            x=t
        elif (spacing=='cos'):
            x=1-cos(pi*t/2)
        elif (spacing=='sqrt'):
            x=1-sqrt(t)
        Xp, Yp = self.Xp(x),self.Yp(x)
        t=linspace(0,1,npoints)
        if (spacing=='linear'):
            x=t
        elif (spacing=='cos'):
            x=1-cos(pi*t/2)
        elif (spacing=='sqrt'):
            x=1-sqrt(t)
        Xs, Ys = self.Xs(x),self.Ys(x)
        n=self.name()+"_n{:d}".format(npoints)+"_space"+spacing+".txt"
        X=concatenate((Xp,Xs),axis=None)
        Y=concatenate((Yp,Ys),axis=None)
        C=stack((X,Y),axis=-1)
        m="# Using npoints = {:d}".format(npoints)
        savetxt(n,C,fmt='%12.9f %12.9f ',header=self.name()+"\n"+m,comments='')