### PART OF FOIL LIBRARY
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
#                 2. Wageningen foils
#                 
#    - Provide extensions for complicated 3D foil geometries (more FreeCAD interaction) 
#    
####Features of 3.7 that do not work with Python 2.7 : 
# 1. from abc import ABC, abstractmethod : requires six
import abc, six

@six.add_metaclass(abc.ABCMeta)
class afoil():
    
    #Does not work with Python 2.7
    #@abstractmethod
    @abc.abstractmethod
    def Xs(self,x):
        """ Suction side (X/c above coordinate)"""
        pass
    
    #Does not work with Python 2.7
    #@abstractmethod
    @abc.abstractmethod
    def Ys(self,x):
        """ Suction side (Y/c above coordinate)"""
        pass
    
    #Does not work with Python 2.7
    #@abstractmethod
    @abc.abstractmethod
    def Xp(self,x):
        """ Pressure side (X/c below coordinate)"""
        pass
    
    #Does not work with Python 2.7
    #@abstractmethod
    @abc.abstractmethod
    def Yp(self,x):
        """ Pressure side (Y/c below coordinate)"""
        pass
    
    #Does not work with Python 2.7
    #@abstractmethod
    @abc.abstractmethod
    def vecS_TE(self):
        """ Tangent at TE at pressure and suction (orientation from pressure to suction - towards LE and back to TE towards wake) """
        # NOTE : Should return the two vectors in the following list format
        #                     [v_PressureSide_from TE_to_LE  _x , v_PressureSide_from TE_to_LE  _y 
        #                      v_SuctionSide _from LE_to_wake_x , v_SuctionSide _from LE_to_wake_y]
        pass
    
    #Does not work with Python 2.7
    #@abstractmethod
    @abc.abstractmethod
    def vecS_TE(self):
        """ Tangent at LE (orientation from pressure to suction) """
        pass
    
    #Does not work with Python 2.7
    #@abstractmethod
    @abc.abstractmethod
    def show_parameters(self):
        """ Print Foil Parameters """
        pass
    
    
    def closed(self,TE_closed=True):
        """ Set Closed Parameter for the foil """
        self.TE_closed=TE_closed
    
    
    def SuctionSide_FCAD(self,npoints=30,LE2TE=True):
        """ Generates lists of npoints (default=20) as X,Y coordinates to define FreeCAD base vectors for the suction side (oriented from LE to TE) """
        from numpy import linspace
        if (LE2TE):
            x=linspace(0,1,npoints)
        else:
            x=linspace(1,0,npoints)
        if (not self.TE_closed):
            print ("Foil Warning : The foil does not have a closed TE. You should add a line to close it ")
        return self.Xs(x), self.Ys(x)
    
    
    def PressureSide_FCAD(self,npoints=30,LE2TE=True):
        """ Generates lists of npoints (default=20) as X,Y coordinates to define FreeCAD base vectors for the suction side (oriented from LE to TE) """
        from numpy import linspace
        x=linspace(1,0,npoints)
        if (not self.TE_closed):
            print ("Foil Warning : The foil does not have a closed TE. You should add a line to close it ")
        return self.Xp(x), self.Yp(x)    
    
    
    def plot_XY(self,show_vecS=True,npoints=100):
        """ Returns a plt handle for the XY coordinates """
        import matplotlib.pyplot as plt
        from numpy import linspace
        x=linspace(0,1,npoints)
        plt.plot(self.Xs(x),self.Ys(x),'bo',markersize=2,label='Suction Side')
        plt.plot(self.Xp(x),self.Yp(x),'ro',markersize=2,label='Pressure Side')
        plt.xlabel('X/c')
        plt.ylabel('Y/c')
        plt.legend()
        plt.grid(1)
        plt.axis('equal')
        if (show_vecS):
            vTE=self.vecS_TE()
            vLE=self.vecS_LE()
            Xs=[self.Xp(1),self.Xp(0),self.Xs(1)]
        #   NOTE :          ^^^ Xp(0)=Xs(0)
            Ys=[self.Yp(1),self.Yp(0),self.Ys(1)]
        #   NOTE :          ^^^ Yp(0)=Ys(0) but Ys(1)=Yp(1) only if TE closed is true 
            Us=[vTE[0],vLE[0],vTE[2]]
            Vs=[vTE[1],vLE[1],vTE[3]]
            plt.quiver(Xs,Ys,Us,Vs,width=0.002)
        return plt
    