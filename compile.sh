#!/bin/bash
echo "Deleting previous setup.py file..."
rm -rf ~/Desktop/Pixels/setup.py
echo "Creating a new setup.py file..."
py2applet --make-setup ~/Desktop/Pixels/Pixels.py
echo "Cleaning up build directories..."
rm -rf ~/Desktop/Pixels/build /Users/orujahmadov/Desktop/Pixels/dist
echo "Building for development..."
python ~/Desktop/Pixels/setup.py py2app
