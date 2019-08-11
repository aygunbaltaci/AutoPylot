# Python Plotter

README description to be added 

Dependency: basemap: https://stackoverflow.com/questions/53223703/installing-basemap-with-python3-6-on-ubuntu-18-04
	Then, install basemap: 
		pip3 install --upgrade --user matplotlib numpy pyproj pyshp OWSLib Pillow
		sudo apt install libgeos-dev
		pip3 install --user --upgrade basemap-1.2.0rel.zip # located in plotting2/ dir.
Uninstall pyproj 2.2.1 https://github.com/matplotlib/basemap/issues/457
	pip3 uninstall pyproj 2.2.1
Install pyproj 1.9.6
	pip3 install pyproj==1.9.6
	
Make sure to set up the proxy settings for arcgisserver (for map plots)

Features to add:
	1. Multiple color support for box plot
	2. Slider functionality to graphs when plotting from functions
	3. Add multiple variable support for plotting from given functions (in 2D graphs)
	