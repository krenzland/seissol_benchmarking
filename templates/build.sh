#!/usr/bin/env bash
#cp -r {{ build_root}} ./tmp

# TODO: Maybe pass tmp dir and reuse?
mkdir tmp
ls

cd tmp 
ls
#scons buildVariablesFile=build/options/marenostrum4.py hdf5=yes netcdf=no order={{ order }} metis=yes commThread=true compileMode=release hdf5Dir=/dss/dsshome1/lrz/sys/spack/release/19.1/opt/x86_avx512/hdf5/1.8.20-intel-6z7sqju -j56 arch='dskx'
CC=mpiicc CXX=mpiicpc FC=mpiifort CMAKE_PREFIX_PATH=~:$CMAKE_PREFIX_PATH PKG_CONFIG_PATH=~/lib/pkgconfig/:$PKG_CONFIG_PATH cmake -DNETCDF=ON -DMETIS=ON -DCOMMTHREAD=ON --DHDF5=ON -DCMAKE_BUILD_TYPE=Release -DTESTING=OFF  -DLOG_LEVEL=warning -DLOG_LEVEL_MASTER=info -DHOST_ARCH=skx -DPRECISION=double -DASAGI=ON -DORDER={{ order }} -- {{ build_root }}
make -j 48 SeisSol-bin

cd ..
execName="$(find . -executable -print0 | xargs -r -0 ls -1 -t | head -1)" # newest file
echo $execName
cp ${execName} {{ executable_name }}
rm -rf tmp
