#!/usr/bin/env python3

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import math
import os
import sys
from colorama import Fore, init # colored output on the terminal
from datetime import datetime
import tkinter
import config_main as config
import config_optional
init(autoreset = True) # turn off colors after each print()

###################### PLOTTER
class plotPython:
    # =============================== Initializer / Instance attributes
    def __init__(self):
        self.colors = ['steelblue', 'sandybrown', 'mediumseagreen', 'indianred', 'dimgrey', 'orchid', 'goldenrod', 'darkcyan', 'mediumslateblue', 'darkkhaki'] # Taken from https://matplotlib.org/3.1.0/gallery/color/named_colors.html
        self.lineTypes = ['-', '--', '-.', '.']
        self.plotFuncName = ''
        self.figRowCnt = 0
        self.figColCnt = 0
        self.numOfRow = 0
        self.plotCounter = 0
        self.guest = []
        self.linesSum = None
        self.labelsSum = None
        self.snsJntPlot = None
        self.date = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.fTxtNoXServer = f"""
{Fore.RED}Your X-server is not running, cannot plot the graph.
Please turn on your X-server first and then hit [enter]"""
        
    # =============================== Prepare the plot
    def prepPlot(self, numOfPlots): 
        exitLoop = False
        plt.rcParams.update(config_optional.parameters) # update matplotlib parameters
        
        while True:
            try:   
                self.numOfRow = config.plotsPerRow if numOfPlots > 1 else 1
                self.fig, self.host = plt.subplots(math.ceil(numOfPlots / self.numOfRow), self.numOfRow, sharex = config.shareX, sharey = config.shareY, figsize = (config.figDimX, config.figDimY), squeeze = False)
                if numOfPlots != 1 and numOfPlots % self.numOfRow != 0: # turn off the axes of last unused plot, because there is leftover plot in when total plots are odd
                    for i in range(numOfPlots % self.numOfRow, self.numOfRow):
                        self.host[int(numOfPlots / self.numOfRow), i].axis('off')
                exitLoop = True
            except tkinter._tkinter.TclError: # fail if X-server not running
                print(self.fTxtNoXServer)
                userInput = input()
                if userInput in ['exit', 'EXIT', 'quit', 'QUIT']: # exit options
                    sys.exit(0)
                exitLoop = False
            if exitLoop: 
                break
       
    # =============================== Reset the plot
    def resetPlot(self):
        self.numOfRow = 0
        self.figRowCnt = 0
        self.figColCnt = 0
        self.fig.clf()
        plt.close()

    # =============================== Color the axes
    def axisColoring(self, numData):
        # color the axes of the plot. For now, it is implemented only for 3-axis 2D graphs. TO BE EXTENDED!
        axisOffset = 1
        self.host[self.figColCnt, self.figRowCnt].spines['left'].set_color(self.colors[config.lineColors[0]])
        self.host[self.figColCnt, self.figRowCnt].tick_params(axis = 'y', colors = self.colors[config.lineColors[0]])
        self.host[self.figColCnt, self.figRowCnt].yaxis.label.set_color(self.colors[config.lineColors[0]])
        for i in range(numData - 1):
            self.guest[i].spines['right'].set_color(self.colors[config.lineColors[i + 1]])
            self.guest[i].spines['right'].set_position(("axes", axisOffset))
            self.guest[i].tick_params(axis='y', colors = self.colors[config.lineColors[i + 1]])
            self.guest[i].yaxis.label.set_color(self.colors[config.lineColors[i + 1]])
            axisOffset += config.axisOffset
    
    # =============================== Label the plot
    def plotConfigs(self, xLabel, yLabel, zLabel, threeD, title, numOfPlots, plotCounter, plotType, numData):
        self.fig.savefig('%s' %config.logDir + os.sep + '%s.%s' %(self.date, config.figFormat), format = config.figFormat)
        self.host[self.figColCnt, self.figRowCnt].set_xlabel(xLabel)
        self.host[self.figColCnt, self.figRowCnt].set_ylabel(yLabel[0])
        if config.multipleAxis:
            for i in range(numData - 1):
                self.guest[i].set_ylabel(yLabel[i + 1])
        if threeD: 
            self.host[self.figColCnt, self.figRowCnt].set_zlabel(zLabel)
        if numOfPlots > 1:
            self.host[self.figColCnt, self.figRowCnt].title.set_text(title)
        if not plotType in {'box', 'histogram'} and not config.multipleAxis: # box and hist plots do not have legend
            self.host[self.figColCnt, self.figRowCnt].legend()
        
        if plotType in {'seaborn regression'}:
            self.snsJntPlot.ax_joint.set_xlabel(xLabel)
            self.snsJntPlot.ax_joint.set_ylabel(yLabel[0])
            self.snsJntPlot.ax_joint.tick_params(axis = 'x')
            self.snsJntPlot.ax_joint.tick_params(axis = 'y')
            plt.suptitle(title)
            plt.subplots_adjust(top = 0.9, bottom = 0.2)
            
        # logic to place subplots in the right location
        if (plotCounter + 1) % self.numOfRow == 0:
            self.figColCnt += 1
            self.figRowCnt -= (self.numOfRow - 1)
        else:
            self.figRowCnt += 1
            
    # =============================== Show the plot
    def showPlot(self, title, numOfPlots):
        self.fig.suptitle(title) # Main title
        self.fig.savefig('%s' %config.logDir + os.sep + '%s.%s' %(self.date, config.figFormat), bbox_inches = 'tight', format = config.figFormat) # save fig to logs dir
        self.fig.tight_layout() # to adjust spacing between graphs and labels
        plt.show()
     
    
    # =============================== Plotter function
    def mainPlotter(self, plotCounter, numOfPlots, plotSelect, plotPlotSelect, numData, colNumX, colNumY, colNumZ, colNumE, legendName, binRes, data):
        # Main if clause for plots
        if plotSelect == 'bar':
            for i in range(numData):
                self.host[self.figColCnt, self.figRowCnt].bar(data[colNumX[i]], data[colNumY[i]], color = self.colors[config.lineColors[i % len(config.lineColors)]], label = legendName[i], kwargs = {'alpha': 0.5}) 
        elif plotSelect == 'box':
            boxData = []
            for i in range(numData):
                boxData.append(data[colNumX[i]])
            self.host[self.figColCnt, self.figRowCnt].boxplot(boxData, positions = np.array(range(len(boxData))) + 1, patch_artist = True, boxprops = dict(facecolor = self.colors[config.lineColors[0]], 
            color = self.colors[config.lineColors[1]]), capprops = dict(color = self.colors[config.lineColors[2]]), whiskerprops = dict(color = self.colors[config.lineColors[3]]), 
            flierprops = dict(color = self.colors[config.lineColors[4]], markeredgecolor = self.colors[config.lineColors[5]]), medianprops = dict(color = self.colors[config.lineColors[6]]))
            self.host[self.figColCnt, self.figRowCnt].set_xticklabels(legendName)
        elif plotSelect == 'cdf':
            for i in range(numData):
                bin_edges_list = [] 
                cdfData = []
                data_size = len(data[colNumX[i]]) # taken from: https://stackoverflow.com/questions/24575869/read-file-and-plot-cdf-in-python
                data_set = sorted(set(data[colNumX[i]]))
                bins = np.append(data_set, data_set[-1] + 1)
                counts, bin_edges = np.histogram(data[colNumX[i]], bins = bins, density = False) # Use histogram function to bin data
                counts = counts.astype(float) / data_size
                cdfData = np.cumsum(counts)
                self.host[self.figColCnt, self.figRowCnt].plot(bin_edges[0:-1], cdfData, self.colors[config.lineColors[i]], label = legendName[i], linewidth = config.lineWidth[i], alpha = config.alpha) 
                #self.host[self.figColCnt, self.figRowCnt].set_xscale('log')
        elif plotSelect == 'histogram':
            self.bins = np.arange(min(data[colNumX[0]]) - binRes, max(data[colNumX[0]]) + binRes * 2, binRes)
            self.host[self.figColCnt, self.figRowCnt].hist(data[colNumX[0]], bins = self.bins, color = self.colors[config.lineColors[0]], align = 'left', alpha = config.alpha)  
            plt.xticks(self.bins[:-1])
        elif plotSelect in ['line/scatter/line+scatter']:
            if config.multipleAxis: # multiple-axis enabled
                p, p2, linesSum, labelsSum  = [], [], [], []
                p.append(0) #initialize array entry
                if plotPlotSelect[0] == 1: # line plot
                    p[0], = self.host[self.figColCnt, self.figRowCnt].plot(data[colNumX[0]], data[colNumY[0]], self.colors[config.lineColors[0]], label = legendName[0], linewidth = config.lineWidth[0], alpha = config.alpha)  
                elif plotPlotSelect[0] == 2: # scatter plot
                    p[0] = self.host[self.figColCnt, self.figRowCnt].scatter(data[colNumX[0]], data[colNumY[0]], c = self.colors[config.lineColors[0]], label = legendName[0], alpha = config.alpha)  
                elif plotPlotSelect[0] == 3: # line+scatter plot
                    p2.append(0) #initialize array entry
                    p[0], p2[-1], = self.host[self.figColCnt, self.figRowCnt].plot(data[colNumX[0]], data[colNumY[0]], '-x', self.colors[config.lineColors[0]], label = legendName[0], linewidth = config.lineWidth[0], alpha = config.alpha)    
                elif plotPlotSelect[0] == 4: # line plot w/ errorbar
                    p[0], = self.host[self.figColCnt, self.figRowCnt].errorbar(data[colNumX[0]], data[colNumY[0]], yerr = data[colNumE[0]], fmt = config.lineErrPlot_lineStyle, c = self.colors[config.lineColors[1]], label = legendName[0], kwargs = {'alpha': 0.5})
                elif plotPlotSelect[0] == 5: # scatter plot w/ errorbar
                    p[0], = self.host[self.figColCnt, self.figRowCnt].errorbar(data[colNumX[0]], data[colNumY[0]], yerr = data[colNumE[0]], fmt = config.scatterErrPlot_lineStyle, c = self.colors[config.lineColors[1]], label = legendName[0], kwargs = {'alpha': 0.5})
                else: # line+scatter plot w/ errorbar
                    p[0], p2[-1], = self.host[self.figColCnt, self.figRowCnt].errorbar(data[colNumX[0]], data[colNumY[0]], yerr = data[colNumE[0]], fmt = config.lineScatErrPlot_lineStyle, c = self.colors[config.lineColors[1]], label = legendName[0], kwargs = {'alpha': 0.5})
                lines, labels = self.host[self.figColCnt, self.figRowCnt].get_legend_handles_labels()
                linesSum += lines
                labelsSum += labels
                for i in range(1, numData):
                    p.append(0) #initialize array entry
                    self.guest.append(0) #initialize array entry
                    j = i - 1
                    if i != numData:
                        self.guest[j] = self.host[self.figColCnt, self.figRowCnt].twinx() # setup 2nd axis based on the first graph
                    if plotPlotSelect[0] == 1: # line plot
                        p[i], = self.guest[j].plot(data[colNumX[i]], data[colNumY[i]], self.colors[config.lineColors[i]], label = legendName[i], linewidth = config.lineWidth[i], alpha = config.alpha)  
                    elif plotPlotSelect[0] == 2: # scatter plot
                        p[i] = self.guest[j].scatter(data[colNumX[i]], data[colNumY[i]], c = self.colors[config.lineColors[i]], label = legendName[i], alpha = config.alpha)  
                    elif plotPlotSelect[0] == 3: # line+scatter plot
                        p2.append(0) #initialize array entry
                        p[i], p2[-1], = self.guest[j].plot(data[colNumX[i]], data[colNumY[i]], '-x', self.colors[config.lineColors[i]], label = legendName[i], linewidth = config.lineWidth[i], alpha = config.alpha)    
                    elif plotPlotSelect[0] == 4: # line plot w/ errorbar
                        p[i], = self.guest[j].errorbar(data[colNumX[i]], data[colNumY[i]], yerr = data[colNumE[i]], fmt = config.lineErrPlot_lineStyle, c = self.colors[config.lineColors[i]], label = legendName[i], kwargs = {'alpha': 0.5})
                    elif plotPlotSelect[0] == 5: # scatter plot w/ errorbar
                        p[i], = self.guest[j].errorbar(data[colNumX[i]], data[colNumY[i]], yerr = data[colNumE[i]], fmt = config.scatterErrPlot_lineStyle, c = self.colors[config.lineColors[i]], label = legendName[i], kwargs = {'alpha': 0.5})
                    else: # line+scatter plot w/ errorbar
                        p2.append(0) #initialize array entry
                        p[i], p2[-1], = self.guest[j].errorbar(data[colNumX[i]], data[colNumY[i]], yerr = data[colNumE[i]], fmt = config.lineScatErrPlot_lineStyle, c = self.colors[config.lineColors[i]], label = legendName[i], kwargs = {'alpha': 0.5})
                    self.guest[j].set_ylim(min(data[colNumY[i]]) - config.yLimThreshold, max(data[colNumY[i]]) + config.yLimThreshold)
                    self.guest[j].grid(False)
                    lines2, labels2 = self.guest[j].get_legend_handles_labels()
                    linesSum += lines2
                    labelsSum += labels2
                #self.host[self.figColCnt, self.figRowCnt].legend(lines, [l.get_label() for l in lines], loc = 'best')
                self.guest[j].legend(linesSum, labelsSum)
                self.axisColoring(numData)
            else:
                for i in range(numData):
                    if plotPlotSelect[i] == 1: # line plot
                        self.host[self.figColCnt, self.figRowCnt].plot(data[colNumX[i]], data[colNumY[i]], self.colors[config.lineColors[i % len(config.lineColors)]], label = legendName[i], linewidth = config.lineWidth[i], alpha = config.alpha)
                    elif plotPlotSelect[i] == 2: # scatter plot
                        self.host[self.figColCnt, self.figRowCnt].scatter(data[colNumX[i]], data[colNumY[i]], c = self.colors[config.lineColors[i % len(config.lineColors)]], label = legendName[i], alpha = config.alpha)
                    elif plotPlotSelect[i] == 3: # line+scatter plot
                        self.host[self.figColCnt, self.figRowCnt].plot(data[colNumX[i]], data[colNumY[i]], config.scatterErrPlot_lineStyle, self.colors[config.lineColors[i % len(config.lineColors)]], label = legendName[i], linewidth = config.lineWidth[i], alpha = config.alpha)
                    elif plotPlotSelect[i] == 4: # line plot w/ errorbar
                        self.host[self.figColCnt, self.figRowCnt].errorbar(data[colNumX[i]], data[colNumY[i]], yerr = data[colNumE[i]], fmt = config.lineErrPlot_lineStyle, c = self.colors[config.lineColors[i % len(config.lineColors)]] , label = legendName[i], kwargs = {'alpha': 0.5})
                    elif plotPlotSelect[i] == 5: # scatter plot w/ errorbar
                        self.host[self.figColCnt, self.figRowCnt].errorbar(data[colNumX[i]], data[colNumY[i]], yerr = data[colNumE[i]], fmt='o', c = self.colors[config.lineColors[i % len(config.lineColors)]], label = legendName[i], kwargs = {'alpha': 0.5})
                    else: # line+scatter plot w/ errorbar
                        self.host[self.figColCnt, self.figRowCnt].errorbar(data[colNumX[i]], data[colNumY[i]], yerr = data[colNumE[i]], fmt='-o', c = self.colors[config.lineColors[i % len(config.lineColors)]], label = legendName[i], kwargs = {'alpha': 0.5})
        elif plotSelect == '3d':
            self.host[self.figColCnt, self.figRowCnt].axis('off')
            numOfRow = 2 if numOfPlots > 1 else 1
            self.host[self.figColCnt, self.figRowCnt] = self.fig.add_subplot(math.ceil(numOfPlots / numOfRow), numOfRow, plotCounter + 1, projection = '3d')
            for i in range(numData):
                self.host[self.figColCnt, self.figRowCnt].plot(data[colNumX[i]], data[colNumY[i]], data[colNumZ[i]], self.colors[config.lineColors[i % len(config.lineColors)]], label = legendName[i], linewidth = config.lineWidth[i], alpha = config.alpha)
            self.host[self.figColCnt, self.figRowCnt].azim = config.threeD_azimDegree
            self.host[self.figColCnt, self.figRowCnt].elev = config.threeD_elevDegree
            # padding and scaling options for z-axis
            self.host[self.figColCnt, self.figRowCnt].axes.zaxis.labelpad = config.zAxis_labelPad
            self.host[self.figColCnt, self.figRowCnt].set_zscale(config.scaleZ)
        elif plotSelect == 'seaborn line':
            if config.multipleAxis: # multiple-axis enabled
                linesSum, labelsSum  = [], []
                sns.lineplot(x = data[colNumX[0]], y = data[colNumY[0]], color = self.colors[config.lineColors[0]], label = legendName[0], ax = self.host[self.figColCnt, self.figRowCnt], linewidth = config.lineWidth[0], alpha = 0.5) 
                lines, labels = self.host[self.figColCnt, self.figRowCnt].get_legend_handles_labels()
                linesSum += lines
                labelsSum += labels
                self.host[self.figColCnt, self.figRowCnt].legend_.remove()
                for i in range(1, numData):
                    self.guest.append(0) #initialize array entry
                    j = i - 1
                    if i != numData:
                        self.guest[j] = self.host[self.figColCnt, self.figRowCnt].twinx() # setup 2nd axis based on the first graph
                    sns.lineplot(x = data[colNumX[i]], y = data[colNumY[i]], color = self.colors[config.lineColors[i % len(config.lineColors)]], label = legendName[i], ax = self.guest[j], linewidth = config.lineWidth[i], alpha = 0.5) 
                    self.guest[j].set_ylim(min(data[colNumY[i]]) - config.yLimThreshold, max(data[colNumY[i]]) + config.yLimThreshold)
                    lines2, labels2 = self.guest[j].get_legend_handles_labels()
                    linesSum += lines2
                    labelsSum += labels2
                    self.guest[j].grid(False)
                    self.guest[j].legend_.remove()
                self.guest[j].legend(linesSum, labelsSum)
                self.axisColoring(numData)
            else:
                for i in range(numData):
                    sns.lineplot(x = data[colNumX[i]], y = data[colNumY[i]], color = self.colors[config.lineColors[i % len(config.lineColors)]], label = legendName[i], ax = self.host[self.figColCnt, self.figRowCnt], linewidth = config.lineWidth[i], alpha = 0.5)
        elif plotSelect == 'seaborn regression':
            for i in range(numData):
                self.snsJntPlot = sns.jointplot(x = data[colNumX[i]], y = data[colNumY[i]], kind = config.regressionPlotKind, color = self.colors[config.lineColors[i % len(config.lineColors)]], label = legendName[i])    
        
        self.plotCounter += 1
     