#! /bin/bash

if [ ! -f '/jumpertx/CMakeLists.txt' ]; then
    echo
    echo "ERROR: JumperTX source not found in /jumpertx. Did you specifiy a valid mount?"
    echo
    exit
fi

# Copy the mounted source to /tmp (3x faster than compiling against the mount)
echo
echo "Copying source to temporary build directory..."
echo
cp -r /jumpertx /tmp/jumpertx

# Move to the build directory
cd /build

echo "Extra CMAKE Flags: $*"
echo

python /build/build_firmware.py $*

echo "Done."
echo

