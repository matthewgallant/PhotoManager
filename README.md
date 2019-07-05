![PhotoManager](/screenshot.png)

# Photo Manager

A simple way to comb through large photo sets.

## About
I originally built this as a tool for combing through large datasets for deep learning. This tool has helped me to very quickly and efficiently choose what images I want my training algorithm to work on.

## Features
This program is pretty barebones, but it works very well. The only real feature to speak of is the abiity to resize the image viewing window to be whatever size you need it to be. Other than that, the program just works.

## How to Run It
__Update__: macOS Binaries are available for download [here](https://github.com/MatthewGallant/PhotoManager/releases). Windows binaries coming soon. The instructions below are only for running from source.

All you need is a copy of Python 3 installed on your system. This program should be cross-platform compatible, but has only been tested on macOS 10.14 Mojave. The application requires no outside dependencies beside PyQT5 and is just one file. I built this application with extreme portability in mind. Everything even down to the icons are encoded in that one file.

## Extra: How to Compile The Binaries
I've included one .sped file for macOS. You will need to run this using [PyInstaller](https://pyinstaller.readthedocs.io). You will also need to modify one of the lines in the file to match your build path.