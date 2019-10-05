#!/usr/bin/python3.6

import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import csv
import numpy as np
import math
import os
import sys
import inspect
from colorama import Fore, Back, Style, init # colored output on the terminal
from datetime import datetime
import tkinter
import config
init(autoreset = True) # turn off colors after each print()

###################### PLOTTER
class plotPython:
    # =============================== Initializer / Instance attributes
    def __init__(self):
        self.colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#bcbd22', '#17becf'] # blue, orange, green, red, purple, brown, pink, dark gray, light green, cyan. Check out https://matplotlib.org/3.1.0/users/dflt_style_changes.html
        self.lineTypes = ['-', '--', '-.', '.']
        self.plotFuncName = ''
        self.color_y1 = 0 
        self.color_y2 = 1 
        self.figRowCnt = 0
        self.figColCnt = 0
        self.date = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.fTxtNoXServer = f"""
{Fore.RED}Your X-server is not running, cannot plot the graph.
Please turn on your X-server first and then hit [enter]"""
        
    # =============================== Prepare the plot
    def prepPlot(self, numOfPlots): 
        exitLoop = False
        while True:
            try: 
                numOfRow = 2 if numOfPlots > 1 else 1
                self.fig, self.host = plt.subplots(math.ceil(numOfPlots / numOfRow), numOfRow, sharex = config.shareX, sharey = config.shareY, figsize = (config.figDimX, config.figDimY), squeeze = False)
                if numOfPlots != 1 and numOfPlots % 2 == 1: # turn off the axes of last unused plot, because there is leftover plot in when total plots are oddW
                    self.host[int(numOfPlots / 2), 1].axis('off')
                exitLoop = True
            except tkinter._tkinter.TclError: # fail if X-server not running
                print(self.fTxtNoXServer)
                userInput = input()
                if userInput in ['exit', 'EXIT', 'quit', 'QUIT']: # exit options
                    sys.exit(0)
                exitLoop = False
            if exitLoop: 
                break
                
    # =============================== Color the axes
    def axisColoring(self):
        # color the axes of the plot. For now, it is implemented only for 3-axis 2D graphs. TO BE EXTENDED!
        self.host[self.figColCnt, self.figRowCnt].spines['left'].set_color(self.colors[self.color_y1])
        self.host[self.figColCnt, self.figRowCnt].tick_params(axis='y', colors=self.colors[self.color_y1])
        self.host[self.figColCnt, self.figRowCnt].yaxis.label.set_color(self.colors[self.color_y1])
        self.guest.spines['right'].set_color(self.colors[self.color_y2])
        self.guest.tick_params(axis='y', colors=self.colors[self.color_y2])
        self.guest.yaxis.label.set_color(self.colors[self.color_y2])
    
    # =============================== Show the plot
    def plotLabeling(self, xLabel, yLabel, yLabel2, zLabel, thirdAxis, threeD, title, numOfPlots, plotCounter):
        self.fig.savefig('%s' %config.logDir + os.sep + '%s.%s' %(self.date, config.figFormat), format = config.figFormat, dpi = config.dpi)
        self.host[self.figColCnt, self.figRowCnt].set_xlabel(xLabel, size = config.axisLabelSize)
        self.host[self.figColCnt, self.figRowCnt].set_ylabel(yLabel, size = config.axisLabelSize)
        if thirdAxis:
            self.guest.set_ylabel(yLabel2, size = config.axisLabelSize)
        if threeD: 
            self.host[self.figColCnt, self.figRowCnt].set_zlabel(zLabel, size = config.axisLabelSize)
        if numOfPlots > 1:
            self.host[self.figColCnt, self.figRowCnt].title.set_text(title)
            self.host[self.figColCnt, self.figRowCnt].title.set_size(config.axisLabelSize)
        if not thirdAxis:
            plt.legend()
        
        # logic to place subplots in the right location
        if plotCounter % 2 == 0:
            self.figRowCnt += 1
        else:
            self.figColCnt += 1
            self.figRowCnt -= 1
        
    def showPlot(self, title, numOfPlots):
        
        self.fig.suptitle(title, size = config.titleLabelSize) # Main title
        # leave some space between subplots
        if numOfPlots >= 2: 
            self.fig.subplots_adjust(hspace = config.subplots_hSpace)

        self.fig.savefig('%s' %config.logDir + os.sep + '%s.%s' %(self.date, config.figFormat), bbox_inches = 'tight', format = config.figFormat, dpi = config.dpi) # save fig to logs dir
        self.fig.tight_layout() # to adjust spacing between graphs and labels
        plt.show()
     
    # =============================== Apply padding and scaling to x- and y-axis
    def padAndScale(self):
        # label padding for x- and y-axis
        self.host[self.figColCnt, self.figRowCnt].axes.xaxis.labelpad = config.xAxis_labelPad
        self.host[self.figColCnt, self.figRowCnt].axes.yaxis.labelpad = config.yAxis_labelPad
        
        # scaling options for x- and y-axis
        self.host[self.figColCnt, self.figRowCnt].set_xscale(config.scaleX)
        self.host[self.figColCnt, self.figRowCnt].set_yscale(config.scaleY)
        
    # =============================== Plotter function
    def mainPlotter(self, plotCounter, numOfPlots, plotType, numData, colNumX, colNumY, colNumZ, legendName, binRes, thirdAxis, data):
        
        # Main if clause for plots
        if plotType == 'bar':
            for i in range(numData):
                self.host[self.figColCnt, self.figRowCnt].bar(data[colNumX[i]], data[colNumY[i]], label = legendName[i]) 
        elif plotType == 'box':
            boxData = []
            for i in range(numData):
                boxData.append(data[colNumX[i]])
            self.host[self.figColCnt, self.figRowCnt].boxplot(boxData, positions = np.array(range(len(boxData))) + 1)
            self.host[self.figColCnt, self.figRowCnt].set_xticklabels(legendName)
        elif plotType == 'cdf':
            bin_edges_list = [] 
            cdfData = []
            data_size = len(data[colNumX[0]]) # taken from: https://stackoverflow.com/questions/24575869/read-file-and-plot-cdf-in-python
            data_set = sorted(set(data[colNumX[0]]))
            bins = np.append(data_set, data_set[-1] + 1)
            counts, bin_edges = np.histogram(data[colNumX[0]], bins = bins, density = False) # Use histogram function to bin data
            counts = counts.astype(float) / data_size
            cdfData = np.cumsum(counts)
            self.host[self.figColCnt, self.figRowCnt].plot(bin_edges[0:-1], cdfData) 
        elif plotType == 'histogram':
            self.bins = np.arange(min(data[colNumX[0]]) - binRes, max(data[colNumX[0]]) + binRes * 2, binRes)
            self.host[self.figColCnt, self.figRowCnt].hist(data[colNumX[0]], bins = self.bins, align = 'left')  
            plt.xticks(self.bins[:-1])
        elif plotType in ['line', 'line + scatter']:
            if thirdAxis:
                if plotType == 'line':
                    p1, = self.host[self.figColCnt, self.figRowCnt].plot(data[colNumX[0]], data[colNumY[0]], self.colors[self.color_y1], label = legendName[0])  
                else:
                    p1, = self.host[self.figColCnt, self.figRowCnt].plot(data[colNumX[0]], data[colNumY[0]], '-o', self.colors[self.color_y1], label = legendName[0])  
                self.guest = self.host[self.figColCnt, self.figRowCnt].twinx() # setup 2nd axis based on the first graph
                if plotType == 'line':
                    p2, = self.guest.plot(data[colNumX[1]], data[colNumY[1]], self.colors[self.color_y2], label = legendName[1])             
                else:
                    p2, = self.guest.plot(data[colNumX[1]], data[colNumY[1]], '-o', self.colors[self.color_y2], label = legendName[1]) 
                lines = [p1, p2]
                self.host[self.figColCnt, self.figRowCnt].legend(lines, [l.get_label() for l in lines])
                self.axisColoring()
            else:
                for i in range(numData):
                    if plotType == 'line':
                        self.host[self.figColCnt, self.figRowCnt].plot(data[colNumX[i]], data[colNumY[i]], label = legendName[i])
                    else:
                        self.host[self.figColCnt, self.figRowCnt].plot(data[colNumX[i]], data[colNumY[i]], '-o', label = legendName[i])
        elif plotType == 'scatter':
            if thirdAxis:
                p1 = self.host[self.figColCnt, self.figRowCnt].scatter(data[colNumX[0]], data[colNumY[0]], c = self.colors[self.color_y1], label = legendName[0])  
                self.guest = self.host[self.figColCnt, self.figRowCnt].twinx() # setup 2nd axis based on the first graph
                p2 = self.guest.scatter(data[colNumX[1]], data[colNumY[1]], c = self.colors[self.color_y2], label = legendName[1])             
                lines = [p1, p2]
                self.host[self.figColCnt, self.figRowCnt].legend(lines, [l.get_label() for l in lines])
                self.axisColoring()
            else:
                for i in range(numData):
                    self.host[self.figColCnt, self.figRowCnt].scatter(data[colNumX[i]], data[colNumY[i]], label = legendName[i])
        elif plotType == '3d':
            self.host[self.figColCnt, self.figRowCnt].axis('off')
            numOfRow = 2 if numOfPlots > 1 else 1
            self.host[self.figColCnt, self.figRowCnt] = self.fig.add_subplot(math.ceil(numOfPlots / numOfRow), numOfRow, plotCounter + 1, projection = '3d')
            for i in range(numData):
                self.host[self.figColCnt, self.figRowCnt].plot(data[colNumX[i]], data[colNumY[i]], data[colNumZ[i]],  label = legendName[i])
            # padding and scaling options for z-axis
            self.host[self.figColCnt, self.figRowCnt].axes.zaxis.labelpad = config.zAxis_labelPad
            self.host[self.figColCnt, self.figRowCnt].set_zscale(config.scaleZ)
        self.padAndScale()
        
###################### USER INTERACTIONS
class userInteractions:
    # =============================== Initializer
    def __init__(self):
        self.defaultThirdAxis = False
        self.defaultThreeD = False
        self.printQuestion = 'q'
        self.printFailure = 'f'
        self.printSuccess = 's'
        self.defaultLabels = [] 
        self.data = []
        self.plotTypes = ['bar', 'box', 'cdf', 'histogram', 'line', 'scatter', 'line + scatter', '3d']
        self.printVars = []
        self.minPlotType = 1
        self.maxPlotType = len(self.plotTypes) 
        self.defaultMinX = 1
        self.defaultMaxX = 100
        self.defaultResX = 1
        self.defaultBinRes = 1
        self.defaultNumOfPlots = 1
        self.defaultFetchColX = 0
        self.defaultFetchColY = 1
        self.defaultFetchColZ = 2
        self.defaultX = np.arange(float(self.defaultMinX), float(self.defaultMaxX), float(self.defaultResX))
        self.defaultY = self.defaultX ** 2
        self.defaultZ = self.defaultY ** 2
        self.printWelcomeTxt = True
       
        # Set default values
        self.thirdAxis = self.defaultThirdAxis
        self.threeD = self.defaultThreeD
        self.legendName = []
        self.xLabel = config.defaultXLabel
        self.yLabel = config.defaultYLabel
        self.yLabel2 = config.defaultYLabel
        self.zLabel = config.defaultZLabel
        self.title = config.defaultTitle
        self.minX = self.defaultMinX
        self.maxX = self.defaultMaxX
        self.resX = self.defaultResX
        self.x = self.defaultX
        self.y = self.defaultY
        self.z = self.defaultZ
        self.maxNumXAxis = 0 # I don't know whether this is a right value to take, might cause errors. DOUBLE CHECK
        self.fetchColX = []
        self.fetchColY = []
        self.fetchColZ = []
        self.minColNum = 0
        self.yDataCounter = 0
        self.numOfPlots = self.defaultNumOfPlots
        self.binRes = self.defaultBinRes
        self.csvData = True
        self.fetchXFunc = False
        self.fetchYFunc = False
        self.fetchZFunc = False
        self.fetchXFunc2 = False
        self.fetchYFunc2 = False
        self.fetchZFunc2 = False
        self.plotPyt = None
        self.numData = 0

        # Print messages
        self.qTxtFileName = f"""
\n\n{Back.BLUE}PYTHON3 PLOTTER{Back.BLACK}\n\n
Type [{Fore.YELLOW}exit{Fore.WHITE} || {Fore.YELLOW}EXIT{Fore.WHITE} || {Fore.YELLOW}quit{Fore.WHITE} || {Fore.YELLOW}QUIT{Fore.WHITE}] to terminate the program at any step.

Enter the name of your data file (located in the same directory of program)."""
        self.qTxtTypeOfPlot = """
GRAPH #: %d

What type of graph do you want to plot? \nOptions:"""
        self.qTxtDefault = f"""
Just hit [{Fore.YELLOW}enter{Fore.WHITE}] for default: ({Fore.CYAN}%s{Fore.WHITE})\n\n"""
        self.qTxtSelectYN = f"""
Please select [{Fore.YELLOW}yY{Fore.WHITE}] or [{Fore.YELLOW}nN{Fore.WHITE}]."""
        self.qTxtNumOfPlots = """
How many graphs do you want to plot?"""
        self.qTxtSkipCsvDataFetch = f"""
If you want to derive data ONLY from a function, you may skip this part by typing [{Fore.YELLOW}sS{Fore.WHITE}] \n\n"""
        self.qTxtDataFromFunction = f"""
If you want to derive data from a function, please type [{Fore.YELLOW}fF{Fore.WHITE}] \n\n"""
        self.qTxtFetchCol = """
What is the column number in your input data for %s-axis?"""
        self.qTxtNoMoreYData = f"""
{Fore.WHITE}If you don't want to plot more data in this graph, please type [{Fore.YELLOW}qQ{Fore.WHITE}]"""
        self.qTxtMinMaxResX = f"""
Please enter the min, max. and resolution of x-axis."""
        self.qTxtEnterFormula = f"""
Enter the formula %s(%s). You may type 
{Fore.YELLOW}numpy (np.*){Fore.WHITE} and {Fore.YELLOW}math (math.*) {Fore.WHITE}functions in your formula."""
        self.qTxtDelimeter = f"""
What is the delimeter?. E.g, type [{Fore.YELLOW},{Fore.WHITE}] to separate data with commas. """
        self.qTxtBinResolution = f"""
What is the bin resolution for dataset {Fore.CYAN}%d{Fore.WHITE}? (e.g. resolution of your data)"""
        self.qTxtMultiGraph = f"""
Do you want to plot multiple graphs? ({Fore.YELLOW}y/N{Fore.WHITE})"""
        self.qTxtMultiXAxis = f"""
Do you want to use different x-axis for each subplot? ({Fore.YELLOW}y/N{Fore.WHITE})"""
        self.qTxtThreeDGraph = f"""
Do you want to plot the graph in 3D? ({Fore.YELLOW}y/N{Fore.WHITE})"""    
        self.qTxtThirdAxis = f"""
Do you want to enable 3rd axis on the graph?"""
        self.qTxtNumColXAxis = """
How many columns are x-axes data in your input csv file?"""
        self.qTxtFetchXAxisColNum = f"""
What is the column number of x-axis for your dataset %d?"""
        self.qTxtLegendName = """
What is the %s name for dataset %d? """ 
        self.qTxtLabelName = """
What is the label name of %s-axis? """    
        self.qTxtTitleName = """
What is the title name of the subplot? """
        self.qTxtMainTitleName = """
What is the main title name of the graph? """ 
        self.fTxtDefault = f"""
Just hit [{Fore.YELLOW}enter{Fore.RED}] for default: ({Fore.CYAN}%s{Fore.RED})\n\n"""
        self.fTxtNotValid = f"""
{Fore.RED}Your input is not valid. """
        self.fInputDataNotValid = f"""
{Fore.RED}Conversion of your input data to float type has failed. 
Please fix the data in your csv file 
and then re-run the program"""
        self.fTxtTypeBetween = """
Please type between [%d] and [%d]. """
        self.fTxtTypeIntOrFloat = """
Please type an integer or float. """
        self.fTxtTypeCorrFormula = """
Please type a valid formula or function from 
numpy (np.*) or math (math.*) libraries. \n\n """
        self.fTxtDelLength = """
Delimeter length cannot be > 1. """
        self.fTxtNumXAxes = f"""
Please enter a number between {Fore.YELLOW}%d{Fore.WHITE} and {Fore.YELLOW}%d{Fore.WHITE} """
        self.fTxtDataSizeNoMatch = """
Please make sure that x and y data sizes match! """
        self.yTxtPlotType = f"""
{Fore.GREEN}Selected plot type is: {Fore.CYAN}%s """
        self.yTxtNumOfPlots = f"""
{Fore.GREEN} Number of plots to be graphed: {Fore.CYAN}%d """
        self.yTxtFileName = f"""
{Fore.GREEN}Your input file: {Fore.CYAN}%s {Fore.GREEN}is found. """
        self.yTxtFetchCol= f"""
{Fore.GREEN}Selected column for %s-axis: {Fore.CYAN}%s """
        self.yTxtDataFromFunction = f"""
{Fore.GREEN}Your inputs are accepted: \n\n %s: {Fore.CYAN}%s"""
        self.yTxtDelimeter = f"""
{Fore.GREEN}Selected delimeter is: ({Fore.CYAN}%s{Fore.GREEN}) """
        self.yTxtMultiGraph = f"""
{Fore.GREEN}Multiple graphs enabled: {Fore.CYAN}%r """
        self.yTxtMultiXAxis = f"""
{Fore.GREEN}Multiple x-axis enabled: {Fore.CYAN}%r """
        self.yTxtNumXAxis = f"""
{Fore.GREEN}Number of x-axis: {Fore.CYAN}%d """
        self.yTxtFetchXAxisColNum = f"""
{Fore.GREEN}Selected column numbers of x-axes are: {Fore.CYAN}%s """
        self.yTxtThreeDGraph = f"""
{Fore.GREEN}3D enabled: {Fore.CYAN}%r """
        self.yTxtThirdAxis = f"""
{Fore.GREEN}3rd axis enabled: {Fore.CYAN}%r """
        self.yTxtLegendName = f"""
{Fore.GREEN}Legend name(s) is/are: {Fore.CYAN}%s """
        self.yTxtLabelName = f"""
{Fore.GREEN}%s-axis label name(s) is/are: {Fore.CYAN}%s """
        self.yTxtTitleName = f"""
{Fore.GREEN}Title of the graph is: {Fore.CYAN}%s """
        
    # =============================== Quit the program
    def check_quit(self, input): # taken from: https://stackoverflow.com/questions/53271077/how-to-end-program-if-input-quit-with-many-if-statements
        if input in ['exit', 'EXIT', 'quit', 'QUIT']:
            sys.exit(0)
    
    # =============================== Find input file
    def inputFileFinder(self, inputFileName):
        files = os.listdir(os.getcwd())
        if inputFileName in files: 
            return True
        else: 
            return False

    # =============================== Question messages on the terminal
    def printText_question(self, printType, printVal):
        if self.processType == 'plotType': 
            # Welcome Text
            print(self.qTxtTypeOfPlot %printVal[0])
            # Get plot type from user
            for i in range(len(self.plotTypes)):
                print("%d. %s," %(i + 1, self.plotTypes[i]))
            print(self.qTxtDefault %printVal[1])
        elif self.processType == 'fetchInputData':
            print(self.qTxtFileName + self.qTxtDefault %printVal + self.qTxtSkipCsvDataFetch)
        elif self.processType == 'numOfPlots':
            print(self.qTxtNumOfPlots + self.qTxtDefault %printVal)
        elif self.processType == 'fetchColX':
            if printVal[0] == 0: # first run, do not ask whether user want to plot any more data
                print(self.qTxtFetchCol %'x' + self.fTxtTypeBetween %(self.minColNum, self.numData - 1) + self.qTxtDefault %printVal[1] + self.qTxtDataFromFunction)
            else:
                print(self.qTxtFetchCol %'x' + self.fTxtTypeBetween %(self.minColNum, self.numData - 1) + self.qTxtDefault %printVal[1] + self.qTxtDataFromFunction + self.qTxtNoMoreYData)
        elif self.processType == 'fetchColY':
            print(self.qTxtFetchCol %'y'+ self.fTxtTypeBetween %(self.minColNum, self.numData - 1) + self.qTxtDataFromFunction)
        elif self.processType == 'fetchColZ':
            print(self.qTxtFetchCol %'z' + self.fTxtTypeBetween %(self.minColNum, self.numData - 1) + self.qTxtDataFromFunction)
        elif self.processType == 'getFuncXFromUser':
            if printVal[0] == 0: # first run, do not ask whether user want to plot any more data
                print(self.qTxtMinMaxResX + self.qTxtDefault %printVal[1:])
        elif self.processType == 'getFuncYFromUser':
            print(self.qTxtEnterFormula %('y', 'x') + self.qTxtDefault %printVal)
        elif self.processType == 'getFuncZFromUser':
            print(self.qTxtEnterFormula %('z', 'x, y')+ self.qTxtDefault %printVal)
        elif self.processType == 'selectDelimeter':
            print(self.qTxtDelimeter + self.qTxtDefault %printVal)
        elif self.processType == 'binResolution':
            print(self.qTxtBinResolution %printVal + self.qTxtDefault %self.defaultBinRes)
        elif self.processType == 'checkMultiGraph':
            print(self.qTxtMultiGraph + self.qTxtDefault %printVal)
        elif self.processType == 'checkMultiXAxis':
            print(self.qTxtMultiXAxis + self.qTxtDefault %printVal)
        elif self.processType == 'checkNumXAxis':
            print(self.qTxtNumColXAxis + self.fTxtNumXAxes %(printVal[0], printVal[1]))
        elif self.processType == 'fetchXAxisColNum':
            print(self.qTxtFetchXAxisColNum % printVal + self.fTxtNumXAxes %(0, self.numData - 1))
        elif self.processType == 'checkThreeDGraph':
            print(self.qTxtThreeDGraph + self.qTxtSelectYN + self.qTxtDefault %printVal)
        elif self.processType == 'checkThirdAxis':
            print(self.qTxtThirdAxis + self.qTxtSelectYN + self.qTxtDefault %printVal)
        elif self.processType == 'getLegendNames':
            print(self.qTxtLegendName %(printVal[2], printVal[0]) + self.qTxtDefault %printVal[1])
        elif self.processType == 'getLabelX':
            print(self.qTxtLabelName %'x' + self.qTxtDefault %printVal)
        elif self.processType == 'getLabelY':
            print(self.qTxtLabelName %'y' + self.qTxtDefault %printVal)
        elif self.processType == 'getLabelZ':
            print(self.qTxtLabelName %'z' + self.qTxtDefault %printVal)
        elif self.processType == 'getTitleName':
            if printVal[0] == True: # print main title
                print(self.qTxtMainTitleName + self.qTxtDefault %printVal[1])
            else:
                print(self.qTxtTitleName + self.qTxtDefault %printVal[1])
                
    # =============================== Failure messages on the terminal
    def printText_failure(self, printType, printVal):
        if self.processType in 'plotType':
            print(self.fTxtNotValid + self.fTxtTypeBetween %(self.minPlotType, self.maxPlotType) + self.fTxtDefault %printVal)
        elif self.processType == 'fetchInputData':
            print(self.fTxtNotValid + self.fTxtDefault %printVal)
        elif self.processType == 'fetchColX':
            print(self.fTxtNotValid + self.fTxtTypeBetween %(self.minColNum, self.numData - 1))
        elif self.processType == 'fetchColY':
            print(self.fTxtNotValid + self.fTxtDataSizeNoMatch + self.fTxtTypeBetween %(self.minColNum, self.numData - 1) + self.qTxtNoMoreYData + self.qTxtDataFromFunction)
        elif self.processType == 'fetchColZ':
            print(self.fTxtNotValid + self.fTxtDataSizeNoMatch + self.fTxtTypeBetween %(self.minColNum, self.numData - 1) + self.qTxtDataFromFunction)
        elif self.processType in ['getFuncXFromUser', 'numOfPlots']:
            print(self.fTxtNotValid + self.fTxtTypeIntOrFloat + self.fTxtDefault %printVal)
        elif self.processType in 'getFuncYFromUser':
            print(self.fTxtNotValid + self.fTxtTypeCorrFormula + self.fTxtDefault %'x**2')
        elif self.processType in 'getFuncZFromUser':
            print(self.fTxtNotValid + self.fTxtTypeCorrFormula + self.fTxtDefault %'y**2')
        elif self.processType in 'selectDelimeter':
            print(self.fTxtNotValid + self.fTxtDelLength + self.fTxtDefault %printVal)
        elif self.processType in 'checkNumXAxis':
            print(self.fTxtNotValid + self.fTxtNumXAxes %(self.defaultNumXAxis, self.maxNumXAxis) + self.fTxtDefault %self.defaultNumXAxis)
        elif self.processType in 'fetchXAxisColNum':
            print(self.fTxtNotValid + self.fTxtNumXAxes %(0, self.numData - 1) + self.fTxtDefault % 0)
        elif self.processType in 'checkMultiGraph' or self.processType in 'checkMultiXAxis' or self.processType == 'checkThreeDGraph' or self.processType == 'checkThirdAxis':
            print(self.fTxtNotValid + self.qTxtSelectYN + self.fTxtDefault %printVal)
    
    # =============================== Success messages on the terminal
    def printText_success(self, printType, printVal):
        if self.processType == 'plotType':   
            print(self.yTxtPlotType %(printVal))
        if self.processType == 'numOfPlots':   
            print(self.yTxtNumOfPlots %printVal)
        elif self.processType == 'fetchInputData':
            print(self.yTxtFileName %printVal)
        elif self.processType == 'fetchColX':
            print(self.yTxtFetchCol %('x', printVal))
        elif self.processType == 'fetchColY':
            print(self.yTxtFetchCol %('y', printVal))
        elif self.processType == 'fetchColZ':
            print(self.yTxtFetchCol %('z', printVal))
        elif self.processType in 'getFuncXFromUser':
            print(self.yTxtDataFromFunction %('x', printVal))
        elif self.processType in 'getFuncYFromUser':
            print(self.yTxtDataFromFunction %('y', printVal))
        elif self.processType in 'getFuncZFromUser':
            print(self.yTxtDataFromFunction %('z', printVal))
        elif self.processType == 'selectDelimeter':
            print(self.yTxtDelimeter %printVal)
        elif self.processType == 'checkMultiGraph':
            print(self.yTxtMultiGraph %printVal)
        elif self.processType == 'checkMultiXAxis':
            print(self.yTxtMultiXAxis %printVal)
        elif self.processType == 'checkNumXAxis':
            print(self.yTxtNumXAxis %printVal)
        elif self.processType == 'fetchXAxisColNum':
            print(self.yTxtFetchXAxisColNum %printVal)
        elif self.processType == 'checkThreeDGraph':
            print(self.yTxtThreeDGraph %printVal)
        elif self.processType == 'checkThirdAxis':
            print(self.yTxtThirdAxis %printVal)
        elif self.processType == 'getLegendNames':
            print(self.yTxtLegendName %printVal)
        elif self.processType == 'getLabelX':
            print(self.yTxtLabelName %('X', printVal))
        elif self.processType == 'getLabelY':
            print(self.yTxtLabelName %('Y', printVal))
        elif self.processType == 'getLabelZ':
            print(self.yTxtLabelName %('Z', printVal))
        elif self.processType == 'getTitleName':
            print(self.yTxtTitleName %printVal)
                
    # =============================== Print messages on the terminal
    def printText(self, printType, printVal):
    
        if printType == self.printQuestion:
            self.printText_question(printType, printVal)
        elif printType == self.printFailure:
            self.printText_failure(printType, printVal)
        elif printType == self.printSuccess:
            self.printText_success(printType, printVal)
        return 0
            
    # =============================== Validate input data given by the user
    def checkUserInput(self, input):
        if self.processType == 'fetchColY' and input == '': # return default y column from csv if user pressed Enter
            input = self.defaultFetchColY
        try: 
            if self.processType in ['plotType', 'binResolution', 'checkNumXAxis', 'fetchXAxisColNum', 'numOfPlots']: # prevFuncName[i][3] is 1st prev. function name, prevFuncName[i+1][3] is 2nd most prev. func. name, etc.
                val = float(input)
                if self.processType == "plotType": # if fetchDataInfo() called, check whether user input is within defined range
                    if not (self.minPlotType <= int(input) <= self.maxPlotType):
                        raise ValueError # not correct way to use exception errors
                elif self.processType == "checkNumXAxis": 
                    if not (self.defaultNumXAxis <= int(input) <= self.maxNumXAxis):
                        raise ValueError # not correct way to use exception errors
                elif self.processType == "fetchXAxisColNum":
                    if not (0 <= val <= self.numData - 1):
                        raise ValueError # not correct way to use exception errors
            elif self.processType == 'fetchInputData':
                if input in ['s', 'S']:
                    pass
                elif not self.inputFileFinder(input) is True:
                    raise ValueError
            elif self.processType in ['fetchColX', 'fetchColY', 'fetchColZ']:
                if self.processType in ['fetchColY', 'fetchColZ'] and not input in ['f', 'F']:
                    input = int(input)
                if (input in ['f', 'F']) or (self.processType is 'fetchColX' and self.yDataCounter > 0 and input in ['q', 'Q']):
                    pass
                elif not self.minColNum <= int(input) <= self.numData - 1: 
                    raise ValueError
                elif self.processType in ['fetchColY', 'fetchColZ'] and (len(self.data[input]) != len(self.data[self.fetchColX[-1]])):
                    raise ValueError
            elif self.processType == 'selectDelimeter':
                if len(input) > 1: # delimeter length cannot be > 1
                    raise ValueError
            elif (self.processType == 'checkMultiGraph' or self.processType == 'checkMultiXAxis' or self.processType == 'checkThreeDGraph' or self.processType == 'checkThirdAxis') and not (input in ['y', 'Y', 'n', 'N']):
                raise ValueError
            elif self.processType == 'getFuncXFromUser':
                val = float(input)
            elif self.processType == 'getFuncYFromUser':
                x = np.array(self.data[self.fetchColX[-1]])
                val = eval(input)
            elif self.processType == 'getFuncZFromUser':
                x = np.array(self.data[self.fetchColX[-1]])
                y = np.array(self.data[self.fetchColY[-1]])
                val = eval(input)
        except (AttributeError, SyntaxError, NameError, TypeError, ZeroDivisionError, ValueError):
            return False
        return True
    
    # =============================== Accept input data given by the user
    def acceptUserInput(self, default):
        while True: 
            userInput = input()
            self.check_quit(userInput) 
            checkedInput = self.checkUserInput(userInput) 
            if userInput == '':
                if self.processType in ['fetchColY', 'fetchColZ'] and checkedInput == False:
                    self.printText(self.printFailure, default) # x, y, z data sizes do not match
                elif self.processType in ['getFuncYFromUser']:
                    userInput = np.array(self.data[self.fetchColX[-1]]) ** 2 # update default Y with given x input from user 
                    break
                else:
                    userInput = default
                    break
            elif checkedInput is True: # DON'T USE 'checkedInput == True' or 'checkedInput', it will mess up the code. Check this out: https://stackoverflow.com/questions/9494404/use-of-true-false-and-none-as-return-values-in-python-functions
                if (self.processType in ['checkMultiGraph', 'checkMultiXAxis', 'checkThreeDGraph', 'checkThirdAxis']) and (userInput in ['y', 'Y']):
                    userInput = True
                elif (self.processType in ['checkMultiGraph', 'checkMultiXAxis', 'checkThreeDGraph', 'checkThirdAxis']) and (userInput in ['n', 'N']):
                    userInput = False
                elif self.processType in ['getFuncXFromUser', 'binResolution', 'checkNumXAxis']:
                    userInput = float(userInput)
                elif self.processType in ['fetchXAxisColNum', 'numOfPlots']:
                    userInput = int(userInput)
                elif self.processType in ['fetchColX', 'fetchColY', 'fetchColZ']:
                    if userInput in ['f', 'F', 'q', 'Q']:
                        pass
                    else:
                        userInput = int(userInput)
                elif self.processType == 'getFuncYFromUser':
                    x = np.array(self.data[self.fetchColX[-1]])
                    userInput = eval(userInput)
                elif self.processType == 'getFuncZFromUser':
                    x = np.array(self.data[self.fetchColX[-1]]) # define "x" and "y" as arrays to be able to evaluate string input function from user in two lines below
                    y = np.array(self.data[self.fetchColY[-1]])
                    userInput = eval(userInput)
                break
            else:
                self.printText(self.printFailure, default)
        return userInput
    
    # =============================== Convert rows to cols in input data from csv
    def transposeData(self):
        self.data = list(map(list, zip(*self.data))) # transpose the self.data: rows -> columns
        self.numData = len(self.data)
       
    # =============================== Fetch default label names from csv file
    def fetchDefLabels(self, plots): 
        # Update default label names if labels are given in the input file
        if not (self.data[0][0].isdigit()): # only check one of the first-row entries. If one of them is not a number, then the other first-row entries should be the same
            for i in range(self.numData):
                self.data[i][0] = self.data[i][0] if self.data[i][0] != '' else 'blank'
                self.defaultLabels.append(self.data[i][0])
            config.defaultLegendNames = self.defaultLabels
            
            # Delete labels from input data
            for i in range(self.numData):
                del self.data[i][0]
    
    # =============================== Convert input data into float
    def convDataToFloat(self): 
        # convert input data to float 
        for i in range(self.numData):
            self.data[i] = [x for x in self.data[i] if len(x.strip()) > 0]
        for i in range(self.numData): # iterate over each column    
            for j in range(len(self.data[i])):
                try:
                    self.data[i][j] = float(self.data[i][j])
                except ValueError: 
                    print(self.fInputDataNotValid)
                    sys.exit(0)
    
    # =============================== Fetch input data from csv 
    def fetchInputData(self):
        # open csv file
        with open(config.defaultInputDir + os.sep + self.inputFile, 'r', encoding = config.defaultEncoding) as csvfile: 
            plots = csv.reader(csvfile, delimiter = self.delimeter)
            # Fetch data from each row
            for row in plots:
                self.data.append(row)
            self.transposeData()
            self.fetchDefLabels(plots)
            self.convDataToFloat()
    
    # =============================== Ask input file name from user      
    def askInputFileName(self):
        # Get input file name from user
        self.printText(self.printQuestion, config.defaultInputFile)
        self.inputFile = self.acceptUserInput(config.defaultInputFile)
        if not self.inputFile in ['s', 'S']:
            self.printText(self.printSuccess, self.inputFile)
            self.askCsvDelimeter()
            self.fetchInputData() # Fetch self.data from .csv file
        else:
            self.csvData = False
            
    # =============================== Ask csv delimeter from user      
    def askCsvDelimeter(self):
        # Get delimeter type from user
        self.processType = 'selectDelimeter'
        self.printText(self.printQuestion, config.defaultDelimeter)
        self.delimeter = self.acceptUserInput(config.defaultDelimeter)
        self.printText(self.printSuccess, self.delimeter)
        
    # =============================== Ask number of plots from user   
    def askNumOfPlots(self):
        # Ask num of plots type from user
        self.processType = 'numOfPlots'
        self.printText(self.printQuestion, self.defaultNumOfPlots)
        self.numOfPlots = self.acceptUserInput(self.defaultNumOfPlots)
        self.printText(self.printSuccess, self.numOfPlots)
       
    # =============================== Reinitialize some variables  
    def main_reinitializeVars(self):
        # Reinitialize some vars
        self.yDataCounter = 0
        self.thirdAxis = False
        self.threeD = False
        self.fetchColX = []
        self.fetchColY = []
        self.fetchColZ = []
        self.legendName = []
        
    # =============================== Ask plot type from user      
    def askPlotType(self, i):
        # Select plot type
        self.processType = 'plotType'
        printVal = [i + 1, config.defaultPlotSelect]
        self.printText(self.printQuestion, printVal)
        self.plotSelect = self.acceptUserInput(config.defaultPlotSelect)
        if not self.plotSelect == config.defaultPlotSelect:
            self.plotSelect = self.plotTypes[int(self.plotSelect) - 1] # - 1 to map user input to correct entry inside self.plotTypes[]. E.g. user input '3' will be mapped to '2' which corresponds to 'line' graph
        self.printText(self.printSuccess, self.plotSelect)
        self.threeD = True if self.plotSelect is '3d' else False
        
    # =============================== Ask x-axis csv data from user      
    def askXData_csv(self):
        self.processType = 'fetchColX'
        printVal = [self.yDataCounter, self.defaultFetchColX]
        self.printText(self.printQuestion, printVal)
        self.fetchColX.append(self.acceptUserInput(self.defaultFetchColX))
        if not self.fetchColX[-1] in ['f', 'F', 'q', 'Q']:
            self.printText(self.printSuccess, self.fetchColX)
            if self.plotSelect in ['cdf', 'histogram']: # do not accept more than 1 x-axis data, no y-axis data needed
                return True
        if self.fetchColX[-1] in ['f', 'F']:
            self.fetchColX.pop()
            self.fetchXFunc = True    
            self.fetchXFunc2 = True 
        elif self.fetchColX[-1] in ['q', 'Q']:
            self.fetchColX.pop()
            return True
        return False
     
    # =============================== Ask y- and z-axis csv data from user      
    def askYZData_csv(self):
        if self.fetchXFunc is False:
            if self.plotSelect != 'box': # no need for y-axis data for bar plot
                self.processType = 'fetchColY'
                self.printText(self.printQuestion, self.defaultFetchColY)
                self.fetchColY.append(self.acceptUserInput(self.defaultFetchColY))
                if self.fetchColY[-1] in ['f', 'F']:
                    self.fetchColY.pop()
                    self.fetchYFunc = True
                    self.fetchYFunc2 = True
                else:
                    self.printText(self.printSuccess, self.fetchColY)
            if self.plotSelect == '3d':
                self.processType = 'fetchColZ'
                self.printText(self.printQuestion, self.defaultFetchColZ)
                self.fetchColZ.append(self.acceptUserInput(self.defaultFetchColZ))
                if self.fetchColZ[-1] in ['f', 'F']:
                    self.fetchColZ.pop()
                    self.fetchZFunc = True
                    self.fetchZFunc2 = True
                else:
                    self.printText(self.printSuccess, self.fetchColZ)
                    
    # =============================== Ask x-axis func data from user      
    def askXData_func(self):
        if not self.processType in ['fetchColY', 'fetchColZ']:
            self.processType = 'getFuncXFromUser'
            if self.yDataCounter >= 1 and not self.csvData: 
                print("Please type [qQ] if you don't want to plot more data in this graph or type any other key to continue")
                userInput = input()
                if userInput in ['q', 'Q']:
                    return True
            printVal = [self.yDataCounter, self.minX, self.maxX, self.resX]
            self.printText(self.printQuestion, printVal)
            print("Min. x: ")
            self.minX = self.acceptUserInput(self.defaultMinX)
            if self.minX in ['q', 'Q']:
                return True
            print("Max. x: ")
            self.maxX = self.acceptUserInput(self.defaultMaxX)
            print("Res. x: ")
            self.resX = self.acceptUserInput(self.defaultResX)
            self.x = np.arange(self.minX, self.maxX, self.resX)
            self.printText(self.printSuccess, self.x)
            self.data.append(self.x)
            self.fetchColX.append(len(self.data) - 1) # record at which index you saved the x data in self.data matrix
            if self.plotSelect in ['cdf', 'histogram']: # do not accept more than 1 x-axis data, no y-axis data needed
                return True
            if self.fetchColX[-1] in ['q', 'Q']:
                self.fetchColX.pop()
                if (self.plotSelect is '3d' and self.yDataCounter < 2):
                    print(f"{Fore.RED}You need to enter at least 2 data sets in order to plot 3D plot")
                else:
                    return True
            return False
        
    # =============================== Ask y-axis func data from user      
    def askYData_func(self):
        self.fetchYFunc = True
        self.fetchYFunc2 = True
        if self.plotSelect != 'box' and self.processType != 'fetchColZ': # no need for y-axis data for bar plot
            self.processType = 'getFuncYFromUser'
            printVal = 'x**2'
            self.printText(self.printQuestion, printVal)
            print("y(x): ")
            self.y = self.acceptUserInput(self.defaultY)
            self.printText(self.printSuccess, self.y)
            self.data.append(self.y)
            self.fetchColY.append(len(self.data) - 1) # record at which index you saved the x data in self.data matrix
           
    # =============================== Ask z-axis func data from user      
    def askZData_func(self):
        self.fetchZFunc = True
        self.fetchZFunc2 = True
        if self.plotSelect == '3d':
            self.processType = 'getFuncZFromUser'
            printVal = 'y**2'
            self.printText(self.printQuestion, printVal)
            print("z(x, y): ")
            self.z = self.acceptUserInput(self.defaultZ)
            self.printText(self.printSuccess, self.z)
            self.data.append(self.z)
            self.fetchColZ.append(len(self.data) - 1) # record at which index you saved the x data in self.data matrix
    
    # =============================== Ask legend names of fetched data from user      
    def askLegendNames(self, i):
        # Fetch legend name(s)
        self.processType = 'getLegendNames'
        if self.plotSelect == 'box':
            if not self.csvData or self.fetchXFunc:
                printVal = [i, config.defaultXLabel, 'xtick']
                self.printText(self.printQuestion, printVal) # send i instead of legend name to be able to print dataset # in printText()
                self.legendName.append(self.acceptUserInput(config.defaultXLabel))
            else:
                printVal = [i, self.defaultLabels[self.fetchColX[-1]], 'xtick']
                self.printText(self.printQuestion, printVal) # send i instead of legend name to be able to print dataset # in printText()
                self.legendName.append(self.acceptUserInput(self.defaultLabels[self.fetchColX[-1]]))
            self.printText(self.printSuccess, self.legendName)
        elif self.plotSelect == '3d': 
            if not self.csvData or self.fetchZFunc:
                printVal = [i, config.defaultZLabel, 'legend']
                self.printText(self.printQuestion, printVal) # send i instead of legend name to be able to print dataset # in printText()
                self.legendName.append(self.acceptUserInput(config.defaultZLabel))
            else:
                printVal = [i, self.defaultLabels[self.fetchColZ[-1]], 'legend']
                self.printText(self.printQuestion, printVal) # send i instead of legend name to be able to print dataset # in printText()
                self.legendName.append(self.acceptUserInput(self.defaultLabels[self.fetchColZ[-1]]))
            self.printText(self.printSuccess, self.legendName)
        else:
            if not self.csvData or self.fetchYFunc:
                printVal = [i, config.defaultYLabel, 'legend']
                self.printText(self.printQuestion, printVal) # send i instead of legend name to be able to print dataset # in printText()
                self.legendName.append(self.acceptUserInput(config.defaultYLabel))
            else:
                printVal = [i, self.defaultLabels[self.fetchColY[-1]], 'legend']
                self.printText(self.printQuestion, printVal) # send i instead of legend name to be able to print dataset # in printText()
                self.legendName.append(self.acceptUserInput(self.defaultLabels[self.fetchColY[-1]]))
            self.printText(self.printSuccess, self.legendName)
        self.fetchXFunc = False
        self.fetchYFunc = False
        self.fetchZFunc = False
    
    # =============================== Ask user if 3rd axis to be enabled in graph
    def ask3rdAxis(self):
        # Check 3rd axis
        if self.plotSelect in ['line', 'scatter'] and self.yDataCounter == 2:
            self.processType = 'checkThirdAxis'
            self.printText(self.printQuestion, self.defaultThirdAxis)
            self.thirdAxis = self.acceptUserInput(self.defaultThirdAxis)
            self.printText(self.printSuccess, self.thirdAxis)
            
    # =============================== Ask x-axis label name from user
    def askXLabel(self):
        # Fetch x-label
        self.processType = 'getLabelX'
        if self.plotSelect == 'box':
            self.printText(self.printQuestion, config.defaultXLabel) # send i instead of legend name to be able to print dataset # in printText()
            self.xLabel = (self.acceptUserInput(config.defaultXLabel))
        else:
            if not self.csvData or self.fetchXFunc2:
                self.printText(self.printQuestion, config.defaultXLabel) # send i instead of legend name to be able to print dataset # in printText()
                self.xLabel = (self.acceptUserInput(config.defaultXLabel))
            else:
                self.printText(self.printQuestion, self.defaultLabels[self.fetchColX[-1]]) 
                self.xLabel = self.acceptUserInput(self.defaultLabels[self.fetchColX[-1]])
            self.printText(self.printSuccess, self.xLabel)
    
    # =============================== Ask bin resolution for histogram graphs from user
    def askBinRes(self):
        if (self.plotSelect == 'histogram'):
            self.processType = 'binResolution'
            self.printText(self.printQuestion, self.defaultBinRes)
            self.binRes = self.acceptUserInput(self.defaultBinRes)
            self.printText(self.printSuccess, self.binRes)
    
    # =============================== Ask y- and z-axis label names from user
    def askYZLabel(self):
        if self.plotSelect == 'cdf':
            self.yLabel = config.cdfDefaultLabel
        elif self.plotSelect == 'histogram':
            self.yLabel = config.histDefaultLabel
        elif self.plotSelect == 'box':
            self.processType = 'getLabelY'
            if not self.csvData or self.fetchYFunc2:
                self.printText(self.printQuestion, config.defaultXLabel) # send i instead of legend name to be able to print dataset # in printText()
                self.yLabel = (self.acceptUserInput(config.defaultXLabel)) # fetch x label to the y-axis
            else:
                self.printText(self.printQuestion, self.defaultLabels[self.fetchColX[-1]]) 
                self.yLabel = (self.acceptUserInput(self.defaultLabels[self.fetchColX[-1]]))
            self.printText(self.printSuccess, self.yLabel)
        
        if not self.plotSelect in ['cdf', 'histogram', 'box']:
            # Fetch y-label
            self.processType = 'getLabelY'
            if not self.thirdAxis:
                if not self.csvData or self.fetchYFunc2:
                    self.printText(self.printQuestion, config.defaultYLabel) # send i instead of legend name to be able to print dataset # in printText()
                    self.yLabel = self.acceptUserInput(config.defaultYLabel)
                else:
                    self.printText(self.printQuestion, self.defaultLabels[self.fetchColY[-1]]) 
                    self.yLabel = self.acceptUserInput(self.defaultLabels[self.fetchColY[-1]])
                self.printText(self.printSuccess, self.yLabel)
            else:
                # Fetch y-label for the 3rd axis
                for j in range(2):
                    if not self.csvData or self.fetchYFunc2:
                        self.printText(self.printQuestion, config.defaultYLabel) # send j instead of legend name to be able to print dataset # in printText()
                        self.yLabel2 = self.acceptUserInput(config.defaultYLabel) # fetch x label to the y-axis
                    else:
                        self.printText(self.printQuestion, self.defaultLabels[self.fetchColY[-2 + j]]) 
                        self.yLabel2 = self.acceptUserInput(self.defaultLabels[self.fetchColY[-2 + j]])
                    self.printText(self.printSuccess, self.yLabel2)
            if self.plotSelect == '3d':
                # set z-axis label
                self.processType = 'getLabelZ'
                if not self.csvData or self.fetchZFunc2:
                    self.printText(self.printQuestion, config.defaultZLabel) # send i instead of legend name to be able to print dataset # in printText()
                    self.zLabel = self.acceptUserInput(config.defaultZLabel)
                else:
                    self.printText(self.printQuestion, self.defaultLabels[self.fetchColZ[-1]]) 
                    self.zLabel = self.acceptUserInput(self.defaultLabels[self.fetchColZ[-1]])
                self.printText(self.printSuccess, self.zLabel)
            self.fetchXFunc2 = False
            self.fetchYFunc2 = False
            self.fetchZFunc2 = False
    
    # =============================== Ask subplot title name from user
    def askSubplotTitle(self):
        if self.numOfPlots > 1: 
            # Fetch title name from user
            self.processType = 'getTitleName'
            mainTitle = False
            printVar = [mainTitle, config.defaultTitle]
            self.printText(self.printQuestion, printVar) 
            self.title = self.acceptUserInput(config.defaultTitle)
            self.printText(self.printSuccess, self.title)
    
    # =============================== Ask main title name from user
    def askMainTitle(self):
        self.processType = 'getTitleName'
        mainTitle = True
        printVar = [mainTitle, config.defaultTitle]
        self.printText(self.printQuestion, printVar) 
        self.title = self.acceptUserInput(config.defaultTitle)
        self.printText(self.printSuccess, self.title)
        
    # =============================== User Interactions             
    def main(self): 
        self.processType = 'fetchInputData'
        self.askInputFileName()
        self.askNumOfPlots()
        self.initiatePlotter() # Initiate the plotter class
        self.plotPyt.prepPlot(self.numOfPlots) # prepare the plot environment
        self.main_reinitializeVars()
        # main plot loop
        for i in range(self.numOfPlots):
            self.askPlotType(i)
            # data generation loop
            while True:
                if self.csvData:
                    # Ask data of x-axis from user
                    if self.askXData_csv():
                        break
                    else:
                        pass
                    self.askYZData_csv()
                if not self.csvData or self.fetchXFunc or self.fetchYFunc or self.fetchZFunc: # generate data from function
                    if self.askXData_func():
                        break
                    else:
                        pass   
                    self.askYData_func()
                    self.askZData_func()
                self.yDataCounter += 1
                self.askLegendNames(i)
            self.ask3rdAxis()
            self.askXLabel()
            self.askBinRes()
            self.askYZLabel()
            self.askSubplotTitle()
            plotCounter = i
            self.plotPyt.mainPlotter(plotCounter, self.numOfPlots, self.plotSelect, self.yDataCounter, self.fetchColX, self.fetchColY, self.fetchColZ, self.legendName, self.binRes, self.thirdAxis, self.data) # TODO: Why do I send self.numOfPlots???
            self.plotPyt.plotLabeling(self.xLabel, self.yLabel, self.yLabel2, self.zLabel, self.thirdAxis, self.threeD, self.title, self.numOfPlots, plotCounter)
            self.main_reinitializeVars() 
            
        # Fetch title name from user
        self.askMainTitle()
        self.plotPyt.showPlot(self.title, self.numOfPlots)
            
       
    # =============================== Initiate and Run the PlotPython Class
    def initiatePlotter(self):
        self.plotPyt = plotPython()

# #################################### MAIN
task = userInteractions()
task.main() # Fetch self.data-related info from user
task.initiatePlotter()  