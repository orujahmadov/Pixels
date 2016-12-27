#!/bin/bash
echo "Creating a setup.py file..."
py2applet --make-setup wallpaper.py
echo "Cleaning up build directories..."
rm -rf build dist
echo "Building for development..."
python setup.py py2app
