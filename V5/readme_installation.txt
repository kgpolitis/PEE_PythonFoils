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
        
    To one of the directories that appeared. The above modules are located
    inside either the directory ForPython27 or ForPython3.
    If the version of python you are using is 2.7 then copy the files provided
    in ForPython27. Otherwise (python 3+, tested with 3.7) use the files 
    located inside the folder ForPython3.
    
4. Restart FreeCAD and type :

import FCFoil
    
    Follow the instructions that appear when you type : 
    
FCFoil.README()

you have a listing of commands (see listing directory) to copy-paste at 
the python console of FreeCAD to test the FCFoil library.

To obtain the documentation of the library :
From either directory ForPython27 or ForPython3 type either:

pydoc -g FOIL.py

or:

pydoc3 -b FOIL.py
