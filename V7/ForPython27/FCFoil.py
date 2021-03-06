### FreeCAD Foil Library : FCFoil
# 
# Author: Konstantinos POLITIS
# 
#   FreeCAD Library for Managing Foils (interface and manipulation of FOIL Library) 
#   
#  To do list : 
#    - Rework help messages and add input/output text
#    - Add help/readme function to guide used 
# 
###
from FreeCAD import Base
import FreeCAD
import abc, six

# Basic Definitions
O =Base.Vector(0,0,0)
ux=Base.Vector(1,0,0)
uy=Base.Vector(0,1,0)
uz=Base.Vector(0,0,1)



### Internal defaults for foil generating functions
# Wageningen : 
__tLE_tmax__=0
__tTE_tmax__=0
__Smooth_LE__=False
__x0s__=0.1
__ks__ =0.5
__x0p__=0.1
__kp__ =0.5

# NACA :
__N4cod_def__="xxxx" 
__NACA4_def__=[0,0,0.15]
__TE_closed__=True

# The chord is zero if smaller than this value
__c_is_zero__=1e-3


# Internal Options 
__useparams__=False
__LE2TEp__=False
__LE2TEs__=False

__spacing_lin__="linear"
__spacing_cos__="cos"
__spacing__=__spacing_lin__

__spacing_z__=__spacing_lin__

### End of Internal defaults for foil generating functions

class Doc:
    """ This is a FreeCAD Document that contains Foil Sections."""
    
    def __init__(self,document_name="Foil",L=1,n_sections=1,b=0.5,c=1,t=0,p=O,u=ux,n=uy):
        """ Create a Named Document (by default the name is MyFoil)  
            Optinal Inputs : 
                document_name : the name of the FC document ("Foil")
                zL            : list of floats : values z/L, the variable z denotes the spanwise internal coordinate of the foil (coincides to the z-axis)
                                through this variable we define the spanwise locations where the functions cL,xbc,tws,p,u,b are evaluated. The default value
                                0,is use for a single foil.
                                The values of these functions evaluated at the locations provided by the array zL are stored in the following 
                                lists : 
                cL            : list of floats : chord distributions at zL (cL=[1])
                xbc           : list of floats : hanging/base point variable of the foil at zL (xbc=[0.5])
                tws           : list of twist angles (degrees) of the foil at zL (tws=[0])
                p             : list of actual hanging/base points at zL (p=[O])
                u             : list of unit vectors representing the chord axis at zL (u=ux) 
                n             : list of unit vectors normal-to-chord axis unit vectors at zL (n=[uy])
            When the above arrays are provided they must have the same length. The user is informed if otherwise."""
        # "pointer" to internal document 
        self.Docu=FreeCAD.newDocument(document_name)
        # Initialisations
        self.ns=n_sections
        self.b=constant(b)
        self.c=constant(c)
        self.t=constant(t)
        self.p=line(p,-uz,L) 
        self.u=constant(u)
        self.n=constant(n)
    
    
    # Initializer for .section 
    # User functions to a add certain foil for the whole span
    def NACA(self,code=__N4cod_def__,params=__NACA4_def__,TE_closed=__TE_closed__):
        """ Define the foil section as a NACA section """
        __spacing__=__spacing_cos__
        self.s=NACA_const(code,params,TE_closed)
    

    def WAGEN(self,Z,EAR,tLE_tmax=__tLE_tmax__,tTE_tmax=__tTE_tmax__,Smooth_LE=__Smooth_LE__,x0s=__x0s__,x0p=__x0p__,ks=__ks__,kp=__kp__):
        """ Define the foil section as a Wageningen section """
        self.s=WAGBS(Z,EAR,tLE_tmax,tTE_tmax,Smooth_LE,x0s,x0p,ks,kp)

    def n_sections(self,n_sections):
        self.ns=n_sections
    
    
    def add(self,nps=40,npp=40,Tvs=0,Tvp=0,zs=0,ze=1,spacing=__spacing_z__,here=False):
        """ Creates a Named Foil Section as a Part:Feature Wire
        Input : 
            1. Afoil    : A foil section instance generated by a foil section generating function
            2. nps, npp : integer : n(umber of )p(oints for)s(uction)/p(ressure side) (40/40)
            3. Tvs, Tvp : logical : use T(angent )v(ectors at )s(uction)/p(ressure side) 
                                    for bspline definitions (True/True)                 
                                    If npp=0 then the first argument correspond to whether we
                                    use (Tvs=True) or not (Tvs=False) the tangent vectors at 
                                    the TE to build the spline. 
            4. zs,ze    : floats  : values between 0 and 1 with zs<ze denoting the starting 
                                    and ending values of the internal spanwise parameter    
            5. spacing  : string  : defines the type of spacing used to define intermediary spanwise sections
            6. here     : logical : if true then the construction is added to the current document.
                                    The default value is false : the construction is performed at 
                                    the document generated by the FCFoil library
            7. Draft    : logical : Create as drafts """
        from numpy import linspace,cos,sign
        import Part
        import Draft
        # Construct array of z values 
        t=linspace(zs,ze,self.ns)
        if (spacing=='linear'):
            self.zL=t
        elif (spacing=='cos'):
            self.zL=1-cos(pi*t/2)
        
        # Bspline Construction
        stopnow=False
        i=-1
        for zL in self.zL:
            
            if ( self.c.at(zL) <= __c_is_zero__ ):
                # Case of zero chord => add a vertex 
                Add_this=Base.Vertex(self.p.at(zL))
                name = "Vertex:c=0"
                
            else:
                
                ### Get foil section at zL
                #    - Set the foil's geometry at the spamwise location zL
                afoil=self.s.at(zL)
                name=afoil.name()
                
                ### Construct Drawing Shape for the Bsplines
                #  
                #  -- Two cases : A. Foil
                #                 B. Propeller 
                #  
                #  For the foil case we define planes
                #  For the blade case we define cylinders
                #  Note that other kind of surfaces can be used (cone, bsplinesurface etc)
                #  but we use only planes and cylinders
                p=self.p.at(zL)
                u=self.u.at(zL)
                n=self.n.at(zL)
                b=self.b.at(zL)
                myMat=Base.Matrix()
                myMat.move(-b*ux)
                ucux=ux.cross(u)
                myMat.rotateZ(u.getAngle(ux)*sign(ucux.z))
                myshape=Part.Plane(p,(u.cross(n)))
                myshape.transform(myMat)
                # note : up to this point no scaling is applied. Scaling is applied to the 
                #        struction afterwards 
                
                if (npp==0) : # construction using one bspline will be used for the foil
                    # Implies that a single line will be used for the wire 
                    # Note that this option is approriate only for a foil whose LE is smooth
                    # If it is not smooth or it is not closed at the LE then the generated bspline will
                    # interpolate points trying to enforce a C2 continuity everywhere (so also at the LE)
                    # if no tangents are used (i.e. Tvs=False). When tangents are used the continuity falls 
                    # to C1. 
                    # For the case where the foil is not closed due to the LE then there is no need to add
                    # a straight line there to our construction
                    
                    sp = __make_spline__(afoil,nps=nps,npp=nps,Tv=Tvs)
                    sp.scale(Base.Vector2d(0,0),self.c.at(zL))
                    
                    if (not afoil.TE_closed):
                        
                        #Add_this=Part.Wire([sp.toShape(),Part.makeLine(sp.EndPoint,sp.StartPoint)])
                        L=Part.Geom2d.Line2dSegment(sp.EndPoint,sp.StartPoint)
                        Add_this=Part.Wire([sp.toShape(myshape),L.toShape(myshape)])
                        
                    else :
                        
                        #Add_this=Part.Wire(sp.toShape())
                        Add_this=Part.Wire(sp.toShape(myshape))
                    
                else: # classic two bspline construction will be used for the foil
                    
                    spP,spS = __make_splines__(afoil,nps=nps,npp=npp,Tvp=Tvp,Tvs=Tvs)
                    spP.scale(Base.Vector2d(0,0),self.c.at(zL))
                    spS.scale(Base.Vector2d(0,0),self.c.at(zL))
                    
                    # Note : The following works only for the default orientation
                    # i.e. TE2LE
                    if ( (not afoil.LE_closed) and (not afoil.TE_closed) ):
                        #L1=Part.Geom2d.Line2dSegment(spP.EndPoint,spS.StartPoint)
                        #L2=Part.Geom2d.Line2dSegment(spS.EndPoint,spP.StartPoint)
                        L1=Part.Geom2d.Line2dSegment(spP.EndPoint,spS.EndPoint)
                        L2=Part.Geom2d.Line2dSegment(spS.StartPoint,spP.StartPoint)
                        
                        #Add_this=Part.Wire([spP.toShape(),part.makeLine(spP.EndPoint,spS.StartPoint),spS.toShape(),part.makeLine(spS.EndPoint,spP.StartPoint)])
                        Add_this=Part.Wire([spP.toShape(myshape),L1.toShape(myshape),spS.toShape(myshape),L2.toShape(myshape)])
                        
                    elif ( (not afoil.LE_closed) and (afoil.TE_closed) ):
                        
                        #L1=Part.Geom2d.Line2dSegment(spP.EndPoint,spS.StartPoint)
                        L1=Part.Geom2d.Line2dSegment(spP.EndPoint,spS.EndPoint)
                        
                        #Add_this=Part.Wire([spP.toShape(),part.makeLine(spP.EndPoint,spS.StartPoint),spS.toShape()])
                        Add_this=Part.Wire([spP.toShape(myshape),L1.toShape(myshape),spS.toShape(myshape)])
                        
                    elif ( (afoil.LE_closed) and (not afoil.TE_closed) ):
                        
                        #L2=Part.Geom2d.Line2dSegment(spS.EndPoint,spP.StartPoint)
                        L2=Part.Geom2d.Line2dSegment(spS.StartPoint,spP.StartPoint)
                        
                        Add_this=Part.Wire([spP.toShape(myshape),spS.toShape(myshape),L2.toShape(myshape)])
                        
                    else:
                        
                        Add_this=Part.Wire([spP.toShape(myshape),spS.toShape(myshape)])
                
                # Make transformations of internal geometry
                #Add_this.translate(-self.u.at(zL)*self.b.at(zL))
                #u=self.u.at(zL)
                #n=self.n.at(zL)
                #Add_this.rotate(O,-(u.cross(n)),self.t.at(zL))
                #Add_this.translate(self.p.at(zL))
                #Add_this.scale(self.c.at(zL))
            
            if (not here): 
                self.Docu.addObject("Part::Feature","zL={:.3f}:".format(zL)+name).Shape=Add_this
            else: 
                Part.show(Add_this,"zL={:.3f}:".format(zL)+name)
            
        
        
###
# Functions for working with FreeCAD
#

def __make_spline__(afoil,nps=40,npp=40,Tv=1):
    """ Return the spline of the Pressure-Suction side of a foil """
    import Part
    
    xpres,ypres,zpres,t=afoil.PressureSide_FCAD(npoints=npp,spacing=__spacing__)
    xsuc,ysuc,zsuc,t=afoil.SuctionSide_FCAD(npoints=nps,spacing=__spacing__)

    # NOTE : Total number of point nps+npp-1
    #V=[Base.Vector(xpres[i],ypres[i],zpres[i]) for i in range(len(xpres)-1)] 
    #V.extend([Base.Vector(xsuc[i],ysuc[i],zsuc[i]) for i in range(len(xsuc))]) 
    V=[Base.Vector2d(xpres[i],ypres[i]) for i in range(len(xpres)-1)] 
    V.extend([Base.Vector2d(xsuc[i],ysuc[i]) for i in range(len(xsuc))]) 
          
    # Setup FreeCAD Spline (one spline)
    sp=Part.Geom2d.BSplineCurve2d()
    
    # Note : By 
    
    if (Tv):
        
        # Get tangent vector at trailing edge
        vecTE=afoil.vecS_TE()
        vTEp = Base.Vector2d(vecTE[0],vecTE[1])
        vTEs = Base.Vector2d(vecTE[2],vecTE[3])
        
        # Set spline
        sp.interpolate(V,InitialTangent=vTEp,FinalTangent=vTEs)
        
    else:
        sp.interpolate(V)
    
    return sp

def __make_splines__(afoil,nps=40,npp=40,Tvp=1,Tvs=1):
    """ Returns the splines of the Pressure and Suction side of a foil """
    import Part
    xpres,ypres,zpres,tp=afoil.PressureSide_FCAD(npoints=npp,spacing=__spacing__,LE2TE=__LE2TEp__)
    xsuc,ysuc,zsuc,ts=afoil.SuctionSide_FCAD(npoints=nps,spacing=__spacing__,LE2TE=__LE2TEs__)

    #Vp=[Base.Vector(xpres[i],ypres[i],zpres[i]) for i in range(len(xpres))] 
    #Vs=[Base.Vector(xsuc[i],ysuc[i],zsuc[i]) for i in range(len(xsuc))] 
    Vp=[Base.Vector2d(xpres[i],ypres[i]) for i in range(len(xpres))] 
    Vs=[Base.Vector2d(xsuc[i],ysuc[i]) for i in range(len(xsuc))] 
    
    if (Tvp or Tvs):
        
        # Get tangent vector at leading/trailing edge
        vecLE=afoil.vecS_LE()
        vecTE=afoil.vecS_TE()
        
        # Arrange Data
        #vLEp = Base.Vector(vecLE[0],vecLE[1],0)
        #vLEs = Base.Vector(vecLE[2],vecLE[3],0)
        #vTEp = Base.Vector(vecTE[0],vecTE[1],0)
        #vTEs = Base.Vector(vecTE[2],vecTE[3],0)
        vLEp = Base.Vector2d(vecLE[0],vecLE[1])
        vLEs = Base.Vector2d(vecLE[2],vecLE[3])
        vTEp = Base.Vector2d(vecTE[0],vecTE[1])
        vTEs = Base.Vector2d(vecTE[2],vecTE[3])
        
    # Setup FreeCAD Splines (two splines)
    spS=Part.Geom2d.BSplineCurve2d()
    spP=Part.Geom2d.BSplineCurve2d()
    
    if (__useparams__):
        
        if (Tvp):
            if (__LE2TEp__) :
                #spP.interpolate(Vp,InitialTangent=-vLEp,FinalTangent=-vTEp,Parameters=tp)
                spP.interpolate(Vp,InitialTangent=Base.Vector2d(-vLEp.x,-vLEp.y),FinalTangent=Base.Vector2d(-vTEp.x,-vTEp.y),Parameters=tp)
                # NOTE : 
                # Here the Base.Vector2d(-vLEp.x,-vLEp.y) are required because the minus unary operation
                # is not defined for the type Vector2d, so if a is Vector2d then -a returns an error
            else :
                spP.interpolate(Vp,InitialTangent=vTEp,FinalTangent=vLEp,Parameters=tp)
        else:
            spP.interpolate(Vp,Parameters=tp)
        
        if (Tvs):    
            if (__LE2TEs__) :
                spS.interpolate(Vs,InitialTangent=vLEs ,FinalTangent=vTEs,Parameters=ts)
            else:
                #spS.interpolate(Vs,InitialTangent=-vTEs ,FinalTangent=-vLEs,Parameters=ts)
                spS.interpolate(Vs,InitialTangent=Base.Vector2d(-vTEs.x,-vTEs.y),FinalTangent=Base.Vector2d(-vLEs.x,-vLEs.y),Parameters=ts)
            
        else:
            spS.interpolate(Vs,Parameters=ts)
        
    else:
        
        if (Tvp):
            if (__LE2TEp__) :
                spP.interpolate(Vp,InitialTangent=Base.Vector2d(-vLEp.x,-vLEp.y),FinalTangent=Base.Vector2d(-vTEp.x,-vTEp.y))
                #spP.interpolate(Vp,InitialTangent=-vLEp,FinalTangent=-vTEp)
            else :
                spP.interpolate(Vp,InitialTangent=vTEp,FinalTangent=vLEp)
        else:
            spP.interpolate(Vp)
    
        if (Tvs):    
            if (__LE2TEs__) :
                spS.interpolate(Vs,InitialTangent=vLEs ,FinalTangent=vTEs)
            else:
                #spS.interpolate(Vs,InitialTangent=-vTEs ,FinalTangent=-vLEs)
                spS.interpolate(Vs,InitialTangent=Base.Vector2d(-vTEs.x,-vTEs.y),FinalTangent=Base.Vector2d(-vLEs.x,-vLEs.y),Parameters=ts)
            
        else:
            spS.interpolate(Vs)
        
    return spP,spS


def __makedraft_splines__(afoil,nps=40,npp=40,Tvp=1,Tvs=1):
    """ Returns the splines of the Pressure and Suction side of a foil """
    import Sketch
    xpres,ypres,zpres,tp=afoil.PressureSide_FCAD(npoints=npp,spacing=__spacing__,LE2TE=__LE2TEp__)
    xsuc,ysuc,zsuc,ts=afoil.SuctionSide_FCAD(npoints=nps,spacing=__spacing__,LE2TE=__LE2TEs__)

    Vp=[Base.Vector(xpres[i],ypres[i],zpres[i]) for i in range(len(xpres))] 
    Vs=[Base.Vector(xsuc[i],ysuc[i],zsuc[i]) for i in range(len(xsuc))] 
    
    if (Tvp or Tvs):
        
        # Get tangent vector at leading/trailing edge
        vecLE=afoil.vecS_LE()
        vecTE=afoil.vecS_TE()
        
        # Arrange Data
        vLEp = Base.Vector(vecLE[0],vecLE[1],0)
        vLEs = Base.Vector(vecLE[2],vecLE[3],0)
        vTEp = Base.Vector(vecTE[0],vecTE[1],0)
        vTEs = Base.Vector(vecTE[2],vecTE[3],0)
        
    # Setup FreeCAD Splines (two splines)
    spS=Part.BSplineCurve()
    spP=Part.BSplineCurve()
    
    if (__useparams__):
        
        if (Tvp):
            if (__LE2TEp__) :
                spP.interpolate(Vp,InitialTangent=-vLEp,FinalTangent=-vTEp,Parameters=tp)
            else :
                spP.interpolate(Vp,InitialTangent=vTEp,FinalTangent=vLEp,Parameters=tp)
        else:
            spP.interpolate(Vp,Parameters=tp)
    
        if (Tvs):    
            if (__LE2TEs__) :
                spS.interpolate(Vs,InitialTangent=-vLEs ,FinalTangent=vTEs,Parameters=ts)
            else:
                spS.interpolate(Vs,InitialTangent=-vTEs ,FinalTangent=-vLEs,Parameters=ts)
            
        else:
            spS.interpolate(Vs,Parameters=ts)
        
    else:
        
        if (Tvp):
            if (__LE2TEp__) :
                spP.interpolate(Vp,InitialTangent=-vLEp,FinalTangent=-vTEp)
            else :
                spP.interpolate(Vp,InitialTangent=vTEp,FinalTangent=vLEp)
        else:
            spP.interpolate(Vp,Parameters=tp)
    
        if (Tvs):    
            if (__LE2TEs__) :
                spS.interpolate(Vs,InitialTangent=vLEs ,FinalTangent=vTEs)
            else:
                spS.interpolate(Vs,InitialTangent=-vTEs ,FinalTangent=-vLEs)
            
        else:
            spS.interpolate(Vs)
        
    return spP,spS



#
# END : Functions for working with FreeCAD
###


@six.add_metaclass(abc.ABCMeta)
class distribution():
    """ Abstract Class Method for generating distribution functions """
    @abc.abstractmethod
    def at(self,zL):
        pass
    
class constant(distribution):
    """ Constant distribution """
    
    def __init__(self,c):
        self.c=c
    
    def at(self,zL):
        return self.c
    
class linear(distribution): 
    """ Linear distribution """
    
    def __init__(self,c1,c2):
        self.c1=c1
        self.c2=c2
    
    def at(self,zL):
        return self.c1*(1-zL)+self.c2*zL

class line(distribution):
    """ Line distribution """
    
    def __init__(self,p,u,L):
        self.p=p
        self.u=u
        self.L=L
    
    def at(self,zL):
        v=self.p+self.u*zL*self.L
        return v

class NACA_const(distribution):
    
    def __init__(self,code,params,TE_closed):
        """ Foil Section Generating Class
            Inputs :
            -Specific for NACA 
                code     : a four digit code representing the Series4 geometry, if it is set to "xxxx"  
                (Digits = 1st digit : max camber, 2nd : location of max camber, 3rd-4rth : thickness) """
        self.code=code
        self.m=constant(params[0])
        self.p=constant(params[1])
        self.t=constant(params[2])
        self.TE_closed=TE_closed
        
    def at(self,zL):
        from NACA_LIB import NACA as NACAPicker
        foil_section=NACAPicker(self.code,[self.m.at(zL),self.p.at(zL),self.t.at(zL)],self.TE_closed)
        return foil_section
    
    
class WAGBS(distribution):
    
    def __init__(self,Z,EAR,tLE,tTE,Smooth_LE,x0s,x0p,ks,kp):
        """ Foil Section Generating Class
            Inputs :  
            -Specific for WAGENINGEN 
                Z        : number of blades 
                EAR      : expanded area ratio 
                tLE      : thickness ratio (over tmax) at Leading Edge   
                tTE      : thickness ratio (over tmax) at Trailing Edge 
                Smooth_LE: if true smooths the leading edge   
                x0s,x0p  : region of smoothing (suction and pressure) 
                ks,kp    : smoothing index"""
        self.Z=Z
        self.EAR=EAR
        self.tLE=tLE
        self.tTE=tTE
        self.Smooth_LE=Smooth_LE
        self.x0s=x0s
        self.x0p=x0p
        self.ks=ks
        self.kp=kp
        
        
    def at(self,zL):
        from WAGENINGEN_LIB import WAGENINGEN 
        #self.s=WAGBS(Z,EAR,tLE_tmax=tLE_tmax,tTE_tmax=tTE_tmax,Smooth_LE=Smooth_LE,x0s=x0s,x0p=x0p,ks=ks,kp=kp)
        foil_section=WAGENINGEN(self.Z,self.EAR,zL,tLE_tmax=self.tLE,tTE_tmax=self.tTE,Smooth_LE=self.Smooth_LE,x0s=self.x0s,x0p=self.x0p,ks=self.ks,kp=self.kp)
        return foil_section

def README():
    """ Help """
    instru='''
    This library helps you create foil sections and established the required operations 
    to facilitate the geometrical constructions. If you need more details about the 
    construction methods used you should check the theory manual. This message provides
    you with the basics to begin your work.
    
    1. Create a document that will contain the sections of a foil :
        The document is created by calling FCFoils.Doc as for exemple :
        
                 MyFoils=FCFoil.Doc() or MyFoils=FCFoil.Doc("optional_name").
        
        The default optional name is MyFoil.
        We will add the foil section to this document.
        Multiple documents can be managed in the same manner.
        In terms of FreeCAD this is a FreeCAD Document instance.
    
    2. Create the foil sections :
        The functions : 
            Wagen, NACA, ...
        create foil section instances, for exemple: 
        
                 FS1=FCFoil.WAGEN(Z=4,EAR=1,rR=0.4)
        
        the FS1 is a foil section instance. In terms of FreeCAD this a Part.Shape 
        instance and thus shares all the methods of Part.Shape objects.
        Multiple foil sections can be created (note that you have to store them to 
        different variables (if this is required). 
        
        Different options are required for different function that generate foil section:
                NACA  : A code that is related to a NACA Series 
                WAGEN : Number of blades, EAR, etc
                
        To check in detail the required input per foil generating function, type : 
        
                FCFoil. or FCFoil.(with a dot). 
                
        A list appears with the name of the module functions. Move the cursor to the 
        name of the foil generating function to see in detail the required and optional input.
        Optional inputs are identified with a default value.  
        
    3. Add the foil section to the document
        If FS1 is a foil section created by either function Wagen or NACA, that is for :
        then :
                 MyFoils.add(FS1) will extend your document with the foil section FS1
        
        At this point the foil section appears on screen.
        You may optionally provide a name MyFoils.add(FC1,'MyFoilName').
    
    NOTE : The following is a listing of commands to test the library :
    
import FCFoil
MyFoil=FCFoil.Doc("My Foil")
FS1=FCFoil.WAGEN(Z=4,EAR=1,rR=0.4)
MyFoil.add(FS1)
FS2=FCFoil.NACA(4430)
MyFoil.add(FS2)
    
    
    You may copy-paste the commands to the Python console to test the functionallity of
    the library (explained above). Note that Python is case-sensitive ! 
    
    End of README
        '''
    print(instru)

