#!/usr/bin/python3.6

############ Input File-related Configurations
defaultInputDir = 'inputCsvFiles' # directory name where input csv files saved
logDir = 'logs' # directory name of folder where plot files to be saved
defaultInputFile = 'plotFromCsv.csv' # default csv file name of input data
defaultDelimeter = ',' # Default delimeter type for CSV files
defaultEncoding = 'utf-8-sig' # Default encoding type for CSV files

############ Output Figure-related Configurations
plotsPerRow = 1 # num of subplots per row
figFormat = 'pdf' # data format type of the plots to be saved
figDimX = 25.60 # figure dimensions
figDimY = 14.40 # figure dimensions
zAxis_labelPad = 2 # padding size between z label and zticks in the plot. Increase it if label conflicts with ticks in the plot
threeD_azimDegree = -160 # Azimuth degree of viewpoint of 3D plots
threeD_elevDegree = 30 # Elevation degree of viewpoint of 3D plots
shareX = False # Have the x-axes of the plots in the same scale. Valid inputs: True, False, 'col', 'row' 
shareY = False # Have the y-axes of the plots in the same scale. Valid inputs: True, False, 'col', 'row'
scaleZ = 'linear' # Scale of z-axes. Valid inputs are: 'linear', 'log', 'symlog', 'logit', ... check out https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.axes.Axes.set_yscale.html
scatterErrPlot_lineStyle = 'o' # line style of "scatter plot w/ errorbar". Acceptable inputs: 'o', '-o', '-x', '--', '-'
lineErrPlot_lineStyle = '-' # line style of "line plot w/ errorbar". Acceptable inputs: 'o', '-o', '-x', '--', '-'
lineScatErrPlot_lineStyle = '-x' # line style of "line+scatter plot w/ errorbar". Acceptable inputs: 'o', '-o', '-x', '--', '-'
lineWidth = [3, 1.5, 1.5, 1, 1, 1, 1, 1, 1, 1] # line width of line plots. First entry of array is the first input data. Increase array size if you plot more than 10 lines in a plot! 
lineColors = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9] # Color order for lines in the plot. 0: steelblue, 1: sandybrown, 2: mediumseagreen, 3: indianred, 4: dimgrey, 5: orchid, 6: goldenrod, 7: darkcyan, 8: mediumslateblue, 9: darkkhaki. ADD MORE COLOR CODES TO "self.colors[]" in plotFuncs.py if you need more color options for your plot!
yLimThreshold = 25 # Valid iff 'multipleAxis = True'. Extra values to add to the y limits of additional y-axes.
alpha = 0.5 # Transparency level of line plots

############ Default Value Definitions for Output Figure
multipleAxis = False # to enable multiple y-axes on each plot
axisOffset = 0.1 # Valid iff 'multipleAxis = True'. y-axes offset value
defaultPlotSelect = 'line/scatter/line+scatter' # default plot type to be used
defaultPlotPlotSelect = 1 # 1: line, 2: scatter, 3: line+scatter. If user selects line/scatter/line+scatter plot type, then the default plot type to be used for each data set in the plot
defaultLegendNames = ['Pkt. Interval (ms)', 'UAV-RC Distance (m)', 'UAV Height (m)', 'legend4', 'legend5', 'legend6', 'legend7', 'legend8', 'legend9', 'legend10'] # Default legend names
defaultSubTitleNames = ['\\textbf{DJI Spark - Downlink}', '\\textbf{DJI Mavic Air - Downlink}', '\\textbf{Packet Interval CDF - Downlink}', 'subtitle4', 'subtitle5', 'subtitle6', 'subtitle7', 'subtitle8', 'subtitle9', 'subtitle10'] # Default subtitle names
defaultXLabel = 'x' # Default x-axis label name
defaultYLabel = 'y' # Default y-axis label name
defaultZLabel = 'z' # Default z-axis label name 
defaultTitle = 'title' # Default title name
histDefaultLabel = 'Number of Occurence' # Default y-axis label name of histogram plots
cdfDefaultLabel = 'CDF (\%)' # Default y-axis label name of CDF plots

############ seaborn related configurations
regressionPlotKind = 'hex' # type of graph for sns.regression plots. Available choices: 'scatter', 'resid', 'reg' (regression), 'kde' (heatmap), 'hex' (hexagonal)

############ Others
defaultMoreData = False # Default answer to whether to plot more dataset or not
oneColSpecPlt = True # Valid iff plotsPerRow = 1. Halve the width of one-column plots. Useful for scientific papers
oneColSpecPlt_loc_xTitle = 0.3 # Valid iff oneColSpecPlt = True
