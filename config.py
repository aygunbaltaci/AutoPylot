#!/usr/bin/python3.6

logDir = "logs" # directory name of folder where plot files to be saved
figFormat = "pdf" # data format type of the plots to be saved
figDimX = 19.2 # save the figure in 1920x1080 format
figDimY = 10.8
dpi = 100 # figure resolution
shareX = False # Have the x-axes of the plots in the same scale. Valid inputs: True, False, 'col', 'row' 
shareY = False # Have the y-axes of the plots in the same scale. Valid inputs: True, False, 'col', 'row'
scaleX = 'linear' # Scale of x-axes. Valid inputs are: "linear", "log", "symlog", "logit", ... check out https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.axes.Axes.set_yscale.html
scaleY = 'linear' # Scale of y-axes. Valid inputs are: "linear", "log", "symlog", "logit", ... check out https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.axes.Axes.set_yscale.html
axisLabelSize = 15 # font size of axes
titleLabelSize = 25 # font size of labels
xAxis_labelPad = 10 # padding size between x label and xticks in the plot. Increase it if label conflicts with ticks in the plot
yAxis_labelPad = 10 # padding size between y label and yticks in the plot. Increase it if label conflicts with ticks in the plot
zAxis_labelPad = 10 # padding size between z label and zticks in the plot. Increase it if label conflicts with ticks in the plot
defaultPlotSelect = 'line' # default plot type to be used
defaultInputDir = 'inputCsvFiles' # directory name where input csv files saved
defaultInputFile = 'plotFromCsv.csv' # default csv file name of input data
defaultDelimeter = ','
defaultEncoding = 'utf-8-sig'
defaultLegendNames = ['self.data']
defaultXLabel = 'x'
defaultYLabel = 'y'
defaultZLabel = 'z'
defaultTitle = 'title'
histDefaultLabel = 'Frequency of Occurence'
cdfDefaultLabel = 'CDF (%)'
 
