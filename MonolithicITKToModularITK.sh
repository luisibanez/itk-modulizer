#!/bin/bash

# Author: Xiaoxiao Liu (xiaoxiao.liu@kitware.com)
# Date:11/11/2010

# This script is used to move the files in the monolithic ITK into modules of the  modularized ITK.
# A manifest text file that lists all the files and their destinations is reuiqired to run the script.
# By default, the manifest file is named as "Manifest.txt" in the  same directory of this script.

# To run it, just type "./Modularization/MonolithicITKToModularITk.sh"  in your shell terminal from
# ITK root directory.

echo "*************************************************************************"
echo "WARNINGs! This modularization script is still in its experiemntal stage."
echo "Current ITK users should NOT run this script."
echo "This bash script  will move the files from the monolithick ITK to  new "
echo "directories of modular ITK according to a mannually created manifest file,"
echo "which lists the files and their new locations."
echo "*************************************************************************"


read -p "Is your current directoy the modulizer root directory (y/n)?"
[ "$REPLY" == "n" ] && echo "please go to the modulizer root directory first"  && exit 1 || echo "good to go"

echo "Please enter the path of the modular ITK directory (default is the current directory by pressing [ENTER] only):"
read modularITKRoot

echo "Please enter the path of the monolithic/original ITK directory and press [ENTER]):"
read ITKRoot

if [ "$modularITKRoot" == "" ];then
  modularITKRoot="./modularITK"
fi
echo "Files will be moved to: $modularITKRoot"


while read line
  do echo $line

  #parse input and output
  inputFile=$ITKRoot"/"$(echo "$line"| awk  '{print $1}')
  echo "$inputFile"
  outputDir=$modularITKRoot"/"$(echo "$line"| awk  '{print $2"/"$3"/"$4}')

  #make sure input file exists and output path exsits
  if test -e "$inputFile";then
    if test -d "$outputDir";then
       mv  $inputFile  $outputDir
    else
      echo "create directory:$outputDir"
      mkdir -p $outputDir
      mv  $inputFile  $outputDir
    fi
  else #input file missing
    echo "$inputFile is missing" > ./missingFiles.log
  fi

done < ./Manifest.txt

# new added files? (residual files in the root)
find  $ITKRoot/Code -type f  \( ! -iname ".*" \) -print > ./newFiles.log
