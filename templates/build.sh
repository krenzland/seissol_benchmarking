#!/usr/bin/env bash
echo "Building..."
exit 0

cp -r {{ build_root}} ./tmp
ls

cd tmp 
ls
scons buildVariablesFile=build/options/marenostrum4.py hdf5=yes netcdf=no order={{ order }} metis=yes commThread=true compileMode=release hdf5Dir=/dss/dsshome1/lrz/sys/spack/release/19.1/opt/x86_avx512/hdf5/1.8.20-intel-6z7sqju -j56 arch='dhsw'


cd ..
execName="$(find . -executable -print0 | xargs -r -0 ls -1 -t | head -1)" # newest file
echo $execName
cp ${execName} {{ executable_name }}
rm -rf tmp
