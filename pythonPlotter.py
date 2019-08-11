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
init(autoreset = True) # turn off colors after each print()

###################### PLOTTER
class plotPython:
    # =============================== Initializer / Instance attributes
    def __init__(self, numData, thirdAxis, threeD, multiGraph, legendName, xLabel, yLabel, zLabel, title, data, binRes, xAxesColNums):
        self.numData = numData
        self.thirdAxis = thirdAxis
        self.threeD = threeD
        self.multiGraph = multiGraph
        self.legendName = legendName
        self.xLabel = xLabel
        self.yLabel = yLabel
        self.zLabel = zLabel
        self.title  = title
        self.data = data
        self.binRes = binRes
        self.xAxesColNums = xAxesColNums
        self.colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#bcbd22', '#17becf'] # blue, orange, green, red, purple, brown, pink, dark gray, light green, cyan. Check out https://matplotlib.org/3.1.0/users/dflt_style_changes.html
        self.lineTypes = ['-', '--', '-.', '.']
        self.plotFuncName = ''
        self.color_y1 = 0 
        self.color_y2 = 1 
        self.logDir = "logs"
        self.figFormat = "pdf"
        self.figDimX = 19.2 # save the figure in 1920x1080 format
        self.figDimY = 10.8
        self.dpi = 1000 # figure resolution
        self.axisLabelSize = 15 
        self.titleLabelSize = 25
        self.date = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.fTxtNoXServer = f"""
{Fore.RED}Your X-server is not running, cannot plot the graph.
Please turn on your X-server first and then hit [enter]"""
        
    # =============================== Prepare the plot
    def prepPlot(self, numOfPlots): 
        exitLoop = False
        while True:
            try: 
                self.fig = plt.figure(figsize = (self.figDimX,self.figDimY)) 
                exitLoop = True
            except tkinter._tkinter.TclError: # fail if X-server not running
                print(self.fTxtNoXServer)
                userInput = input()
                if userInput in ['exit', 'EXIT', 'quit', 'QUIT']:
                    sys.exit(0)
                exitLoop = False
            if exitLoop: 
                break
        
        #if self.threeD == True: 
        #    self.host = self.fig.add_subplot(111, projection = '3d')
        #else: 
        #    self.host = self.fig.add_subplot(111)
        
            
    # =============================== Color the axes
    def axisColoring(self):
        # color the axes of the plot. For now, it is implemented only for 3-axis 2D graphs. TO BE EXTENDED!
        self.host.spines['left'].set_color(self.colors[self.color_y1])
        self.host.tick_params(axis='y', colors=self.colors[self.color_y1])
        self.host.yaxis.label.set_color(self.colors[self.color_y1])
        self.guest.spines['right'].set_color(self.colors[self.color_y2])
        self.guest.tick_params(axis='y', colors=self.colors[self.color_y2])
        self.guest.yaxis.label.set_color(self.colors[self.color_y2])
    
    # =============================== Show the plot
    def plotLabeling(self, xLabel, yLabel, zLabel, thirdAxis, threeD, title, numOfPlots):
        self.fig.savefig('%s' %self.logDir + os.sep + '%s.%s' %(self.date, self.figFormat), format = self.figFormat, dpi = self.dpi)
        self.host.set_xlabel(xLabel, size = self.axisLabelSize)
        self.host.set_ylabel(yLabel, size = self.axisLabelSize)
        if thirdAxis:
            self.guest.set_ylabel(yLabel, size = self.axisLabelSize)
        if threeD: 
            self.host.set_zlabel(zLabel, size = self.axisLabelSize)
        #self.fig.suptitle(title, size = self.titleLabelSize) # Main title
        if numOfPlots > 1:
            self.host.title.set_text(title)
            self.host.title.set_size(self.axisLabelSize)
        if not thirdAxis:
            plt.legend()
        
    def showPlot(self, title, numOfPlots):
        #plt.title(title, size = self.titleLabelSize)
        self.fig.suptitle(title, size = self.titleLabelSize) # Main title
        if numOfPlots == 2: 
            self.fig.subplots_adjust(hspace = 0.5)

        self.fig.savefig('%s' %self.logDir + os.sep + '%s.%s' %(self.date, self.figFormat), bbox_inches = 'tight', format = self.figFormat, dpi = self.dpi)
        #self.fig.tight_layout() # to adjust spacing between graphs and labels
        self.fig.tight_layout() # to adjust spacing between graphs and labels
        plt.show()
        
    # =============================== Plot bar graph
    def barPlot(self):
        self.mainPlotter()
    
    # =============================== Plot box graph
    def boxPlot(self):
        self.prepPlot()
        plt.boxplot(self.data)
        self.showPlot()
    
    # =============================== Plot CDF graph
    def cdfPlot(self):
        self.mainPlotter()
        
    # =============================== Plot line graph
    def linePlot(self):
        self.mainPlotter()
        
    # =============================== Plot scatter Graph
    def scatterPlot(self):
        self.mainPlotter()
    
    # =============================== Plot histogram Graph    
    def histogramPlot(self):
        self.mainPlotter()
    
    # =============================== Plotter function
    def mainPlotter(self, plotCounter, numOfPlots, plotType, numData, colNumX, colNumY, colNumZ, legendName, binRes, thirdAxis, data):
        plotPerRow = 2 if numOfPlots > 1 else 1
        if plotType == '3d':
            self.host = self.fig.add_subplot(math.ceil(numOfPlots / plotPerRow), plotPerRow, plotCounter + 1, projection = '3d') # # of plots in x-axis, # of plots in y-axis, plotNum(e.g. 1 is the left top plot, 2 is the right top)
        else:
            if numOfPlots == 2: # display vertically if only 2 graphs 
                self.host = self.fig.add_subplot(plotPerRow, math.ceil(numOfPlots / plotPerRow), plotCounter + 1) # # of plots in x-axis, # of plots in y-axis, plotNum(e.g. 1 is the left top plot, 2 is the right top)
            else:
                self.host = self.fig.add_subplot(math.ceil(numOfPlots / plotPerRow), plotPerRow, plotCounter + 1)
        if plotType == 'bar':
            for i in range(numData):
                self.host.bar(data[colNumX[i]], data[colNumY[i]], label = legendName[i]) 
        elif plotType == 'box':
            boxData = []
            for i in range(numData):
                boxData.append(data[colNumX[i]])
            self.host.boxplot(boxData, positions = np.array(range(len(boxData))) + 1)
            self.host.set_xticklabels(legendName)
            #self.host.set(xticklabels.append(str(i))) np.array(range(len(boxData))) + 1
        elif plotType == 'cdf':
            bin_edges_list = [] 
            cdfData = []
            data_size = len(data[colNumX[0]]) # taken from: https://stackoverflow.com/questions/24575869/read-file-and-plot-cdf-in-python
            #for j in range(numData - 1):
            data_set = sorted(set(data[colNumX[0]]))
            bins = np.append(data_set, data_set[-1] + 1)
            counts, bin_edges = np.histogram(data[colNumX[0]], bins = bins, density = False) # Use histogram function to bin data
            counts = counts.astype(float) / data_size
            #bin_edges_list.append(bin_edges)
            cdfData = np.cumsum(counts)
            self.host.plot(bin_edges[0:-1], cdfData) 
        elif plotType == 'histogram':
            self.bins = np.arange(min(data[colNumX[0]]) - binRes, max(data[colNumX[0]]) + binRes * 2, binRes)
            self.host.hist(data[colNumX[0]], bins = self.bins, align = 'left')  
            plt.xticks(self.bins[:-1])
        elif plotType in ['line', 'line + scatter']:
            if thirdAxis:
                if plotType == 'line':
                    p1, = self.host.plot(data[colNumX[0]], data[colNumY[0]], self.colors[self.color_y1], label = legendName[0])  
                else:
                    p1, = self.host.plot(data[colNumX[0]], data[colNumY[0]], '-o', self.colors[self.color_y1], label = legendName[0])  
                self.guest = self.host.twinx() # setup 2nd axis based on the first graph
                if plotType == 'line':
                    p2, = self.guest.plot(data[colNumX[1]], data[colNumY[1]], self.colors[self.color_y2], label = legendName[1])             
                else:
                    p2, = self.guest.plot(data[colNumX[1]], data[colNumY[1]], '-o', self.colors[self.color_y2], label = legendName[1]) 
                lines = [p1, p2]
                self.host.legend(lines, [l.get_label() for l in lines])
                self.axisColoring()
            else:
                for i in range(numData):
                    if plotType == 'line':
                        self.host.plot(data[colNumX[i]], data[colNumY[i]], label = legendName[i])
                    else:
                        self.host.plot(data[colNumX[i]], data[colNumY[i]], '-o', label = legendName[i])
        elif plotType == 'scatter':
            if thirdAxis:
                p1 = self.host.scatter(data[colNumX[0]], data[colNumY[0]], c = self.colors[self.color_y1], label = legendName[0])  
                #plt.legend()
                self.guest = self.host.twinx() # setup 2nd axis based on the first graph
                p2 = self.guest.scatter(data[colNumX[1]], data[colNumY[1]], c = self.colors[self.color_y2], label = legendName[1])             
                lines = [p1, p2]
                self.host.legend(lines, [l.get_label() for l in lines])
                self.axisColoring()
            else:
                for i in range(numData):
                    self.host.scatter(data[colNumX[i]], data[colNumY[i]], label = legendName[i])
                    #self.host.plot(data[colNumX[i]], data[colNumY[i]], label = legendName[i])
        elif plotType == '3d':
            for i in range(numData):
                self.host.plot(data[colNumX[i]], data[colNumY[i]], data[colNumZ[i]],  label = legendName[i])
        
        '''
        if not self.multiGraph: # 1 graph only
            self.prepPlot()
            if not self.thirdAxis and not self.threeD:
                for i in range(1, self.numData): 
                    if prevFuncName == 'linePlot':
                        self.host.plot(self.data[0], self.data[i], label=self.legendName[i - 1]) 
                    elif prevFuncName == 'scatterPlot':
                        self.host.scatter(self.data[0], self.data[i], label=self.legendName[i - 1]) 
                    elif prevFuncName == 'barPlot':
                        self.host.bar(self.data[0], self.data[i], label=self.legendName[i - 1]) 
                    elif prevFuncName == 'cdfPlot':
                        print(bin_edges_list[i - 1])
                        print(cdfData[i-1])
                        self.host.plot(bin_edges_list[i - 1][0:-1], cdfData[i - 1], label = self.legendName[i - 1]) 
                    elif prevFuncName == 'histogramPlot':
                        self.bins = np.arange(min(self.data[i - 1]) - self.binRes[i - 1], max(self.data[i - 1]) + self.binRes[i - 1] * 2, self.binRes[i - 1])
                        self.host.hist(self.data[i - 1], bins=self.bins, align='left', label=self.legendName[i - 1])  
                        plt.xticks(self.bins[:-1])
                    else:
                        break
            elif self.threeD: # plot 3D
                for i in range(2, self.numData):
                    if prevFuncName == 'linePlot':
                        self.host.plot(self.data[0], self.data[1], self.data[i],  label=self.legendName[0]) 
                    elif prevFuncName == 'scatterPlot':
                        self.host.scatter(self.data[0], self.data[1], self.data[i],  label=self.legendName[0]) 
                    elif prevFuncName == 'barPlot':
                        self.host.bar(self.data[0], self.data[1], self.data[i],  label=self.legendName[0]) 
                    else:
                        break
            else: # plot with a 3rd axis, 
            # taken from: https://stackoverflow.com/questions/48618992/matplotlib-graph-with-more-than-2-y-axes
                if prevFuncName == 'linePlot':
                    p1, = self.host.plot(self.data[0], self.data[1], self.colors[self.color_y1], label=self.legendName[0]) 
                elif prevFuncName == 'scatterPlot':
                    p1, = self.host.scatter(self.data[0], self.data[1], self.colors[1]+self.lineTypes[0], label=self.legendName[0])  
                elif prevFuncName == 'barPlot':
                    p1, = self.host.bar(self.data[0], self.data[1], self.colors[1]+self.lineTypes[0], label=self.legendName[0])  
                plt.legend()
                self.guest = self.host.twinx() # setup 2nd axis based on the first graph
                if prevFuncName == 'linePlot':
                    p2, = self.guest.plot(self.data[0], self.data[2], self.colors[self.color_y2], label=self.legendName[1])             
                elif prevFuncName == 'scatterPlot':
                    p2, = self.guest.scatter(self.data[0], self.data[2], self.colors[2]+self.lineTypes[1], label=self.legendName[1])
                elif prevFuncName == 'barPlot':
                    p2, = self.guest.bar(self.data[0], self.data[2], self.colors[2]+self.lineTypes[1], label=self.legendName[1])
                lines = [p1, p2]
                self.host.legend(lines, [l.get_label() for l in lines])
                self.axisColoring()
            #self.showPlot()
        else: # multiple graphs
            plotRows = 2 # print 2 cols of plots
            self.fig = plt.figure(figsize=(self.figDimX,self.figDimY))
            self.fig.suptitle(self.title, size = self.titleLabelSize) # Main title
            i = 1
            for i in range(1, self.numData - len(self.xAxesColNums)): # +1 to make subplot values start from 1
                if not self.thirdAxis and not self.threeD:
                    #for i in range(1, numData): 
                    self.host = self.fig.add_subplot(math.ceil((self.numData - len(self.xAxesColNums))/ plotRows), (self.numData - len(self.xAxesColNums)) / plotRows, i)
                    if prevFuncName == 'linePlot':
                        self.host.plot(self.data[self.xAxesColNums[i]], self.data[i], label=self.legendName[i - 1])
                    elif prevFuncName == 'scatterPlot':
                        self.host.scatter(self.data[self.xAxesColNums[i]], self.data[i], label=self.legendName[i - 1])
                    elif prevFuncName == 'barPlot':
                        self.host.bar(self.data[self.xAxesColNums[i]], self.data[i], label=self.legendName[i - 1])
                    elif prevFuncName == 'cdfPlot':
                        self.host.plot(bin_edges_list[i - 1][0:-1], cdfData[i - 1], label=self.legendName[i - 1])
                    elif prevFuncName == 'histogramPlot':
                        self.bins = np.arange(min(self.data[i - 1]) - self.binRes[i - 1], max(self.data[i - 1]) + self.binRes[i - 1] * 2, self.binRes[i - 1])
                        self.host.hist(self.data[i - 1], bins=self.bins, align='left', label=self.legendName[i - 1])
                        plt.xticks(self.bins[:-1])
                    else:
                        break
                    self.host.set_xlabel(self.xLabel)
                    self.host.set_ylabel(self.yLabel[i - 1])
                    plt.legend()
                elif self.threeD: # plot 3D, TBD
                    for i in range(2, self.numData): 
                        self.host = self.fig.add_subplot(j, k, i, projection = '3d')
                        if prevFuncName == 'linePlot':
                            self.host.plot(self.data[0], self.data[1], self.data[i],  label=self.legendName[0])
                        elif prevFuncName == 'scatterPlot':
                            self.host.scatter(self.data[0], self.data[1], self.data[i],  label=self.legendName[0])
                        elif prevFuncName == 'barPlot':
                            self.host.bar(self.data[0], self.data[1], self.data[i],  label=self.legendName[0])
                        else:
                            break   
                i = i + 1 
                if i == self.numData + 1: # You've plotted all the graphs
                    break
            
            self.fig.savefig('%s' %self.logDir + os.sep + '%s.%s' %(self.date, self.figFormat), format = self.figFormat, dpi = self.dpi)
            plt.tight_layout()
            plt.show()
            '''
###################### USER INTERACTIONS
class userInteractions:
    # =============================== Initializer
    def __init__(self):
        self.defaultThirdAxis = False
        self.defaultThreeD = False
        self.defaultMultiGraph = False
        self.defaultMultiXAxis = False
        self.defaultNumXAxis = 2
        self.printQuestion = 'q'
        self.printFailure = 'f'
        self.printSuccess = 's'
        self.defaultPlotSelect = 'line'
        self.defaultInputDir = 'inputCsvFiles'
        self.defaultInputFile = 'plotFromCsv.csv'
        self.defaultDelimeter = ','
        self.defaultEncoding = 'utf-8-sig'
        self.defaultLegendNames = ['self.data']
        self.defaultLabels = [] 
        self.defaultXLabel = 'x'
        self.defaultYLabel = 'y'
        self.defaultZLabel = 'z'
        self.defaultTitle = 'title'
        self.histDefaultLabel = 'Frequency of Occurence'
        self.cdfDefaultLabel = 'CDF (%)'
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
        self.defaultZ = self.defaultX ** 2 + self.defaultY ** 2
        self.printWelcomeTxt = True
       
        # Set default values
        self.thirdAxis = self.defaultThirdAxis
        self.threeD = self.defaultThreeD
        self.multiGraph = self.defaultMultiGraph
        self.multiXAxis = self.defaultMultiXAxis
        self.numXAxis = self.defaultNumXAxis
        self.legendName = []
        self.xLabel = self.defaultXLabel
        self.yLabel = self.defaultYLabel
        self.zLabel = self.defaultZLabel
        self.title = self.defaultTitle
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
        self.xAxesColNums = []
        self.numYDataPerPlot = []
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
Please select [{Fore.YELLOW}yY{Fore.WHITE}] or [{Fore.YELLOW}nN]{Fore.WHITE}."""
        self.qTxtNumOfPlots = """
How many graphs do you want to plot?"""
        self.qTxtSkipCsvDataFetch = f"""
If you want to derive data ONLY from a function, you may skip this part by typing [{Fore.YELLOW}sS{Fore.WHITE}] \n\n"""
        self.qTxtDataFromFunction = f"""
If you want to derive data from a function, please type [{Fore.YELLOW}fF{Fore.WHITE}] \n\n"""
        self.qTxtFetchCol = """
What is the column number in your input data for %s-axis?"""
        self.qTxtNoMoreYData = f"""
If you don't want to plot more data in this graph, please type [{Fore.YELLOW}qQ{Fore.WHITE}]"""
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
Do you want to enable 3rd axis on the graph? ({Fore.YELLOW}y/N{Fore.WHITE})"""
        self.qTxtNumColXAxis = """
How many columns are x-axes data in your input csv file?"""
        self.qTxtFetchXAxisColNum = f"""
What is the column number of x-axis for your dataset %d?"""
        self.qTxtLegendName = """
What is the %s name for dataset %d? """ 
        self.qTxtLabelName = """
What is the label name of %s-axis? """
        self.qTxtLabelMultiGraph = """
Subplot %d """      
        self.qTxtLabelThirdAxis = """
%s axis """
        self.qTxtTitleName = """
What is the title name of the graph? """
        self.qTxtMainTitleName = """
What is the main title name? """ 
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
    - Please enter a number between {Fore.YELLOW}%d{Fore.WHITE} and {Fore.YELLOW}%d{Fore.WHITE} """
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

    # =============================== Print messages on the terminal
    def printText(self, printType, printVal, processType):
        if printType == self.printQuestion:
            if processType == 'plotType': 
                # Welcome Text
                print(self.qTxtTypeOfPlot %printVal[0])
                # Get plot type from user
                for i in range(len(self.plotTypes)):
                    print("%d. %s," %(i + 1, self.plotTypes[i]))
                print(self.qTxtDefault %printVal[1])
            elif processType == 'fetchInputData':
                print(self.qTxtFileName + self.qTxtDefault %printVal + self.qTxtSkipCsvDataFetch)
            elif processType == 'numOfPlots':
                print(self.qTxtNumOfPlots + self.qTxtDefault %printVal)
            elif processType == 'fetchColX':
                if printVal[0] == 0: # first run, do not ask whether user want to plot any more data
                    print(self.qTxtFetchCol %'x' + self.fTxtTypeBetween %(self.minColNum, self.numData - 1) + self.qTxtDefault %printVal[1] + self.qTxtDataFromFunction)
                else:
                    print(self.qTxtFetchCol %'x' + self.fTxtTypeBetween %(self.minColNum, self.numData - 1) + self.qTxtDefault %printVal[1] + self.qTxtDataFromFunction + self.qTxtNoMoreYData)
            elif processType == 'fetchColY':
                print(self.qTxtFetchCol %'y'+ self.fTxtTypeBetween %(self.minColNum, self.numData - 1) + self.qTxtDataFromFunction)
            elif processType == 'fetchColZ':
                print(self.qTxtFetchCol %'z' + self.fTxtTypeBetween %(self.minColNum, self.numData - 1) + self.qTxtDataFromFunction)
            elif processType == 'getFuncXFromUser':
                if printVal[0] == 0: # first run, do not ask whether user want to plot any more data
                    print(self.qTxtMinMaxResX + self.qTxtDefault %printVal[1:])
            elif processType == 'getFuncYFromUser':
                print(self.qTxtEnterFormula %('y', 'x') + self.qTxtDefault %printVal)
            elif processType == 'getFuncZFromUser':
                print(self.qTxtEnterFormula %('z', 'x, y')+ self.qTxtDefault %printVal)
            elif processType == 'selectDelimeter':
                print(self.qTxtDelimeter + self.qTxtDefault %printVal)
            elif processType == 'binResolution':
                print(self.qTxtBinResolution %printVal + self.qTxtDefault %self.defaultBinRes)
            elif processType == 'checkMultiGraph':
                print(self.qTxtMultiGraph + self.qTxtDefault %printVal)
            elif processType == 'checkMultiXAxis':
                print(self.qTxtMultiXAxis + self.qTxtDefault %printVal)
            elif processType == 'checkNumXAxis':
                print(self.qTxtNumColXAxis + self.fTxtNumXAxes %(printVal[0], printVal[1]))
            elif processType == 'fetchXAxisColNum':
                print(self.qTxtFetchXAxisColNum % printVal + self.fTxtNumXAxes %(0, self.numData - 1))
            elif processType == 'checkThreeDGraph':
                print(self.qTxtThreeDGraph + self.qTxtSelectYN + self.qTxtDefault %printVal)
            elif processType == 'checkThirdAxis':
                print(self.qTxtThirdAxis + self.qTxtSelectYN + self.qTxtDefault %printVal)
            elif processType == 'getLegendNames':
                print(self.qTxtLegendName %(printVal[2], printVal[0]) + self.qTxtDefault %printVal[1])
            elif processType == 'getLabelX':
                print(self.qTxtLabelName %'x' + self.qTxtDefault %printVal)
            elif processType == 'getLabelY':
                print(self.qTxtLabelName %'y' + self.qTxtDefault %printVal)
            elif processType == 'getLabelZ':
                print(self.qTxtLabelName %'z' + self.qTxtDefault %printVal)
            elif processType == 'getTitleName':
                if printVal[0] == True: # print main title
                    print(self.qTxtMainTitleName + self.qTxtDefault %printVal[1])
                else:
                    print(self.qTxtTitleName + self.qTxtDefault %printVal[1])

        elif printType == self.printFailure:
            if processType in 'plotType':
                print(self.fTxtNotValid + self.fTxtTypeBetween %(self.minPlotType, self.maxPlotType) + self.fTxtDefault %printVal)
            elif processType == 'fetchInputData':
                print(self.fTxtNotValid + self.fTxtDefault %printVal)
            elif processType == 'fetchColX':
                print(self.fTxtNotValid + self.fTxtTypeBetween %(self.minColNum, self.numData - 1))
            elif processType == 'fetchColY':
                print(self.fTxtNotValid + self.fTxtDataSizeNoMatch + self.fTxtTypeBetween %(self.minColNum, self.numData - 1) + self.qTxtNoMoreYData + self.qTxtDataFromFunction)
            elif processType == 'fetchColZ':
                print(self.fTxtNotValid + self.fTxtDataSizeNoMatch + self.fTxtTypeBetween %(self.minColNum, self.numData - 1) + self.qTxtDataFromFunction)
            elif processType in ['getFuncXFromUser', 'numOfPlots']:
                print(self.fTxtNotValid + self.fTxtTypeIntOrFloat + self.fTxtDefault %printVal)
            elif processType in 'getFuncYFromUser':
                print(self.fTxtNotValid + self.fTxtTypeCorrFormula + self.fTxtDefault %'x**2')
            elif processType in 'getFuncZFromUser':
                print(self.fTxtNotValid + self.fTxtTypeCorrFormula + self.fTxtDefault %'x**2 + y**2')
            elif processType in 'selectDelimeter':
                print(self.fTxtNotValid + self.fTxtDelLength + self.fTxtDefault %printVal)
            elif processType in 'checkNumXAxis':
                print(self.fTxtNotValid + self.fTxtNumXAxes %(self.defaultNumXAxis, self.maxNumXAxis) + self.fTxtDefault %self.defaultNumXAxis)
            elif processType in 'fetchXAxisColNum':
                print(self.fTxtNotValid + self.fTxtNumXAxes %(0, self.numData - 1) + self.fTxtDefault % 0)
            elif processType in 'checkMultiGraph' or processType in 'checkMultiXAxis' or processType == 'checkThreeDGraph' or processType == 'checkThirdAxis':
                print(self.fTxtNotValid + self.qTxtSelectYN + self.fTxtDefault %printVal)

        elif printType == self.printSuccess:
            if processType == 'plotType':   
                print(self.yTxtPlotType %(printVal))
            if processType == 'numOfPlots':   
                print(self.yTxtNumOfPlots %printVal)
            elif processType == 'fetchInputData':
                print(self.yTxtFileName %printVal)
            elif processType == 'fetchColX':
                print(self.yTxtFetchCol %('x', printVal))
            elif processType == 'fetchColY':
                print(self.yTxtFetchCol %('y', printVal))
            elif processType == 'fetchColZ':
                print(self.yTxtFetchCol %('z', printVal))
            elif processType in 'getFuncXFromUser':
                print(self.yTxtDataFromFunction %('x', printVal))
            elif processType in 'getFuncYFromUser':
                print(self.yTxtDataFromFunction %('y', printVal))
            elif processType in 'getFuncZFromUser':
                print(self.yTxtDataFromFunction %('z', printVal))
            elif processType == 'selectDelimeter':
                print(self.yTxtDelimeter %printVal)
            elif processType == 'checkMultiGraph':
                print(self.yTxtMultiGraph %printVal)
            elif processType == 'checkMultiXAxis':
                print(self.yTxtMultiXAxis %printVal)
            elif processType == 'checkNumXAxis':
                print(self.yTxtNumXAxis %printVal)
            elif processType == 'fetchXAxisColNum':
                print(self.yTxtFetchXAxisColNum %printVal)
            elif processType == 'checkThreeDGraph':
                print(self.yTxtThreeDGraph %printVal)
            elif processType == 'checkThirdAxis':
                print(self.yTxtThirdAxis %printVal)
            elif processType == 'getLegendNames':
                print(self.yTxtLegendName %printVal)
            elif processType == 'getLabelX':
                print(self.yTxtLabelName %('X', printVal))
            elif processType == 'getLabelY':
                print(self.yTxtLabelName %('Y', printVal))
            elif processType == 'getLabelZ':
                print(self.yTxtLabelName %('Z', printVal))
            elif processType == 'getTitleName':
                print(self.yTxtTitleName %printVal)
        return 0
            
    # =============================== Validate input data given by the user
    def checkUserInput(self, input, processType):
        if processType == 'fetchColY' and input == '':
            input = self.defaultFetchColY
        try: 
            if processType in ['plotType', 'binResolution', 'checkNumXAxis', 'fetchXAxisColNum', 'numOfPlots']: # prevFuncName[i][3] is 1st prev. function name, prevFuncName[i+1][3] is 2nd most prev. func. name, etc.
                val = float(input)
                if processType == "plotType": # if fetchDataInfo() called, check whether user input is within defined range
                    if not (self.minPlotType <= int(input) <= self.maxPlotType):
                        raise ValueError # not correct way to use exception errors
                elif processType == "checkNumXAxis": 
                    if not (self.defaultNumXAxis <= int(input) <= self.maxNumXAxis):
                        raise ValueError # not correct way to use exception errors
                elif processType == "fetchXAxisColNum":
                    if not (0 <= val <= self.numData - 1):
                        raise ValueError # not correct way to use exception errors
            elif processType == 'fetchInputData':
                if input in ['s', 'S']:
                    pass
                elif not self.inputFileFinder(input) is True:
                    raise ValueError
            elif processType in ['fetchColX', 'fetchColY', 'fetchColZ']:
                if processType in ['fetchColY', 'fetchColZ'] and not input in ['f', 'F']:
                    input = int(input)
                if (input in ['f', 'F']) or (processType is 'fetchColX' and self.yDataCounter > 0 and input in ['q', 'Q']):
                    pass
                elif not self.minColNum <= int(input) <= self.numData - 1: 
                    raise ValueError
                elif processType in ['fetchColY', 'fetchColZ'] and (len(self.data[input]) != len(self.data[self.fetchColX[-1]])):
                    raise ValueError
            elif processType == 'selectDelimeter':
                if len(input) > 1: # delimeter length cannot be > 1
                    raise ValueError
            elif (processType == 'checkMultiGraph' or processType == 'checkMultiXAxis' or processType == 'checkThreeDGraph' or processType == 'checkThirdAxis') and not (input in ['y', 'Y', 'n', 'N']):
                raise ValueError
            elif processType == 'getFuncXFromUser':
                val = float(input)
            elif processType == 'getFuncYFromUser':
                x = np.array(self.data[self.fetchColX[-1]])
                val = eval(input)
            elif processType == 'getFuncZFromUser':
                x = np.array(self.data[self.fetchColX[-1]])
                y = np.array(self.data[self.fetchColY[-1]])
                val = eval(input)
        except (AttributeError, SyntaxError, NameError, TypeError, ZeroDivisionError, ValueError):
            return False
        return True
    
    # =============================== Accept input data given by the user
    def acceptUserInput(self, default, processType):
        while True: 
            userInput = input()
            self.check_quit(userInput) 
            checkedInput = self.checkUserInput(userInput, processType) 
            if userInput == '':
                if processType in ['fetchColY', 'fetchColZ'] and checkedInput == False:
                    self.printText(self.printFailure, default, processType) # x, y, z data sizes do not match
                else:
                    userInput = default
                    break
            elif checkedInput is True: # DON'T USE 'checkedInput == True' or 'checkedInput', it will mess up the code. Check this out: https://stackoverflow.com/questions/9494404/use-of-true-false-and-none-as-return-values-in-python-functions
                if (processType in ['checkMultiGraph', 'checkMultiXAxis', 'checkThreeDGraph', 'checkThirdAxis']) and (userInput in ['y', 'Y']):
                    userInput = True
                elif (processType in ['checkMultiGraph', 'checkMultiXAxis', 'checkThreeDGraph', 'checkThirdAxis']) and (userInput in ['n', 'N']):
                    userInput = False
                elif processType in ['getFuncXFromUser', 'binResolution', 'checkNumXAxis']:
                    userInput = float(userInput)
                elif processType in ['fetchXAxisColNum', 'numOfPlots']:
                    userInput = int(userInput)
                elif processType in ['fetchColX', 'fetchColY', 'fetchColZ']:
                    if userInput in ['f', 'F', 'q', 'Q']:
                        pass
                    else:
                        userInput = int(userInput)
                elif processType == 'getFuncYFromUser':
                    x = np.array(self.data[self.fetchColX[-1]])
                    userInput = eval(userInput)
                elif processType == 'getFuncZFromUser':
                    x = np.array(self.data[self.fetchColX[-1]])
                    y = np.array(self.data[self.fetchColY[-1]])
                    userInput = eval(userInput)
                break
            else:
                self.printText(self.printFailure, default, processType)
        return userInput
            
    # =============================== Fetch input data from csv 
    def fetchInputData(self):
        with open(self.defaultInputDir + os.sep + self.inputFile, 'r', encoding = self.defaultEncoding) as csvfile:
            plots = csv.reader(csvfile, delimiter = self.delimeter)
            
            # Fetch the self.data from each row
            for row in plots:
                self.data.append(row)
            
            
            self.data = list(map(list, zip(*self.data))) # transpose the self.data: rows -> columns
            
            self.numData = len(self.data)
            
            # Update default label names if labels are given in the input file
            if not (self.data[0][0].isdigit()): # only check one of the first-row entries. If one of them is not a number, then the other first-row entries should be the same
                for i in range(self.numData):
                    self.data[i][0] = self.data[i][0] if self.data[i][0] != '' else 'blank'
                    self.defaultLabels.append(self.data[i][0])
                self.defaultLegendNames = self.defaultLabels
                
                # Delete labels
                for i in range(self.numData):
                    del self.data[i][0]
            
            # convert input self.data to float 
            #print(self.data)
            for i in range(self.numData):
                self.data[i] = [x for x in self.data[i] if len(x.strip()) > 0]
            #print(self.data)
            for i in range(self.numData): # iterate over each column    
               for j in range(len(self.data[i])):
               # try: # Exit the program if conversion to float fails
                    #self.data[i] = list(map(float, self.data[i]))  # convert self.data to float
                    #self.data[i][j] = self.data[i][j] if self.data[i][j] != '' else 0.0 # convert empty cells to float 
                    try:
                        #if self.data[i][j] != '': # dealing with empty cells is problematic. !!! FIND A SOLUTION!!!
                            self.data[i][j] = float(self.data[i][j])
                        #else:
                            #str_list = list(filter(None, str_list))
                            #del self.data[i][j]
                            #continue
                    except ValueError: 
                        print(self.fInputDataNotValid)
                        sys.exit(0)
                    
    # =============================== User Interactions             
    def main(self): 
        # Get input file name from user
        processType = 'fetchInputData'
        self.printText(self.printQuestion, self.defaultInputFile, processType)
        self.inputFile = self.acceptUserInput(self.defaultInputFile, processType)
        if not self.inputFile in ['s', 'S']:
            self.printText(self.printSuccess, self.inputFile, processType)
            # Get self.delimeter type from user
            processType = 'selectDelimeter'
            self.printText(self.printQuestion, self.defaultDelimeter, processType)
            self.delimeter = self.acceptUserInput(self.defaultDelimeter, processType)
            self.printText(self.printSuccess, self.delimeter, processType)
            self.fetchInputData() # Fetch self.data from .csv file
        else:
            self.csvData = False
        # Get self.delimeter type from user
        processType = 'numOfPlots'
        self.printText(self.printQuestion, self.defaultNumOfPlots, processType)
        self.numOfPlots = self.acceptUserInput(self.defaultNumOfPlots, processType)
        self.printText(self.printSuccess, self.numOfPlots, processType)
        
        
        self.initiatePlotter() # Initiate the plotter class
        self.plotPyt.prepPlot(self.numOfPlots) # prepare the plot environment
        
        self.thirdAxis = False
        self.fetchColX = []
        self.fetchColY = []
        self.fetchColZ = []
        self.legendName = []
        for i in range(self.numOfPlots):
            # Select plot type
            processType = 'plotType'
            printVal = [i + 1, self.defaultPlotSelect]
            self.printText(self.printQuestion, printVal, processType)
            self.plotSelect = self.acceptUserInput(self.defaultPlotSelect, processType)
            if not self.plotSelect == self.defaultPlotSelect:
                self.plotSelect = self.plotTypes[int(self.plotSelect) - 1] # - 1 to map user input to correct entry inside self.plotTypes[]. E.g. user input '3' will be mapped to '2' which corresponds to 'line' graph
            self.printText(self.printSuccess, self.plotSelect, processType)
            
            self.threeD = True if self.plotSelect is '3d' else False
            
            while True:
                if self.csvData:
                    # Fetch data of x-axis
                    processType = 'fetchColX'
                    printVal = [self.yDataCounter, self.defaultFetchColX]
                    self.printText(self.printQuestion, printVal, processType)
                    self.fetchColX.append(self.acceptUserInput(self.defaultFetchColX, processType))
                    if not self.fetchColX[-1] in ['f', 'F', 'q', 'Q']:
                        self.printText(self.printSuccess, self.fetchColX, processType)
                        if self.plotSelect in ['cdf', 'histogram']: # do not accept more than 1 x-axis data, no y-axis data needed
                            break
                    if self.fetchColX[-1] in ['f', 'F']:
                        self.fetchColX.pop()
                        self.fetchXFunc = True    
                        self.fetchXFunc2 = True 
                    elif self.fetchColX[-1] in ['q', 'Q']:
                        self.fetchColX.pop()
                        break
                
                    # Fetch data of y-axis
                    if self.fetchXFunc is False:
                        if self.plotSelect != 'box': # no need for y-axis data for bar plot
                            processType = 'fetchColY'
                            self.printText(self.printQuestion, self.defaultFetchColY, processType)
                            self.fetchColY.append(self.acceptUserInput(self.defaultFetchColY, processType))
                            if self.fetchColY[-1] in ['f', 'F']:
                                self.fetchColY.pop()
                                self.fetchYFunc = True
                                self.fetchYFunc2 = True
                            else:
                                self.printText(self.printSuccess, self.fetchColY, processType)
                        
                        if self.plotSelect == '3d':
                            processType = 'fetchColZ'
                            self.printText(self.printQuestion, self.defaultFetchColZ, processType)
                            self.fetchColZ.append(self.acceptUserInput(self.defaultFetchColZ, processType))
                            if self.fetchColZ[-1] in ['f', 'F']:
                                self.fetchColZ.pop()
                                self.fetchZFunc = True
                                self.fetchZFunc2 = True
                            else:
                                self.printText(self.printSuccess, self.fetchColZ, processType)
                                
                if not self.csvData or self.fetchXFunc or self.fetchYFunc or self.fetchZFunc: # generate data from function
                    if not processType in ['fetchColY', 'fetchColZ']:
                        processType = 'getFuncXFromUser'
                        if self.yDataCounter >= 1 and not self.csvData: 
                            print("Please type [qQ] if you don't want to plot more data in this graph or type any other key to continue")
                            userInput = input()
                            if userInput in ['q', 'Q']:
                                break
                        printVal = [self.yDataCounter, self.minX, self.maxX, self.resX]
                        self.printText(self.printQuestion, printVal, processType)
                        print("Min. x: ")
                        self.minX = self.acceptUserInput(self.defaultMinX, processType)
                        if self.minX in ['q', 'Q']:
                            break
                        print("Max. x: ")
                        self.maxX = self.acceptUserInput(self.defaultMaxX, processType)
                        print("Res. x: ")
                        self.resX = self.acceptUserInput(self.defaultResX, processType)
                        self.x = np.arange(self.minX, self.maxX, self.resX)
                        self.printText(self.printSuccess, self.x, processType)
                        self.data.append(self.x)
                        self.fetchColX.append(len(self.data) - 1) # record at which index you saved the x data in self.data matrix
                        if self.plotSelect in ['cdf', 'histogram']: # do not accept more than 1 x-axis data, no y-axis data needed
                            break
                            
                        if self.fetchColX[-1] in ['q', 'Q']:
                            self.fetchColX.pop()
                            if (self.plotSelect is '3d' and self.yDataCounter < 2):
                                print(f"{Fore.RED}You need to enter at least 2 data sets in order to plot 3D plot")
                            else:
                                break
                                
                    
                    self.fetchYFunc = True
                    self.fetchYFunc2 = True
                    if self.plotSelect != 'box' and processType != 'fetchColZ': # no need for y-axis data for bar plot
                        processType = 'getFuncYFromUser'
                        printVal = 'x**2'
                        self.printText(self.printQuestion, printVal, processType)
                        print("y(x): ")
                        self.y = self.acceptUserInput(self.defaultY, processType)
                        self.printText(self.printSuccess, self.y, processType)
                        self.data.append(self.y)
                        self.fetchColY.append(len(self.data) - 1) # record at which index you saved the x data in self.data matrix
                    
                    self.fetchZFunc = True
                    self.fetchZFunc2 = True
                    if self.plotSelect == '3d':
                        processType = 'getFuncZFromUser'
                        printVal = 'x**2 + y**2'
                        self.printText(self.printQuestion, printVal, processType)
                        print("z(x, y): ")
                        self.z = self.acceptUserInput(self.defaultZ, processType)
                        self.printText(self.printSuccess, self.z, processType)
                        self.data.append(self.z)
                        self.fetchColZ.append(len(self.data) - 1) # record at which index you saved the x data in self.data matrix

                self.yDataCounter += 1
                
                # Fetch legend name
                processType = 'getLegendNames'
                if self.plotSelect == 'box':
                    if not self.csvData or self.fetchXFunc:
                        printVal = [i, self.defaultXLabel, 'xtick']
                        self.printText(self.printQuestion, printVal, processType) # send i instead of legend name to be able to print dataset # in printText()
                        self.legendName.append(self.acceptUserInput(self.defaultXLabel, processType))
                    else:
                        printVal = [i, self.defaultLabels[self.fetchColX[-1]], 'xtick']
                        self.printText(self.printQuestion, printVal, processType) # send i instead of legend name to be able to print dataset # in printText()
                        self.legendName.append(self.acceptUserInput(self.defaultLabels[self.fetchColX[-1]], processType))
                    self.printText(self.printSuccess, self.legendName, processType)
                elif self.plotSelect == '3d': 
                    if not self.csvData or self.fetchZFunc:
                        printVal = [i, self.defaultZLabel, 'legend']
                        self.printText(self.printQuestion, printVal, processType) # send i instead of legend name to be able to print dataset # in printText()
                        self.legendName.append(self.acceptUserInput(self.defaultZLabel, processType))
                    else:
                        printVal = [i, self.defaultLabels[self.fetchColZ[-1]], 'legend']
                        self.printText(self.printQuestion, printVal, processType) # send i instead of legend name to be able to print dataset # in printText()
                        self.legendName.append(self.acceptUserInput(self.defaultLabels[self.fetchColZ[-1]], processType))
                    self.printText(self.printSuccess, self.legendName, processType)
                else:
                    if not self.csvData or self.fetchYFunc:
                        printVal = [i, self.defaultYLabel, 'legend']
                        self.printText(self.printQuestion, printVal, processType) # send i instead of legend name to be able to print dataset # in printText()
                        self.legendName.append(self.acceptUserInput(self.defaultYLabel, processType))
                    else:
                        printVal = [i, self.defaultLabels[self.fetchColY[-1]], 'legend']
                        self.printText(self.printQuestion, printVal, processType) # send i instead of legend name to be able to print dataset # in printText()
                        self.legendName.append(self.acceptUserInput(self.defaultLabels[self.fetchColY[-1]], processType))
                    self.printText(self.printSuccess, self.legendName, processType)
                self.fetchXFunc = False
                self.fetchYFunc = False
                self.fetchZFunc = False
            
            # Check 3rd axis
            if self.plotSelect in ['line', 'scatter'] and self.yDataCounter == 2:
                processType = 'checkThirdAxis'
                self.printText(self.printQuestion, self.defaultThirdAxis, processType)
                self.thirdAxis = self.acceptUserInput(self.defaultThirdAxis, processType)
                self.printText(self.printSuccess, self.thirdAxis, processType)
                
            # Fetch x-label
            processType = 'getLabelX'
            if self.plotSelect == 'box':
                self.printText(self.printQuestion, self.defaultXLabel, processType) # send i instead of legend name to be able to print dataset # in printText()
                self.xLabel = (self.acceptUserInput(self.defaultXLabel, processType))
            else:
                if not self.csvData or self.fetchXFunc2:
                    self.printText(self.printQuestion, self.defaultXLabel, processType) # send i instead of legend name to be able to print dataset # in printText()
                    self.xLabel = (self.acceptUserInput(self.defaultXLabel, processType))
                else:
                    self.printText(self.printQuestion, self.defaultLabels[self.fetchColX[-1]], processType) 
                    self.xLabel = self.acceptUserInput(self.defaultLabels[self.fetchColX[-1]], processType)
                self.printText(self.printSuccess, self.xLabel, processType)
            
            if (self.plotSelect == 'histogram'):
                processType = 'binResolution'
                self.printText(self.printQuestion, self.defaultBinRes, processType)
                self.binRes = self.acceptUserInput(self.defaultBinRes, processType)
                self.printText(self.printSuccess, self.binRes, processType)
                    
            if self.plotSelect == 'cdf':
                self.yLabel = self.cdfDefaultLabel
            elif self.plotSelect == 'histogram':
                self.yLabel = self.histDefaultLabel
            elif self.plotSelect == 'box':
                processType = 'getLabelY'
                if not self.csvData or self.fetchYFunc2:
                    self.printText(self.printQuestion, self.defaultXLabel, processType) # send i instead of legend name to be able to print dataset # in printText()
                    self.yLabel = (self.acceptUserInput(self.defaultXLabel, processType)) # fetch x label to the y-axis
                else:
                    self.printText(self.printQuestion, self.defaultLabels[self.fetchColX[-1]], processType) 
                    self.yLabel = self.acceptUserInput(self.defaultLabels[self.fetchColX[-1]], processType)
                self.printText(self.printSuccess, self.yLabel, processType)
            
            if not self.plotSelect in ['cdf', 'histogram', 'box']:
                # Fetch y-label
                processType = 'getLabelY'
                if not self.csvData or self.fetchYFunc2:
                    self.printText(self.printQuestion, self.defaultYLabel, processType) # send i instead of legend name to be able to print dataset # in printText()
                    self.yLabel = (self.acceptUserInput(self.defaultYLabel, processType))
                else:
                    self.printText(self.printQuestion, self.defaultLabels[self.fetchColY[-1]], processType) 
                    self.yLabel = self.acceptUserInput(self.defaultLabels[self.fetchColY[-1]], processType)
                self.printText(self.printSuccess, self.yLabel, processType)
                
                
                if self.plotSelect == '3d':
                    # set z-axis label
                    processType = 'getLabelZ'
                    if not self.csvData or self.fetchZFunc2:
                        self.printText(self.printQuestion, self.defaultZLabel, processType) # send i instead of legend name to be able to print dataset # in printText()
                        self.zLabel = (self.acceptUserInput(self.defaultZLabel, processType))
                    else:
                        self.printText(self.printQuestion, self.defaultLabels[self.fetchColZ[-1]], processType) 
                        self.zLabel = self.acceptUserInput(self.defaultLabels[self.fetchColZ[-1]], processType)
                    self.printText(self.printSuccess, self.zLabel, processType)
                    
                self.fetchXFunc2 = False
                self.fetchYFunc2 = False
                self.fetchZFunc2 = False
            
            if self.numOfPlots > 1: 
                    # Fetch title name from user
                    processType = 'getTitleName'
                    mainTitle = False
                    printVar = [mainTitle, self.defaultTitle]
                    self.printText(self.printQuestion, printVar, processType) 
                    self.title = self.acceptUserInput(self.defaultTitle, processType)
                    self.printText(self.printSuccess, self.title, processType)
            #self.printText(self.printQuestion, i, processType) # send i instead of legend name to be able to print dataset # in printText()
            #self.legendName.append(self.acceptUserInput(self.defaultLegendNames[i], processType))
            #self.printText(self.printSuccess, self.legendName, processType)
                    
            #self.printText(self.printSuccess, self.fetchColY, processType)
            plotCounter = i
            self.plotPyt.mainPlotter(plotCounter, self.numOfPlots, self.plotSelect, self.yDataCounter, self.fetchColX, self.fetchColY, self.fetchColZ, self.legendName, self.binRes, self.thirdAxis, self.data) # TODO: Why do I send self.numOfPlots???
            self.plotPyt.plotLabeling(self.xLabel, self.yLabel, self.zLabel, self.thirdAxis, self.threeD, self.title, self.numOfPlots)
            self.yDataCounter = 0
            self.fetchColX = []
            self.fetchColY = []
            self.fetchColZ = []
            self.legendName = []
            self.threeD = False
            #self.xLabel = ''
            #self.yLabel = ''
            #self.zLabel = ''
            #self.title = ''
            
            
            
            #functionCallName = 'plotPyt.'+ self.plotSelect + 'Plot(', self.plotSelect, ')')
            #exec(functionCallName.translate(str.maketrans({"'":None}))) # execute the expression    
            
        # Fetch title name from user
        processType = 'getTitleName'
        mainTitle = True
        printVar = [mainTitle, self.defaultTitle]
        self.printText(self.printQuestion, printVar, processType) 
        self.title = self.acceptUserInput(self.defaultTitle, processType)
        self.printText(self.printSuccess, self.title, processType)
        
        self.plotPyt.showPlot(self.title, self.numOfPlots)
            
            
    # =============================== Fetch bin resolution
        '''
        if (self.plotSelect == 'histogram'):
            for i in range(1, self.numData):
                processType = 'binResolution'
                self.printText(self.printQuestion, i - 1, processType)
                self.binRes.append(self.acceptUserInput(self.defaultBinRes, processType))
                self.printText(self.printSuccess, self.binRes, processType)
            
    # =============================== Multiple Plotting
        if (self.numData > 2):
            processType = 'checkMultiGraph'
            self.printText(self.printQuestion, self.defaultMultiGraph, processType)
            self.multiGraph = self.acceptUserInput(self.defaultMultiGraph, processType)
            self.printText(self.printSuccess, self.multiGraph, processType)
    
    # =============================== 3D Plotting
        # Enable 3D plotting
        if (self.plotSelect == 'line' or self.plotSelect == 'scatter') and (self.numData >= 3 and self.multiGraph == False):
            processType = 'checkThreeDGraph'
            self.printText(self.printQuestion, self.defaultThreeD, processType)
            self.threeD = self.acceptUserInput(self.defaultThreeD, processType)
            self.printText(self.printSuccess, self.threeD, processType)
    
    # =============================== 2D with 3rd-axis Plotting 
        # Enable 3rd axis for line plot
        if (self.plotSelect == 'line' or self.plotSelect == 'scatter') and (self.numData == 3 and self.multiGraph == False and self.threeD == False): 
            processType = 'checkThirdAxis'
            self.printText(self.printQuestion, self.defaultThirdAxis, processType)
            self.thirdAxis = self.acceptUserInput(self.defaultThirdAxis, processType)
            self.printText(self.printSuccess, self.thirdAxis, processType)
    
    # =============================== Check for Multi X-Axes
        if self.multiGraph and (self.plotSelect is not 'cdf' or self.plotSelect is not 'histogram'):
            processType = 'checkMultiXAxis'
            self.printText(self.printQuestion, self.defaultThirdAxis, processType)
            self.multiXAxis = self.acceptUserInput(self.defaultMultiXAxis, processType)
            self.printText(self.printSuccess, self.multiXAxis, processType)
            
    # =============================== Check Number of Different X-Axes
        if self.multiXAxis and (self.plotSelect is not 'cdf' or self.plotSelect is not 'histogram'):
            self.maxNumXAxis = math.floor(self.numData / 2)
            printVal = [self.defaultNumXAxis, self.maxNumXAxis]
            processType = 'checkNumXAxis'
            self.printText(self.printQuestion, printVal, processType)
            self.numXAxis = self.acceptUserInput(self.defaultNumXAxis, processType)
            self.printText(self.printSuccess, self.numXAxis, processType)
        numYData = self.numData - self.numXAxis
    # =============================== Fetch X-Axis Column Numbers from User
        if self.multiXAxis and (self.plotSelect is not 'cdf' or self.plotSelect is not 'histogram'):        
            processType = 'fetchXAxisColNum'
            for i in range(0, int(numYData)):
                self.printText(self.printQuestion, i, processType) # send i instead of legend name to be able to print dataset # in printText()
                self.xAxesColNums.append(self.acceptUserInput(0, processType))
            self.printText(self.printSuccess, self.xAxesColNums, processType)
        
    # =============================== Get Legend Names
        # Get legend name(s) from user
        if not self.threeD: # obtain legend omitting 1st self.dataset
            for i in range(0, int(numYData)):
                processType = 'getLegendNames'
                self.printText(self.printQuestion, i, processType) # send i instead of legend name to be able to print dataset # in printText()
                self.legendName.append(self.acceptUserInput(self.defaultLegendNames[i], processType))
            self.printText(self.printSuccess, self.legendName, processType)
        else: # obtain legend name omitting 1st and 2nd self.dataset
            for i in range(2, self.numData):
                processType = 'getLegendNames'
                self.printText(self.printQuestion, i - 2, processType) # send i instead of legend name to be able to print dataset # in printText()
                self.legendName.append(self.acceptUserInput(self.defaultLegendNames[i - 2], processType))
            self.printText(self.printSuccess, self.legendName, processType)
    
    # =============================== Get X-axis Label
        processType = 'getLabelX'
        self.printText(self.printQuestion, self.defaultXLabel, processType) 
        self.xLabel = self.acceptUserInput(self.defaultXLabel, processType)
        self.printText(self.printSuccess, self.xLabel, processType)
        
    # =============================== Get Y-axis Label
        if self.multiGraph:
            # set y-axes labels
            for i in range(0, int(numYData)):
                processType = 'getLabelY'
                self.printText(self.printQuestion, i, processType) # send i instead of legend name to be able to print dataset # in printText()
                self.yLabel.append(self.acceptUserInput(self.defaultYLabel[i], processType))
            self.printText(self.printSuccess, self.yLabel, processType)
        elif self.threeD: 
            # set y-axis label
            processType = processType
            self.printText(self.printQuestion, 0, processType) 
            self.yLabel.append(self.acceptUserInput(self.defaultYLabel[0], processType))
            self.printText(self.printSuccess, 0, processType)
            
            # set z-axis label
            processType = 'getLabelY'
            self.printText(self.printQuestion, 1, processType) 
            self.zLabel = self.acceptUserInput(self.defaultYLabel[1], processType)
            self.printText(self.printSuccess, 1, processType)
        elif self.thirdAxis:
            # set 1st y-axis label
            processType = 'getLabelY'
            self.printText(self.printQuestion, 0, processType) 
            self.yLabel.append(self.acceptUserInput(self.defaultYLabel[0], processType))
            self.printText(self.printSuccess, 0, processType)
            
            # set 2nd y-axis label
            self.printText(self.printQuestion, 1, processType) 
            self.yLabel.append(self.acceptUserInput(self.defaultYLabel[1], processType))
            self.printText(self.printSuccess, 1, processType)
        else: # 2D regular plot 
            processType = 'getLabelY'
            self.printText(self.printQuestion, 0, processType) 
            self.yLabel.append(self.acceptUserInput(self.defaultYLabel[0], processType))
            self.printText(self.printSuccess, self.yLabel, processType)
        
    # =============================== Get Title Name
        # Get title name from user
        processType = 'getTitleName'
        self.printText(self.printQuestion, self.defaultTitle, processType) 
        self.title = self.acceptUserInput(self.defaultTitle, processType)
        self.printText(self.printSuccess, self.title, processType)
        '''
    # =============================== Initiate and Run the PlotPython Class
    def initiatePlotter(self):
        self.plotPyt = plotPython(self.numData, self.thirdAxis, self.threeD, self.multiGraph, self.legendName, self.xLabel, self.yLabel, self.zLabel, self.title, self.data, self.binRes, self.xAxesColNums)
        # Execute the corresponding plotting function
        #functionCallName = 'task2.'+ self.plotSelect + 'Plot()'
        #exec(functionCallName.translate(str.maketrans({"'":None}))) # execute the expression

# #################################### MAIN
task = userInteractions()
task.main() # Fetch self.data-related info from user
task.initiatePlotter()  