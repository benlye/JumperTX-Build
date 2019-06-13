# JumperTX-Build
A Docker container for building [JumperTX](https://github.com/JumperXYZ/JumperTX), the firmware for the [Jumper T16](https://www.jumper.xyz/jumpertx-t16) radio.

[![Build Status](https://travis-ci.org/benlye/JumperTX-Docker.svg?branch=master)](https://travis-ci.org/benlye/JumperTX-Docker)

# Instructions
1. Install Docker
1. Clone the JumperTX repository:

   `git clone --recursive https://github.com/JumperXYZ/JumperTX.git`
   
1. Pull the container:

   `docker pull benlye/jumpertx-build`
   
1. Run the container, specifying the path to the JumperTX source as a mount volume:

   `docker run --rm -it -v [JumperTX Source Path]:/jumpertx benlye/jumpertx-build`
   
   For example (Windows):
   
   `docker run --rm -it -v "C:/Users/benlye/Github/JumperTX:/jumpertx" benlye/jumpertx-build`
   
   Or (Linux):
   
   `docker run --rm -it -v "/home/benlye/github/JumperTX:/jumpertx" benlye/jumpertx-build`

The compiled firmware image, `jumpertx-t16.bin`, will be placed in the root of the source directory when the build has finished.

## Changing the build flags
Build flags can be changed by passing a switch to the Docker container when it is run.

The syntax is `-e "CMAKE_FLAGS=FLAG1=VALUE1 FLAG2=VALUE2"`.

Default flags will be replaced by the new value, additional flags will be appended.

### Examples
1. Build from the source in `C:\Users\benlyeGithub\JumperTX` and disable `HELI`:

   `docker run --rm -it -v "C:/Users/benlye/Github/JumperTX:/jumpertx" -e "CMAKE_FLAGS=HELI=NO" benlye/jumpertx-build`

1. Build from the source in `C:\Users\benlyeGithub\JumperTX`, disabling `HELI` and passing a new flag:

   `docker run --rm -it -v "C:/Users/benlye/Github/JumperTX:/jumpertx" -e "CMAKE_FLAGS=HELI=NO FOO=BAR" benlye/jumpertx-build`

