#!/usr/bin/python3.6

# !!! NOTE: EACH ENTRY OF ARRAY-BASED INPUTS CORRESPOND TO YOUR EACH SUBPLOT E.g. To modify your 1st subplot, modify the 1st entry of the arrays. Unless otherwise specified !!!

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

############ Default Value Definitions for Output Figure
fetchXLabelFromCsv = True # Fetch x label name from csv file. It will overwrite the values in defaultXLabel below.
fetchYLabelFromCsv = True # Fetch y label name from csv file. It will overwrite the values in defaultXLabel below.
fetchZLabelFromCsv = False # Fetch z label name from csv file. It will overwrite the values in defaultXLabel below.
defaultXLabel = ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'] # Default x-axis label name
defaultYLabel = ['y', 'y', 'y', 'y', 'y', 'y', 'y', 'y', 'y', 'y'] # Default y-axis label name
defaultZLabel = ['z', 'z', 'z', 'z', 'z', 'z', 'z', 'z', 'z', 'z'] # Default z-axis label name 
defaultLegendNames = ['DJI Spark - Manual', 'DJI Mavic Air - Manual', 'DJI Spark - Waypoint', 'DJI Spark - Formula', 'DJI Spark - UL', 'DJI Mavic Air - UL', 'Parrot AR - UL', 'DJI Spark - UL - Formula', 'legend9', 'legend10'] # PER LINE, NOT PER PLOT. Default legend names
defaultSubTitleNames = ['\\textbf{Uplink}', '\\textbf{Downlink}', '\\textbf{Downlink CDF Analysis}', '\\textbf{Uplink CDF Analysis}', 'subtitle5', 'subtitle6', 'subtitle7', 'subtitle8', 'subtitle9', 'subtitle10'] # Default subtitle names
defaultTitle = ' ' # Default title name
defaultMoreData = False # Default answer to whether to plot more dataset or not
defaultPlotSelect = 'line, scatter, errorbars' # default plot type to be used
defaultPlotPlotSelect = 1 # 1: line, 2: line with errorbars. If user selects line, scatter, errorbars plot type, then the default plot type to be used for each data set in the plot
histDefaultLabel = 'Density' # Default y-axis label name of histogram plots
cdfDefaultLabel = 'CDF' # Default y-axis label name of CDF plots

########### Multiple y-axis Settings
additionalYAxes = False # to enable multiple y-axes on each plot
additionalYAxes_enable = [True, True, True, True, True, True, True, True, True, True] # Valid iff additionalYAxes = True. Turn on or off additional y-axes. 1st entry is the 1st y-axis on the right side of the plot (2nd y-axis of the plot). 

########### Other Plot-related Settings
shareX = False # Have the x-axes of the plots in the same scale. Valid inputs: True, False, 'col', 'row' 
shareY = False # Have the y-axes of the plots in the same scale. Valid inputs: True, False, 'col', 'row'
oneColSpecPlt = True # Valid iff plotsPerRow = 1. Halve the width of one-column plots. Better x&y scaling for two-column scientific papers
oneColSpecPlt_loc_xTitle = 0.3 # Valid iff oneColSpecPlt = True. Lcoation of x title. 0.3 is center.
limX = [(None, None), (None, None), (None, None), (None, None), (None, None), (None, None), (None, None), (None, None), (None, None), (None, None)] # limit the range of x-axes. E.g. (0, 100) 0: starting point, 100: ending point
limY = [(None, None), (None, None), (None, None), (None, None), (None, None), (None, None), (None, None), (None, None), (None, None), (None, None)] # limit the range of y-axes. E.g. (0, 100) 0: starting point, 100: ending point 
limZ = [(None, None), (None, None), (None, None), (None, None), (None, None), (None, None), (None, None), (None, None), (None, None), (None, None)] # limit the range of z-axes. E.g. (0, 100) 0: starting point, 100: ending point
xticks = [(0, 51, 10), (0, 51, 10), (None, None, None), (None, None, None), (None, None, None), (None, None, None), (None, None, None), (None, None, None), (None, None, None), (None, None, None)] # set spacing of xticks. 
yticks = [(0, 126, 50), (0, 3001, 1000), (None, None, None), (None, None, None), (None, None, None), (None, None, None), (None, None, None), (None, None, None), (None, None, None), (None, None, None)] # set spacing of yticks. 
zticks = [(None, None, None), (None, None, None), (None, None, None), (None, None, None), (None, None, None), (None, None, None), (None, None, None), (None, None, None), (None, None, None), (None, None, None)] # set spacing of yticks. 
scaleX = ['linear', 'linear', 'linear', 'linear', 'linear', 'linear', 'linear', 'linear', 'linear', 'linear'] # Scale of x-axes. Valid inputs are: 'linear', 'log', 'symlog', 'logit', ... check out https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.axes.Axes.set_yscale.html
scaleY = ['linear', 'linear', 'linear', 'linear', 'linear', 'linear', 'linear', 'linear', 'linear', 'linear'] # Scale of y-axes. Valid inputs are: 'linear', 'log', 'symlog', 'logit', ... check out https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.axes.Axes.set_yscale.html
scaleZ = ['linear', 'linear', 'linear', 'linear', 'linear', 'linear', 'linear', 'linear', 'linear', 'linear'] # Scale of z-axes. Valid inputs are: 'linear', 'log', 'symlog', 'logit', ... check out https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.axes.Axes.set_yscale.html
xAxis_labelPad = [2, 2, 2, 2, 2, 2, 2, 2, 2, 2] # padding size between x label and xticks in the plot. Increase it if label conflicts with ticks in the plot
yAxis_labelPad = [2, 2, 2, 2, 2, 2, 2, 2, 2, 2] # padding size between y label and yticks in the plot. Increase it if label conflicts with ticks in the plot
zAxis_labelPad = [2, 2, 2, 2, 2, 2, 2, 2, 2, 2] # padding size between z label and zticks in the plot. Increase it if label conflicts with ticks in the plot
threeD_azimDegree = [-160, -160, -160, -160, -160, -160, -160, -160, -160, -160] # Azimuth degree of viewpoint of 3D plots
threeD_elevDegree = [30, 30, 30, 30, 30, 30, 30, 30, 30, 30] # Elevation degree of viewpoint of 3D plots
yLimThreshold = [25, 25, 25, 25, 25, 25, 25, 25, 25, 25] # PER LINE, NOT PER PLOT. Valid iff 'additionalYAxes = True'. Extra values to add to the y limits of additional y-axes. 
axisOffset = [0.1, 0.1, 0.2, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1] # Valid iff 'additionalYAxes = True'. y-axes offset value
alpha = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5] # Transparency level of plots

############ Legend-related Configurations (valid if 'additionalYAxes == False')
subplotLegend = False # print legend per subplot
figLegend = True # print all legends of subplots together at one place
legend_bbox_to_anchor = (0.25, 0) # !!! IF SET, ONLY THE LEGENDS OF LAST PLOT WILL BE USED !!! Place legend in a specific box configuration. Use 'None' for default. Format: '(x, y) or (x, y, w, h)'. Check out: https://matplotlib.org/api/_as_gen/matplotlib.pyplot.legend.html
legend_loc = "center"
legend_mode = None # 'expand' # set to 'expand' if you want horizontal expansion
legend_border_axesPad = 0
legend_nCol = 1 # number of columns

######################### PLOT-TYPE-SPECIFIC SETTINGS #########################
############ Inputs for 'bar' plots - https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.pyplot.bar.html
bar_barColors = [0, 1, 2, 4, 3, 5, 6, 7, 8, 9] # PER LINE, NOT PER PLOT. Color order for lines per plot. 0: steelblue, 1: sandybrown, 2: mediumseagreen, 3: indianred, 4: dimgrey, 5: orchid, 6: goldenrod, 7: darkcyan, 8: mediumslateblue, 9: darkkhaki. ADD MORE COLOR CODES TO "self.colors[]" in plotFuncs.py if you need more color options for your plot!
bar_edgeColors = [0, 1, 2, 4, 3, 5, 6, 7, 8, 9] # PER LINE, NOT PER PLOT. Color order for lines per plot. 0: steelblue, 1: sandybrown, 2: mediumseagreen, 3: indianred, 4: dimgrey, 5: orchid, 6: goldenrod, 7: darkcyan, 8: mediumslateblue, 9: darkkhaki. ADD MORE COLOR CODES TO "self.colors[]" in plotFuncs.py if you need more color options for your plot!
bar_edgeWidths = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1] # PER LINE, NOT PER PLOT. edge widths of bars. 0 means don't draw edges
bar_labels = [None, None, None, None, None, None, None, None, None, None] # labels of each bar. Set to None if you do not want labels
bar_capSize = [None, None, None, None, None, None, None, None, None, None] # cap size of each bar. Set to None if you do not want labels
bar_widths = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]   # widths of the bars
bar_bottom = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0] # valid inputs: array of scalar. Y coordinates of bars bases
bar_align = ['center', 'center', 'center', 'center', 'center', 'center', 'center', 'center', 'center', 'center']  # alignments of bars to x-coordinates. Valid inputs: 'center', 'edge'

############ Inputs for 'box' plots - https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.pyplot.boxplot.html
box_boxColors = [0, 1, 2, 4, 3, 5, 6, 7, 8, 9] # PER LINE, NOT PER PLOT. Color order for lines per plot. 0: steelblue, 1: sandybrown, 2: mediumseagreen, 3: indianred, 4: dimgrey, 5: orchid, 6: goldenrod, 7: darkcyan, 8: mediumslateblue, 9: darkkhaki. ADD MORE COLOR CODES TO "self.colors[]" in plotFuncs.py if you need more color options for your plot!
box_lineColors = [0, 1, 2, 4, 3, 5, 6, 7, 8, 9] # PER LINE, NOT PER PLOT. Color order for lines per plot. 0: steelblue, 1: sandybrown, 2: mediumseagreen, 3: indianred, 4: dimgrey, 5: orchid, 6: goldenrod, 7: darkcyan, 8: mediumslateblue, 9: darkkhaki. ADD MORE COLOR CODES TO "self.colors[]" in plotFuncs.py if you need more color options for your plot!
box_capColors = [0, 1, 2, 4, 3, 5, 6, 7, 8, 9] # PER LINE, NOT PER PLOT. Color order for lines per plot. 0: steelblue, 1: sandybrown, 2: mediumseagreen, 3: indianred, 4: dimgrey, 5: orchid, 6: goldenrod, 7: darkcyan, 8: mediumslateblue, 9: darkkhaki. ADD MORE COLOR CODES TO "self.colors[]" in plotFuncs.py if you need more color options for your plot!
box_whiskerColors = [0, 1, 2, 4, 3, 5, 6, 7, 8, 9] # PER LINE, NOT PER PLOT. Color order for lines per plot. 0: steelblue, 1: sandybrown, 2: mediumseagreen, 3: indianred, 4: dimgrey, 5: orchid, 6: goldenrod, 7: darkcyan, 8: mediumslateblue, 9: darkkhaki. ADD MORE COLOR CODES TO "self.colors[]" in plotFuncs.py if you need more color options for your plot!
box_flierColors = [0, 1, 2, 4, 3, 5, 6, 7, 8, 9] # PER LINE, NOT PER PLOT. Color order for lines per plot. 0: steelblue, 1: sandybrown, 2: mediumseagreen, 3: indianred, 4: dimgrey, 5: orchid, 6: goldenrod, 7: darkcyan, 8: mediumslateblue, 9: darkkhaki. ADD MORE COLOR CODES TO "self.colors[]" in plotFuncs.py if you need more color options for your plot!
box_markerEdgeColors = [0, 1, 2, 4, 3, 5, 6, 7, 8, 9] # PER LINE, NOT PER PLOT. Color order for lines per plot. 0: steelblue, 1: sandybrown, 2: mediumseagreen, 3: indianred, 4: dimgrey, 5: orchid, 6: goldenrod, 7: darkcyan, 8: mediumslateblue, 9: darkkhaki. ADD MORE COLOR CODES TO "self.colors[]" in plotFuncs.py if you need more color options for your plot!
box_medianColors = [0, 1, 2, 4, 3, 5, 6, 7, 8, 9] # PER LINE, NOT PER PLOT. Color order for lines per plot. 0: steelblue, 1: sandybrown, 2: mediumseagreen, 3: indianred, 4: dimgrey, 5: orchid, 6: goldenrod, 7: darkcyan, 8: mediumslateblue, 9: darkkhaki. ADD MORE COLOR CODES TO "self.colors[]" in plotFuncs.py if you need more color options for your plot!
box_widths = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5] # widths of each box plot
box_labels = ['label1', 'label2', 'label3', 'label4', 'label5', 'label6', 'label7', 'label8', 'label9', 'label10'] # labels of each box plot. Set to None if you do not want labels
box_vert = [False, False, False, False, False, False, False, False, False, False] # to produce vertical box plots
box_notched = [False, False, False, False, False, False, False, False, False, False]  # to produce notched box plots
box_whis = [1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5] # the reach of whiskers beyond the 1st and 3rd quartiles
box_bootstrap = [None, None, None, None, None, None, None, None, None, None]  # valid inputs: int. number of times to bootstrap the median to determine its 95% confidence intervals. 
box_patchArtist = [True, True, True, True, True, True, True, True, True, True]  # to draw boxes with patch artists 
box_zOrder = [None, None, None, None, None, None, None, None, None, None] # Valid inputs: scaler. Sets the zorder of the boxplot.

############ Inputs for 'cdf' plots - https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.pyplot.plot.html
cdf_lineColors = [0, 1, 2, 4, 3, 5, 6, 7, 8, 9] # PER LINE, NOT PER PLOT. Color order for lines per plot. 0: steelblue, 1: sandybrown, 2: mediumseagreen, 3: indianred, 4: dimgrey, 5: orchid, 6: goldenrod, 7: darkcyan, 8: mediumslateblue, 9: darkkhaki. ADD MORE COLOR CODES TO "self.colors[]" in plotFuncs.py if you need more color options for your plot!
cdf_lineWidth = [10, 10, 10, 10, 5, 5, 5, 3, 1, 1] # PER LINE, NOT PER PLOT. line width for lines per plots. First entry of array is the first input data. Increase array size if you plot more than 10 lines in a plot! 
cdf_lineStyle = ['solid', 'solid', 'dashed', 'dashed', 'solid', 'solid', 'solid', 'dashed', '', ''] # linestyle per plot. Valid inputs: {'-', '--', '-.', ':', 'None', ' ', '', 'solid', 'dashed', 'dashdot', 'dotted'}
cdf_markerStyle = ['', 'v', '', '', 'x', '', '', '', '', ''] # PER LINE, NOT PER PLOT. marker style. For acceptable inputs, check out https://matplotlib.org/api/markers_api.html#module-matplotlib.markers
cdf_markerSize = [15, 15, 15, 15, 10, 1, 1, 1, 1, 1] # PER LINE, NOT PER PLOT. marker size. 

############ Inputs for 'hist' plots - https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.pyplot.hist.html
hist_colors = [0, 1, 2, 4, 3, 5, 6, 7, 8, 9] # PER LINE, NOT PER PLOT. Color order for lines per plot. 0: steelblue, 1: sandybrown, 2: mediumseagreen, 3: indianred, 4: dimgrey, 5: orchid, 6: goldenrod, 7: darkcyan, 8: mediumslateblue, 9: darkkhaki. ADD MORE COLOR CODES TO "self.colors[]" in plotFuncs.py if you need more color options for your plot!
hist_edgeColors = ['black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black'] # edge color of histogram bars
hist_histType = ['bar', 'bar', 'bar', 'bar', 'bar', 'bar', 'bar', 'bar', 'bar', 'bar'] # valid inputs: {'bar', 'barstacked', 'step', 'stepfilled'}. Type of histogram to draw. 
hist_density = [True, True, False, False, False, False, False, False, False, False] # normalized probability density 
hist_cumulative = [False, False, False, False, False, False, False, False, False, False] # cumulative histogram 
hist_bottom = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0] # valid inputs: array of scalar. Location of the bottom baseline of each bin. 
hist_align = ['left', 'left', 'left', 'left', 'left', 'left', 'left', 'left', 'left', 'left']  # valid inputs: {'left', 'mid', 'right'}. alignment of histogram bars
hist_orientation = ['vertical', 'vertical', 'vertical', 'vertical', 'vertical', 'vertical', 'vertical', 'vertical', 'vertical', 'vertical']  # valid inputs: {'horizontal', 'vertical'}
hist_rwidth = [None, None, None, None, None, None, None, None, None, None] # valid inputs: scalar or None. Relative width of the bars as a fraction of the bin width. 
hist_stacked = [False, False, False, False, False, False, False, False, False, False] # multiple data stacked on top of each other. 

############ Inputs for 'line' plots - https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.pyplot.plot.html
line_lineColors = [0, 1, 2, 4, 3, 5, 6, 7, 8, 9] # PER LINE, NOT PER PLOT. Color order for lines per plot. 0: steelblue, 1: sandybrown, 2: mediumseagreen, 3: indianred, 4: dimgrey, 5: orchid, 6: goldenrod, 7: darkcyan, 8: mediumslateblue, 9: darkkhaki. ADD MORE COLOR CODES TO "self.colors[]" in plotFuncs.py if you need more color options for your plot!
line_lineWidth = [12, 5, 1, 1, 1, 1, 1, 1, 1, 1] # PER LINE, NOT PER PLOT. line width for lines per plots. First entry of array is the first input data. Increase array size if you plot more than 10 lines in a plot! 
line_lineStyle = ['solid', 'solid', 'solid', 'dashed', 'solid', 'solid', 'solid', 'dashed', '', ''] # linestyle per plot. Valid inputs: {'-', '--', '-.', ':', 'None', ' ', '', 'solid', 'dashed', 'dashdot', 'dotted'}
line_markerStyle = ['', '', 's', '', 'x', '', '', '', '', ''] # PER LINE, NOT PER PLOT. marker style. For acceptable inputs, check out https://matplotlib.org/api/markers_api.html#module-matplotlib.markers
line_markerSize = [10, 10, 1, 1, 1, 1, 1, 1, 1, 1] # PER LINE, NOT PER PLOT. marker size. 

############ Inputs for 'errorbar' plots - https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.pyplot.errorbar.html
errorbar_lineColors = [0, 1, 2, 4, 3, 5, 6, 7, 8, 9] # PER LINE, NOT PER PLOT. Color order for lines per plot. 0: steelblue, 1: sandybrown, 2: mediumseagreen, 3: indianred, 4: dimgrey, 5: orchid, 6: goldenrod, 7: darkcyan, 8: mediumslateblue, 9: darkkhaki. ADD MORE COLOR CODES TO "self.colors[]" in plotFuncs.py if you need more color options for your plot!
errorbar_lineWidth = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1] # PER LINE, NOT PER PLOT. line width for lines per plots. First entry of array is the first input data. Increase array size if you plot more than 10 lines in a plot! 
errorbar_lineStyle = ['solid', 'solid', 'solid', 'dashed', 'solid', 'solid', 'solid', 'dashed', '', ''] # linestyle per plot. Valid inputs: {'-', '--', '-.', ':', 'None', ' ', '', 'solid', 'dashed', 'dashdot', 'dotted'}
errorbar_capSize = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1] # PER LINE, NOT PER PLOT. cap size of errorbars. 
errorbar_capThickness = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1] # PER LINE, NOT PER PLOT. cap thickness of errorbars. 
errorbar_barsAbove = [False, False, False, False, False, False, False, False, False, False]  # PER LINE, NOT PER PLOT. If true, it will plot errorbars above the plot symbols

############ Inputs for '3d' plots - https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.pyplot.plot.html
threeD_lineColors = [0, 1, 2, 4, 3, 5, 6, 7, 8, 9] # PER LINE, NOT PER PLOT. Color order for lines per plot. 0: steelblue, 1: sandybrown, 2: mediumseagreen, 3: indianred, 4: dimgrey, 5: orchid, 6: goldenrod, 7: darkcyan, 8: mediumslateblue, 9: darkkhaki. ADD MORE COLOR CODES TO "self.colors[]" in plotFuncs.py if you need more color options for your plot!
threeD_lineWidth = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1] # PER LINE, NOT PER PLOT. line width for lines per plots. First entry of array is the first input data. Increase array size if you plot more than 10 lines in a plot! 
threeD_lineStyle = ['solid', 'solid', 'solid', 'dashed', 'solid', 'solid', 'solid', 'dashed', '', ''] # linestyle per plot. Valid inputs: {'-', '--', '-.', ':', 'None', ' ', '', 'solid', 'dashed', 'dashdot', 'dotted'}
threeD_markerStyle = ['', 'v', 's', '', 'x', '', '', '', '', ''] # PER LINE, NOT PER PLOT. marker style. For acceptable inputs, check out https://matplotlib.org/api/markers_api.html#module-matplotlib.markers
threeD_markerSize = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1] # PER LINE, NOT PER PLOT. marker size. 

############ Inputs for 'seaborn line' plots - https://seaborn.pydata.org/generated/seaborn.lineplot.html https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.pyplot.plot.html 
snsLine_lineColors = [0, 1, 2, 4, 3, 5, 6, 7, 8, 9] # PER LINE, NOT PER PLOT. Color order for lines per plot. 0: steelblue, 1: sandybrown, 2: mediumseagreen, 3: indianred, 4: dimgrey, 5: orchid, 6: goldenrod, 7: darkcyan, 8: mediumslateblue, 9: darkkhaki. ADD MORE COLOR CODES TO "self.colors[]" in plotFuncs.py if you need more color options for your plot!
snsLine_lineWidth = [10, 10, 10, 5, 5, 5, 5, 3, 1, 1] # PER LINE, NOT PER PLOT. line width for lines per plots. First entry of array is the first input data. Increase array size if you plot more than 10 lines in a plot! 
snsLine_lineStyle = ['solid', 'solid', 'dashed', 'dashed', 'solid', 'solid', 'solid', 'dashed', '', ''] # linestyle per plot. Valid inputs: {'-', '--', '-.', ':', 'None', ' ', '', 'solid', 'dashed', 'dashdot', 'dotted'}
snsLine_markerStyle = ['', 'v', '', '', '', '', '', '', '', ''] # PER LINE, NOT PER PLOT. marker style. For acceptable inputs, check out https://matplotlib.org/api/markers_api.html#module-matplotlib.markers
snsLine_markerSize = [15, 20, 15, 15, 10, 1, 1, 1, 1, 1] # PER LINE, NOT PER PLOT. marker size. 
snsLine_hue = [None, None, None, None, None, None, None, None, None, None] # groupling variable that will produce lines with different colors
snsLine_size = [None, None, None, None, None, None, None, None, None, None] # groupling variable that will produce lines with different widths
snsLine_style = [None, None, None, None, None, None, None, None, None, None] # groupling variable that will produce lines with different dashes and/or markers

############ Inputs for 'seaborn joint' plots - https://seaborn.pydata.org/generated/seaborn.jointplot.html
snsJoint_lineColors = [0, 1, 2, 4, 3, 5, 6, 7, 8, 9] # PER LINE, NOT PER PLOT. Color order for lines per plot. 0: steelblue, 1: sandybrown, 2: mediumseagreen, 3: indianred, 4: dimgrey, 5: orchid, 6: goldenrod, 7: darkcyan, 8: mediumslateblue, 9: darkkhaki. ADD MORE COLOR CODES TO "self.colors[]" in plotFuncs.py if you need more color options for your plot!
snsJoint_kind = 'reg' # type of graph for sns.regression plots. Valid inputs: {'scatter', 'resid', 'reg', 'kde', 'hex'}
