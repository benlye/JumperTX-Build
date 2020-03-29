# A Debian image for compiling JumperTX 2.2
FROM debian:stretch

# Update and install the required components
RUN DEBIAN_FRONTEND=noninteractive apt-get -y update && apt-get -y install wget zip bzip2 cmake build-essential python3 python3-pil git lib32ncurses5 libgtest-dev clang-7 python3-pip
RUN pip3 install clang

# Retrieve and install the required version of the ARM compiler
RUN wget https://launchpad.net/gcc-arm-embedded/4.7/4.7-2013-q3-update/+download/gcc-arm-none-eabi-4_7-2013q3-20130916-linux.tar.bz2 -P /tmp --progress=bar:force
RUN tar -C /tmp -xjf /tmp/gcc-arm-none-eabi-4_7-2013q3-20130916-linux.tar.bz2
RUN mv /tmp/gcc-arm-none-eabi-4_7-2013q3 /opt/gcc-arm-none-eabi
RUN rm /tmp/gcc-arm-none-eabi-4_7-2013q3-20130916-linux.tar.bz2

# Declare the mount point
VOLUME ["/jumpertx"]

# Set the working directory to /build
WORKDIR /build

# Add the build scripts
COPY build_firmware.py /build

# Update the path
ENV PATH $PATH:/opt/gcc-arm-none-eabi/bin:/jumpertx/radio/util

# Make Python3 the default
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3 10

# Run the shell script to build the firmware
CMD ["bash", "-c", "python /build/build_firmware.py $CMAKE_FLAGS"]
