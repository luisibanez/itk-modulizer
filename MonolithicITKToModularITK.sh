#!/bin/bash
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
#==========================================================================*/
# This script is used to move the files in the monolithic ITK into modules of the  modularized ITK.
# A manifest text file that lists all the files and their destinations is reuiqired to run the script.
# By default, the manifest file is named as "Manifest.txt" in the  same directory of this script.

# To run it, just type "./MonolithicITKToModularITk.sh"  in your shell terminal from
# the itk-modulizer root directory.

echo "*************************************************************************"
echo "WARNINGs! This modularization script is still in its experiemntal stage."
echo "Current ITK users should NOT run this script."
echo "This bash script  will move the files from the monolithick ITK to  new "
echo "directories of modular ITK according to a mannually created manifest file,"
echo "which lists the files and their new locations."
echo "*************************************************************************"


read -p "Is your current directoy the modulizer root directory (y/n)?"
[ "$REPLY" == "n" ] && echo "please go to the modulizer root directory first"  && exit 1 || echo "good to go"

echo "Please enter the path of the modular ITK directory (default is the current directory by pressing [ENTER] only) No "/" at the end, please:"
read modularITKRoot

echo "Please enter the path of the monolithic/original ITK directory and press [ENTER]) No \"/\" at the end, please:"
read ITKRoot

if [ "$modularITKRoot" == "" ];then
  modularITKRoot="./modularITK"
fi
echo "Files will be moved to: $modularITKRoot"


while read line
  do echo $line

  # parse input and output
    inputFile=$ITKRoot"/"$(echo "$line"| awk  '{print $1}')
  echo "Input File : $inputFile"
  outputDir=$modularITKRoot"/"$(echo "$line"| awk  '{print $2"/"$3"/"$4}')
  echo "Output Directory : $outputDir"

  # make sure output path exists
  if [ ! -d "$outputDir" ]
    then
    echo "create directory: $outputDir"
    echo "create directory: $outputDir" >> ./createdDirectories.log
    mkdir -p "$outputDir"
  fi

  # make sure input file exists
  if [ -r "$inputFile" ]
    then
    mv  "$inputFile"  "$outputDir"
    echo "moved $inputFile to $outputDir" >> ./movedFiles.log
  else #input file missing
    echo "$inputFile is missing" > ./missingFiles.log
  fi

done < ./Manifest.txt

# new added files? (residual files in the root)
find  "$ITKRoot/Code" -type f  \( ! -iname ".*" \) -print > ./newFiles.log
