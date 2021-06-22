### FreeCAD Foil Library : Utilities
# 
# Author: Konstantinos POLITIS (unless otherwise specified) 
# 
#   User defined functions 
#   
#  To do list : 
#    
###

0.000353485
-0.00333758 (EAR)J 2
- 0.00478125 (EAR)(P/D)J
+ 0.000257792   (log(Re) -0.301) 2 $ (A E /A O )J 2
+ 0.0000643192  (log(Re) -0.301)(P/D) 6 J 2
-0.0000110636   (log(Re) -0.301) 2 (P/D) 6 J 2
- 0.0000276305  (log(Re) -0.301) Z(A E /A O )J 2
+ 0.0000954     (log(Re) -0.301)Z(A E /A O )(P/D)J
+ 0.0000032049  (log(Re) -0.301) Z 2 (A E /A O ) (P/D) 3 J


def loft_2foils(foil1,foil2):
    """ Creates a loft from two foils """
    # Define