#!/bin/bash

# Developers need to customize the paths of the VTK to run the visualization

export LD_LIBRARY_PATH=/home/ibanez/bin/VTK/Release/bin
HEADOfITKTree=/home/ibanez/src/ITK


./includefindertocsv.py $HEADOfITKTree
#./includefinder.py $HEADOfITKTree

./hierarchyexporternogroups.py $HEADOfITKTree
#./hierarchyexporter.py $HEADOfITKTree

myPythonVTK=/home/ibanez/bin/VTK/Release/bin/vtkpython

$myPythonVTK  cone_layout.py
$myPythonVTK  hierarchical_graph2.py
$myPythonVTK  hierarchical_ring.py
