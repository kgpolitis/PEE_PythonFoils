0. Install FreeCAD :
    see for exemple : 
        https://www.freecadweb.org/wiki/Install_on_Windows
        https://www.freecadweb.org/wiki/Install_on_Unix
        
1. Start FreeCAD

2. Open a Python Console from the menu: 
                          (File,Edit,) View (,Tools,...) 
                                        |--> Panel 
                                               |--> Python Console

3. Check module path supervised by FreeCAD. 
    Using the Python Console of FreeCAD, type or copy-paste the following :
    (don'to forget the colon : or the tabs, copy-paste if not sure)
    
import sys
for path in sys.path:
    print(path)
    
    
    Hit enter twice and a list of directories appears. Copy the modules :
        
        FCFoil.py
        FOIL.py
        NACA_LIB.py
        WAGENINGEN_LIB.py
        
    To one of the directories that appeared.
    (note if your python version is 2.7 then copy the 27 versions of the
    libraries)
    
4. Restart FreeCAD and type :

import FCFoil
    
    Follow the instructions that appear when you type : 
    
FCFoil.README()

you have a listing of commands to copy-paste at the python console of FreeCAD
to test the FCFoil library.
