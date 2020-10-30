#!/bin/bash

if [ "$EUID" -ne 0 ]
  then echo "Please Run This As Root To Uninstall"
  exit
fi

echo "Removing Binary"
rm /usr/bin/photomanager

echo "Removing Desktop Entry"
rm /usr/share/applications/photomanager.desktop

echo "Removing Icon"
rm /usr/share/pixmaps/photomanager.png

echo "Uninstall Completed"
