#!/bin/bash

if [ "$EUID" -ne 0 ]
  then echo "Please Run This As Root To Install"
  exit
fi

echo "Copying Binary"
cp photomanager /usr/bin/

echo "Copying Desktop Entry"
cp photomanager.desktop /usr/share/applications/

echo "Copying Icon"
cp photomanager.png /usr/share/pixmaps/

echo "Setting Execute Permission For Binary"
chmod +x /usr/bin/photomanager

echo "Install Completed"
echo "You may need to logout and back in again for PhotoManager to appear in your apps."

