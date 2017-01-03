#!/bin/bash
echo "Creating a setup.py file..."
py2applet --make-setup /Users/orujahmadov/Desktop/Pixels/pixels.py
echo "Cleaning up build directories..."
rm -rf /Users/orujahmadov/Desktop/Pixels/build /Users/orujahmadov/Desktop/Pixels/dist
echo "Building for development..."
python /Users/orujahmadov/Desktop/Pixels/setup.py py2app
