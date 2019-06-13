#!/usr/bin/env python

from __future__ import print_function
import os
import sys
import subprocess
import shutil
import time
from collections import OrderedDict

# Show a header
print("")
print("JumperTX-Build - https://hub.docker.com/r/benlye/jumpertx-build")
print("")

# Specify some paths for the build
build_dir = "/build"
source_dir = "/tmp/jumpertx"
output_dir = "/jumpertx"
output_filename = "jumpertx"
output_extension = ".bin"

# Maximum size for the compiled firmware
t16_max_size = 2 * 1024 * 1024

# Default T16 cmake flags
t16_default_options = OrderedDict([
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

# Check that the source is valid
if not os.path.exists("/jumpertx/CMakeLists.txt"):
    print("ERROR: JumperTX source not found in /jumpertx. Did you specifiy a valid mount?")
    print("")
    exit(5)

# Parse the extra options from the command line
extra_options = OrderedDict()
if len(sys.argv) > 1:
    for i in range(1,len(sys.argv)):
        opt, val = sys.argv[i].split("=")
        extra_options[opt] = val

    # Print the CMAKE flags from the Docker command line
    print ("Container CMAKE flags: %s" % " ".join(sys.argv[1:]))
else:
    print ("No additional CMAKE flags specified.")

# If specified, get the PCB from the flags; default to the T16
board = "T16"
if "PCB" in extra_options:
    board = extra_options["PCB"].upper()

# Get the board defaults
if board == "T16" or board == "T16HD":
    default_options = t16_default_options
    max_size = t16_max_size
else:
    print("ERROR: Invalid board (%s) specified. Valid boards are T16 and T16HD." % board)
    print("")
    exit(3)

# Compare the extra options to the board's defaults
extra_command_options = OrderedDict()
flagchanges = False
for ext_opt, ext_value in extra_options.items():
    found = False
    for def_opt, def_value in default_options.items():
        if ext_opt == def_opt:
            found = True
            break

    if found:
        if ext_value != def_value:
            default_options[def_opt] = ext_value
            print ("Overriding default flag: %s=%s => %s=%s" % (def_opt, def_value, def_opt, ext_value))
        else:
            if def_opt != "PCB":
                print ("Override for default flag matches default value: %s=%s" % (def_opt, def_value))
    else:
        print ("Adding additional flag: %s=%s" % (ext_opt, ext_value))
        extra_command_options[ext_opt] = ext_value

# Start the timer
start = time.time()

# Change to the build directory
os.chdir(build_dir)

# Copy the source tree to the temporary folder - makes build 3x faster than building against the mount on Windows
print("")
print ("Copying source from /jumpertx to /tmp/jumpertx ...")
print("")
shutil.copytree("/jumpertx", "/tmp/jumpertx")

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

print(" ".join(cmd))
print("")

# Launch cmake
proc = subprocess.Popen(cmd)
proc.wait()

# Exit if cmake errored
if proc.returncode != 0:
    print("")
    print("ERROR: cmake configuration failed.")
    print("")
    exit(2)

# Launch make with two threads
proc = subprocess.Popen(["make", "-j2", "firmware"])
proc.wait()

# Exit if make errored
if proc.returncode != 0:
    print("")
    print("ERROR: make compilation failed.")
    print("")
    exit(2)

# Stop the timer
end = time.time()

# Append the PCB type to the output file name
output_filename = output_filename + "-" + default_options["PCB"].lower()

# Get the firmware version
stampfile = "radio/src/stamp.h"
for line in open(stampfile):
 if "#define VERSION " in line:
   firmware_version = line.split()[2].replace('"','')

# Append the version to the output file name
if firmware_version:
    output_filename = output_filename + "-" + firmware_version

# Append the language to the output file name if one is specified
if "TRANSLATIONS" in extra_command_options:
    output_filename = output_filename + "-" + extra_command_options["TRANSLATIONS"].lower()

# Append the extension to the output file name
output_filename = output_filename + output_extension

# Assemble the output path
output_path = os.path.join(output_dir, output_filename)

# Move the new binary to the output path
shutil.move("firmware.bin", output_path)

# Get the size of the binary
binsize = os.stat(output_path).st_size

# Print out the file name and size
print("")
print("Build completed in {0:.1f} seconds.".format((end-start)))
print("")
print("Firmware file: %s" % (output_path))
print("Firmware size: {0}KB ({1:.0%})".format(binsize/1024, float(binsize)/float(max_size)))
print("")

# Exit with an error if the firmware is too big
if binsize > max_size:
    print("ERROR: Firmware is too large for radio.")
    print("")
    exit(1)

# Exit with success result code
exit(0)
