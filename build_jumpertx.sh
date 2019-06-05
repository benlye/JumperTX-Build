#! /bin/bash

if [ ! -f '/jumpertx/CMakeLists.txt' ]; then
    echo
    echo "ERROR: JumperTX source not found in /jumpertx. Did you specifiy a valid mount?"
    echo
    exit
fi

# Copy the mounted source to /tmp (3x faster than compiling against the mount)
echo "Copying source to temporary build directory..."
cp -r /jumpertx /tmp/jumpertx

# Move to the build directory
cd /build

# Run cmake to configure the build using the standard command for the T16
echo "Configuring..."
cmake -DPCB=T16 -DGUI=YES -DGVARS=YES -DHELI=YES -DLCD_DUAL_BUFFER=YES -DLUA=YES -DLUA_COMPILER=YES -DMODULE_R9M_FULLSIZE=YES -DMULTIMODULE=YES -DPPM_CENTER_ADJUSTABLE=YES -DPPM_UNIT=US -DRAS=YES -DDISABLE_COMPANION=YES -DCMAKE_BUILD_TYPE=Release /tmp/jumpertx

# Compile the firmware
echo "Compiling..."
make -j2 firmware

# Copy the buld back to the source path
echo "Copying compiled firmware to source tree..."
cp -r /build/firmware.bin /jumpertx/

echo
echo "Done."
echo
