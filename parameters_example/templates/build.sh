#!/usr/bin/env bash
mkdir tmp
ls

cd tmp 
ls
#CC=mpiicc CXX=mpiicpc FC=mpiifort CMAKE_PREFIX_PATH=~:$CMAKE_PREFIX_PATH PKG_CONFIG_PATH=~/lib/pkgconfig/:$PKG_CONFIG_PATH cmake -DNETCDF=ON -DMETIS=ON -DCOMMTHREAD=ON --DHDF5=ON -DCMAKE_BUILD_TYPE=Release -DTESTING=OFF  -DLOG_LEVEL=warning -DLOG_LEVEL_MASTER=info -DHOST_ARCH=skx -DPRECISION=double -DASAGI=ON -DORDER={{ order }} -- {{ build_root }}
#make -j 48 SeisSol-bin
touch SeisSol
chmod +x SeisSol

cd ..
execName="$(find . -executable -print0 | xargs -r -0 ls -1 -t | head -1)" # newest file
echo $execName
cp ${execName} {{ executable_name }}
rm -rf tmp
