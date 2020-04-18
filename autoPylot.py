#!/usr/bin/env python3

import os
import sys
import math
from colorama import Fore, Back, init # colored output on the terminal
from datetime import datetime
import pandas as pd
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
        self.error_filenotexist = f"{Fore.RED} Your input file does not exist!: %s {Fore.WHITE}"
        self.error_invalidFunc = f"{Fore.RED} Your function for %s is invalid. Please enter a valid function from numpy (np.*) or math (math.*) libraries. {Fore.WHITE}"
        self.error_outsideboundary = f"{Fore.RED} Following inputs in %s need to defined with their corresponding boundaries: Input: %s \t Valid range: %s {Fore.WHITE}"
        self.error_wrongtype = f"{Fore.RED} Following inputs in %s must be %s: %s {Fore.WHITE}"
        self.inputFile = '' 
        self.inputFileDir = '' 
        self.limits_data_columns = ['input_edata', 'input_xdata', 'input_ydata', 'input_zdata']
        self.limits_mainconfig_graph_alpha = np.arange(0, 1, 0.00001)
        self.limits_mainconfig_graph_type = ['bar', 'box', 'cdf', 'errorbar', 'histogram', 'line', 'seaborn line', 'seaborn joint']
        self.limits_mainconfig_inputfile_format = ['csv']
        self.limits_mainconfig_inputfile_encoder = ['ascii', 'utf-7' 'utf-8', 'utf-8-sig', 'utf-16', 'utf-16-be', 'utf-16-le', 'utf-32', 'utf-32-be', 'utf-32-le'] # from https://docs.python.org/3/library/codecs.html#standard-encodings
        self.limits_mainconfig_legend_location = np.arange(0, 10, 1)
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
        self.limits_plotconfig_names = ['align_bar', 'align_histogram', 'color', 'markerstyle', 'orientation', 'kind', 'style', 'type']
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
        self.mainconfig_integers = ['figurelegend_location', 'figurelegend_ncolumn', 'figure_plotperrow', 'plot_threed_azimdegree', 'plot_threed_elevdegree', 
                'plotlegend_location', 'plotlegend_ncolumn', 'yaxis_ylimthreshold']
        self.mainconfig_strings = ['inputfile_delimeter', 'inputfile_directory', 'inputfile_format', 'inputfile_name', 'outputfigure_format'] # error if empty of nonstring
        self.plotconfig_booleans = ['barsabove', 'cumulative', 'density', 'notched', 'patchartist', 'stacked', 'vertical']
        self.plotconfig_floats = ['bottom', 'capsize', 'capthickness', 'edgewidth', 'width', 'whiskerreach', 'markersize', 'position']
        self.plotconfig_integers = ['binres', 'bootstrap']
        
    # =============================== Check number of dataset for given subplot in main config
    def check_num_dataset(self, subplotnum):
        counter = 0
        for word in self.mainconfig['PLOT']['Subplot' + str(subplotnum)]:
            if re.search('dataset.', word):
                counter += 1
        return counter

    # =============================== Open main config file
    def readFile(self, file_dir, file_name, file_format):
        full_dir = file_dir + os.sep + file_name + '.' + file_format
        try:
            if file_format == 'csv':
                with open(full_dir, 'r', encoding = self.mainconfig['MAIN']['inputfile_encoder']) as csvfile: 
                    data = []
                    inputData = csv.reader(csvfile, delimiter = self.mainconfig['MAIN']['inputfile_delimeter'])
                    for row in inputData:
                        data.append(row)
            elif file_format == 'yaml':
                with open(full_dir, 'r') as input_file:
                    data = yaml.safe_load(input_file)
        except FileNotFoundError:
            print(self.error_filenotexist %(full_dir))
            return False
        return data

    # =============================== Append function data to csv files
    def update_input_file(self, data_header, data_write):
        data = self.readFile(
                self.mainconfig['MAIN']['inputfile_directory'], 
                self.mainconfig['MAIN']['inputfile_name'], 
                self.mainconfig['MAIN']['inputfile_format'])

        with open(self.mainconfig['MAIN']['inputfile_directory'] + os.sep + self.mainconfig['MAIN']['inputfile_name'] + '.' + self.mainconfig['MAIN']['inputfile_format'], 'w', newline = '') as write_obj:
            csv_writer = csv.writer(write_obj)
            cnt = 0
            data_write = list(data_write)
            data_write.insert(0, data_header)
            cnt = 0

            if len(data) >= len(data_write):
                for row in data:
                    data_to_csv = []
                    if cnt < len(data_write):
                        for i in range(len(row)):
                            data_to_csv.append(row[i])
                        data_to_csv.append(data_write[cnt])
                        csv_writer.writerow(data_to_csv)
                        cnt += 1
                        data_col_num = len(data_to_csv) - 1
                    else:
                        csv_writer.writerow(row)
            else:
                for row in data_write:
                    data_to_csv = []
                    if cnt < len(data):
                        for i in range(len(data[cnt])):
                            data_to_csv.append(data[cnt][i])
                        data_to_csv.append(row)
                        csv_writer.writerow(data_to_csv)
                    else:
                        for i in range(len(data[0])):
                            data_to_csv.append(None)
                        data_to_csv.append(row)
                        csv_writer.writerow(data_to_csv)
                    data_col_num = len(data_to_csv) - 1
                    cnt += 1
          
        return data_col_num 
        
    # =============================== Update function inputs to corresponding column number in csv
    def update_mainconfig(self, value, column_number):
        for i in range(len(self.mainconfig['PLOT'])):
            for j in range(self.check_num_dataset(i)):
                for k in self.mainconfig['PLOT']['Subplot' + str(i)]['dataset' + str(j)]:
                    if self.mainconfig['PLOT']['Subplot' + str(i)]['dataset' + str(j)][k] == value:
                        self.mainconfig['PLOT']['Subplot' + str(i)]['dataset' + str(j)][k] = column_number

        with open(self.config_folderdirectory + os.sep + self.mainconfig_name + '.' + self.config_format, 'w') as outfile:
            yaml.dump(self.mainconfig, outfile, default_flow_style = False)

    # =============================== Find the given key in a dictionary
    def findkeys(self, input_dict, input_key):
        # Taken from https://stackoverflow.com/questions/9807634/find-all-occurrences-of-a-key-in-nested-dictionaries-and-lists
        if isinstance(input_dict, list):
            for i in input_dict:
                for x in self.findkeys(i, input_key):
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
                    for j in range(len(list(self.findkeys(self.mainconfig, i)))):
                        if not isinstance(list(self.findkeys(self.mainconfig, i))[j], bool):
                            error_vars_bool.append(i)
                            raise BoolError
                for i in self.mainconfig_floats:
                    for j in range(len(list(self.findkeys(self.mainconfig, i)))):
                        if not isinstance(list(self.findkeys(self.mainconfig, i))[j], float) and not isinstance(list(self.findkeys(self.mainconfig, i))[j], int) and not list(self.findkeys(self.mainconfig, i))[j] is None:
                            error_vars_float.append(i)
                            raise FloatError
                for i in self.mainconfig_integers:
                    for j in range(len(list(self.findkeys(self.mainconfig, i)))):
                        if not isinstance(list(self.findkeys(self.mainconfig, i))[j], int) and not list(self.findkeys(self.mainconfig, i))[j] is None:
                            error_vars_int.append(i)
                            raise IntError
                cnt = 0
                for i in self.limits_mainconfig_names:
                    for j in range(len(list(self.findkeys(self.mainconfig, i)))):
                        if not list(self.findkeys(self.mainconfig, i))[j] in self.limits_mainconfig_sum[cnt]:
                            error_vars_limit.append(self.limits_mainconfig_sum[cnt])
                            error_vars_limit_name.append(i)
                            raise LimitError
                    cnt += 1

                for i in self.limits_data_columns:
                    limit = np.arange(0, self.numData)
                    for j in range(len(list(self.findkeys(self.mainconfig, i)))):
                        if type(list(self.findkeys(self.mainconfig, i))[j]) is str:
                            if i == 'input_xdata':
                                data_x = eval(list(self.findkeys(self.mainconfig, i))[j])
                                self.data.append(data_x) # TODO, add function inputs, add len check for x-y-z data, functionirize check_config()
                                self.numData = len(self.data)
                                column_number_x = self.update_input_file(list(self.findkeys(self.mainconfig, i))[j], data_x)
                                self.update_mainconfig(list(self.findkeys(self.mainconfig, i))[j], column_number_x)
                            elif i == 'input_ydata':
                                x = data_x
                                data_y = eval(list(self.findkeys(self.mainconfig, i))[j])
                                self.data.append(data_y) # TODO, add function inputs, add len check for x-y-z data, functionirize check_config()
                                self.numData = len(self.data)
                                column_number_y = self.update_input_file(list(self.findkeys(self.mainconfig, i))[j], data_y)
                                self.update_mainconfig(list(self.findkeys(self.mainconfig, i))[j], column_number_y)
                            elif i == 'input_zdata':
                                x = data_x
                                y = data_y
                                data_z = eval(list(self.findkeys(self.mainconfig, i))[j])
                                self.data.append(data_z) # TODO, add function inputs, add len check for x-y-z data, functionirize check_config()
                                self.numData = len(self.data)
                                column_number_z = self.update_input_file(list(self.findkeys(self.mainconfig, i))[j], data_z)
                                self.update_mainconfig(list(self.findkeys(self.mainconfig, i))[j], column_number_z)
                        elif type(list(self.findkeys(self.mainconfig, i))[j]) is list:
                            for item in list(self.findkeys(self.mainconfig, i))[j]:
                                if not item in limit and not item is None:
                                    error_vars_limit.append(limit)
                                    error_vars_limit_name.append(i)
                                    raise LimitError
                        elif not list(self.findkeys(self.mainconfig, i))[j] in limit and not list(self.findkeys(self.mainconfig, i))[j] is None: # -1 since column numbers start from 0
                            error_vars_limit.append(limit)
                            error_vars_limit_name.append(i)
                            raise LimitError

                for i in self.mainconfig_strings:
                    for j in range(len(list(self.findkeys(self.mainconfig, i)))):
                        if not isinstance(list(self.findkeys(self.mainconfig, i))[j], str):
                            error_vars_str.append(i)
                            raise StrError
                
            if config_name == self.plotconfig_name:
                for i in self.plotconfig_booleans:
                    for j in range(len(list(self.findkeys(self.mainconfig, i)))):
                        if not isinstance(list(self.findkeys(self.plotconfig, i))[j], bool):
                            error_vars_bool.append(i)
                            raise BoolError
                for i in self.plotconfig_floats:
                    for j in range(len(list(self.findkeys(self.mainconfig, i)))):
                        if not isinstance(list(self.findkeys(self.plotconfig, i))[j], float) and not isinstance(list(self.findkeys(self.plotconfig, i))[j], int) and not list(self.findkeys(self.plotconfig, i))[j] is None:
                            error_vars_float.append(i)
                            raise FloatError
                for i in self.plotconfig_integers:
                    for j in range(len(list(self.findkeys(self.mainconfig, i)))):
                        if not isinstance(list(self.findkeys(self.plotconfig, i))[j], int) and not list(self.findkeys(self.plotconfig, i))[j] is None:
                            error_vars_int.append(i)
                            raise IntError
                cnt = 0
                for i in self.limits_plotconfig_names:
                    for j in range(len(list(self.findkeys(self.mainconfig, i)))):
                        if not list(self.findkeys(self.plotconfig, i))[j] in self.limits_plotconfig_sum[cnt]:
                            error_vars_limit.append(self.limits_plotconfig_sum[cnt])
                            error_vars_limit_name.append(i)
                            raise LimitError
                    cnt += 1

        except BoolError:
            print(self.error_wrongtype %(config_name, 'boolean', error_vars_bool))
            return False
        except FloatError:
            print(self.error_wrongtype %(config_name, 'float', error_vars_float))
            return False
        except IntError:
            print(self.error_wrongtype %(config_name, 'integer', error_vars_int))
            return False
        except LimitError:
            print(self.error_outsideboundary %(config_name, error_vars_limit_name, error_vars_limit))
            return False
        except ValueError:
            print(self.error_outsideboundary %(config_name, error_vars_limit_name, error_vars_limit))
            return False
        except StrError:
            print(self.error_wrongtype %(config_name, 'string', error_vars_bool))
            return False
        return True

    # =============================== Incrementer to accept correct values for xmin, xmax and xres in x-axis of function plots
    def adjust_xInput_func(self): 
        self.counter_acceptUserInput += 1
        if self.counter_acceptUserInput == 3:
            self.counter_acceptUserInput = 0
    
    # =============================== Convert rows to cols in input data from csv
    def transpose_list(self, data):
        data = list(map(list, zip(*data))) # transpose the self.data: rows -> columns
        return data

    # =============================== Fetch default label names from csv file
    def fetchDefLabels(self): 
        self.numData = len(self.data)
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
        self.data = self.readFile(
                self.mainconfig['MAIN']['inputfile_directory'], 
                self.mainconfig['MAIN']['inputfile_name'], 
                self.mainconfig['MAIN']['inputfile_format'])
        self.numData = len(self.data)

    # =============================== Main logic
    def main(self):
        # open main config file
        self.mainconfig = self.readFile(
                self.config_folderdirectory, 
                self.mainconfig_name, 
                self.config_format)

        # fetch input data
        self.fetchInputData()
        self.data = self.transpose_list(self.data)
        self.fetchDefLabels()
        self.convDataToFloat()

        # open plot config file
        self.plotconfig = self.readFile(
                self.config_folderdirectory, 
                self.plotconfig_name, 
                self.config_format)
        
        # validate the inputs of config files
        check_mainconfig = self.checkConfig(self.mainconfig_name)
        if not self.checkConfig(self.plotconfig_name) or not check_mainconfig: sys.exit(0)

###################### PLOTTER
class plotPython:
    # =============================== Initializer / Instance attributes
    def __init__(self, data, mainconfig, plotconfig):
        #super().__init__() # inherit all the methods and instances from parent class
        self.boxplot_data = []
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

    # =============================== Color the axes for multi-y axes (seaborn) line plots
    def axisColoring(self, colorHost, colorGuest):
        # color host
        self.host[self.figColCnt, self.figRowCnt].yaxis.label.set_color(self.colors[colorHost])
        self.host[self.figColCnt, self.figRowCnt].yaxis.label.set_alpha(self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['dataset' + str(0)]['graph_alpha'])
        # color guests     
        self.guest[self.guestPlotCnt - 1].yaxis.label.set_color(self.colors[colorGuest])
        self.guest[self.guestPlotCnt - 1].yaxis.label.set_alpha(self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['graph_alpha'])

    # =============================== Check number of dataset for given subplot in main config
    def check_num_dataset(self, subplotnum):
        counter = 0
        for word in self.mainconfig['PLOT']['Subplot' + str(subplotnum)]:
            if re.search('dataset.', word):
                counter += 1
        return counter
    
    # =============================== Graph Configurations
    def graphConfigs(self, xLabel, yLabel, zLabel, threeD, title, numOfPlots, numData):
        if not self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['graph_type'] in {'box'}:
            self.set_axis_label_scale(threeD)
        if threeD: 
            self.set_azim_elev()
        self.set_axis_limit(threeD)
        self.set_axis_tick(threeD)
        self.set_axis_label(numData, threeD, xLabel, yLabel, zLabel)
        self.set_axis_label_pad(threeD)
        self.set_subtitle(numOfPlots, title)
        self.set_plot_legend()
        self.set_snsjoint_setting(title)
        self.place_subplot()
    
    # =============================== logic to place subplots in the right location
    def place_subplot(self):
        if not self.oneColSpecPlt:
            if (self.plotCounter + 1) % self.numOfRow == 0:
                self.figColCnt += 1
                self.figRowCnt -= (self.numOfRow - 1)
            else:
                self.figRowCnt += 1
        else:
            self.figColCnt += 1

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
        plt.close()
    
    # =============================== save figure
    def save_figure(self):
            self.fig.savefig(
            '%s' %self.mainconfig['MAIN']['outputfigure_directory'] + os.sep + 
            '%s.%s' %(self.date, self.mainconfig['MAIN']['outputfigure_format']), 
            bbox_inches = 'tight', format = self.mainconfig['MAIN']['outputfigure_format'])
    
    # =============================== set axis labels
    def set_axis_label(self, numData, threeD, xLabel, yLabel, zLabel):
        self.host[self.figColCnt, self.figRowCnt].set_xlabel(xLabel)
        self.host[self.figColCnt, self.figRowCnt].set_ylabel(yLabel[0])
        if self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['multipleyaxis']:# and plotSelect in ['line', 'seaborn line']:
            guestCnt = 0
            for i in range(numData - 1):
                if self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['yaxis_on']: 
                    self.guest[guestCnt].set_ylabel(yLabel[i + 1])
                    guestCnt += 1
        if threeD: self.host[self.figColCnt, self.figRowCnt].set_zlabel(zLabel)

    # =============================== set axis label paddings
    def set_axis_label_pad(self, threeD):
        self.host[self.figColCnt, self.figRowCnt].axes.xaxis.labelpad = self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['plot_xlabel_pad']
        self.host[self.figColCnt, self.figRowCnt].axes.yaxis.labelpad = self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['plot_ylabel_pad']
        if threeD: self.host[self.figColCnt, self.figRowCnt].axes.zaxis.labelpad = self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['plot_zlabel_pad']

    # =============================== set label scales
    def set_axis_label_scale(self, threeD):
        self.host[self.figColCnt, self.figRowCnt].set_xscale(self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['plot_xscale'])
        self.host[self.figColCnt, self.figRowCnt].set_yscale(self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['plot_yscale'])
        if threeD: 
            self.host[self.figColCnt, self.figRowCnt].set_zscale(self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['plot_zscale'])
    
    # =============================== set axis limits
    def set_axis_limit(self, threeD):
        self.host[self.figColCnt, self.figRowCnt].set_xlim(xmin = self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['plot_xlimit_min'],
                xmax = self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['plot_xlimit_max'])
        self.host[self.figColCnt, self.figRowCnt].set_ylim(ymin = self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['plot_ylimit_min'],
                ymax = self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['plot_ylimit_max'])
        if threeD: 
            self.host[self.figColCnt, self.figRowCnt].set_zlim(zmin = self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['plot_zlimit_min'],
                zmax = self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['plot_zlimit_max'])
    
    # =============================== set axis ticks
    def set_axis_tick(self, threeD):
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

    # =============================== set azimuth and elevation angles for 3D plots
    def set_azim_elev(self):
        self.host[self.figColCnt, self.figRowCnt].azim = self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['plot_threed_azimdegree']
        self.host[self.figColCnt, self.figRowCnt].elev = self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['plot_threed_elevdegree']
     
    # =============================== set figure legend
    def set_figure_legend(self):
        self.fig.legend(
                bbox_to_anchor = self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['plotlegend_ncolumn'], 
                loc = self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['plotlegend_location'], 
                mode = self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['plotlegend_mode'], 
                borderaxespad = self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['plotlegend_border_axisPad'], 
                ncol = self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['plotlegend_ncolumn'])
    
    # =============================== set plot legends
    def set_plot_legend(self):
        if self.guestPlotCnt > 0: 
            self.linesSum = self.hostLines + self.linesSum
            self.labelsSum = self.hostLabels + self.labelsSum
            self.guest[self.guestPlotCnt - 1].legend(self.linesSum, self.labelsSum)
        if self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['plotlegend']:
            if not self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['graph_type'] in {'box'} and not self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['multipleyaxis']: # box plots do not have legend
                if self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['plotlegend_ncolumn'] != None: # TODO is this correct ??? Set up legend only for the last plot
                    self.host[self.figColCnt, self.figRowCnt].legend(
                            bbox_to_anchor = self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['plotlegend_bbox_to_anchor'], 
                            loc = self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['plotlegend_location'], 
                            mode = self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['plotlegend_mode'], 
                            borderaxespad = self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['plotlegend_border_axisPad'], 
                            ncol = self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['plotlegend_ncolumn'])
                else:    
                    self.host[self.figColCnt, self.figRowCnt].legend(
                            bbox_to_anchor = self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['plotlegend_bbox_to_anchor'], 
                            loc = self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['plotlegend_location'], 
                            mode = self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['plotlegend_mode'], 
                            borderaxespad = self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['plotlegend_border_axisPad'], 
                            ncol = self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['plotlegend_ncolumn'])
            self.hostLines, self.hostLabels, self.guestLines, self.guestLabels, self.linesSum, self.labelsSum  = [], [], [], [], [], [] # reinitialize label arrays

    # =============================== set settings for sns joint plot
    def set_snsjoint_setting(self, title):
        # seaborn jointplot specific settings
        if self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['graph_type'] in {'seaborn joint'}:
            self.snsJntPlot.ax_joint.set_xlabel(xLabel)
            self.snsJntPlot.ax_joint.set_ylabel(yLabel[0])
            self.snsJntPlot.ax_joint.tick_params(axis = 'x')
            self.snsJntPlot.ax_joint.tick_params(axis = 'y')
            plt.suptitle(title)
            plt.subplots_adjust(top = 0.9, bottom = 0.2)
    
    # =============================== set subtitle
    def set_subtitle(self, numOfPlots, title):
        # set subtitle
        if numOfPlots > 1:
            self.host[self.figColCnt, self.figRowCnt].title.set_text(title)
            
    # =============================== Show the plot
    def showPlot(self, title, numOfPlots):
        if not self.oneColSpecPlt:
            self.fig.suptitle(title) # Main title
        else:
            self.fig.suptitle(title, x = self.mainconfig['MAIN']['figure_singlecolumnnarrowplot_xtitlelocation']) # Main title
        if self.mainconfig['MAIN']['figurelegend']: 
            self.set_figure_legend()
        self.save_figure()
        self.fig.tight_layout() # to adjust spacing between graphs and labels
        plt.show()
    
    # =============================== Bar graph
    def barPlot(self, colNumX, colNumY, legendName):
        self.host[self.figColCnt, self.figRowCnt].bar(
                self.data[colNumX], 
                self.data[colNumY], 
                color = self.colors[self.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['BAR']['color']], 
                edgecolor = self.colors[self.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['BAR']['edgecolor']],
                linewidth = self.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['BAR']['edgewidth'], 
                tick_label = self.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['BAR']['label'], 
                capsize = self.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['BAR']['capsize'], 
                width = self.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['BAR']['width'], 
                bottom = self.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['BAR']['bottom'], 
                align = self.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['BAR']['align_bar'], 
                label = legendName[self.dataNum], 
                alpha = self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['graph_alpha']) 

    # =============================== Box graph
    def boxPlot(self, colNumX, legendName):
        boxplot_data = []
        
        if type(colNumX) is list:
            for item in colNumX:
                boxplot_data.append(self.data[item])
        else:
            boxplot_data.append(self.data[colNumX])
 
        self.host[self.figColCnt, self.figRowCnt].boxplot(
                boxplot_data, 
                positions = self.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['BOX']['position'],
                boxprops = dict(facecolor = self.colors[self.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['BOX']['boxcolor']], 
                color = self.colors[self.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['BOX']['linecolor']]), 
                capprops = dict(color = self.colors[self.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['BOX']['capcolor']]), 
                whiskerprops = dict(color = self.colors[self.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['BOX']['whiskercolor']]), 
                flierprops = dict(color = self.colors[self.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['BOX']['fliercolor']], 
                markeredgecolor = self.colors[self.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['BOX']['markeredgecolor']]), 
                medianprops = dict(color = self.colors[self.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['BOX']['mediancolor']]), 
                widths = self.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['BOX']['width'], 
                labels = self.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['BOX']['label'], 
                vert = self.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['BOX']['vertical'], 
                notch = self.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['BOX']['notched'], 
                whis = self.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['BOX']['whiskerreach'], 
                bootstrap = self.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['BOX']['bootstrap'], 
                patch_artist = self.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['BOX']['patchartist'], 
                zorder = self.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['BOX']['zorder'])

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
                self.colors[self.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['CDF']['color']], 
                linewidth = self.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['CDF']['width'], 
                linestyle = self.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['CDF']['style'], 
                marker = self.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['CDF']['markerstyle'], 
                markersize = self.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['CDF']['markersize'], 
                label = legendName[self.dataNum],   
                alpha = self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['graph_alpha'])
        print(self.host[self.figColCnt, self.figRowCnt].legend())

    # =============================== Histogram graph
    def histogramPlot(self, colNumX, legendName):
        self.bins = np.arange(min(self.data[colNumX]) - self.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['HISTOGRAM']['binres'], max(self.data[colNumX]) + self.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['HISTOGRAM']['binres'] * 2, self.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['HISTOGRAM']['binres']) # TODO get rid of this. Only do number of bins
        self.host[self.figColCnt, self.figRowCnt].hist(
                self.data[colNumX], 
                bins = self.bins, 
                color = self.colors[self.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['HISTOGRAM']['color']], 
                edgecolor = self.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['HISTOGRAM']['edgecolor'], 
                histtype = self.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['HISTOGRAM']['type'], 
                density = self.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['HISTOGRAM']['density'], 
                cumulative = self.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['HISTOGRAM']['cumulative'], 
                bottom = self.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['HISTOGRAM']['bottom'], 
                align = self.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['HISTOGRAM']['align_histogram'],
                orientation = self.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['HISTOGRAM']['orientation'], 
                rwidth = self.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['HISTOGRAM']['relativewidth'], 
                stacked = self.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['HISTOGRAM']['stacked'],
                label = legendName[i], 
                alpha = self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['graph_alpha'])  
        self.host[self.figColCnt, self.figRowCnt].set_xticks(self.bins[:-1]) # TODO modify this per ax

    # =============================== Line Plot - Primary y-axis  
    def linePlot_host(self, p, colNumX, colNumY, colNumE, legendName):
        p.append(0) #initialize array entry
        p[self.guestPlotCnt], = self.host[self.figColCnt, self.figRowCnt].plot(
                self.data[colNumX], 
                self.data[colNumY], 
                self.colors[self.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['LINE']['color']], 
                linewidth = self.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['LINE']['width'], 
                linestyle = self.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['LINE']['style'], 
                marker = self.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['LINE']['markerstyle'], 
                markersize = self.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['LINE']['markersize'],  
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
                self.colors[self.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['LINE']['color']], 
                linewidth = self.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['LINE']['width'], 
                linestyle = self.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['LINE']['style'], 
                marker = self.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['LINE']['markerstyle'], 
                markersize = self.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['LINE']['markersize'],  
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
                yerr = self.data[colNumE], ecolor = self.colors[self.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['ERRORBAR']['color']], 
                elinewidth = self.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['ERRORBAR']['width'], 
                fmt = self.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['ERRORBAR']['style'], 
                capsize = self.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['ERRORBAR']['capsize'], 
                capthick = self.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['ERRORBAR']['capthickness'],  
                barsabove = self.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['ERRORBAR']['barsabove'], 
                label = legendName[self.dataNum], 
                kwargs = {'alpha': self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['graph_alpha']})

    # =============================== Errorbar Plot - Additional y-axes
    def errorbarPlot_guest(self, p, colNumX, colNumY, colNumE, legendName):
        p.append(0) #initialize array entry
        self.guest.append(0) #initialize array entry
        self.guest[self.guestPlotCnt] = self.host[self.figColCnt, self.figRowCnt].twinx() # setup 2nd axis based on the first graph
        p[self.guestPlotCnt], = self.guest[self.guestPlotCnt].errorbar(self.data[colNumX], self.data[colNumY], 
                yerr = self.data[colNumE], ecolor = self.colors[self.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['ERRORBAR']['color']], 
                elinewidth = self.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['ERRORBAR']['width'], 
                fmt = self.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['ERRORBAR']['style'], 
                capsize = self.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['ERRORBAR']['capsize'], 
                capthick = self.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['ERRORBAR']['capthickness'],  
                barsabove = self.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['ERRORBAR']['barabove'], 
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
                    self.colors[self.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['THREED']['color']], 
                    linewidth = self.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['THREED']['width'], 
                    linestyle = self.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['THREED']['style'], 
                    marker = self.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['THREED']['markerstyle'], 
                    markersize = self.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['THREED']['markersize'],
                    label = legendName[i], 
                    alpha = self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['graph_alpha'])

    # =============================== Seaborn Line Graph - Primary y-axis
    def seabornLinePlot_host(self, colNumX, colNumY, legendName):
        sns.lineplot(x = self.data[colNumX], y = self.data[colNumY], 
                color = self.colors[self.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['SNSLINE']['color']], 
                linewidth = self.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['SNSLINE']['width'], 
                marker = self.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['SNSLINE']['markerstyle'],
                markersize = self.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['SNSLINE']['markersize'], 
                hue = self.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['SNSLINE']['hue'], 
                size = self.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['SNSLINE']['size'], 
                style = self.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['SNSLINE']['sns_style'], 
                label = legendName[i], alpha = self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['graph_alpha'],
                ax = self.host[self.figColCnt, self.figRowCnt]) 
        self.host[self.figColCnt, self.figRowCnt].lines[self.dataNum].set_linestyle(self.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['SNSLINE']['style'])
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
                linewidth = self.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['SNSLINE']['width'], 
                marker = self.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['SNSLINE']['markerstyle'],
                markersize = self.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['SNSLINE']['markersize'], 
                hue = self.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['SNSLINE']['hue'], 
                size = self.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['SNSLINE']['size'], 
                style = self.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['SNSLINE']['sns_style'], 
                label = legendName[i], alpha = self.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['graph_alpha'],
                ax = self.guest[self.guestPlotCnt]) 
        self.guest[self.guestPlotCnt].lines[0].set_linestyle(self.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['SNSLINE']['style'])
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
                kind = self.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['SNSJOINT']['kind'], 
                color = self.colors[self.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['SNSJOINT']['color']], 
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
                    self.mainconfig['PLOT']['Subplot' + str(i)]['dataset' + str(j)]['graph_type'])
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