#!/usr/bin/python3.6

######################### FIGURE-RELATED SETTINGS #########################
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

########### Other Plot-related Settings
multipleAxis = True # to enable multiple y-axes on each plot
shareX = False # Have the x-axes of the plots in the same scale. Valid inputs: True, False, 'col', 'row' 
shareY = False # Have the y-axes of the plots in the same scale. Valid inputs: True, False, 'col', 'row'
oneColSpecPlt = True # Valid iff plotsPerRow = 1. Halve the width of one-column plots. Useful for scientific papers
oneColSpecPlt_loc_xTitle = 0.3 # Valid iff oneColSpecPlt = True
zAxis_labelPad = 2 # padding size between z label and zticks in the plot. Increase it if label conflicts with ticks in the plot
threeD_azimDegree = -160 # Azimuth degree of viewpoint of 3D plots
threeD_elevDegree = 30 # Elevation degree of viewpoint of 3D plots
scaleZ = 'linear' # Scale of z-axes. Valid inputs are: 'linear', 'log', 'symlog', 'logit', ... check out https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.axes.Axes.set_yscale.html
yLimThreshold = 25 # Valid iff 'multipleAxis = True'. Extra values to add to the y limits of additional y-axes.
axisOffset = 0.1 # Valid iff 'multipleAxis = True'. y-axes offset value
alpha = 0.5 # Transparency level of line plots

############ Default Value Definitions for Output Figure
defaultLegendNames = ['legend1', 'legend2', 'legend3', 'legend4', 'legend5', 'legend6', 'legend7', 'legend8', 'legend9', 'legend10'] # Default legend names
defaultSubTitleNames = ['subtitle1', 'subtitle2', 'subtitle3', 'subtitle4', 'subtitle5', 'subtitle6', 'subtitle7', 'subtitle8', 'subtitle9', 'subtitle10'] # Default subtitle names
defaultMoreData = False # Default answer to whether to plot more dataset or not
defaultPlotSelect = 'line||scatter||line+scatter' # default plot type to be used
defaultPlotPlotSelect = 1 # 1: line, 2: scatter, 3: line+scatter. If user selects line||scatter||line+scatter plot type, then the default plot type to be used for each data set in the plot
defaultXLabel = 'x' # Default x-axis label name
defaultYLabel = 'y' # Default y-axis label name
defaultZLabel = 'z' # Default z-axis label name 
defaultTitle = '\\textbf{Seaborn Joint Heatmap Plot}' # Default title name
histDefaultLabel = 'Number of Occurence' # Default y-axis label name of histogram plots
cdfDefaultLabel = 'CDF (\%)' # Default y-axis label name of CDF plots

######################### PLOT-TYPE-SPECIFIC SETTINGS #########################
############ Inputs for 'seaborn jointplot'
jointPlotKind = 'kde' # type of graph for sns.regression plots. Available choices: 'scatter', 'resid', 'reg' (regression), 'kde' (heatmap), 'hex' (hexagonal)

############ Inputs for 'line||scatter||line+scatter'
############ line plots (line, line with errorbars and seaborn line plots) 
lineWidth = [5, 5, 5, 1, 1, 1, 1, 1, 1, 1] # line width for lines per plots. First entry of array is the first input data. Increase array size if you plot more than 10 lines in a plot! 
lineColors = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9] # Color order for lines per plot. 0: steelblue, 1: sandybrown, 2: mediumseagreen, 3: indianred, 4: dimgrey, 5: orchid, 6: goldenrod, 7: darkcyan, 8: mediumslateblue, 9: darkkhaki. ADD MORE COLOR CODES TO "self.colors[]" in plotFuncs.py if you need more color options for your plot!
lineStyle = ['o', '-', 'dashed', 'dashed', '-', '-', '-', '-', '-', '-'] # linestyle per plot. valid inputs are: '-', '--', '-.', ':', 'None', ' ', '', 'solid', 'dashed', 'dashdot', 'dotted'
############ scatter plots (scatter, scatter with errorbar plots) 
scatter_style = ['4', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o'] # scatter style of "scatter plots". For acceptable inputs, check out: https://matplotlib.org/api/markers_api.html#module-matplotlib.markers
############ line+scatter plots (line+scatter, line+scatter with errorbar plots) 
lineScatter_style = ['-x', '-x', '-x', '-x', '-x', '-x', '-x', '-x', '-x', '-x'] # line style of "line+scatter plot w/ errorbar". Acceptable inputs: 'o', '-o', '-x', '--', '-'

