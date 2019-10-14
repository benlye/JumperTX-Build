# JumperTX-Build
![Travis CI Status](https://travis-ci.org/benlye/JumperTX-Build.svg?branch=master)
![Docker Stars](https://img.shields.io/docker/stars/benlye/jumpertx-build.svg)
![Docker Pulls](https://img.shields.io/docker/pulls/benlye/jumpertx-build.svg)

A Docker container for building [JumperTX](https://github.com/JumperXYZ/JumperTX), the firmware for the [Jumper T16](https://www.jumper.xyz/portal.php?mod=view&aid=13) and [Jumper T12](https://www.jumper.xyz/portal.php?mod=view&aid=14) radio.

The container contains a Debian Linux image pre-configured with the tools required to build JumperTX.  Running the container will compile the firmware from a local source tree and produce a compiled firmware image.

# Instructions
## Setup
1. [Install Docker](https://docs.docker.com/install/)
   * If installing on Windows choose **Linux Containers** when prompted
   
1. Pull the container:

   `docker pull benlye/jumpertx-build`

1. Clone the JumperTX repository:

   `git clone --recursive https://github.com/JumperXYZ/JumperTX.git`

## Modify the Firmware
Use your tool of choice to make changes to the JumperTX source.

([Visual Studio Code](https://code.visualstudio.com/download) is a good option).

## Build the Firmware
1. Run the container, specifying the path to the JumperTX source as a mount volume:

   `docker run --rm -it -v [JumperTX Source Path]:/jumpertx benlye/jumpertx-build`
   
   For example (Windows):
   
   `docker run --rm -it -v "C:/Users/benlye/Github/JumperTX:/jumpertx" benlye/jumpertx-build`
   
   Or (Linux):
   
   `docker run --rm -it -v "/home/benlye/github/JumperTX:/jumpertx" benlye/jumpertx-build`

The compiled firmware image will be placed in the root of the source directory when the build has finished.  

The default output name is `jumpertx-t16-2.2.3-en.bin` but this will vary depending on any optional flags that may have been passed.  The format is `jumpertx-[PCB]-[version]-[language].bin`.

## Changing the Build Flags
Build flags can be changed by passing a switch to the Docker container when it is run.

The syntax is `-e "CMAKE_FLAGS=FLAG1=VALUE1 FLAG2=VALUE2"`.

Default flags will be replaced by the new value, additional flags will be appended.

### Examples
1. Build from the source in `C:\Users\benlyeGithub\JumperTX` and enable support for R9 Flex:

   `docker run --rm -it -v "C:/Users/benlye/Github/JumperTX:/jumpertx" -e "CMAKE_FLAGS=MODULE_R9M_FLEX_FW=YES" benlye/jumpertx-build`

1. Build from the source in `C:\Users\benlyeGithub\JumperTX` and disable `HELI`:

   `docker run --rm -it -v "C:/Users/benlye/Github/JumperTX:/jumpertx" -e "CMAKE_FLAGS=HELI=NO" benlye/jumpertx-build`

1. Build from the source in `C:\Users\benlyeGithub\JumperTX`, disabling `HELI` and passing a new flag:

   `docker run --rm -it -v "C:/Users/benlye/Github/JumperTX:/jumpertx" -e "CMAKE_FLAGS=HELI=NO FOO=BAR" benlye/jumpertx-build`

## Setting PCB board
The default PCB board is Jumper T16, changing to alternative PCB board by setting the `PCB=` CMAKE flag with a valid PCB code.

### Example:
1. Build from the source in `C:\Users\benlyeGithub\JumperTX` for Jumper T12:
    `docker run --rm -it -v "C:/Users/benlye/Github/JumperTX:/jumpertx" -e "CMAKE_FLAGS=PCB=T12" benlye/jumpertx-build`

## Changing the Language
The default language is English.  Alternative languages can by setting the `TRANSLATIONS=` CMAKE flag with a valid language code.

Valid language codes are: 
* EN (English) 
* FR (French) 
* SE (Swedish)
* IT (Italian)
* CZ (Czech)
* DE (German)
* PT (Portugese)
* ES (Spanish)
* PL (Polish)
* NL (Dutch)

### Example: 
1. Build from the source in `C:\Users\benlyeGithub\JumperTX` with the language set to German:

   `docker run --rm -it -v "C:/Users/benlye/Github/JumperTX:/jumpertx" -e "CMAKE_FLAGS=TRANSLATIONS=DE" benlye/jumpertx-build`
