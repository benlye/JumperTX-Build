# JumperTX-Docker
A Docker container for building JumperTX for the Jumper T16 radio

[![Build Status](https://travis-ci.org/benlye/JumperTX-Docker.svg?branch=master)](https://travis-ci.org/benlye/JumperTX-Docker)

# Instructions
1. Install Docker
1. Clone the JumperTX repository:

   `git clone --recursive https://github.com/JumperXYZ/JumperTX.git`
   
1. Pull the container:

   `docker pull benlye/jumpertx-build`
   
1. Run the container, specifying the path to the JumperTX repo as a mount volume:

   `docker run --rm -it -v [JumperTX Source Path]:/jumpertx benlye/jumpertx-build`
   
   For example:
   
   `docker run --rm -it -v "C:/Users/benlye/Github/JumperTX:/jumpertx" benlye/jumpertx-build`
   
   Or:
   
   `docker run --rm -it -v "/home/benlye/github/JumperTX:/jumpertx" benlye/jumpertx-build`

When finished the compiled firmware, `firmware.bin` will be in the root of the source directory.
