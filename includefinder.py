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
# This script is used to find all the #include relationships between ITK files.
# It looks in the Manifest.txt file and for each file it generates the list of
# files that are included from there.

#
# To run it, type ./includefinder.py   ITK_SOURCE_TREE
#
# from the directory where the Manifest.txt file is.
# an output file called itkIncludes.xml will be generated.
#

import glob
import sys
import os.path
import re

if len(sys.argv) != 3:
    print("USAGE:  {0} [monolithic ITK PATH] [modular ITK PATH]".format(sys.argv[0]))
    sys.exit(-1)


HeadOfITKTree = sys.argv[1];
if (HeadOfITKTree[-1] == '/'):
    HeadOfITKTree = HeadOfITKTree[0:-1]

HeadOfModularITKTree = sys.argv[2];
if (HeadOfModularITKTree[-1] ==  '/'):
    HeadOfModularITKTree = HeadOfModularITKTree[0:-1]

testFiles = glob.glob(HeadOfITKTree+'/Testing/Code/*/*.cxx')

includesTable =  open('./itkIncludes.xml','w')
missingEntries =  open('./missingIncludes.log','w')

manifestfile = open("./Manifest.txt",'r')
manifestlines = manifestfile.readlines()

moduletable = {'classname':'modulename'}

for line in manifestlines:
  words = line.split()
  inputfile = words[0]
  group = words[1]
  module = words[2]
  destinationSubdir = words[3]
  if destinationSubdir == 'Source':
    basepath, basefilename = os.path.split(inputfile)
    basename, extension = os.path.splitext(basefilename)
    moduletable[basename] = module

for line in manifestlines:
  words = line.split()
  inputfile = words[0]
  group = words[1]
  module = words[2]
  destinationSubdir = words[3]
  if destinationSubdir == 'Source':
    basepath, basefilename = os.path.split(inputfile)
    basename, extension = os.path.splitext(basefilename)
    includesTable.write('<class id="'+basename+'" module="'+module+'">\n')
    fullinputfile = HeadOfITKTree+'/'+inputfile
    for codeline in open(fullinputfile,'r'):
      if codeline.find("#include") != -1:
        searchresult = re.search('itk.*\.h',codeline)
        if searchresult:
          includedclass = searchresult.group()
          if not re.search('\+',includedclass):
            if not re.search('itksys',includedclass):
              includebasename, includeextension = os.path.splitext(includedclass)
              includemodule = moduletable.get(includebasename,'not-found')
              if includemodule == 'not-found':
                missingEntries.write(includedclass+' included from '+inputfile+'\n')
              includesTable.write('\t<class id="'+includebasename+'" module="'+includemodule+'">\n')
              includesTable.write('\t</class>\n')
    includesTable.write('</class>\n')

includesTable.close()
missingEntries.close()
