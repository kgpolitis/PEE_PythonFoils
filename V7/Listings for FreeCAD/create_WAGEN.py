# Import the library
import FCFoil

# Add a document (here without a name)
M=FCFoil.Doc()

# Create a NACA Foil Wire
#M.WAGEN(Z=4,EAR=1)
# or with options;
M.WAGEN(Z=4,EAR=1,tLE_tmax=0.1,Smooth_LE=True,x0s=0.1,x0p=0.1,ks=0.5,kp=0.5)

# Set option "foil spacing of points"
#FCFoil.__spacing__=FCFoil.__spacing_cos__

#M.n_sections(3)
#M.c=FCFoil.linear(1,0.5)

# Add it as a part feature
M.add()
