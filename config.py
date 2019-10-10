#!/usr/bin/python3.6

logDir = "logs" # directory name of folder where plot files to be saved
figFormat = "pdf" # data format type of the plots to be saved
figDimX = 19.2 # save the figure in 1920x1080 format
figDimY = 10.8
dpi = 100 # figure resolution
shareX = False # Have the x-axes of the plots in the same scale. Valid inputs: True, False, 'col', 'row' 
shareY = False # Have the y-axes of the plots in the same scale. Valid inputs: True, False, 'col', 'row'
scaleX = 'linear' # Scale of x-axes. Valid inputs are: 'linear', 'log', 'symlog', 'logit', ... check out https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.axes.Axes.set_yscale.html
scaleY = 'linear' # Scale of y-axes. Valid inputs are: 'linear', 'log', 'symlog', 'logit', ... check out https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.axes.Axes.set_yscale.html
scaleZ = 'linear' # Scale of z-axes. Valid inputs are: 'linear', 'log', 'symlog', 'logit', ... check out https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.axes.Axes.set_yscale.html
legendLoc = 'upper right' # NOTE: Option 'best' does not always show all the legends!! Choose the legend location of plots. Valid inputs are: 'best', 'upper left', 'upper right', 'lower left', 'lower right', 'upper center', 'lower center', 'center left', 'center right'
axisLabelSize = 12 # font size of axes
titleLabelSize = 25 # font size of main title
xAxis_labelPad = 8 # padding size between x label and xticks in the plot. Increase it if label conflicts with ticks in the plot
yAxis_labelPad = 8 # padding size between y label and yticks in the plot. Increase it if label conflicts with ticks in the plot
zAxis_labelPad = 2 # padding size between z label and zticks in the plot. Increase it if label conflicts with ticks in the plot
subplots_hSpace = 0.5 # horizontal spacing between subplots. 
threeD_azimDegree = -160 # Azimuth degree of viewpoint of 3D plots
threeD_elevDegree = 30 # Elevation degree of viewpoint of 3D plots
defaultPlotSelect = 'line' # default plot type to be used
defaultInputDir = 'inputCsvFiles' # directory name where input csv files saved
defaultInputFile = 'plotFromCsv.csv' # default csv file name of input data
defaultDelimeter = ',' # Default delimeter type for CSV files
defaultEncoding = 'utf-8-sig' # Default encoding type for CSV files
defaultLegendNames = ['data'] # Default legend name
defaultXLabel = 'x' # Default x-axis label name
defaultYLabel = 'y' # Default y-axis label name
defaultZLabel = 'z' # Default z-axis label name 
defaultTitle = 'title' # Default title name
histDefaultLabel = 'Frequency of Occurence' # Default y-axis label name of histogram plots
cdfDefaultLabel = 'CDF (%)' # Default y-axis label name of CDF plots
 
