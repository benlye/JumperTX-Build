# JumperTX-Build
A Docker container for building [JumperTX](https://github.com/JumperXYZ/JumperTX), the firmware for the [Jumper T16](https://www.jumper.xyz/jumpertx-t16) radio.

[![Build Status](https://travis-ci.org/benlye/JumperTX-Build.svg?branch=master)](https://travis-ci.org/benlye/JumperTX-Build)

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

The compiled firmware image will be placed in the root of the source directory when the build has finished.  

The default output name is `jumpertx-t16-2.2.3-en.bin` but this will vary depending on any optional flags that may have been passed.  The format is `jumpertx-[PCB]-[version]-[language].bin`.

## Languages
The default language is English.  Alternative languages can by setting the `TRANSLATIONS=` CMAKE flag with a valid language code.

Valid language codes are: EN (English), FR (French), SE (Swedish), IT (Italian), CZ (Czech), DE (German), PT (Portugese), ES (Spanish), PL (Polish), NL (Dutch).

## Changing the build flags
Build flags can be changed by passing a switch to the Docker container when it is run.

The syntax is `-e "CMAKE_FLAGS=FLAG1=VALUE1 FLAG2=VALUE2"`.

Default flags will be replaced by the new value, additional flags will be appended.

### Examples
1. Build from the source in `C:\Users\benlyeGithub\JumperTX` and disable `HELI`:

   `docker run --rm -it -v "C:/Users/benlye/Github/JumperTX:/jumpertx" -e "CMAKE_FLAGS=HELI=NO" benlye/jumpertx-build`

1. Build from the source in `C:\Users\benlyeGithub\JumperTX`, disabling `HELI` and passing a new flag:

   `docker run --rm -it -v "C:/Users/benlye/Github/JumperTX:/jumpertx" -e "CMAKE_FLAGS=HELI=NO FOO=BAR" benlye/jumpertx-build`

1. Build from the source in `C:\Users\benlyeGithub\JumperTX` with the language set to German:

   `docker run --rm -it -v "C:/Users/benlye/Github/JumperTX:/jumpertx" -e "CMAKE_FLAGS=TRANSLATIONS=DE" benlye/jumpertx-build`
