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
# This script is used to automate the modulization process. The following
# steps  are included:
# 1. Move the files in the monolithic ITK into modules of the modularized ITK.
#    A manifest text file that lists all the files and their destinations is
#    reuiqired to run the script.By default, the manifest file is named as
#    "Manifest.txt" in the  same directory of this script.
# 2. Create CMake Files and put them into modules.



# To run it, type ./modulizer.py  ITK_PATH  ModularITK_PATH   from
# the itk-modulizer root directory.

print "*************************************************************************"
print "WARNINGs! This modularization script is still in its experiemntal stage."
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
HeadOfModularITKTree = sys.argv[2];

# copy the whole ITK tree over to a tempery dir
HeadOfTempTree ="./ITK"

if os.path.isdir(HeadOfTempTree):
    shutil.rmtree(HeadOfTempTree)

print ("start to copy"+HeadOfITKTree+" to ./ITK ...")
shutil.copytree(HeadOfITKTree,HeadOfTempTree, ignore = shutil.ignore_patterns('.git','.git*'))
print ("done copying")

# clean up the dirs first
if os.path.isdir(HeadOfModularITKTree):
    shutil.rmtree(HeadOfModularITKTree)


# read the manifest file
print ("moving files from ./ITK into modules")
numOfMissingFiles = 0;
missingf =  open('./missingFiles.log','w')
for line in open("./Manifest.txt",'r'):
  # parse the string
  words = line.split()
  inputfile = HeadOfTempTree+'/'+words[0]
  outputPath=HeadOfModularITKTree+'/'+ words[1]+'/'+words[2]+'/'+words[3]

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


# detect new files: what's left in HeadOfTempTree

# go through the directory tree
def walktree (top = ".", depthfirst = True):
    names = os.listdir(top)
    if not depthfirst:
        yield top, names
    for name in names:
        try:
            st = os.lstat(os.path.join(top, name))
        except os.error:
            continue
        if stat.S_ISDIR(st.st_mode):
            for (newtop, children) in walktree (os.path.join(top, name), depthfirst):
                yield newtop, children
    if depthfirst:
        yield top, names

# list the new files
newf =  open('./newFiles.log','w')
for (basepath, children) in walktree(HeadOfTempTree,False):
    for child in children:
     newf.write(os.path.join(basepath, child)+'\n')
newf.close()
print ("listed new files to ./newFiles.log")



###########################################################################
# put the files for modulues
groupList =os.listdir(HeadOfModularITKTree);
for groupName in groupList:
    moduleList = os.listdir(HeadOfModularITKTree+'/'+groupName)

    for  moduleName in moduleList:
         print ('creating files in {0}'.format(moduleName))
         # cooy the LICENSE and NOTICE
         shutil.copy('./template_module/LICENSE', HeadOfModularITKTree+'/'+groupName+'/'+moduleName)
         shutil.copy('./template_module/NOTICE',  HeadOfModularITKTree+'/'+groupName+'/'+moduleName)

         # write CMakeLists.txt
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
         o = open( HeadOfModularITKTree+'/'+groupName+'/'+moduleName+'/Source/CMakeLists.txt','w')
         for line in open('./template_module/Source/CMakeLists.txt','r'):
              line = line.replace('@itk-module-name@',moduleName)
              line = line.replace('@LIST_OF_SOURCE_FILES@',cxxFileList)
              o.write(line);
         o.close()

         # write Testing/CMakeLists.txt
         #o = open( HeadOfModularITKTree+'/'+groupName+'/'+moduleName+'/Testing/CMakeLists.txt','w')
         #for line in open('./template_module/Testing/CMakeLists.txt','r'):
         #     line = line.replace('@itk-module-name@',moduleName)
         #     o.write(line);
         #o.close()



