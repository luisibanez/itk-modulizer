#!/usr/bin/python
#==========================================================================
#
#   Copyright Insight Software Consortium
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#          http://www.apache.org/licenses/LICENSE-2.0.txt
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
#
#==========================================================================*/
# This script is used to generate two XML files that organize the hierarchy
# of groups, modules and classes.
#
# To run it, type ./modulefinder.py   ITK_SOURCE_TREE
#
# from the directory where the Manifest.txt file is.
# an output file called itkModules.xml will be generated.
#

import glob
import sys
import os.path
import re

if len(sys.argv) != 2:
    print("USAGE:  {0} [monolithic ITK PATH]".format(sys.argv[0]))
    sys.exit(-1)


HeadOfITKTree = sys.argv[1];
if (HeadOfITKTree[-1] == '/'):
    HeadOfITKTree = HeadOfITKTree[0:-1]

testFiles = glob.glob(HeadOfITKTree+'/Testing/Code/*/*.cxx')

modulesTable =  open('./itkModulesNoGroups.xml','w')
missingEntries =  open('./missingIncludes.log','w')
print('create ./itkModulesNoGroups.xml and ./missingIncludes.log')

manifestfile = open(HeadOfITKTree+"/Modularization/Manifest.txt",'r')
manifestlines = manifestfile.readlines()

classmoduletable = {'classname':'modulename'}
modulegrouptable = {'modulename':'groupname'}
groupnames = []

modulesTable.write('<node id="Modular ITK">\n')

#
#  Harvest information from the Manifest.txt file
#  and populate internal tables.
#
for line in manifestlines:
  if (line[0] != "#"):
    words = line.split()
    inputfile = words[0]
    group = words[1]
    module = words[2]
    destinationSubdir = words[3]
    if destinationSubdir == 'src':
      basepath, basefilename = os.path.split(inputfile)
      basename, extension = os.path.splitext(basefilename)
      classmoduletable[basename] = module
      modulegroup = modulegrouptable.get(module,'not-found')

      if modulegroup == 'not-found':
        modulegrouptable[module] = group

      try:
          groupindex = groupnames.index(group)
      except ValueError:
          groupindex = -1

      if groupindex == -1:
        groupnames.append(group)

moduleId = 0

#
#  Iterate through the tables to generate hierarchical
#  information and write it to a XML file.
#
for groupname in groupnames:
  print groupname
#  modulesTable.write('\t<node id="'+groupname+'" name="'+groupname+'">\n')

  for modulename in modulegrouptable:
    if modulegrouptable[modulename] == groupname:
      modulesTable.write('\t\t<node id="'+modulename+'" name="'+modulename+'" colorId="'+str(moduleId)+'">\n')

      for classname in classmoduletable:
        if classmoduletable[classname] == modulename:
          modulesTable.write('\t\t\t<node id="'+classname+'" name="" colorId="'+str(moduleId)+'">\n')
          modulesTable.write('\t\t\t</node>\n')

      modulesTable.write('\t\t</node>\n')

    moduleId=moduleId+1

#  modulesTable.write('\t</node>\n')

modulesTable.write('</node>\n')


modulesTable.close()
missingEntries.close()
