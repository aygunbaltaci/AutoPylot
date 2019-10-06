# Python Plotter

![Alt text](supportedPlots.png?raw=true "PythonPlotter")

This program is an automized tool to provide a plotting platform with many features based on python matplotlib library. Whether you have sets of data or math functions to be plotted, this program can be utilized to plot your graphs without needing to write a python program. 
The program takes csv file as input and provides the plots by asking questions to the user. It is a user-interactive program to provide the highest level of flexibility to the user. Also, *config.py* allows user to flexibly set up certain parameters for the program. 
Each plot is saved in the *logs/* directory. 


## Features
	- No need for programming to generate plots. Simply give your input data/function to the program and plot your data. 
	- Supported plot types: bar, box, cdf, histogram, line, scatter, line+scatter, 3D line
		- Flexibility of selecting any plot type for each subplot.
	- Subplots are supported
	- Provide your input data either via csv file (delimeter type can be specified in the program) or generate x-axis based on *numpy.arange()* and create y-axis functions with *numpy.** or *math.** libraries.
	- Flexibly enter your x- and y-axis labels, legend names, (sub)plot titles, etc.
		- axis labels and legend names can also be tken from csv file if provided in the first row of each data set (check out sample data file given in *inputCsvFiles/* directory.
	- 3rd-axis support for two data sets in line, scatter and line+scatter plots
	- Generated plots are automatically saved in *logs/.* directory in  *YearMonthDay_HourMinuteSecond* format. 

## Dependencies

Installation commamnds are given for Ubuntu (tested on Ubuntu 18.04).

** Program is written in python3 (version 3.6)**

> sudo apt install python3-dev python3-pip

**Matplotlib, tk-inter**

> sudo apt install python3-matplotlib python3-tk

**Csv, numpy,colorama, tinker, **

> pip3 install numpy colorama

## Usage

Simply run the program.

> ./pythonPlotter.py

The program will ask you questions to generate your plots. Answer to the questions accordingly and check out the flow diagram and its explanation below to better understand how the program works. 

![Alt text](flowDiagram.png?raw=true "Flow Diagram of PythonPlotter")

## Description of Flow Diagram
	
Please report the bugs so that I can improve the program. Also, expect to run into bugs as this is currently the first version of the program and I need feedbacks to improve the program. Thanks!
## Features to be Added in the Future:
1. Surface and wired 3D plots
2. Heat map plots
3. Multi-color box plots
4. Slider tabs for function-based plots 