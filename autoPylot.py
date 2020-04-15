#!/usr/bin/env python3

import os
import sys
import math
from colorama import Fore, Back, init # colored output on the terminal
from datetime import datetime
import tkinter
import csv
import numpy as np
import yaml
import re
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import seaborn as sns
sys.path.append('config' + os.sep)
import config_matplotlibrc
init(autoreset = True) # turn off colors after each print()


###################### USER INTERACTIONS

class autoPylot:
    # =============================== Initialize variables
    def __init__(self):
        self.config_folderdirectory = os.getcwd() + os.sep + 'config'
        self.mainconfig_name = 'mainconfig'
        self.plotconfig_name = 'plotconfig'
        self.config_format = 'yaml'
        self.config_separator = ','
        self.data = []
        self.defaultLabels = []
        self.inputFile = '' 
        self.inputFileDir = '' 
        self.limits_mainconfig_graph_alpha = (0, 1)
        self.limits_mainconfig_graph_type = ['bar', 'box', 'cdf', 'errorbar', 'histogram', 'line', 'seaborn line', 'seaborn joint']
        self.limits_mainconfig_inputfile_format = ['csv']
        self.limits_mainconfig_inputfile_encoder = ['utf-sig-8'] # TODO extend it
        self.limits_mainconfig_legend_location = (0, 10)
        self.limits_mainconfig_names = ['graph_alpha', 'graph_type', 'inputfile_format', 'inputfile_encoder', 'figurelegend_location', 'outputfigure_format',
                'plotlegend_location', 'plot_xscale', 'plot_yscale', 'plot_zscale']
        self.limits_mainconfig_outputfigure_format = ['eps', 'jpg', 'pdf', 'png', 'svg']
        self.limits_mainconfig_plot_scale = ['linear', 'log', 'logit', 'symlog']
        self.limits_mainconfig_sum = [self.limits_mainconfig_graph_alpha, self.limits_mainconfig_graph_type, self.limits_mainconfig_inputfile_format,
            self.limits_mainconfig_inputfile_encoder, self.limits_mainconfig_legend_location, self.limits_mainconfig_outputfigure_format, 
            self.limits_mainconfig_legend_location, self.limits_mainconfig_plot_scale, self.limits_mainconfig_plot_scale, self.limits_mainconfig_plot_scale]
        self.limits_plotconfig_align_bar = ['center', 'edge']
        self.limits_plotconfig_align_histogram = ['left', 'mid', 'right']
        self.limits_plotconfig_color = (0, 9)
        self.limits_plotconfig_markerstyle = [None, '', ' ', '.', ',', 'o', 'v', '^', '<', '>', '1', '2', '3', '4', '8', 's', 'p', 'P', '*', 'h', 'H', 
                '+', 'x', 'X', 'D', 'd', '|', '_', 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        self.limits_plotconfig_names = ['align_bar', 'align_histogram', 'color', 'markerstyle', 'orientation', 'snsjoint_kind', 'style', 'type']
        self.limits_plotconfig_orientation = ['horizontal', 'vertical']
        self.limits_plotconfig_snsjoint_kind = ['hex', 'kde', 'reg', 'resid', 'scatter']
        self.limits_plotconfig_style = ['', ' ', '-', '--', '-.', ':', 'dashed', 'dashdot', 'dotted', 'solid']
        self.limits_plotconfig_type = ['bar', 'barstacked', 'step', 'stepfilled'] 
        self.limits_plotconfig_sum = [self.limits_plotconfig_align_bar, self.limits_plotconfig_align_histogram, self.limits_plotconfig_color,
                self.limits_plotconfig_markerstyle, self.limits_plotconfig_orientation, self.limits_plotconfig_snsjoint_kind, self.limits_plotconfig_style,
                self.limits_plotconfig_type]
        self.mainconfig_booleans = ['figure_singlecolumnnarrowplot', 'figure_sharexaxis', 'figure_shareyaxis', 'figure_xlabelfrominputfile', 
                'figure_ylabelfrominputfile', 'figure_zlabelfrominputfile', 'figurelegend', 'multipleyaxis', 'plotlegend', 'yaxis_on']
        self.mainconfig_floats = ['figure_singlecolumnnarrowplot_xtitlelocation', 'figurelegend_border_axispad', 'outputfigure_xdimension',
                'outputfigure_ydimension', 'plot_xlabel_pad', 'plot_ylabel_pad', 'plot_zlabel_pad', 'plotlegend_border_axisPad', 'yaxis_axisoffset']
        self.mainconfig_integers = ['figurelegend_location', 'figurelegend_ncolumn', 'figure_plotperrow', 'input_edata', 'input_xdata', 'input_ydata', 
                'input_zdata','plot_threed_azimdegree', 'plot_threed_elevdegree', 'plotlegend_location', 'plotlegend_ncolumn', 'yaxis_ylimthreshold']
        self.mainconfig_strings = ['inputfile_delimeter', 'inputfile_directory', 'inputfile_format', 'inputfile_name', 'outputfigure_format'] # error if empty of nonstring
        self.plotconfig_booleans = ['barsabove', 'cumulative', 'density', 'notched', 'patchartist', 'stacked', 'vertical']
        self.plotconfig_floats = ['bottom', 'capsize', 'capthickness' 'edgewidth', 'width', 'whiskerreach', 'markersize']
        self.plotconfig_integers = ['binres', 'bootstrap']
        ##### PRINT MESSAGES #####

        self.error_filenotexist = f"{Fore.RED} Your input file does not exist!: %s {Fore.WHITE}"
        self.error_outsideboundary = f"{Fore.RED} Following inputs in %s need to defined with their corresponding boundaries: %s \t %s {Fore.WHITE}"
        self.error_wrongtype = f"{Fore.RED} Following inputs in %s must be %s: %s {Fore.WHITE}"
        mainconfig = 'a'

    # =============================== Open main config file
    def openFile(self, file_dir, file_name, file_format):
        full_dir = file_dir + os.sep + file_name + '.' + file_format
        try:
            if file_format == 'csv':
                with open(full_dir, 'r', encoding = self.mainconfig['MAIN']['inputfile_encoder']) as csvfile: 
                    data = []
                    inputData = csv.reader(csvfile, delimiter = self.mainconfig['MAIN']['inputfile_delimeter'])
                    for row in inputData:
                        data.append(row)
            elif file_format == 'yaml':
                with open(full_dir, 'r') as input_data:
                    data = yaml.safe_load(input_data)
        except FileNotFoundError:
            print(self.error_filenotexist %(full_dir))
            return False
        return data

    # =============================== Find the given key in a dictionary
    def findkeys(self, input_dict, input_key):
        # Taken from https://stackoverflow.com/questions/9807634/find-all-occurrences-of-a-key-in-nested-dictionaries-and-lists
        if isinstance(input_dict, list):
            for i in input_dict:
                for x in findkeys(i, input_key):
                    yield x
        elif isinstance(input_dict, dict):
            if input_key in input_dict:
                yield input_dict[input_key]
            for j in input_dict.values():
                for x in self.findkeys(j, input_key):
                    yield x

    # =============================== Check data type of inputs from config files 
    def checkConfig(self, config_name):
        error_vars_bool, error_vars_float, error_vars_int, error_vars_limit, error_vars_limit_name, error_vars_str = [], [], [], [], [], [] 
        
        if config_name == self.mainconfig_name:
            self.inputFile = self.mainconfig['MAIN']['inputfile_name'] + '.' + self.mainconfig['MAIN']['inputfile_format']
            self.inputFileDir = os.listdir(os.getcwd() + os.sep + self.mainconfig['MAIN']['inputfile_directory']) 
        
        try: 
            if config_name == self.mainconfig_name:
                for i in self.mainconfig_booleans:
                    if not isinstance(list(self.findkeys(self.mainconfig, i))[0], bool):
                        error_vars_bool.append(i)
                        raise BoolError
                for i in self.mainconfig_floats:
                    if not isinstance(list(self.findkeys(self.mainconfig, i))[0], float):
                        error_vars_float.append(i)
                        raise FloatError
                for i in self.mainconfig_integers:
                    if not isinstance(list(self.findkeys(self.mainconfig, i))[0], int):
                        error_vars_int.append(i)
                        raise IntError
                cnt = 0
                for i in self.limits_mainconfig_names:
                    cnt += 1
                    if not list(self.findkeys(self.mainconfig, i))[0] in self.limits_mainconfig_sum[cnt]:
                        error_vars_limit.append(self.limits_mainconfig_sum[cnt])
                        error_vars_limit_name.append(i)
                        raise LimitError
                for i in self.mainconfig_strings:
                    if not isinstance(list(self.findkeys(self.mainconfig, i))[0], str):
                        error_vars_str.append(i)
                        raise StrError
                
            if config_name == self.plotconfig_name:
                for i in self.plotconfig_booleans:
                    if not isinstance(list(self.findkeys(self.plotconfig, i))[0], bool):
                        error_vars_bool.append(i)
                        raise BoolError
                for i in self.plotconfig_floats:
                    if not isinstance(list(self.findkeys(self.plotconfig, i))[0], float):
                        error_vars_float.append(i)
                        raise FloatError
                for i in self.plotconfig_integers:
                    if not isinstance(list(self.findkeys(self.plotconfig, i))[0], int):
                        error_vars_int.append(i)
                        raise IntError
                cnt = 0
                for i in self.limits_plotconfig_names:
                    if not list(self.findkeys(self.plotconfig, i))[0] in self.limits_plotconfig_sum[cnt]:
                        error_vars_limit.append(self.limits_plotconfig_sum[cnt])
                        error_vars_limit_name.append(i)
                        raise LimitError

        except BoolError:
            print(self.error_wrongtype %(config_name, 'boolean', error_vars_bool))
            return False
        except FloatError:
            print(self.error_wrongtype %(config_name, 'float', error_vars_bool))
            return False
        except IntError:
            print(self.error_wrongtype %(config_name, 'integer', error_vars_bool))
            return False
        except LimitError:
            print(self.error_outsideboundary %(config_name, error_vars_limit, error_vars_limit_name))
            return False
        except StrError:
            print(self.error_wrongtype %(config_name, 'string', error_vars_bool))
            return False

    # =============================== Incrementer to accept correct values for xmin, xmax and xres in x-axis of function plots
    def adjust_xInput_func(self): 
        self.counter_acceptUserInput += 1
        if self.counter_acceptUserInput == 3:
            self.counter_acceptUserInput = 0
    

    # =============================== Validate input data given by the user
    def checkUserInput(self, input):
        pass
        '''
        errorCode = 0 # to determine which if causes the problem
        if self.processType in ['plotType', 'plotPlotType', 'binResolution', 'checkNumXAxis', 'fetchXAxisColNum', 'numOfPlots']: # prevFuncName[i][3] is 1st prev. function name, prevFuncName[i+1][3] is 2nd most prev. func. name, etc.
            val = float(input)
            if self.processType == 'plotType': # if fetchDataInfo() called, check whether user input is within defined range
                if not (self.minPlotType <= int(input) <= self.maxPlotType):
                    raise ValueError # not correct way to use exception errors
            elif self.processType == 'plotPlotType':
                if not (self.minPlotPlotType <= int(input) <= self.maxPlotPlotType):
                    raise ValueError # not correct way to use exception errors
            elif self.processType == 'checkNumXAxis': 
                if not (self.defaultNumXAxis <= int(input) <= self.maxNumXAxis):
                    raise ValueError # not correct way to use exception errors
            elif self.processType == 'fetchXAxisColNum':
                if not (0 <= val <= self.numData - 1):
                    raise ValueError # not correct way to use exception errors
        elif self.processType == 'fetchInputData':
            if input in ['s', 'S']:
                pass
            elif not self.inputFileFinder(input) is True:
                raise ValueError
        elif self.processType in ['fetchColX', 'fetchColY', 'fetchColZ', 'fetchErrorBar']:
            if self.processType in ['fetchColY', 'fetchColZ', 'fetchErrorBar'] and not input in ['f', 'F']:
                input = int(input)
            if (input in ['f', 'F']) or (self.processType == 'fetchColX' and self.yDataCounter > 0):
                pass
            elif not self.minColNum <= int(input) <= self.numData - 1: 
                raise ValueError
            elif self.processType in ['fetchColY', 'fetchColZ', 'fetchErrorBar'] and (len(self.data[input]) != len(self.data[self.fetchColX[-1]])):
                raise ValueError
        elif (self.processType in ['checkMultiGraph', 'checkMultiXAxis', 'checkThreeDGraph', 'moreData']) and not (input in ['y', 'Y', 'n', 'N']):
            raise ValueError
        elif self.processType == 'getFuncXFromUser':
            val = float(input)
            if self.counter_acceptUserInput == 0: 
                self.x_min = val
            elif self.counter_acceptUserInput == 1:
                if val <= self.x_min: # avoid maximum value of x-axis to be smaller that minimum value of x-axis.
                    return False
            elif self.counter_acceptUserInput == 2 and val <= 0: # avoid resolution value of x-axis to be less or equal than 0.
                return False
            self.adjust_xInput_func()
        elif self.processType in ['getFuncYFromUser', 'getFuncEFromUser']:
            x = np.array(self.data[self.fetchColX[-1]])
            val = eval(input)
        elif self.processType == 'getFuncZFromUser':
            x = np.array(self.data[self.fetchColX[-1]])
            y = np.array(self.data[self.fetchColY[-1]])
            val = eval(input)
    except (AttributeError, SyntaxError, NameError, TypeError, ZeroDivisionError, ValueError):
        return False
    return True
    '''
    
    # =============================== Accept input data given by the user
    def acceptUserInput(self, default):
        while True: 
            userInput = input()
            self.check_quit(userInput)
            if userInput in self.undoCommands: 
                break
            checkedInput = self.checkUserInput(userInput) 
            if userInput == '':
                if self.processType in ['fetchColY', 'fetchColZ', 'fetchErrorBar'] and checkedInput == False:
                    self.printText(self.printFailure, default) # x, y, z data sizes do not match
                elif self.processType in ['getFuncYFromUser', 'getFuncEFromUser']:
                    userInput = np.array(self.data[self.fetchColX[-1]]) ** 2 if self.processType == 'getFuncYFromUser' else np.array(np.random.random_sample(len(self.data[self.fetchColX[-1]])))  # update default Y or errorbar with given x input from user 
                    break
                else:
                    userInput = default
                    if self.processType == 'getFuncXFromUser':
                        if self.counter_acceptUserInput == 0:
                            self.x_min = default
                        elif self.counter_acceptUserInput == 1: 
                            self.x_max = default
                        self.adjust_xInput_func()
                    break
            elif checkedInput is True: # DON'T USE 'checkedInput == True' or 'checkedInput', it will mess up the code. Check this out: https://stackoverflow.com/questions/9494404/use-of-true-false-and-none-as-return-values-in-python-functions
                if (self.processType in ['checkMultiGraph', 'checkMultiXAxis', 'checkThreeDGraph', 'moreData']) and (userInput in ['y', 'Y']):
                    userInput = True
                elif (self.processType in ['checkMultiGraph', 'checkMultiXAxis', 'checkThreeDGraph', 'moreData']) and (userInput in ['n', 'N']):
                    userInput = False
                elif self.processType in ['getFuncXFromUser', 'binResolution', 'checkNumXAxis']:
                    userInput = float(userInput)
                elif self.processType in ['fetchXAxisColNum', 'numOfPlots']:
                    userInput = int(userInput)
                elif self.processType in ['fetchColX', 'fetchColY', 'fetchColZ', 'fetchErrorBar']:
                    if userInput in ['f', 'F']:
                        pass
                    else:
                        userInput = int(userInput)
                elif self.processType in ['getFuncYFromUser', 'getFuncEFromUser']:
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
    def fetchDefLabels(self): 
        # Update default label names if labels are given in the input file
        if not (self.data[0][0].isdigit()): # only check one of the first-row entries. If one of them is not a number, then the other first-row entries should be the same
            for i in range(self.numData):
                self.data[i][0] = self.data[i][0] if self.data[i][0] != '' else 'blank'
                self.defaultLabels.append(self.data[i][0])
            
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
        self.data = self.openFile(
                self.mainconfig['MAIN']['inputfile_directory'], 
                self.mainconfig['MAIN']['inputfile_name'], 
                self.mainconfig['MAIN']['inputfile_format'])
        self.transposeData()
        self.fetchDefLabels()
        self.convDataToFloat()

    # =============================== Main logic
    def main(self):
        # initialize plotFunctions class
        #self.init_plotFunctions()
        # open config file
        self.mainconfig = self.openFile(
                self.config_folderdirectory, 
                self.mainconfig_name, 
                self.config_format)
        self.checkConfig(self.mainconfig_name)

        self.plotconfig = self.openFile(
                self.config_folderdirectory, 
                self.plotconfig_name, 
                self.config_format)
        self.checkConfig(self.plotconfig_name)

        # fetch input data
        self.fetchInputData()
        # logic for plots
        '''
        for i in range(len(self.mainconfig['PLOT'])):
            for j in range(self.check_num_dataset, i):
            #for j in range(len(self.mainconfig['PLOT']['Subplot' + str(i)]) - 34): # TODO Fix -33!!! 34 - 1
                self.plotPyt.mainPlotter(
                        i, 
                        len(self.mainconfig['PLOT']), 
                        self.mainconfig['PLOT']['Subplot' + str(i)]['dataset' + str(j)]['graph_type'], # REMOVE IT 
                        j,
                        self.mainconfig['PLOT']['Subplot' + str(i)]['dataset' + str(j)]['input_xdata'], 
                        self.mainconfig['PLOT']['Subplot' + str(i)]['dataset' + str(j)]['input_ydata'], 
                        self.mainconfig['PLOT']['Subplot' + str(i)]['dataset' + str(j)]['input_zdata'], 
                        self.mainconfig['PLOT']['Subplot' + str(i)]['dataset' + str(j)]['input_edata'], 
                        self.mainconfig['PLOT']['Subplot' + str(i)]['dataset' + str(j)]['plot_legend'], 
                        self.data) # TODO: Why do I send self.numOfPlots???
                self.threeD = True if self.mainconfig['PLOT']['Subplot' + str(i)]['dataset' + str(j)]['graph_type'] == '3d' else False
            self.plotPyt.graphConfigs(
                    self.mainconfig['PLOT']['Subplot' + str(i)]['plot_xlabel'], 
                    self.mainconfig['PLOT']['Subplot' + str(i)]['plot_ylabel'], 
                    self.mainconfig['PLOT']['Subplot' + str(i)]['plot_zlabel'], 
                    self.threeD, self.mainconfig['PLOT']['Subplot' + str(i)]['plot_title'], 
                    len(self.mainconfig['PLOT']), 
                    self.mainconfig['PLOT']['Subplot' + str(i)]['dataset' + str(j)]['graph_type'], 
                    len(self.mainconfig['PLOT']['Subplot' + str(i)]) - 34) # TODO get rid of plotselect, does not make sense
        self.showGraph()
        '''

###################### PLOTTER
class plotPython:
    # =============================== Initializer / Instance attributes
    def __init__(self, data, mainconfig, plotconfig):
        #super().__init__() # inherit all the methods and instances from parent class
        self.colors = ['steelblue', 'sandybrown', 'mediumseagreen', 'indianred', 'dimgrey', 'orchid', 'goldenrod', 'darkcyan', 'mediumslateblue', 'darkkhaki'] # Taken from https://matplotlib.org/3.1.0/gallery/color/named_colors.html
        self.data = data
        self.dataNum = 0
        self.lineTypes = ['-', '--', '-.', '.']
        self.figRowCnt = 0
        self.figColCnt = 0
        self.mainconfig = mainconfig
        self.numOfRow = 0
        self.plotCounter = 0
        self.plotconfig = plotconfig
        self.plotFuncName = ''
        self.oneColSpecPlt = False
        self.guest = []
        self.hostLines, self.hostLabels, self.guestLines, self.guestLabels, self.linesSum, self.labelsSum  = [], [], [], [], [], []
        self.snsJntPlot = None
        self.date = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.fTxtNoXServer = f"""
{Fore.RED}Your X-server is not running, cannot plot the graph.
Please turn on your X-server first and then hit [enter]"""

    # =============================== Check number of dataset for given subplot in main config
    def check_num_dataset(self, subplotnum):
        counter = 0
        for word in self.mainconfig['PLOT']['Subplot' + str(subplotnum)]:
            if re.search('dataset.', word):
                counter += 1
        return counter

    # =============================== Prepare the plot
    def prepPlot(self, numOfPlots):
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
    def axisColoring(self, colorHost, colorGuest):
        # color host
        self.host[self.figColCnt, self.figRowCnt].yaxis.label.set_color(self.colors[colorHost])
        self.host[self.figColCnt, self.figRowCnt].yaxis.label.set_alpha(self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['dataset' + str(0)]['graph_alpha'])
        # color guests     
        self.guest[self.guestPlotCnt - 1].yaxis.label.set_color(self.colors[colorGuest])
        self.guest[self.guestPlotCnt - 1].yaxis.label.set_alpha(self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['graph_alpha'])

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
                if self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['yaxis_on']: 
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
    def barPlot(self, colNumX, colNumY, legendName):
        self.host[self.figColCnt, self.figRowCnt].bar(
                self.data[colNumX], 
                self.data[colNumY], 
                color = self.colors[self.plotconfig['BAR']['Plot' + str(self.plotCounter)]['color']], 
                edgecolor = self.colors[self.plotconfig['BAR']['Plot' + str(self.plotCounter)]['edgecolor']],
                linewidth = self.plotconfig['BAR']['Plot' + str(self.plotCounter)]['edgewidth'], 
                tick_label = self.plotconfig['BAR']['Plot' + str(self.plotCounter)]['label'], 
                capsize = self.plotconfig['BAR']['Plot' + str(self.plotCounter)]['capsize'], 
                width = self.plotconfig['BAR']['Plot' + str(self.plotCounter)]['width'], 
                bottom = self.plotconfig['BAR']['Plot' + str(self.plotCounter)]['bottom'], 
                align = self.plotconfig['BAR']['Plot' + str(self.plotCounter)]['align_bar'], 
                label = legendName[self.dataNum], 
                alpha = self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['graph_alpha']) 

    # =============================== Box graph
    def boxPlot(self, colNumX, legendName):
        self.host[self.figColCnt, self.figRowCnt].boxplot(
                self.data[colNumX], 
                positions = np.array(range(len(self.data[colNumX]))) + 1, 
                boxprops = dict(facecolor = self.colors[self.plotconfig['BOX']['Plot' + str(self.plotCounter)]['boxcolor']], 
                color = self.colors[self.plotconfig['BOX']['Plot' + str(self.plotCounter)]['linecolor']]), 
                capprops = dict(color = self.colors[self.plotconfig['BOX']['Plot' + str(self.plotCounter)]['capcolor']]), 
                whiskerprops = dict(color = self.colors[self.plotconfig['BOX']['Plot' + str(self.plotCounter)]['whiskercolor']]), 
                flierprops = dict(color = self.colors[self.plotconfig['BOX']['Plot' + str(self.plotCounter)]['fliercolor']], 
                markeredgecolor = self.colors[self.plotconfig['BOX']['Plot' + str(self.plotCounter)]['markeredgecolor']]), 
                medianprops = dict(color = self.colors[self.plotconfig['BOX']['Plot' + str(self.plotCounter)]['mediancolor']]), 
                widths = self.plotconfig['BOX']['Plot' + str(self.plotCounter)]['width'], 
                labels = self.plotconfig['BOX']['Plot' + str(self.plotCounter)]['label'], 
                vert = self.plotconfig['BOX']['Plot' + str(self.plotCounter)]['vertical'], 
                notch = self.plotconfig['BOX']['Plot' + str(self.plotCounter)]['notched'], 
                whis = self.plotconfig['BOX']['Plot' + str(self.plotCounter)]['whiskerreach'], 
                bootstrap = self.plotconfig['BOX']['Plot' + str(self.plotCounter)]['bootstrap'], 
                patch_artist = self.plotconfig['BOX']['Plot' + str(self.plotCounter)]['patchartist'], 
                zorder = self.plotconfig['BOX']['Plot' + str(self.plotCounter)]['zorder'])
        self.host[self.figColCnt, self.figRowCnt].set_xticklabels(legendName)

    # =============================== CDF graph
    def cdfPlot(self, colNumX, legendName):
        bin_edges_list = [] 
        cdfData = []
        data_size = len(self.data[colNumX]) # taken from: https://stackoverflow.com/questions/24575869/read-file-and-plot-cdf-in-python
        data_set = sorted(set(self.data[colNumX]))
        bins = np.append(data_set, data_set[-1] + 1)
        counts, bin_edges = np.histogram(self.data[colNumX], bins = bins, density = False) # Use histogram function to bin data
        counts = counts.astype(float) / data_size
        cdfData = np.cumsum(counts)
        self.host[self.figColCnt, self.figRowCnt].plot(
                bin_edges[0:-1], 
                cdfData, 
                self.colors[self.plotconfig['CDF']['Plot' + str(self.plotCounter)]['color']], 
                linewidth = self.plotconfig['CDF']['Plot' + str(self.plotCounter)]['width'], 
                linestyle = self.plotconfig['CDF']['Plot' + str(self.plotCounter)]['style'], 
                marker = self.plotconfig['CDF']['Plot' + str(self.plotCounter)]['markerstyle'], 
                markersize = self.plotconfig['CDF']['Plot' + str(self.plotCounter)]['markersize'], 
                label = legendName[self.dataNum],   
                alpha = self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['graph_alpha'])
        print(self.host[self.figColCnt, self.figRowCnt].legend())

    # =============================== Histogram graph
    def histogramPlot(self, colNumX, legendName):
        self.bins = np.arange(min(self.data[colNumX]) - self.plotconfig['HISTOGRAM']['Plot' + self.plotCounter]['binres'], max(self.data[colNumX]) + self.plotconfig['HISTOGRAM']['Plot' + self.plotCounter]['binres'] * 2, self.plotconfig['HISTOGRAM']['Plot' + self.plotCounter]['binres']) # TODO get rid of this. Only do number of bins
        self.host[self.figColCnt, self.figRowCnt].hist(
                self.data[colNumX], 
                bins = self.bins, 
                color = self.colors[self.plotconfig['HISTOGRAM']['Plot' + self.plotCounter]['color']], 
                edgecolor = self.plotconfig['HISTOGRAM']['Plot' + self.plotCounter]['edgecolor'], 
                histtype = self.plotconfig['HISTOGRAM']['Plot' + self.plotCounter]['type'], 
                density = self.plotconfig['HISTOGRAM']['Plot' + self.plotCounter]['density'], 
                cumulative = self.plotconfig['HISTOGRAM']['Plot' + self.plotCounter]['cumulative'], 
                bottom = self.plotconfig['HISTOGRAM']['Plot' + self.plotCounter]['bottom'], 
                align = self.plotconfig['HISTOGRAM']['Plot' + self.plotCounter]['align_histogram'],
                orientation = self.plotconfig['HISTOGRAM']['Plot' + self.plotCounter]['orientation'], 
                rwidth = self.plotconfig['HISTOGRAM']['Plot' + self.plotCounter]['relativewidth'], 
                stacked = self.plotconfig['HISTOGRAM']['Plot' + self.plotCounter]['stacked'],
                label = legendName[i], 
                alpha = self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['graph_alpha'])  
        self.host[self.figColCnt, self.figRowCnt].set_xticks(self.bins[:-1]) # TODO modify this per ax

    # =============================== Line Plot - Primary y-axis  
    def linePlot_host(self, p, colNumX, colNumY, colNumE, legendName):
        p.append(0) #initialize array entry
        p[self.guestPlotCnt], = self.host[self.figColCnt, self.figRowCnt].plot(
                self.data[colNumX], 
                self.data[colNumY], 
                self.colors[self.plotconfig['LINE']['Plot' + str(self.plotCounter)]['color']], 
                linewidth = self.plotconfig['LINE']['Plot' + str(self.plotCounter)]['width'], 
                linestyle = self.plotconfig['LINE']['Plot' + str(self.plotCounter)]['style'], 
                marker = self.plotconfig['LINE']['Plot' + str(self.plotCounter)]['markerstyle'], 
                markersize = self.plotconfig['LINE']['Plot' + str(self.plotCounter)]['markersize'],  
                label = legendName[self.dataNum], 
                alpha = self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['graph_alpha'])

    # =============================== Line Plot - Additional y-axes
    def linePlot_guest(self, p, colNumX, colNumY, colNumE, legendName):
        p.append(0) #initialize array entry
        self.guest.append(0) #initialize array entry
        self.guest[self.guestPlotCnt] = self.host[self.figColCnt, self.figRowCnt].twinx() # setup 2nd axis based on the first graph
        p[self.guestPlotCnt], = self.guest[self.guestPlotCnt].plot(
                self.data[colNumX], 
                self.data[colNumY], 
                self.colors[self.plotconfig['LINE']['Plot' + str(self.plotCounter)]['color']], 
                linewidth = self.plotconfig['LINE']['Plot' + str(self.plotCounter)]['width'], 
                linestyle = self.plotconfig['LINE']['Plot' + str(self.plotCounter)]['style'], 
                marker = self.plotconfig['LINE']['Plot' + str(self.plotCounter)]['markerstyle'], 
                markersize = self.plotconfig['LINE']['Plot' + str(self.plotCounter)]['markersize'],  
                label = legendName[i], 
                kwargs = {'alpha': self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['graph_alpha']})
        self.guest[self.guestPlotCnt].set_ylim(min(self.data[colNumY]) - self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['yaxis_ylimthreshold'], max(self.data[colNumY]) + self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['yaxis_ylimthreshold'])
        self.guest[self.guestPlotCnt].grid(False)
        self.guest[self.guestPlotCnt].spines['right'].set_position(("axes", self.axisOffset)) 
        lines, labels = self.guest[self.guestPlotCnt].get_legend_handles_labels()
        return lines, labels

    # =============================== Line-type graphs
    def linePlot(self, colNumX, colNumY, colNumE, legendName):
        p = []
        if self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['multipleyaxis']: # multiple-axis enabled
            if self.dataNum == 0:
                self.linePlot_host(p, colNumX, 
                        colNumY, colNumE, legendName)
            else:
                if self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['yaxis_on']:
                    lines, labels = self.linePlot_guest(self.dataNum, p, colNumX,
                            colNumY, colNumE, legendName)
                    self.guestLines += lines
                    self.guestLabels += labels
                    self.guestPlotCnt += 1
                    self.axisOffset += self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['yaxis_axisoffset']
                else:
                    self.linePlot_host(p, colNumX, colNumY, colNumE, 
                            legendName)
            self.hostLines, self.hostLabels = self.host[self.figColCnt, self.figRowCnt].get_legend_handles_labels()
            self.linesSum = self.hostLines + self.guestLines
            self.labelsSum = self.hostLabels + self.guestLabels
            if self.guestPlotCnt > 0: self.guest[self.guestPlotCnt - 1].legend(self.linesSum, self.labelsSum)
            if self.guestPlotCnt == self.dataNum - 1: self.axisColoring(self.plotconfig['LINE']['Plot' + str(0)]['color'], self.plotconfig['LINE']['Plot' + str(self.dataNum)]['color']) # color the axes iff each line has a y-axis
        else:
            self.linePlot_host(p, colNumX, 
                        colNumY, colNumE, legendName)

    # =============================== Errorbar Plot - Primary y-axis  
    def errorbarPlot_host(self, p, colNumX, colNumY, colNumE, legendName):
        p.append(0) #initialize array entry
        p[self.guestPlotCnt], = self.host[self.figColCnt, self.figRowCnt].errorbar(self.data[colNumX], self.data[colNumY], 
                yerr = self.data[colNumE], ecolor = self.colors[self.plotconfig['ERRORBAR']['Plot' + self.plotCounter]['color']], 
                elinewidth = self.plotconfig['ERRORBAR']['Plot' + self.plotCounter]['width'], 
                fmt = self.plotconfig['ERRORBAR']['Plot' + self.plotCounter]['style'], 
                capsize = self.plotconfig['ERRORBAR']['Plot' + self.plotCounter]['capsize'], 
                capthick = self.plotconfig['ERRORBAR']['Plot' + self.plotCounter]['capthickness'],  
                barsabove = self.plotconfig['ERRORBAR']['Plot' + self.plotCounter]['barsabove'], 
                label = legendName[self.dataNum], 
                kwargs = {'alpha': self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['graph_alpha']})

    # =============================== Errorbar Plot - Additional y-axes
    def errorbarPlot_guest(self, p, colNumX, colNumY, colNumE, legendName):
        p.append(0) #initialize array entry
        self.guest.append(0) #initialize array entry
        self.guest[self.guestPlotCnt] = self.host[self.figColCnt, self.figRowCnt].twinx() # setup 2nd axis based on the first graph
        p[self.guestPlotCnt], = self.guest[self.guestPlotCnt].errorbar(self.data[colNumX], self.data[colNumY], 
                yerr = self.data[colNumE], ecolor = self.colors[self.plotconfig['ERRORBAR']['Plot' + self.plotCounter]['color']], 
                elinewidth = self.plotconfig['ERRORBAR']['Plot' + self.plotCounter]['width'], 
                fmt = self.plotconfig['ERRORBAR']['Plot' + self.plotCounter]['style'], 
                capsize = self.plotconfig['ERRORBAR']['Plot' + self.plotCounter]['capsize'], 
                capthick = self.plotconfig['ERRORBAR']['Plot' + self.plotCounter]['capthickness'],  
                barsabove = self.plotconfig['ERRORBAR']['Plot' + self.plotCounter]['barabove'], 
                label = legendName[self.dataNum], 
                kwargs = {'alpha': self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['graph_alpha']})
        self.guest[self.guestPlotCnt].set_ylim(min(self.data[colNumY]) - self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['yaxis_ylimthreshold'], max(self.data[colNumY]) + self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['yaxis_ylimthreshold'])
        self.guest[self.guestPlotCnt].grid(False)
        self.guest[self.guestPlotCnt].spines['right'].set_position(("axes", self.axisOffset)) 
        lines, labels = self.guest[self.guestPlotCnt].get_legend_handles_labels()
        return lines, labels

    # =============================== Errorbar-type graphs
    def errorbarPlot(self, colNumX, colNumY, colNumE, legendName):
        p = []
        if self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['multipleyaxis']: # multiple-axis enabled
            if dataNum == 0:
                self.errorbarPlot_host(p, colNumX, 
                        colNumY, colNumE, legendName)
            else:
                if self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['dataset' + str(dataNum)]['yaxis_on']:
                    lines, labels = self.errorbarPlot_guest(p, colNumX,
                            colNumY, colNumE, legendName)
                    self.guestLines += lines
                    self.guestLabels += labels
                    self.guestPlotCnt += 1
                    self.axisOffset += self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['dataset' + str(dataNum)]['yaxis_axisoffset']
                else:
                    self.errorbarPlot_host(p, colNumX, colNumY, colNumE, legendName)
            self.hostLines, self.hostLabels = self.host[self.figColCnt, self.figRowCnt].get_legend_handles_labels()
            self.linesSum = self.hostLines + self.guestLines
            self.labelsSum = self.hostLabels + self.guestLabels
            if self.guestPlotCnt > 0: self.guest[self.guestPlotCnt - 1].legend(self.linesSum, self.labelsSum)
            if self.guestPlotCnt == dataNum - 1: self.axisColoring(dataNum, self.plotconfig['LINE']['Plot' + str(0)]['color'], self.plotconfig['LINE']['Plot' + str(dataNum)]['color']) # color the axes iff each line has a y-axis
        else:
            self.errorbarPlot_host(p, colNumX, 
                        colNumY, colNumE, legendName)
                    
    # =============================== 3D graph
    def threeDPlot(self, numOfPlots, plotSelect, colNumX, colNumY, colNumZ, legendName):
        self.host[self.figColCnt, self.figRowCnt].axis('off')
        numOfRow = 2 if numOfPlots > 1 else 1
        self.host[self.figColCnt, self.figRowCnt] = self.fig.add_subplot(math.ceil(numOfPlots / numOfRow), numOfRow, self.plotCounter + 1, projection = '3d') # TODO move this to prepplot()
        for i in range(self.dataNum):
            self.host[self.figColCnt, self.figRowCnt].plot(
                    self.data[colNumX], 
                    self.data[colNumY], 
                    self.data[colNumZ], 
                    self.colors[self.plotconfig['THREED']['Plot' + self.plotCounter]['color']], 
                    linewidth = self.plotconfig['THREED']['Plot' + self.plotCounter]['width'], 
                    linestyle = self.plotconfig['THREED']['Plot' + self.plotCounter]['style'], 
                    marker = self.plotconfig['THREED']['Plot' + self.plotCounter]['markerstyle'], 
                    markersize = self.plotconfig['THREED']['Plot' + self.plotCounter]['markersize'],
                    label = legendName[i], 
                    alpha = self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['graph_alpha'])

    # =============================== Seaborn Line Graph - Primary y-axis
    def seabornLinePlot_host(self, colNumX, colNumY, legendName):
        sns.lineplot(x = self.data[colNumX], y = self.data[colNumY], 
                color = self.colors[self.plotconfig['SNSLINE']['Plot' + self.plotCounter]['color']], 
                linewidth = self.plotconfig['SNSLINE']['Plot' + self.plotCounter]['width'], 
                marker = self.plotconfig['SNSLINE']['Plot' + self.plotCounter]['markerstyle'],
                markersize = self.plotconfig['SNSLINE']['Plot' + self.plotCounter]['markersize'], 
                hue = self.plotconfig['SNSLINE']['Plot' + self.plotCounter]['hue'], 
                size = self.plotconfig['SNSLINE']['Plot' + self.plotCounter]['size'], 
                style = self.plotconfig['SNSLINE']['Plot' + self.plotCounter]['sns_style'], 
                label = legendName[i], alpha = self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['graph_alpha'],
                ax = self.host[self.figColCnt, self.figRowCnt]) 
        self.host[self.figColCnt, self.figRowCnt].lines[self.dataNum].set_linestyle(self.plotconfig['SNSLINE']['Plot' + self.plotCounter]['style'])
        self.host[self.figColCnt, self.figRowCnt].legend_.remove()

    # =============================== Seaborn Line Graph - Primary y-axis when used with guest plot
    def seabornLinePlot_host_withGuest(self, colNumX, colNumY, legendName):
        self.seabornLinePlot_host(colNumX,
                            colNumY, legendName, self.data)
        lines, labels = self.host[self.figColCnt, self.figRowCnt].get_legend_handles_labels()
        self.hostLines += lines
        self.hostLabels += labels

    # =============================== Seaborn Line Graph - Additional y-axes
    def seabornLinePlot_guest(self, colNumX, colNumY, legendName):
        self.guest.append(0) # initialize array entry
        self.guest[self.guestPlotCnt] = self.host[self.figColCnt, self.figRowCnt].twinx() # setup 2nd axis based on the first graph
        sns.lineplot(x = self.data[colNumX], y = self.data[colNumY], 
                color = self.colors[self.snsline_color.split(self.config_separator)[i % len(self.snsline_color.split(self.config_separator))]], 
                linewidth = self.plotconfig['SNSLINE']['Plot' + self.plotCounter]['width'], 
                marker = self.plotconfig['SNSLINE']['Plot' + self.plotCounter]['markerstyle'],
                markersize = self.plotconfig['SNSLINE']['Plot' + self.plotCounter]['markersize'], 
                hue = self.plotconfig['SNSLINE']['Plot' + self.plotCounter]['hue'], 
                size = self.plotconfig['SNSLINE']['Plot' + self.plotCounter]['size'], 
                style = self.plotconfig['SNSLINE']['Plot' + self.plotCounter]['sns_style'], 
                label = legendName[i], alpha = self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['graph_alpha'],
                ax = self.guest[self.guestPlotCnt]) 
        self.guest[self.guestPlotCnt].lines[0].set_linestyle(self.plotconfig['SNSLINE']['Plot' + self.plotCounter]['style'])
        self.guest[self.guestPlotCnt].set_ylim(min(self.data[colNumY]) - self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['yaxis_ylimthreshold'], max(self.data[colNumY]) + self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['yaxis_ylimthreshold'])
        self.guest[self.guestPlotCnt].grid(False)
        self.guest[self.guestPlotCnt].legend_.remove()
        self.guest[self.guestPlotCnt].spines['right'].set_position(("axes", self.axisOffset))
        lines, labels = self.guest[self.guestPlotCnt].get_legend_handles_labels()
        self.linesSum += lines
        self.labelsSum += labels
        self.guestPlotCnt += 1
        self.axisOffset += self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['yaxis_axisoffset']

    # =============================== Seaborn Line Graph
    def seabornLinePlot(self, colNumX, colNumY, legendName):
        if self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['multipleyaxis']: # multiple-axis enabled
            if self.dataNum == 0:
                self.seabornLinePlot_host_withGuest(colNumX,
                            colNumY, legendName)
            else:
                if self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['yaxis_on']:
                    self.seabornLinePlot_guest(colNumX,
                            colNumY, legendName)
                else:
                    self.seabornLinePlot_host_withGuest(colNumX,
                            colNumY, legendName)
            if any(self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['yaxis_on']) and self.guestPlotCnt > 0: self.axisColoring(self.dataNum, self.snsline_color.split(self.config_separator)[0], self.snsline_color.split(self.config_separator)[self.dataNum]) # TODO find a solution instead of any() color the axes iff each line has a y-axis
        else:
            self.seabornLinePlot_host(colNumX,
                    colNumY, legendName)

    # =============================== Seaborn Joint Graph
    def seabornJointPlot(self, colNumX, colNumY, legendName):
        sns.jointplot(
                x = self.data[colNumX], 
                y = self.data[colNumY], 
                kind = self.plotconfig['SNSJOINT']['Plot' + self.plotCounter]['kind'], 
                color = self.colors[self.plotconfig['SNSJOINT']['Plot' + self.plotCounter]['color']], 
                label = legendName[i])

    # =============================== Plotter function
    def mainPlotter(self, plotCounter, numOfPlots, plotSelect, dataNum, colNumX, colNumY, colNumZ, colNumE, legendName):
        self.plotCounter = plotCounter
        self.dataNum = dataNum

        if self.dataNum == 0:
            self.guestPlotCnt = 0
            self.axisOffset = 1
        # Main if clause for plots
        if plotSelect == 'bar':
            self.barPlot(colNumX, colNumY, legendName)
        elif plotSelect == 'box':
            self.boxPlot(colNumX, legendName)
        elif plotSelect == 'cdf':
            self.cdfPlot(colNumX, legendName)
        elif plotSelect == 'histogram':
            self.histogramPlot(colNumX, legendName)
        elif plotSelect in 'line':
            self.linePlot(colNumX, colNumY, colNumE, legendName)
        elif plotSelect in 'errorbar':
            self.errorbarPlot(colNumX, colNumY, colNumE, legendName)
        elif plotSelect == '3d':
            self.threeDPlot(numOfPlots, plotSelect, colNumX, colNumY, colNumZ, legendName)
        elif plotSelect == 'seaborn line':
            self.seabornLinePlot(colNumX, colNumY, legendName)
        elif plotSelect == 'seaborn jointplot':
            self.seabornJointPlot(colNumX, colNumY, legendName)  

    # =============================== Main function
    def main(self):
        # prepare the plot environment
        self.prepPlot(len(self.mainconfig['PLOT'])) 

        # logic for subplot generation
        for i in range(len(self.mainconfig['PLOT'])):
            for j in range(self.check_num_dataset(i)):
            #for j in range(len(self.mainconfig['PLOT']['Subplot' + str(i)]) - 34): # TODO Fix -33!!! 34 - 1
                self.mainPlotter(
                        i, 
                        len(self.mainconfig['PLOT']), 
                        self.mainconfig['PLOT']['Subplot' + str(i)]['dataset' + str(j)]['graph_type'], # REMOVE IT 
                        j,
                        self.mainconfig['PLOT']['Subplot' + str(i)]['dataset' + str(j)]['input_xdata'], 
                        self.mainconfig['PLOT']['Subplot' + str(i)]['dataset' + str(j)]['input_ydata'], 
                        self.mainconfig['PLOT']['Subplot' + str(i)]['dataset' + str(j)]['input_zdata'], 
                        self.mainconfig['PLOT']['Subplot' + str(i)]['dataset' + str(j)]['input_edata'], 
                        self.mainconfig['PLOT']['Subplot' + str(i)]['dataset' + str(j)]['plot_legend']) # TODO: Why do I send self.numOfPlots???
                self.threeD = True if self.mainconfig['PLOT']['Subplot' + str(i)]['dataset' + str(j)]['graph_type'] == '3d' else False
            self.graphConfigs(
                    self.mainconfig['PLOT']['Subplot' + str(i)]['plot_xlabel'], 
                    self.mainconfig['PLOT']['Subplot' + str(i)]['plot_ylabel'], 
                    self.mainconfig['PLOT']['Subplot' + str(i)]['plot_zlabel'], 
                    self.threeD, self.mainconfig['PLOT']['Subplot' + str(i)]['plot_title'], 
                    len(self.mainconfig['PLOT']), 
                    self.mainconfig['PLOT']['Subplot' + str(i)]['dataset' + str(j)]['graph_type'], 
                    self.check_num_dataset(i)) # TODO get rid of plotselect, does not make sense
        self.showPlot(self.mainconfig['MAIN']['figure_title'], len(self.mainconfig['PLOT']))

class BoolError(Exception):
    """Exception raised for errors in the input.

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self):
        pass
        #self.expression = expression
        #self.message = message

class FloatError(Exception):
    def __init__(self):
        pass
        #self.expression = expression
        #self.message = message

class IntError(Exception):
    def __init__(self):
        pass
        #self.expression = expression
        #self.message = message

class LimitError(Exception):
    def __init__(self):
        pass
        #self.expression = expression
        #self.message = message

class StrError(Exception):
    def __init__(self):
        pass
        #self.expression = expression
        #self.message = message

task = autoPylot()
task.main() # Fetch self.data-related info from user
plot = plotPython(task.data, task.mainconfig, task.plotconfig)
plot.main()