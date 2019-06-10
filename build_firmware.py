#!/usr/bin/env python

from __future__ import print_function
import os
import sys
import subprocess
import shutil
from collections import OrderedDict

# Specify some paths for the build
build_dir = "/build"
source_dir = "/tmp/jumpertx"
output_dir = "/jumpertx"
output_filename = "jumpertx-t16.bin"
output_path = os.path.join(output_dir, output_filename)

# Maximum size for the compiled firmware
max_size = 2 * 1024 * 1024

# Default T16 cmake flags
default_options = OrderedDict([
    ("PCB", "T16"),
    ("GUI", "YES"),
    ("GVARS", "YES"),
    ("HELI", "YES"),
    ("LCD_DUAL_BUFFER", "YES"),
    ("LUA", "YES"),
    ("LUA_COMPILER", "YES"),
    ("MODULE_R9M_FULLSIZE", "YES"),
    ("MULTIMODULE", "YES"),
    ("PPM_CENTER_ADJUSTABLE", "YES"),
    ("PPM_UNIT", "US"),
    ("RAS", "YES"),
    ("DISABLE_COMPANION", "YES"),
    ("CMAKE_BUILD_TYPE", "Release")
])

# Parse the extra options from the command line
extra_options = OrderedDict()
if len(sys.argv) > 1:
    for i in range(1,len(sys.argv)):
        opt, val = sys.argv[i].split("=")
        extra_options[opt] = val

# Compare the extra options to the defaults
extra_command_options = OrderedDict()
for ext_opt, ext_value in extra_options.items():
    found = False
    for def_opt, def_value in default_options.items():
        if ext_opt == def_opt:
            found = True
            break

    if found:
        if ext_value != def_value:
            default_options[def_opt] = ext_value;
            print ("Overriding default flag: %s=%s => %s=%s" % (def_opt, def_value, def_opt, ext_value))
        else:
            print ("Override for default flag matches default value: %s=%s" % (def_opt, def_value))
    else:
        print ("Adding additional flag: %s=%s" % (ext_opt, ext_value))
        extra_command_options[ext_opt] = ext_value

# Remove any existing output file
if os.path.isfile(output_path):
    print("")
    print("Removing existing firmware file '%s'" % (output_path))
    os.remove(output_path)

# Change to the build directory
os.chdir(build_dir)

# Prepare the cmake command
cmd = ["cmake"]

# Append the default flags
for opt, value in default_options.items():
    cmd.append("-D%s=%s" % (opt, value))

# Append the extra flags
for opt, value in extra_command_options.items():
    cmd.append("-D%s=%s" % (opt, value))

# Append the source directory
cmd.append(source_dir)

# Output the cmake command line
print("")
print(" ".join(cmd))
print("")

# Launch cmake
proc = subprocess.Popen(cmd)
proc.wait()

# Exit if cmake errored
if proc.returncode != 0:
    print("cmake compilation error!")
    print("")
    exit(2)
    
# Launch make with two threads
proc = subprocess.Popen(["make", "-j2", "firmware"])
proc.wait()

# Exit if make errored
if proc.returncode != 0:
    print("make compilation error!")
    print("")
    exit(2)

# Copy binary to the output path
shutil.move("firmware.bin", output_path)

# Get the size of the binary
binsize = os.stat(output_path).st_size

# Print out the file name and size
print("")
print("Firmware file: %s" % (output_path))
print("Firmware size: {0}KB ({1:.0%})".format(binsize/1024, float(binsize)/float(max_size)))
print("")

# Exit with an error if the firmware is too big
if binsize > max_size:
    exit(1)

# Exit with success result code
exit(0)
