#!/usr/bin/env bash
cp -r /home/ga24dib/src/SeisSol-Coupling ./tmp
ls

cd tmp 
ls
CPPPATH=~/include/ LD_LIBRARY_PATH="/home/ga24dib/lib:${LD_LIBRARY_PATH}" PKG_CONFIG_PATH="/home/ga24dib/lib/pkgconfig/:${PKG_CONFIG_PATH}" scons buildVariablesFile=build/options/supermuc2.py order={{ order }} compiler=intel netcdf=yes hdf5=yes metis=yes asagi=yes zlibDir=~/src/ASAGI/build/lib/ compileMode=relWithDebInfo commThread=false equations=elastic -j12

cd ..
execName="$(find . -executable -print0 | xargs -r -0 ls -1 -t | head -1)" # newest file
echo $execName
cp ${execName} {{ executable_name }}
rm -rf tmp
