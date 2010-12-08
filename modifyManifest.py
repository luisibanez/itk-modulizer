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

# This mini script finds the .h and .txx files and put them into include directory

import sys
import os

newManifest = open('./newManifest.txt','w')

for line in open("./Manifest.txt",'r'):
  # skip the comments
  if line[0] != '#':
      # parse the string
      words = line.split()
      if words[0][-2:] == '.h':
         words[3]='include'
      if words[0][-4:] == '.txx':
         words[3]='include'
      line=words[0]+' '+words[1]+' '+words[2]+' '+words[3]+'\n'
  newManifest.write(line);

newManifest.close()

