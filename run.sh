#!/usr/bin/zsh
./modulizer.py    \
/home/ibanez/src/ITK/    \
/home/ibanez/src/ModularITK/modular

grep -v Wrapping newFiles.log | \
grep -v Utilities | \
grep -v Validation | \
grep -v Examples | \
grep -v Testing | \
grep -v Review | \
grep -v CMake | \
grep -v Documentation | \
tee  filesToClassify.log

wc Manifest.txt
wc filesToClassify.log
wc missingFiles.log
