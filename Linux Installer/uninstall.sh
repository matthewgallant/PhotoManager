#!/bin/bash

if [ "$EUID" -ne 0 ]
  then echo "Please Run This As Root To Install"
  exit
fi

echo "Removing Binary"
rm /usr/bin/photomanager

echo "Removing Desktop Entry"
rm /usr/share/applications/PhotoManager.desktop

echo "Removing Icon"
rm /usr/share/pixmaps/photomanager.png

echo "Uninstall Completed"
