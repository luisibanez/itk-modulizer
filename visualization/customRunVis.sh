#!/bin/bash

# Developers need to customize the paths of the VTK to run the visualization

export LD_LIBRARY_PATH=/media/work/bin/VTK/Release/bin
HEADOfITKTree=/media/work/src/ITK
HEADOfModularITKTree=/media/work/src/ModularITK/modularITK/


./includefindertocvs.py $HEADOfITKTree
#./includefinder.py $HEADOfITKTree

./hierarchyexporternogroups.py $HEADOfITKTree 
#./hierarchyexporter.py $HEADOfITKTree

$myPythonVTK  cone_layout.py
$myPythonVTK  hierarchical_graph2.py
