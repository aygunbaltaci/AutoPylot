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
import yaml
sys.path.append('config' + os.sep)
import config_matplotlibrc
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
        self.currentPath = os.getcwd() 
        self.config_folderdirectory = self.currentPath + os.sep + 'config' + os.sep
        self.mainconfig_name = 'mainconfig'
        self.plotconfig_name = 'plotconfig'
        self.config_format = '.yaml'
        self.config_separator = ','
        self.fTxtNoXServer = f"""
{Fore.RED}Your X-server is not running, cannot plot the graph.
Please turn on your X-server first and then hit [enter]"""

    # =============================== Open main config file
    def openMainConfig(self):
        with open(self.config_folderdirectory + self.mainconfig_name + self.config_format, 'r') as stream:
            self.mainconfig = yaml.safe_load(stream)
        
    # =============================== Open plot config file
    def openPlotConfig(self):
        with open(self.config_folderdirectory + self.plotconfig_name + self.config_format, 'r') as stream:
            self.plotconfig = yaml.safe_load(stream)

    # =============================== Prepare the plot
    def prepPlot(self, numOfPlots):
        # open config files
        self.openMainConfig()
        self.openPlotConfig()

        exitLoop = False
        plt.rcParams.update(config_matplotlibrc.parameters) # update matplotlib parameters
        
        while True:
            try:   
                self.numOfRow = self.mainconfig['MAIN']['figure_plotperrow'] if numOfPlots > 1 else 1
                if (self.mainconfig['MAIN']['figure_plotperrow'] == 1 and numOfPlots > 1) and self.mainconfig['MAIN']['figure_singlecolumnnarrowplot']:
                    self.numOfRow = 2
                    self.oneColSpecPlt = True
                else:
                    self.oneColSpecPlt = False

                if not self.oneColSpecPlt:
                    self.fig, self.host = plt.subplots(math.ceil(numOfPlots / self.numOfRow), self.numOfRow, 
                            sharex = self.mainconfig['MAIN']['figure_sharexaxis'], sharey = self.mainconfig['MAIN']['figure_shareyaxis'], 
                            figsize = (self.mainconfig['MAIN']['outputfigure_xdimension'], self.mainconfig['MAIN']['outputfigure_ydimension']), squeeze = False)
                    if numOfPlots != 1 and numOfPlots % self.numOfRow != 0: # turn off the axes of last unused plot, because there is leftover plot in when total plots are odd
                        for i in range(numOfPlots % self.numOfRow, self.numOfRow):
                            self.host[int(numOfPlots / self.numOfRow), i].axis('off')
                else:
                    self.fig, self.host = plt.subplots(numOfPlots, self.numOfRow, 
                            sharex = self.mainconfig['MAIN']['figure_sharexaxis'], sharey = self.mainconfig['MAIN']['figure_shareyaxis'], 
                            figsize = (self.mainconfig['MAIN']['outputfigure_xdimension'], self.mainconfig['MAIN']['outputfigure_ydimension']), squeeze = False)
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
    def axisColoring(self, dataNum, colorHost, colorGuest):
        # color host
        self.host[self.figColCnt, self.figRowCnt].yaxis.label.set_color(self.colors[colorHost])
        self.host[self.figColCnt, self.figRowCnt].yaxis.label.set_alpha(self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['dataset' + str(0)]['graph_alpha'])
        # color guests     
        self.guest[self.guestPlotCnt - 1].yaxis.label.set_color(self.colors[colorGuest])
        self.guest[self.guestPlotCnt - 1].yaxis.label.set_alpha(self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['dataset' + str(dataNum)]['graph_alpha'])

    # =============================== Graph Configurations
    def graphConfigs(self, xLabel, yLabel, zLabel, threeD, title, numOfPlots, plotSelect, numData):
        # save fig
        self.fig.savefig('%s' %self.mainconfig['MAIN']['outputfigure_directory'] + os.sep + 
                '%s.%s' %(self.date, self.mainconfig['MAIN']['outputfigure_format']), 
                format = self.mainconfig['MAIN']['outputfigure_format'])
        
        # set label scalings
        self.host[self.figColCnt, self.figRowCnt].set_xscale(self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['plot_xscale'])
        self.host[self.figColCnt, self.figRowCnt].set_yscale(self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['plot_yscale'])
        if threeD: 
            self.host[self.figColCnt, self.figRowCnt].set_zscale(self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['plot_zscale'])
            # set azimuth and elevation angles for 3D plot 
            self.host[self.figColCnt, self.figRowCnt].azim = self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['plot_threed_azimdegree']
            self.host[self.figColCnt, self.figRowCnt].elev = self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['plot_threed_elevdegree']

        # set axis limits
        self.host[self.figColCnt, self.figRowCnt].set_xlim(xmin = self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['plot_xlimit_min'],
                xmax = self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['plot_xlimit_max'])
        self.host[self.figColCnt, self.figRowCnt].set_ylim(ymin = self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['plot_ylimit_min'],
                ymax = self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['plot_ylimit_max'])
        if threeD: 
            self.host[self.figColCnt, self.figRowCnt].set_zlim(zmin = self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['plot_zlimit_min'],
                zmax = self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['plot_zlimit_max'])
        #if self.plotCounter == 1: self.guest[self.guestPlotCnt - 1].set_ylim(0, 50)
        
        # set ticks
        if not self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['plot_xticks_distance'] is None: # check if user set spacing for ticks, otherwise don't set up xticks manually
            if self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['plot_xticks_min'] is None or self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['plot_xticks_max'] is None: # get start and end points from ax if user did not define them
                ticksStart, ticksEnd = self.host[self.figColCnt, self.figRowCnt].get_xlim()
                self.host[self.figColCnt, self.figRowCnt].xaxis.set_ticks(np.arange(ticksStart, ticksEnd, self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['plot_xticks_distance']))
            else:
                self.host[self.figColCnt, self.figRowCnt].xaxis.set_ticks(np.arange(self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['plot_xticks_min'], self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['plot_xticks_max'], self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['plot_xticks_distance']))
        if not self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['plot_yticks_distance'] is None:
            if self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['plot_yticks_min'] is None or self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['plot_yticks_max'] is None:
                ticksStart, ticksEnd = self.host[self.figColCnt, self.figRowCnt].get_ylim()
                self.host[self.figColCnt, self.figRowCnt].yaxis.set_ticks(np.arange(ticksStart, ticksEnd, self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['plot_yticks_distance']))
            else:
                self.host[self.figColCnt, self.figRowCnt].yaxis.set_ticks(np.arange(self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['plot_yticks_min'], self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['plot_yticks_max'], self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['plot_yticks_distance']))
        if threeD and not self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['plot_zticks_distance'] is None: 
            if self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['plot_zticks_min'] is None or self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['plot_zticks_max'] is None:
                ticksStart, ticksEnd = self.host[self.figColCnt, self.figRowCnt].get_zlim()
                self.host[self.figColCnt, self.figRowCnt].zaxis.set_ticks(np.arange(ticksStart, ticksEnd, self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['plot_zticks_distance']))
            else:
                self.host[self.figColCnt, self.figRowCnt].zaxis.set_ticks(np.arange(self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['plot_zticks_min'], self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['plot_zticks_max'], self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['plot_zticks_distance']))

        # set labels
        self.host[self.figColCnt, self.figRowCnt].set_xlabel(xLabel)
        self.host[self.figColCnt, self.figRowCnt].set_ylabel(yLabel[0])
        if self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['multipleyaxis']:# and plotSelect in ['line', 'seaborn line']:
            guestCnt = 0
            for i in range(numData - 1):
                if self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['dataset' + str(i)]['yaxis_on']: 
                    self.guest[guestCnt].set_ylabel(yLabel[i + 1])
                    guestCnt += 1
        if threeD: self.host[self.figColCnt, self.figRowCnt].set_zlabel(zLabel)

        # set label paddings
        self.host[self.figColCnt, self.figRowCnt].axes.xaxis.labelpad = self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['plot_xlabel_pad']
        self.host[self.figColCnt, self.figRowCnt].axes.yaxis.labelpad = self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['plot_ylabel_pad']
        if threeD: self.host[self.figColCnt, self.figRowCnt].axes.zaxis.labelpad = self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['plot_zlabel_pad']

        # set subtitle
        if numOfPlots > 1:
            self.host[self.figColCnt, self.figRowCnt].title.set_text(title)
        
        # set legend
        if self.guestPlotCnt > 0: 
            self.linesSum = self.hostLines + self.linesSum
            self.labelsSum = self.hostLabels + self.labelsSum
            self.guest[self.guestPlotCnt - 1].legend(self.linesSum, self.labelsSum)
        if self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['plotlegend']:
            if not plotSelect in {'box'} and not self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['multipleyaxis']: # box plots do not have legend
                if self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['plotlegend_ncolumn'] != None: # TODO is this correct ??? Set up legend only for the last plot
                    self.host[self.figColCnt, self.figRowCnt].legend(bbox_to_anchor = self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['plotlegend_bbox_to_anchor'], 
                    loc = self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['plotlegend_location'], mode = self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['plotlegend_mode'], 
                    borderaxespad = self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['plotlegend_border_axisPad'], ncol = self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['plotlegend_ncolumn'])
                else:    
                    self.host[self.figColCnt, self.figRowCnt].legend(bbox_to_anchor = self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['plotlegend_bbox_to_anchor'], 
                    loc = self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['plotlegend_location'], mode = self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['plotlegend_mode'], 
                    borderaxespad = self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['plotlegend_border_axisPad'], ncol = self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['plotlegend_ncolumn'])
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
            if (self.plotCounter + 1) % self.numOfRow == 0:
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
            self.fig.suptitle(title, x = self.mainconfig['MAIN']['self.figure_singlecolumnnarrowplot_xtitlelocation']) # Main title
        if self.mainconfig['MAIN']['figurelegend']: 
            self.fig.legend(bbox_to_anchor = self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['plotlegend_ncolumn'], 
                    loc = self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['plotlegend_location'], 
                    mode = self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['plotlegend_mode'], 
                    borderaxespad = self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['plotlegend_border_axisPad'], 
                    ncol = self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['plotlegend_ncolumn'])
        self.fig.savefig('%s' %self.mainconfig['MAIN']['outputfigure_directory'] + os.sep + '%s.%s' %(self.date, self.mainconfig['MAIN']['outputfigure_format']), bbox_inches = 'tight', format = self.mainconfig['MAIN']['outputfigure_format']) # save fig to logs dir
        self.fig.tight_layout() # to adjust spacing between graphs and labels
        plt.show()
    
    # =============================== Bar graph
    def barPlot(self, i, colNumX, colNumY, legendName, data):
        print(data)
        self.host[self.figColCnt, self.figRowCnt].bar(
                data[colNumX], 
                data[colNumY], 
                color = self.colors[self.plotconfig['BAR']['Plot' + str(i)]['color']], 
                edgecolor = self.colors[self.plotconfig['BAR']['Plot' + str(i)]['edgecolor']],
                linewidth = self.plotconfig['BAR']['Plot' + str(i)]['edgewidth'], 
                tick_label = self.plotconfig['BAR']['Plot' + str(i)]['label'], 
                capsize = self.plotconfig['BAR']['Plot' + str(i)]['capsize'], 
                width = self.plotconfig['BAR']['Plot' + str(i)]['width'], 
                bottom = self.plotconfig['BAR']['Plot' + str(i)]['bottom'], 
                align = self.plotconfig['BAR']['Plot' + str(i)]['align'], 
                label = legendName[i], 
                alpha = self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['dataset' + str(i)]['graph_alpha']) 

    # =============================== Box graph
    def boxPlot(self, i, colNumX, legendName, data):
        self.host[self.figColCnt, self.figRowCnt].boxplot(
                data[colNumX], 
                positions = np.array(range(len(data[colNumX]))) + 1, 
                boxprops = dict(facecolor = self.colors[self.plotconfig['BOX']['Plot' + str(i)]['boxcolor']], 
                color = self.colors[self.plotconfig['BOX']['Plot' + str(i)]['linecolor']]), 
                capprops = dict(color = self.colors[self.plotconfig['BOX']['Plot' + str(i)]['capcolor']]), 
                whiskerprops = dict(color = self.colors[self.plotconfig['BOX']['Plot' + str(i)]['whiskercolor']]), 
                flierprops = dict(color = self.colors[self.plotconfig['BOX']['Plot' + str(i)]['fliercolor']], 
                markeredgecolor = self.colors[self.plotconfig['BOX']['Plot' + str(i)]['markeredgecolor']]), 
                medianprops = dict(color = self.colors[self.plotconfig['BOX']['Plot' + str(i)]['mediancolor']]), 
                widths = self.plotconfig['BOX']['Plot' + str(i)]['width'], 
                labels = self.plotconfig['BOX']['Plot' + str(i)]['label'], 
                vert = self.plotconfig['BOX']['Plot' + str(i)]['vertical'], 
                notch = self.plotconfig['BOX']['Plot' + str(i)]['notch'], 
                whis = self.plotconfig['BOX']['Plot' + str(i)]['whiskerreach'], 
                bootstrap = self.plotconfig['BOX']['Plot' + str(i)]['bootstrap'], 
                patch_artist = self.plotconfig['BOX']['Plot' + str(i)]['patchartist'], 
                zorder = self.plotconfig['BOX']['Plot' + str(i)]['zorder'])
        self.host[self.figColCnt, self.figRowCnt].set_xticklabels(legendName)

    # =============================== CDF graph
    def cdfPlot(self, i, colNumX, legendName, data):
        bin_edges_list = [] 
        cdfData = []
        data_size = len(data[colNumX]) # taken from: https://stackoverflow.com/questions/24575869/read-file-and-plot-cdf-in-python
        data_set = sorted(set(data[colNumX]))
        bins = np.append(data_set, data_set[-1] + 1)
        counts, bin_edges = np.histogram(data[colNumX], bins = bins, density = False) # Use histogram function to bin data
        counts = counts.astype(float) / data_size
        cdfData = np.cumsum(counts)
        self.host[self.figColCnt, self.figRowCnt].plot(
                bin_edges[0:-1], 
                cdfData, 
                self.colors[self.plotconfig['CDF']['Plot' + str(i)]['color']], 
                linewidth = self.plotconfig['CDF']['Plot' + str(i)]['width'], 
                linestyle = self.plotconfig['CDF']['Plot' + str(i)]['style'], 
                marker = self.plotconfig['CDF']['Plot' + str(i)]['markerstyle'], 
                markersize = self.plotconfig['CDF']['Plot' + str(i)]['markersize'], 
                label = legendName[i],   
                alpha = self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['dataset' + str(i)]['graph_alpha'])
        print(self.host[self.figColCnt, self.figRowCnt].legend())

    # =============================== Histogram graph
    def histogramPlot(self, i, colNumX, legendName, data):
        self.bins = np.arange(min(data[colNumX]) - binRes, max(data[colNumX]) + binRes * 2, binRes) # TODO get rid of this. Only do number of bins
        self.host[self.figColCnt, self.figRowCnt].hist(
                data[colNumX], 
                bins = self.bins, 
                color = self.colors[self.plotconfig['HISTOGRAM']['Plot' + str(i)]['color']], 
                edgecolor = self.plotconfig['HISTOGRAM']['Plot' + str(i)]['edgecolor'], 
                histtype = self.plotconfig['HISTOGRAM']['Plot' + str(i)]['type'], 
                density = self.plotconfig['HISTOGRAM']['Plot' + str(i)]['density'], 
                cumulative = self.plotconfig['HISTOGRAM']['Plot' + str(i)]['cumulative'], 
                bottom = self.plotconfig['HISTOGRAM']['Plot' + str(i)]['bottom'], 
                align = self.plotconfig['HISTOGRAM']['Plot' + str(i)]['align'],
                orientation = self.plotconfig['HISTOGRAM']['Plot' + str(i)]['align'], 
                rwidth = self.plotconfig['HISTOGRAM']['Plot' + str(i)]['relativewidth'], 
                stacked = self.plotconfig['HISTOGRAM']['Plot' + str(i)]['stacked'],
                label = legendName[i], 
                alpha = self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['dataset' + str(i)]['graph_alpha'])  
        self.host[self.figColCnt, self.figRowCnt].set_xticks(self.bins[:-1]) # TODO modify this per ax

    # =============================== Line Plot - Primary y-axis  
    def linePlot_host(self, i, p, colNumX, colNumY, colNumE, legendName, data):
        p.append(0) #initialize array entry
        p[self.guestPlotCnt], = self.host[self.figColCnt, self.figRowCnt].plot(
                data[colNumX], 
                data[colNumY], 
                self.colors[self.plotconfig['LINE']['Plot' + str(i)]['color']], 
                linewidth = self.plotconfig['LINE']['Plot' + str(i)]['width'], 
                linestyle = self.plotconfig['LINE']['Plot' + str(i)]['style'], 
                marker = self.plotconfig['LINE']['Plot' + str(i)]['markerstyle'], 
                markersize = self.plotconfig['LINE']['Plot' + str(i)]['markersize'],  
                label = legendName[i], 
                kwargs = {'alpha': self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['dataset' + str(i)]['graph_alpha']})

    # =============================== Line Plot - Additional y-axes
    def linePlot_guest(self, i, p, colNumX, colNumY, colNumE, legendName, data):
        p.append(0) #initialize array entry
        self.guest.append(0) #initialize array entry
        self.guest[self.guestPlotCnt] = self.host[self.figColCnt, self.figRowCnt].twinx() # setup 2nd axis based on the first graph
        p[self.guestPlotCnt], = self.guest[self.guestPlotCnt].plot(
                data[colNumX], 
                data[colNumY], 
                self.colors[self.plotconfig['LINE']['Plot' + str(i)]['color']], 
                linewidth = self.plotconfig['LINE']['Plot' + str(i)]['width'], 
                linestyle = self.plotconfig['LINE']['Plot' + str(i)]['style'], 
                marker = self.plotconfig['LINE']['Plot' + str(i)]['markerstyle'], 
                markersize = self.plotconfig['LINE']['Plot' + str(i)]['markersize'],  
                label = legendName[i], 
                kwargs = {'alpha': self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['dataset' + str(i)]['graph_alpha']})
        self.guest[self.guestPlotCnt].set_ylim(min(data[colNumY]) - self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['dataset' + str(i)]['yaxis_ylimthreshold'], max(data[colNumY]) + self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['dataset' + str(i)]['yaxis_ylimthreshold'])
        self.guest[self.guestPlotCnt].grid(False)
        self.guest[self.guestPlotCnt].spines['right'].set_position(("axes", self.axisOffset)) 
        lines, labels = self.guest[self.guestPlotCnt].get_legend_handles_labels()
        return lines, labels

    # =============================== Line-type graphs
    def linePlot(self, dataNum, colNumX, colNumY, colNumE, legendName, data):
        p = []
        if self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['multipleyaxis']: # multiple-axis enabled
            if dataNum == 0:
                self.linePlot_host(dataNum, p, plotPlotSelect, colNumX, 
                        colNumY, colNumE, legendName, data)
            else:
                if self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['dataset' + str(dataNum)]['yaxis_on']:
                    lines, labels = self.linePlot_guest(dataNum, p, plotPlotSelect, colNumX,
                            colNumY, colNumE, legendName, data)
                    self.guestLines += lines
                    self.guestLabels += labels
                    self.guestPlotCnt += 1
                    self.axisOffset += self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['dataset' + str(dataNum)]['yaxis_axisoffset']
                else:
                    self.linePlot_host(dataNum, p, plotPlotSelect, colNumX, colNumY, colNumE, 
                            legendName, data)
            self.hostLines, self.hostLabels = self.host[self.figColCnt, self.figRowCnt].get_legend_handles_labels()
            self.linesSum = self.hostLines + self.guestLines
            self.labelsSum = self.hostLabels + self.guestLabels
            if self.guestPlotCnt > 0: self.guest[self.guestPlotCnt - 1].legend(self.linesSum, self.labelsSum)
            if self.guestPlotCnt == dataNum - 1: self.axisColoring(dataNum, self.plotconfig['LINE']['Plot' + str(0)]['color'], self.plotconfig['LINE']['Plot' + str(dataNum)]['color']) # color the axes iff each line has a y-axis
        else:
            self.linePlot_host(dataNum, p, plotPlotSelect, colNumX, 
                        colNumY, colNumE, legendName, data)

    # =============================== Errorbar Plot - Primary y-axis  
    def errorbarPlot_host(self, i, p, colNumX, colNumY, colNumE, legendName, data):
        p.append(0) #initialize array entry
        p[self.guestPlotCnt], = self.host[self.figColCnt, self.figRowCnt].errorbar(data[colNumX], data[colNumY], 
                yerr = data[colNumE], ecolor = self.colors[self.plotconfig['ERRORBAR']['Plot' + str(i)]['color']], 
                elinewidth = self.plotconfig['ERRORBAR']['Plot' + str(i)]['width'], 
                fmt = self.plotconfig['ERRORBAR']['Plot' + str(i)]['style'], 
                capsize = self.plotconfig['ERRORBAR']['Plot' + str(i)]['capsize'], 
                capthick = self.plotconfig['ERRORBAR']['Plot' + str(i)]['capthickness'],  
                barsabove = self.plotconfig['ERRORBAR']['Plot' + str(i)]['barsabove'], 
                label = legendName[i], 
                kwargs = {'alpha': self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['dataset' + str(i)]['graph_alpha']})

    # =============================== Errorbar Plot - Additional y-axes
    def errorbarPlot_guest(self, i, p, colNumX, colNumY, colNumE, legendName, data):
        p.append(0) #initialize array entry
        self.guest.append(0) #initialize array entry
        self.guest[self.guestPlotCnt] = self.host[self.figColCnt, self.figRowCnt].twinx() # setup 2nd axis based on the first graph
        p[self.guestPlotCnt], = self.guest[self.guestPlotCnt].errorbar(data[colNumX], data[colNumY], 
                yerr = data[colNumE], ecolor = self.colors[self.plotconfig['ERRORBAR']['Plot' + str(i)]['color']], 
                elinewidth = self.plotconfig['ERRORBAR']['Plot' + str(i)]['width'], 
                fmt = self.plotconfig['ERRORBAR']['Plot' + str(i)]['style'], 
                capsize = self.plotconfig['ERRORBAR']['Plot' + str(i)]['capsize'], 
                capthick = self.plotconfig['ERRORBAR']['Plot' + str(i)]['capthickness'],  
                barsabove = self.plotconfig['ERRORBAR']['Plot' + str(i)]['barabove'], 
                label = legendName[i], 
                kwargs = {'alpha': self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['dataset' + str(i)]['graph_alpha']})
        self.guest[self.guestPlotCnt].set_ylim(min(data[colNumY]) - self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['dataset' + str(i)]['yaxis_ylimthreshold'], max(data[colNumY]) + self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['dataset' + str(i)]['yaxis_ylimthreshold'])
        self.guest[self.guestPlotCnt].grid(False)
        self.guest[self.guestPlotCnt].spines['right'].set_position(("axes", self.axisOffset)) 
        lines, labels = self.guest[self.guestPlotCnt].get_legend_handles_labels()
        return lines, labels

    # =============================== Errorbar-type graphs
    def errorbarPlot(self, dataNum, colNumX, colNumY, colNumE, legendName, data):
        p = []
        if self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['multipleyaxis']: # multiple-axis enabled
            if dataNum == 0:
                self.errorbarPlot_host(dataNum, p, colNumX, 
                        colNumY, colNumE, legendName, data)
            else:
                if self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['dataset' + str(dataNum)]['yaxis_on']:
                    lines, labels = self.errorbarPlot_guest(dataNum, p, colNumX,
                            colNumY, colNumE, legendName, data)
                    self.guestLines += lines
                    self.guestLabels += labels
                    self.guestPlotCnt += 1
                    self.axisOffset += self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['dataset' + str(dataNum)]['yaxis_axisoffset']
                else:
                    self.errorbarPlot_host(dataNum, p, colNumX, colNumY, colNumE, 
                            legendName, data)
            self.hostLines, self.hostLabels = self.host[self.figColCnt, self.figRowCnt].get_legend_handles_labels()
            self.linesSum = self.hostLines + self.guestLines
            self.labelsSum = self.hostLabels + self.guestLabels
            if self.guestPlotCnt > 0: self.guest[self.guestPlotCnt - 1].legend(self.linesSum, self.labelsSum)
            if self.guestPlotCnt == dataNum - 1: self.axisColoring(dataNum, self.plotconfig['LINE']['Plot' + str(0)]['color'], self.plotconfig['LINE']['Plot' + str(dataNum)]['color']) # color the axes iff each line has a y-axis
        else:
            self.errorbarPlot_host(dataNum, p, colNumX, 
                        colNumY, colNumE, legendName, data)
                    
    # =============================== 3D graph
    def threeDPlot(self, numOfPlots, plotSelect, numData, colNumX, colNumY, colNumZ, legendName, data):
        self.host[self.figColCnt, self.figRowCnt].axis('off')
        numOfRow = 2 if numOfPlots > 1 else 1
        self.host[self.figColCnt, self.figRowCnt] = self.fig.add_subplot(math.ceil(numOfPlots / numOfRow), numOfRow, self.plotCounter + 1, projection = '3d') # TODO move this to prepplot()
        for i in range(numData):
            self.host[self.figColCnt, self.figRowCnt].plot(
                    data[colNumX], 
                    data[colNumY], 
                    data[colNumZ], 
                    self.colors[self.plotconfig['THREED']['Plot' + str(i)]['color']], 
                    linewidth = self.plotconfig['THREED']['Plot' + str(i)]['width'], 
                    linestyle = self.plotconfig['THREED']['Plot' + str(i)]['style'], 
                    marker = self.plotconfig['THREED']['Plot' + str(i)]['markerstyle'], 
                    markersize = self.plotconfig['THREED']['Plot' + str(i)]['markersize'],
                    label = legendName[i], 
                    alpha = self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['dataset' + str(i)]['graph_alpha'])

    # =============================== Seaborn Line Graph - Primary y-axis
    def seabornLinePlot_host(self, i, colNumX, colNumY, legendName, data):
        sns.lineplot(x = data[colNumX], y = data[colNumY], 
                color = self.colors[self.plotconfig['SNSLINE']['Plot' + str(i)]['color']], 
                linewidth = self.plotconfig['SNSLINE']['Plot' + str(i)]['width'], 
                marker = self.plotconfig['SNSLINE']['Plot' + str(i)]['markerstyle'],
                markersize = self.plotconfig['SNSLINE']['Plot' + str(i)]['markersize'], 
                hue = self.plotconfig['SNSLINE']['Plot' + str(i)]['hue'], 
                size = self.plotconfig['SNSLINE']['Plot' + str(i)]['size'], 
                style = self.plotconfig['SNSLINE']['Plot' + str(i)]['style'], 
                label = legendName[i], alpha = self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['dataset' + str(i)]['graph_alpha'],
                ax = self.host[self.figColCnt, self.figRowCnt]) 
        self.host[self.figColCnt, self.figRowCnt].lines[i].set_linestyle(self.plotconfig['SNSLINE']['Plot' + str(i)]['linestyle'])
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
        sns.lineplot(x = data[colNumX], y = data[colNumY], 
                color = self.colors[self.snsline_color.split(self.config_separator)[i % len(self.snsline_color.split(self.config_separator))]], 
                linewidth = self.plotconfig['SNSLINE']['Plot' + str(i)]['width'], 
                marker = self.plotconfig['SNSLINE']['Plot' + str(i)]['marker'],
                markersize = self.plotconfig['SNSLINE']['Plot' + str(i)]['markersize'], 
                hue = self.plotconfig['SNSLINE']['Plot' + str(i)]['hue'], 
                size = self.plotconfig['SNSLINE']['Plot' + str(i)]['size'], 
                style = self.plotconfig['SNSLINE']['Plot' + str(i)]['style'], 
                label = legendName[i], alpha = self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['dataset' + str(i)]['graph_alpha'],
                ax = self.guest[self.guestPlotCnt]) 
        self.guest[self.guestPlotCnt].lines[0].set_linestyle(self.plotconfig['SNSLINE']['Plot' + str(i)]['linestyle'])
        self.guest[self.guestPlotCnt].set_ylim(min(data[colNumY]) - self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['dataset' + str(i)]['yaxis_ylimthreshold'], max(data[colNumY]) + self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['dataset' + str(i)]['yaxis_ylimthreshold'])
        self.guest[self.guestPlotCnt].grid(False)
        self.guest[self.guestPlotCnt].legend_.remove()
        self.guest[self.guestPlotCnt].spines['right'].set_position(("axes", self.axisOffset))
        lines, labels = self.guest[self.guestPlotCnt].get_legend_handles_labels()
        self.linesSum += lines
        self.labelsSum += labels
        self.guestPlotCnt += 1
        self.axisOffset += self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['dataset' + str(dataNum)]['yaxis_axisoffset']

    # =============================== Seaborn Line Graph
    def seabornLinePlot(self, i, dataNum, colNumX, colNumY, legendName, data):
        if self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['multipleyaxis']: # multiple-axis enabled
            if dataNum == 0:
                self.seabornLinePlot_host_withGuest(dataNum, colNumX,
                            colNumY, legendName, data)
            else:
                if self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['dataset' + str(dataNum)]['yaxis_on']:
                    self.seabornLinePlot_guest(dataNum, colNumX,
                            colNumY, legendName, data)
                else:
                    self.seabornLinePlot_host_withGuest(dataNum, colNumX,
                            colNumY, legendName, data)
            if any(self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['dataset' + str(i)]['yaxis_on']) and self.guestPlotCnt > 0: self.axisColoring(dataNum, self.snsline_color.split(self.config_separator)[0], self.snsline_color.split(self.config_separator)[dataNum]) # TODO find a solution instead of any() color the axes iff each line has a y-axis
        else:
            self.seabornLinePlot_host(dataNum, colNumX,
                    colNumY, legendName, data)

    # =============================== Seaborn Joint Graph
    def seabornJointPlot(self, i, colNumX, colNumY, legendName, data):
        sns.jointplot(
                x = data[colNumX], 
                y = data[colNumY], 
                kind = self.plotconfig['SNSJOINT']['Plot' + str(i)]['kind'], 
                color = self.colors[self.plotconfig['SNSJOINT']['Plot' + str(i)]['color']], 
                label = legendName[i])

    # =============================== Plotter function
    def mainPlotter(self, plotCounter, numOfPlots, plotSelect, dataNum, colNumX, colNumY, colNumZ, colNumE, legendName, data):
        self.plotCounter = plotCounter
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
            self.histogramPlot(dataNum, colNumX, legendName, data)
        elif plotSelect in 'line':
            self.linePlot(dataNum, colNumX, colNumY, colNumE, legendName, data)
        elif plotSelect in 'errorbar':
            self.errorbarPlot(dataNum, colNumX, colNumY, colNumE, legendName, data)
        elif plotSelect == '3d':
            self.threeDPlot(numOfPlots, plotSelect, dataNum, colNumX, colNumY, colNumZ, legendName, data)
        elif plotSelect == 'seaborn line':
            self.seabornLinePlot(dataNum, colNumX, colNumY, legendName, data)
        elif plotSelect == 'seaborn jointplot':
            self.seabornJointPlot(dataNum, colNumX, colNumY, legendName, data)       