#!/usr/bin/python3.6

############ Input File-related Configurations
defaultInputDir = 'inputCsvFiles' # directory name where input csv files saved
logDir = 'logs' # directory name of folder where plot files to be saved
defaultInputFile = 'plotFromCsv.csv' # default csv file name of input data
defaultDelimeter = ',' # Default delimeter type for CSV files
defaultEncoding = 'utf-8-sig' # Default encoding type for CSV files

############ Output Figure-related Configurations
plotsPerRow = 1 # num of subplots per row
figFormat = 'png' # data format type of the plots to be saved
figDimX = 19.2 # save the figure in 1920x1080 format
figDimY = 10.8 # save the figure in 1920x1080 format
showGrid = ['True', 'False', 'True', 'True', 'True', 'True', 'True', 'True', 'True', 'True'] # whether to show grid on each subplot, the first entry corresponds to first subplot. Add more entry if you have more than 10 plots!
gridLineWidth = 0.1 # line width of grids
gridLineColor = 'teal' # line color of grids
backgroundColor = 'whitesmoke' # background color of plots
dpi = 100 # figure resolution
xTickSize = 21 # x tick font size
yTickSize = 21 # y tick font size
axisLabelSize = 24 # font size of axes
titleLabelSize = 24 # font size of main title
xAxis_labelPad = 8 # padding size between x label and xticks in the plot. Increase it if label conflicts with ticks in the plot
yAxis_labelPad = 8 # padding size between y label and yticks in the plot. Increase it if label conflicts with ticks in the plot
zAxis_labelPad = 2 # padding size between z label and zticks in the plot. Increase it if label conflicts with ticks in the plot
subplots_hSpace = 0.5 # vertical spacing between subplots. 
threeD_azimDegree = -160 # Azimuth degree of viewpoint of 3D plots
threeD_elevDegree = 30 # Elevation degree of viewpoint of 3D plots
axesOff = ['top', 'bottom', 'left', 'right'] # Write down the axes you wish to turn off. Acceptable inputs: 'top', 'bottom', 'right', 'left'.
shareX = False # Have the x-axes of the plots in the same scale. Valid inputs: True, False, 'col', 'row' 
shareY = False # Have the y-axes of the plots in the same scale. Valid inputs: True, False, 'col', 'row'
scaleX = 'linear' # Scale of x-axes. Valid inputs are: 'linear', 'log', 'symlog', 'logit', ... check out https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.axes.Axes.set_yscale.html
scaleY = 'linear' # Scale of y-axes. Valid inputs are: 'linear', 'log', 'symlog', 'logit', ... check out https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.axes.Axes.set_yscale.html
scaleZ = 'linear' # Scale of z-axes. Valid inputs are: 'linear', 'log', 'symlog', 'logit', ... check out https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.axes.Axes.set_yscale.html
legendLoc = 'upper right' # NOTE: Option 'best' does not always show all the legends!! Choose the legend location of plots. Valid inputs are: 'best', 'upper left', 'upper right', 'lower left', 'lower right', 'upper center', 'lower center', 'center left', 'center right'
scatterErrPlot_lineStyle = 'o' # line style of "scatter plot w/ errorbar". Acceptable inputs: 'o', '-o', '-x', '--', '-'
lineErrPlot_lineStyle = '-' # line style of "line plot w/ errorbar". Acceptable inputs: 'o', '-o', '-x', '--', '-'
lineScatErrPlot_lineStyle = '-x' # line style of "line+scatter plot w/ errorbar". Acceptable inputs: 'o', '-o', '-x', '--', '-'
alpha = 0.5 # opacity level of plots (except seaborn plots)
lineWidth = [5, 1, 2, 1, 1, 1, 1, 1, 1, 1] # line width of line plots. First entry of array is the first input data. Increase array size if you plot more than 10 lines in a plot! 

############ Default Value Definitions for Output Figure
lineColors = [0, 3, 2, 4, 9, 1, 7, 8, 5, 6] # Color order for lines in the plot. 0: blue, 1: orange, 2: green, 3: red, 4: purple, 5: brown, 6: pink, 7: dark grey, 8: light green, 9: cyan. ADD MORE COLOR CODES TO "self.colors[]" in pythonPlotter.py if you need more color options for your plot!
defaultPlotSelect = 'line/scatter/line+scatter' # default plot type to be used
defaultPlotPlotSelect = 1 # 1: line, 2: scatter, 3: line+scatter. If user selects line/scatter/line+scatter plot type, then the default plot type to be used for each data set in the plot
defaultLegendNames = ['legend1', 'legend2', 'legend3', 'legend4', 'legend5', 'legend6', 'legend7', 'legend8', 'legend9', 'legend10'] # Default legend names
defaultXLabel = 'x' # Default x-axis label name
defaultYLabel = 'y' # Default y-axis label name
defaultZLabel = 'z' # Default z-axis label name 
defaultTitle = 'title' # Default title name
histDefaultLabel = 'Number of Occurence' # Default y-axis label name of histogram plots
cdfDefaultLabel = 'CDF (%)' # Default y-axis label name of CDF plots

############ seaborn related configurations
regressionPlotKind = 'hex' # type of graph for sns.regression plots. Available choices: 'scatter', 'resid', 'reg' (regression), 'kde' (heatmap), 'hex' (hexagonal)

############ Others
defaultMoreData = False # Default answer to whether or not to plot more dataset
