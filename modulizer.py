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
# This script is used to automate the modularization process. The following
# steps  are included:
# 1. Move the files in the monolithic ITK into modules of the modularized ITK.
#    A manifest text file that lists all the files and their destinations is
#    required to run the script.By default, the manifest file is named as
#    "Manifest.txt" in the  same directory of this script.
# 2. Create CMake Files and put them into modules.



# To run it, type ./modulizer.py  ITK_PATH  ModularITK_PATH   from
# the itk-modulizer root directory.

print "*************************************************************************"
print "WARNINGs! This modularization script is still in its experimental stage."
print "Current ITK users should NOT run this script."
print "*************************************************************************"


import shutil
import os.path
import re
import sys
import os
import stat
import glob


if len(sys.argv) != 3:
    print("USAGE:  {0} [monolithic ITK PATH] [modular ITK PATH]".format(sys.argv[0]))
    sys.exit(-1)

HeadOfITKTree = sys.argv[1];
if (HeadOfITKTree[-1] == '/'):
    HeadOfITKTree = HeadOfITKTree[0:-1]

HeadOfModularITKTree = sys.argv[2];
if (HeadOfModularITKTree[-1] ==  '/'):
    HeadOfModularITKTree = HeadOfModularITKTree[0:-1]

# copy the whole ITK tree over to a tempery dir
HeadOfTempTree ="./ITK_remaining"

if os.path.isdir(HeadOfTempTree):
    shutil.rmtree(HeadOfTempTree)

print("Start to copy" + HeadOfITKTree + " to  ./ITK_remaining ...")
shutil.copytree(HeadOfITKTree,HeadOfTempTree, ignore = shutil.ignore_patterns('.git','.git*'))
print("Done copying!")


# clean up the dirs first
if os.path.isdir(HeadOfModularITKTree):
    print("Warning: The directory {0} exists! It needs to be wiped out first.".format(HeadOfModularITKTree))
    answer = raw_input("Are you sure you want to clean up this directory? [y/n]: " )
    if (answer == 'y'):
       shutil.rmtree(HeadOfModularITKTree)
    else:
       exit()


# read the manifest file
print ("moving files from ./ITK_remaining into modules in {0}".format(HeadOfModularITKTree))
numOfMissingFiles = 0;
missingf =  open('./missingFiles.log','w')
for line in open("./Manifest.txt",'r'):
  # parse the string
  words = line.split()

  if len(words) != 4:
    print "Missing entries at: "+line

  inputfile = HeadOfTempTree+'/'+words[0]
  outputPath = HeadOfModularITKTree+'/'+ words[1]+'/'+words[2]+'/'+words[3]

  # creat the path
  if not os.path.isdir(outputPath):
     os.makedirs(outputPath)

  # copying files to the destination
  if  os.path.isfile(inputfile):
     shutil.move(inputfile, outputPath)
  else:
     missingf.write(inputfile+'\n')
     numOfMissingFiles = numOfMissingFiles + 1;

missingf.close()
print ("listed {0} missing files to ./missingFiles.log").format(numOfMissingFiles)



# list the new files
newf =  open('./newFiles.log','w')
for (root, subDirs, files) in os.walk(HeadOfTempTree):
   for afile in files:
     newf.write(os.path.join(root, afile)+'\n')
newf.close()
print ("listed new files to ./newFiles.log")

###########################################################################
# put the files for modulues
print ('creating cmake files for each module (from the template module)')
groupList =os.listdir(HeadOfModularITKTree);
for groupName in groupList:
    moduleList = os.listdir(HeadOfModularITKTree+'/'+groupName)
    for  moduleName in moduleList:
         # cooy the LICENSE and NOTICE
         shutil.copy('./template_module/LICENSE', HeadOfModularITKTree+'/'+groupName+'/'+moduleName)
         shutil.copy('./template_module/NOTICE',  HeadOfModularITKTree+'/'+groupName+'/'+moduleName)

         # write CMakeLists.txt
         if os.path.isdir(HeadOfModularITKTree+'/'+groupName+'/'+moduleName):
           o = open( HeadOfModularITKTree+'/'+groupName+'/'+moduleName+'/CMakeLists.txt','w')
           for line in open('./template_module/CMakeLists.txt','r'):
               line = line.replace('@itk-module-name@',moduleName)
               o.write(line);
           o.close()

         # write Source/CMakeLists.txt
         # list of CXX files
         cxxFiles = glob.glob(HeadOfModularITKTree+'/'+groupName+'/'+moduleName+'/Source/*.cxx')
         cxxFileList='';
         for cxxf in cxxFiles:
              cxxFileList = cxxFileList+cxxf.split('/')[-1]+'\n'

         if os.path.isdir(HeadOfModularITKTree+'/'+groupName+'/'+moduleName+'/Source'):
           o = open( HeadOfModularITKTree+'/'+groupName+'/'+moduleName+'/Source/CMakeLists.txt','w')
           for line in open('./template_module/Source/CMakeLists.txt','r'):
                line = line.replace('@itk-module-name@',moduleName)
                line = line.replace('@LIST_OF_SOURCE_FILES@',cxxFileList[0:-1]) #get rid of the last \n
                o.write(line);
           o.close()

         # write Testing/CMakeLists.txt
         if os.path.isdir(HeadOfModularITKTree+'/'+groupName+'/'+moduleName+'/Testing'):
           o = open( HeadOfModularITKTree+'/'+groupName+'/'+moduleName+'/Testing/CMakeLists.txt','w')
           for line in open('./template_module/Testing/CMakeLists.txt','r'):
                line = line.replace('@itk-module-name@',moduleName)
                o.write(line);
           o.close()

