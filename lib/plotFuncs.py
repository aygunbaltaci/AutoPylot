#!/usr/bin/env python3

import os
import sys
import math
from colorama import Fore, init 
from datetime import datetime
import tkinter
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import seaborn as sns
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
        self.oneColSpecPlt = False
        self.guest = []
        self.hostLines, self.hostLabels, self.guestLines, self.guestLabels, self.linesSum, self.labelsSum  = [], [], [], [], [], []
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
                if (config.plotsPerRow == 1 and numOfPlots > 1) and config.oneColSpecPlt:
                    self.numOfRow = 2
                    self.oneColSpecPlt = True
                else:
                    self.oneColSpecPlt = False

                if not self.oneColSpecPlt:
                    self.fig, self.host = plt.subplots(math.ceil(numOfPlots / self.numOfRow), self.numOfRow, sharex = config.shareX, sharey = config.shareY, figsize = (config.figDimX, config.figDimY), squeeze = False)
                    if numOfPlots != 1 and numOfPlots % self.numOfRow != 0: # turn off the axes of last unused plot, because there is leftover plot in when total plots are odd
                        for i in range(numOfPlots % self.numOfRow, self.numOfRow):
                            self.host[int(numOfPlots / self.numOfRow), i].axis('off')
                else:
                    self.fig, self.host = plt.subplots(numOfPlots, self.numOfRow, sharex = config.shareX, sharey = config.shareY, figsize = (config.figDimX, config.figDimY), squeeze = False)
                    for i in range(numOfPlots):
                        self.host[i, 1].remove()

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
        #self.host[self.figColCnt, self.figRowCnt].clf() # use this instead of self.fig.clf() if you find a way to do undo over multi-plots.
        plt.close()

    # =============================== Color the axes for multi-y axes (seaborn) line plots
    def axisColoring(self, dataNum):
        # color host
        self.host[self.figColCnt, self.figRowCnt].yaxis.label.set_color(self.colors[config.line_colors[0]])
        self.host[self.figColCnt, self.figRowCnt].yaxis.label.set_alpha(config.alpha[0])
        # color guests     
        self.guest[self.guestPlotCnt - 1].yaxis.label.set_color(self.colors[config.line_colors[dataNum]])
        self.guest[self.guestPlotCnt - 1].yaxis.label.set_alpha(config.alpha[dataNum])

    # =============================== Graph Configurations
    def graphConfigs(self, xLabel, yLabel, zLabel, threeD, title, numOfPlots, plotCounter, plotSelect, numData):
        # save fig
        self.fig.savefig('%s' %config.logDir + os.sep + '%s.%s' %(self.date, config.figFormat), format = config.figFormat)
        
        # set label scalings
        self.host[self.figColCnt, self.figRowCnt].set_xscale(config.scaleX[plotCounter])
        self.host[self.figColCnt, self.figRowCnt].set_yscale(config.scaleY[plotCounter])
        if threeD: 
            self.host[self.figColCnt, self.figRowCnt].set_zscale(config.scaleZ[plotCounter])
            # set azimuth and elevation angles for 3D plot 
            self.host[self.figColCnt, self.figRowCnt].azim = config.threeD_azimDegree[plotCounter]
            self.host[self.figColCnt, self.figRowCnt].elev = config.threeD_elevDegree[plotCounter]

        # set axis limits
        self.host[self.figColCnt, self.figRowCnt].set_xlim(config.limX[plotCounter])
        self.host[self.figColCnt, self.figRowCnt].set_ylim(config.limY[plotCounter])
        if threeD: 
            self.host[self.figColCnt, self.figRowCnt].set_zlim(config.limZ[plotCounter])
        
        # set ticks
        if not config.xticks[plotCounter][-1] is None: # check if user set spacing for ticks, otherwise don't set up xticks manually
            if config.xticks[plotCounter][0] is None or config.xticks[plotCounter][1] is None: # get start and end points from ax if user did not define them
                ticksStart, ticksEnd = self.host[self.figColCnt, self.figRowCnt].get_xlim()
                self.host[self.figColCnt, self.figRowCnt].xaxis.set_ticks(np.arange(ticksStart, ticksEnd, config.xticks[plotCounter][2]))
            else:
                self.host[self.figColCnt, self.figRowCnt].xaxis.set_ticks(np.arange(config.xticks[plotCounter][0], config.xticks[plotCounter][1], config.xticks[plotCounter][2]))
        if not config.yticks[plotCounter][-1] is None:
            if config.yticks[plotCounter][0] is None or config.yticks[plotCounter][1] is None:
                ticksStart, ticksEnd = self.host[self.figColCnt, self.figRowCnt].get_ylim()
                self.host[self.figColCnt, self.figRowCnt].yaxis.set_ticks(np.arange(ticksStart, ticksEnd, config.yticks[plotCounter][2]))
            else:
                self.host[self.figColCnt, self.figRowCnt].yaxis.set_ticks(np.arange(config.yticks[plotCounter][0], config.yticks[plotCounter][1], config.yticks[plotCounter][2]))
        if threeD and not config.zticks[plotCounter][-1] is None: 
            if config.zticks[plotCounter][0] is None or config.zticks[plotCounter][1] is None:
                ticksStart, ticksEnd = self.host[self.figColCnt, self.figRowCnt].get_zlim()
                self.host[self.figColCnt, self.figRowCnt].zaxis.set_ticks(np.arange(ticksStart, ticksEnd, config.zticks[plotCounter][2]))
            else:
                self.host[self.figColCnt, self.figRowCnt].zaxis.set_ticks(np.arange(config.zticks[plotCounter][0], config.zticks[plotCounter][1], config.zticks[plotCounter][2]))

        # set labels
        self.host[self.figColCnt, self.figRowCnt].set_xlabel(xLabel)
        self.host[self.figColCnt, self.figRowCnt].set_ylabel(yLabel[0])
        if config.additionalYAxes:# and plotSelect in ['line', 'seaborn line']:
            guestCnt = 0
            for i in range(numData - 1):
                if config.additionalYAxes_enable[i]: 
                    self.guest[guestCnt].set_ylabel(yLabel[i + 1])
                    guestCnt += 1
        if threeD: self.host[self.figColCnt, self.figRowCnt].set_zlabel(zLabel)

        # set label paddings
        self.host[self.figColCnt, self.figRowCnt].axes.xaxis.labelpad = config.xAxis_labelPad[plotCounter]
        self.host[self.figColCnt, self.figRowCnt].axes.yaxis.labelpad = config.yAxis_labelPad[plotCounter]
        if threeD: self.host[self.figColCnt, self.figRowCnt].axes.zaxis.labelpad = config.zAxis_labelPad[plotCounter]

        # set subtitle
        if numOfPlots > 1:
            self.host[self.figColCnt, self.figRowCnt].title.set_text(title)
        
        # set legend
        if self.guestPlotCnt > 0: 
            self.linesSum = self.hostLines + self.linesSum
            self.labelsSum = self.hostLabels + self.labelsSum
            self.guest[self.guestPlotCnt - 1].legend(self.linesSum, self.labelsSum)
        if config.subplotLegend:
            if not plotSelect in {'box'} and not config.additionalYAxes: # box plots do not have legend
                if config.legend_bbox_to_anchor != None: # Set up legend only for the last plot
                    self.host[self.figColCnt, self.figRowCnt].legend(bbox_to_anchor = config.legend_bbox_to_anchor, loc = config.legend_loc, 
                            mode = config.legend_mode, borderaxespad = config.legend_border_axesPad, ncol = config.legend_nCol)
                else:    
                    self.host[self.figColCnt, self.figRowCnt].legend(bbox_to_anchor = config.legend_bbox_to_anchor, loc = config.legend_loc, 
                            mode = config.legend_mode, borderaxespad = config.legend_border_axesPad, ncol = config.legend_nCol)
            self.hostLines, self.hostLabels, self.guestLines, self.guestLabels, self.linesSum, self.labelsSum  = [], [], [], [], [], [] # reinitialize label arrays
 
        # seaborn jointplot specific settings
        if plotSelect in {'seaborn jointplot'}:
            self.snsJntPlot.ax_joint.set_xlabel(xLabel)
            self.snsJntPlot.ax_joint.set_ylabel(yLabel[0])
            self.snsJntPlot.ax_joint.tick_params(axis = 'x')
            self.snsJntPlot.ax_joint.tick_params(axis = 'y')
            plt.suptitle(title)
            plt.subplots_adjust(top = 0.9, bottom = 0.2)
            
        # logic to place subplots in the right location
        if not self.oneColSpecPlt:
            if (plotCounter + 1) % self.numOfRow == 0:
                self.figColCnt += 1
                self.figRowCnt -= (self.numOfRow - 1)
            else:
                self.figRowCnt += 1
        else:
            self.figColCnt += 1
            
    # =============================== Show the plot
    def showPlot(self, title, numOfPlots):
        if not self.oneColSpecPlt:
            self.fig.suptitle(title) # Main title
        else:
            self.fig.suptitle(title, x = config.oneColSpecPlt_loc_xTitle) # Main title
        if config.figLegend: 
            self.fig.legend(bbox_to_anchor = config.legend_bbox_to_anchor, loc = config.legend_loc, 
                    mode = config.legend_mode, borderaxespad = config.legend_border_axesPad, ncol = config.legend_nCol)
        self.fig.savefig('%s' %config.logDir + os.sep + '%s.%s' %(self.date, config.figFormat), bbox_inches = 'tight', format = config.figFormat) # save fig to logs dir
        self.fig.tight_layout() # to adjust spacing between graphs and labels
        plt.show()
    
    # =============================== Bar graph
    def barPlot(self, i, colNumX, colNumY, legendName, data):
        self.host[self.figColCnt, self.figRowCnt].bar(data[colNumX[i]], data[colNumY[i]], color = self.colors[config.line_colors[i % len(config.line_colors)]], 
                width = config.bar_width[i], bottom = config.bar_bottom[i], align = config.bar_align[i], label = legendName[i], alpha = config.alpha[i]) 

    # =============================== Box graph
    def boxPlot(self, i, colNumX, legendName, data):
        self.host[self.figColCnt, self.figRowCnt].boxplot(data[colNumX[i]], positions = np.array(range(len(data[colNumX[i]]))) + 1, notch = config.box_notched[i], vert = config.box_vert[i],
                whis = config.box_whis[i], bootstrap = config.box_bootstrap[i], widths = config.box_widths[i], patch_artist = config.box_patchArtist[i], labels = config.box_labels[i], 
                zorder = config.box_zOrder[i], boxprops = dict(facecolor = self.colors[config.line_colors[0]], color = self.colors[config.line_colors[1]]), 
                capprops = dict(color = self.colors[config.line_colors[2]]), whiskerprops = dict(color = self.colors[config.line_colors[3]]), 
                flierprops = dict(color = self.colors[config.line_colors[4]], markeredgecolor = self.colors[config.line_colors[5]]), 
                medianprops = dict(color = self.colors[config.line_colors[6]]))
        self.host[self.figColCnt, self.figRowCnt].set_xticklabels(legendName)

    # =============================== CDF graph
    def cdfPlot(self, i, colNumX, legendName, data):
        bin_edges_list = [] 
        cdfData = []
        data_size = len(data[colNumX[i]]) # taken from: https://stackoverflow.com/questions/24575869/read-file-and-plot-cdf-in-python
        data_set = sorted(set(data[colNumX[i]]))
        bins = np.append(data_set, data_set[-1] + 1)
        counts, bin_edges = np.histogram(data[colNumX[i]], bins = bins, density = False) # Use histogram function to bin data
        counts = counts.astype(float) / data_size
        cdfData = np.cumsum(counts)
        self.host[self.figColCnt, self.figRowCnt].plot(bin_edges[0:-1], cdfData, 
                self.colors[config.line_colors[i]], linestyle = config.line_style[i], 
                label = legendName[i], linewidth = config.line_width[i], 
                marker = config.line_markerStyle[i], alpha = config.alpha[i])
        print(self.host[self.figColCnt, self.figRowCnt].legend())

    # =============================== Histogram graph
    def histogramPlot(self, i, colNumX, binRes, legendName, data):
        self.bins = np.arange(min(data[colNumX[i]]) - binRes, max(data[colNumX[i]]) + binRes * 2, binRes)
        self.host[self.figColCnt, self.figRowCnt].hist(data[colNumX[i]], bins = self.bins, density = config.hist_density[i], cumulative = config.hist_cumulative[i],
                bottom = config.hist_bottom[i], histtype = config.hist_histtype[i], align = config.hist_align[i], orientation = config.hist_orientation[i],
                rwidth = config.hist_rwidth[i], color = self.colors[config.line_colors[i]], stacked = config.hist_stacked[i], 
                edgecolor = config.hist_edgeColor[i], label = legendName[i], alpha = config.alpha[i])  
        self.host[self.figColCnt, self.figRowCnt].set_xticks(self.bins[:-1]) # TODO modify this per ax

    # =============================== Line Plot - Primary y-axis  
    def linePlot_host(self, i, p, plotPlotSelect, colNumX, colNumY, colNumE, legendName, data):
        p.append(0) #initialize array entry
        if plotPlotSelect[0] == 1: # line plot
            p[self.guestPlotCnt], = self.host[self.figColCnt, self.figRowCnt].plot(data[colNumX[i]], data[colNumY[i]], self.colors[config.line_colors[i]], 
                    linestyle = config.line_style[i], label = legendName[i], linewidth = config.line_width[i], marker = config.line_markerStyle[i], alpha = config.alpha[i])  
        elif plotPlotSelect[0] == 2: # line plot w/ errorbar
            p[self.guestPlotCnt], = self.host[self.figColCnt, self.figRowCnt].errorbar(data[colNumX[i]], data[colNumY[i]], yerr = data[colNumE[i]], 
                    c = self.colors[config.line_colors[i]], fmt = config.line_style[i], label = legendName[i], kwargs = {'alpha': config.alpha[i]})

    # =============================== Line Plot - Additional y-axes
    def linePlot_guest(self, i, p, plotPlotSelect, colNumX, colNumY, colNumE, legendName, data):
        p.append(0) #initialize array entry
        self.guest.append(0) #initialize array entry
        self.guest[self.guestPlotCnt] = self.host[self.figColCnt, self.figRowCnt].twinx() # setup 2nd axis based on the first graph
        if plotPlotSelect[0] == 1: # line plot
            p[self.guestPlotCnt], = self.guest[self.guestPlotCnt].plot(data[colNumX[i]], data[colNumY[i]], self.colors[config.line_colors[i]], linestyle = config.line_style[i], 
            label = legendName[i], linewidth = config.line_width[i], marker = config.line_markerStyle[i], alpha = config.alpha[i])  
        elif plotPlotSelect[0] == 2: # line plot w/ errorbar
            p[self.guestPlotCnt], = self.guest[self.guestPlotCnt].errorbar(data[colNumX[i]], data[colNumY[i]], yerr = data[colNumE[i]], c = self.colors[config.line_colors[i]], 
            fmt = config.line_style[i], label = legendName[i], kwargs = {'alpha': config.alpha[i]})
        self.guest[self.guestPlotCnt].set_ylim(min(data[colNumY[i]]) - config.yLimThreshold[i], max(data[colNumY[i]]) + config.yLimThreshold[i])
        self.guest[self.guestPlotCnt].grid(False)
        self.guest[self.guestPlotCnt].spines['right'].set_position(("axes", self.axisOffset)) 
        lines, labels = self.guest[self.guestPlotCnt].get_legend_handles_labels()
        return lines, labels

    # =============================== Line-type graphs
    def linePlot(self, plotPlotSelect, dataNum, colNumX, colNumY, colNumE, legendName, data):
        p = []
        if config.additionalYAxes: # multiple-axis enabled
            if dataNum == 0:
                self.linePlot_host(dataNum, p, plotPlotSelect, colNumX, 
                        colNumY, colNumE, legendName, data)
            else:
                if config.additionalYAxes_enable[dataNum]:
                    lines, labels = self.linePlot_guest(dataNum, p, plotPlotSelect, colNumX,
                            colNumY, colNumE, legendName, data)
                    self.guestLines += lines
                    self.guestLabels += labels
                    self.guestPlotCnt += 1
                    self.axisOffset += config.axisOffset[self.guestPlotCnt]
                else:
                    self.linePlot_host(dataNum, p, plotPlotSelect, colNumX, colNumY, colNumE, 
                            legendName, data)
            self.hostLines, self.hostLabels = self.host[self.figColCnt, self.figRowCnt].get_legend_handles_labels()
            self.linesSum = self.hostLines + self.guestLines
            self.labelsSum = self.hostLabels + self.guestLabels
            if self.guestPlotCnt > 0: self.guest[self.guestPlotCnt - 1].legend(self.linesSum, self.labelsSum)
            if self.guestPlotCnt == dataNum - 1: self.axisColoring(dataNum) # color the axes iff each line has a y-axis
        else:
            self.linePlot_host(dataNum, p, plotPlotSelect, colNumX, 
                        colNumY, colNumE, legendName, data)
                    
    # =============================== 3D graph
    def threeDPlot(self, numOfPlots, plotSelect, numData, colNumX, colNumY, colNumZ, legendName, data):
        self.host[self.figColCnt, self.figRowCnt].axis('off')
        numOfRow = 2 if numOfPlots > 1 else 1
        self.host[self.figColCnt, self.figRowCnt] = self.fig.add_subplot(math.ceil(numOfPlots / numOfRow), numOfRow, plotCounter + 1, projection = '3d') # TODO move this to prepplot()
        for i in range(numData):
            self.host[self.figColCnt, self.figRowCnt].plot(data[colNumX[i]], data[colNumY[i]], data[colNumZ[i]], self.colors[config.line_colors[i % len(config.line_colors)]], 
                    label = legendName[i], linewidth = config.line_width[i], marker = config.line_markerStyle[i], alpha = config.alpha[i])

    # =============================== Seaborn Line Graph - Primary y-axis
    def seabornLinePlot_host(self, i, colNumX, colNumY, legendName, data):
        sns.lineplot(x = data[colNumX[i]], y = data[colNumY[i]], color = self.colors[config.line_colors[i]], label = legendName[i], 
                ax = self.host[self.figColCnt, self.figRowCnt], linewidth = config.line_width[i], marker = config.line_markerStyle[i], 
                hue = config.snsLine_hue[i], size = config.snsLine_size[i], style = config.snsLine_style[i], alpha = config.alpha[i]) 
        self.host[self.figColCnt, self.figRowCnt].lines[i].set_linestyle(config.line_style[i])
        self.host[self.figColCnt, self.figRowCnt].legend_.remove()

    # =============================== Seaborn Line Graph - Primary y-axis when used with guest plot
    def seabornLinePlot_host_withGuest(self, i, colNumX, colNumY, legendName, data):
        self.seabornLinePlot_host(i, colNumX,
                            colNumY, legendName, data)
        lines, labels = self.host[self.figColCnt, self.figRowCnt].get_legend_handles_labels()
        self.hostLines += lines
        self.hostLabels += labels

    # =============================== Seaborn Line Graph - Additional y-axes
    def seabornLinePlot_guest(self, i, colNumX, colNumY, legendName, data):
        self.guest.append(0) # initialize array entry
        self.guest[self.guestPlotCnt] = self.host[self.figColCnt, self.figRowCnt].twinx() # setup 2nd axis based on the first graph
        sns.lineplot(x = data[colNumX[i]], y = data[colNumY[i]], color = self.colors[config.line_colors[i % len(config.line_colors)]], label = legendName[i], 
                ax = self.guest[self.guestPlotCnt], linewidth = config.line_width[i], marker = config.line_markerStyle[i],
                hue = config.snsLine_hue[i], size = config.snsLine_size[i], style = config.snsLine_style[i], alpha = config.alpha[i]) 
        self.guest[self.guestPlotCnt].lines[0].set_linestyle(config.line_style[i])
        self.guest[self.guestPlotCnt].set_ylim(min(data[colNumY[i]]) - config.yLimThreshold[i], max(data[colNumY[i]]) + config.yLimThreshold[i])
        self.guest[self.guestPlotCnt].grid(False)
        self.guest[self.guestPlotCnt].legend_.remove()
        self.guest[self.guestPlotCnt].spines['right'].set_position(("axes", self.axisOffset))
        lines, labels = self.guest[self.guestPlotCnt].get_legend_handles_labels()
        self.linesSum += lines
        self.labelsSum += labels
        self.guestPlotCnt += 1
        self.axisOffset += config.axisOffset[self.guestPlotCnt]

    # =============================== Seaborn Line Graph
    def seabornLinePlot(self, dataNum, colNumX, colNumY, legendName, data):
        if config.additionalYAxes: # multiple-axis enabled
            if dataNum == 0:
                self.seabornLinePlot_host_withGuest(dataNum, colNumX,
                            colNumY, legendName, data)
            else:
                if config.additionalYAxes_enable[dataNum]:
                    self.seabornLinePlot_guest(dataNum, colNumX,
                            colNumY, legendName, data)
                else:
                    self.seabornLinePlot_host_withGuest(dataNum, colNumX,
                            colNumY, legendName, data)
            if any(config.additionalYAxes_enable) and self.guestPlotCnt > 0: self.axisColoring(dataNum) # color the axes iff each line has a y-axis
        else:
            self.seabornLinePlot_host(dataNum, colNumX,
                    colNumY, legendName, data)

    # =============================== Seaborn Joint Graph
    def seabornJointPlot(self, i, colNumX, colNumY, legendName, data):
        self.snsJntPlot = sns.jointplot(x = data[colNumX[i]], y = data[colNumY[i]], kind = config.snsJoint_kind, 
        color = self.colors[config.line_colors[i % len(config.line_colors)]], label = legendName[i])

    # =============================== Plotter function
    def mainPlotter(self, plotCounter, numOfPlots, plotSelect, plotPlotSelect, dataNum, colNumX, colNumY, colNumZ, colNumE, legendName, binRes, data):
        if dataNum == 0:
            self.guestPlotCnt = 0
            self.axisOffset = 1
        # Main if clause for plots
        if plotSelect == 'bar':
            self.barPlot(dataNum, colNumX, colNumY, legendName, data)
        elif plotSelect == 'box':
            self.boxPlot(dataNum, colNumX, legendName, data)
        elif plotSelect == 'cdf':
            self.cdfPlot(dataNum, colNumX, legendName, data)
        elif plotSelect == 'histogram':
            self.histogramPlot(dataNum, colNumX, binRes, legendName, data)
        elif plotSelect in ['line, scatter, errorbars']:
            self.linePlot(plotPlotSelect, dataNum, colNumX, colNumY, colNumE, legendName, data)
        elif plotSelect == '3d':
            self.threeDPlot(numOfPlots, plotSelect, dataNum, colNumX, colNumY, colNumZ, legendName, data)
        elif plotSelect == 'seaborn line':
            self.seabornLinePlot(dataNum, colNumX, colNumY, legendName, data)
        elif plotSelect == 'seaborn jointplot':
            self.seabornJointPlot(dataNum, colNumX, colNumY, legendName, data)
        self.plotCounter += 1
     