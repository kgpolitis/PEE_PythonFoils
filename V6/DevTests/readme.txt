In this location we conduct the tests during developpement. 
To switch between libraries we can use the map27.sh or map3.sh
script. After execution the local to this directory libraries : 

 FOIL.sh
 NACA_LIB.sh
 WAGENINGEN_LIB.sh

are mapped to the files located inside the directory :

    ForPython27 (map27.sh)   or   ForPython3 (map3.sh)

To use these files type :

chmoad +x map27.sh map3.sh

and then : 
    
    ./map27.sh 
    
or  
    ./map3.sh

To confirm the mapping type : 

    ls -al
