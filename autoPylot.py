#!/usr/bin/env python3

from colorama import Fore, Back, init # colored output on the terminal
import csv
from datetime import datetime
import math
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import os
import pandas as pd
import re
import seaborn as sns
import sys
import tkinter
import yaml
sys.path.append('config' + os.sep)
import config_matplotlibrc

init(autoreset = True) # turn off colors after each print()

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

class AutoPylot:
    # =============================== Initializer / Instance attributes
    def __init__(self):
        self.data_handler = dataHandler()
        self.graph_handler = graphHandler(self.data_handler)
        self.plot_handler = plotHandler(self.data_handler, self.graph_handler)
    
    def MAIN(self):
        self.data_handler.main()
        #self.graph_handler.main()

        # prepare the plot environment
        self.graph_handler.prepare_graph(len(self.data_handler.mainconfig['PLOT']), False) 

        # logic for subplot generation
        for i in range(len(self.data_handler.mainconfig['PLOT'])):
            for j in range(self.data_handler.check_num_dataset(i)):
                if self.data_handler.mainconfig['PLOT']['Subplot' + str(i)]['dataset' + str(j)]['graph_type'] == 'threed':
                    self.graph_handler.prepare_graph(len(self.data_handler.mainconfig['PLOT']), True) 
                self.plot_handler.main(
                        i, 
                        len(self.data_handler.mainconfig['PLOT']), 
                        self.data_handler.mainconfig['PLOT']['Subplot' + str(i)]['dataset' + str(j)]['graph_type'], # REMOVE IT 
                        j,
                        self.data_handler.mainconfig['PLOT']['Subplot' + str(i)]['dataset' + str(j)]['input_xdata'], 
                        self.data_handler.mainconfig['PLOT']['Subplot' + str(i)]['dataset' + str(j)]['input_ydata'], 
                        self.data_handler.mainconfig['PLOT']['Subplot' + str(i)]['dataset' + str(j)]['input_zdata'], 
                        self.data_handler.mainconfig['PLOT']['Subplot' + str(i)]['dataset' + str(j)]['input_edata'], 
                        self.data_handler.mainconfig['PLOT']['Subplot' + str(i)]['dataset' + str(j)]['plot_legend']) # TODO: Why do I send self.numOfPlots???
                self.threeD = True if self.data_handler.mainconfig['PLOT']['Subplot' + str(i)]['dataset' + str(j)]['graph_type'] == 'threed' else False
            self.graph_handler.graph_configs(
                    j, # TODO get rid of this
                    self.plot_handler.guestPlotCnt,
                    self.data_handler.mainconfig['PLOT']['Subplot' + str(i)]['plot_xlabel'], 
                    self.data_handler.mainconfig['PLOT']['Subplot' + str(i)]['plot_ylabel'], 
                    self.data_handler.mainconfig['PLOT']['Subplot' + str(i)]['plot_zlabel'], 
                    self.threeD, 
                    self.data_handler.mainconfig['PLOT']['Subplot' + str(i)]['plot_title'], 
                    len(self.data_handler.mainconfig['PLOT']), 
                    self.data_handler.check_num_dataset(i), 
                    i,
                    self.plot_handler.boxplot,
                    self.plot_handler.boxplot_legendname)
        self.graph_handler.show_graph(self.data_handler.mainconfig['MAIN']['figure_title'], len(self.data_handler.mainconfig['PLOT']))

###################### USER INTERACTIONS
class dataHandler(AutoPylot):
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
        self.limits_mainconfig_graph_type = ['bar', 'box', 'cdf', 'errorbar', 'histogram', 'line', 'snsline', 'snsjoint', 'threed']
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

    # =============================== Check data type of inputs from config files 
    def check_config(self, config_name):
        error_vars_bool, error_vars_float, error_vars_int, error_vars_limit, error_vars_limit_name, error_vars_str = [], [], [], [], [], [] 
        
        if config_name == self.mainconfig_name:
            self.inputFile = self.mainconfig['MAIN']['inputfile_name'] + '.' + self.mainconfig['MAIN']['inputfile_format']
            self.inputFileDir = os.listdir(os.getcwd() + os.sep + self.mainconfig['MAIN']['inputfile_directory']) 
        
        try: 
            if config_name == self.mainconfig_name:
                for i in self.mainconfig_booleans:
                    for j in range(len(list(self.find_keys(self.mainconfig, i)))):
                        if not isinstance(list(self.find_keys(self.mainconfig, i))[j], bool):
                            error_vars_bool.append(i)
                            raise BoolError
                for i in self.mainconfig_floats:
                    for j in range(len(list(self.find_keys(self.mainconfig, i)))):
                        if not isinstance(list(self.find_keys(self.mainconfig, i))[j], float) and not isinstance(list(self.find_keys(self.mainconfig, i))[j], int) and not list(self.find_keys(self.mainconfig, i))[j] is None:
                            error_vars_float.append(i)
                            raise FloatError
                for i in self.mainconfig_integers:
                    for j in range(len(list(self.find_keys(self.mainconfig, i)))):
                        if not isinstance(list(self.find_keys(self.mainconfig, i))[j], int) and not list(self.find_keys(self.mainconfig, i))[j] is None:
                            error_vars_int.append(i)
                            raise IntError
                cnt = 0
                for i in self.limits_mainconfig_names:
                    for j in range(len(list(self.find_keys(self.mainconfig, i)))):
                        if not list(self.find_keys(self.mainconfig, i))[j] in self.limits_mainconfig_sum[cnt]:
                            error_vars_limit.append(self.limits_mainconfig_sum[cnt])
                            error_vars_limit_name.append(i)
                            raise LimitError
                    cnt += 1

                for i in self.limits_data_columns:
                    limit = np.arange(0, self.numData)
                    for j in range(len(list(self.find_keys(self.mainconfig, i)))):
                        if type(list(self.find_keys(self.mainconfig, i))[j]) is str:
                            if i == 'input_xdata':
                                data_x = eval(list(self.find_keys(self.mainconfig, i))[j])
                                self.data.append(data_x) # TODO, add function inputs, add len check for x-y-z data, functionirize check_config()
                                self.numData = len(self.data)
                                column_number_x = self.update_input_file(list(self.find_keys(self.mainconfig, i))[j], data_x)
                                self.update_mainconfig(list(self.find_keys(self.mainconfig, i))[j], column_number_x)
                            elif i == 'input_ydata':
                                x = data_x
                                data_y = eval(list(self.find_keys(self.mainconfig, i))[j])
                                self.data.append(data_y) # TODO, add function inputs, add len check for x-y-z data, functionirize check_config()
                                self.numData = len(self.data)
                                column_number_y = self.update_input_file(list(self.find_keys(self.mainconfig, i))[j], data_y)
                                self.update_mainconfig(list(self.find_keys(self.mainconfig, i))[j], column_number_y)
                            elif i == 'input_zdata':
                                x = data_x
                                y = data_y
                                data_z = eval(list(self.find_keys(self.mainconfig, i))[j])
                                self.data.append(data_z) # TODO, add function inputs, add len check for x-y-z data, functionirize check_config()
                                self.numData = len(self.data)
                                column_number_z = self.update_input_file(list(self.find_keys(self.mainconfig, i))[j], data_z)
                                self.update_mainconfig(list(self.find_keys(self.mainconfig, i))[j], column_number_z)
                        elif type(list(self.find_keys(self.mainconfig, i))[j]) is list:
                            for item in list(self.find_keys(self.mainconfig, i))[j]:
                                if not item in limit and not item is None:
                                    error_vars_limit.append(limit)
                                    error_vars_limit_name.append(i)
                                    raise LimitError
                        elif not list(self.find_keys(self.mainconfig, i))[j] in limit and not list(self.find_keys(self.mainconfig, i))[j] is None: # -1 since column numbers start from 0
                            error_vars_limit.append(limit)
                            error_vars_limit_name.append(i)
                            raise LimitError

                for i in self.mainconfig_strings:
                    for j in range(len(list(self.find_keys(self.mainconfig, i)))):
                        if not isinstance(list(self.find_keys(self.mainconfig, i))[j], str):
                            error_vars_str.append(i)
                            raise StrError
                
            if config_name == self.plotconfig_name:
                for i in self.plotconfig_booleans:
                    for j in range(len(list(self.find_keys(self.mainconfig, i)))):
                        if not isinstance(list(self.find_keys(self.plotconfig, i))[j], bool):
                            error_vars_bool.append(i)
                            raise BoolError
                for i in self.plotconfig_floats:
                    for j in range(len(list(self.find_keys(self.mainconfig, i)))):
                        if not isinstance(list(self.find_keys(self.plotconfig, i))[j], float) and not isinstance(list(self.find_keys(self.plotconfig, i))[j], int) and not list(self.find_keys(self.plotconfig, i))[j] is None:
                            error_vars_float.append(i)
                            raise FloatError
                for i in self.plotconfig_integers:
                    for j in range(len(list(self.find_keys(self.mainconfig, i)))):
                        if not isinstance(list(self.find_keys(self.plotconfig, i))[j], int) and not list(self.find_keys(self.plotconfig, i))[j] is None:
                            error_vars_int.append(i)
                            raise IntError
                cnt = 0
                for i in self.limits_plotconfig_names:
                    for j in range(len(list(self.find_keys(self.mainconfig, i)))):
                        if not list(self.find_keys(self.plotconfig, i))[j] in self.limits_plotconfig_sum[cnt]:
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
    
    # =============================== Check number of dataset for given subplot in main config
    def check_num_dataset(self, subplotnum):
        counter = 0
        for word in self.mainconfig['PLOT']['Subplot' + str(subplotnum)]:
            if re.search('dataset.', word):
                counter += 1
        return counter

    # =============================== Convert input data into float
    def convert_to_float(self): 
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

    # =============================== Find the given key in a dictionary
    def find_keys(self, input_dict, input_key):
        # Taken from https://stackoverflow.com/questions/9807634/find-all-occurrences-of-a-key-in-nested-dictionaries-and-lists
        if isinstance(input_dict, list):
            for i in input_dict:
                for x in self.find_keys(i, input_key):
                    yield x
        elif isinstance(input_dict, dict):
            if input_key in input_dict:
                yield input_dict[input_key]
            for j in input_dict.values():
                for x in self.find_keys(j, input_key):
                    yield x
    
    # =============================== Fetch default label names from csv file
    def fetch_csv_labels(self): 
        self.numData = len(self.data)
        # Update default label names if labels are given in the input file
        if not (self.data[0][0].isdigit()): # only check one of the first-row entries. If one of them is not a number, then the other first-row entries should be the same
            for i in range(self.numData):
                self.data[i][0] = self.data[i][0] if self.data[i][0] != '' else 'blank'
                self.defaultLabels.append(self.data[i][0])
            
            # Delete labels from input data
            for i in range(self.numData):
                del self.data[i][0]
    
    # =============================== Fetch input data from csv 
    def fetch_input_data(self):
        # open csv file
        self.data = self.read_file(
                self.mainconfig['MAIN']['inputfile_directory'], 
                self.mainconfig['MAIN']['inputfile_name'], 
                self.mainconfig['MAIN']['inputfile_format'])
        self.numData = len(self.data)
    
    # =============================== Main logic
    def main(self):
        # open main config file
        self.mainconfig = self.read_file(
                self.config_folderdirectory, 
                self.mainconfig_name, 
                self.config_format)

        # fetch input data
        self.fetch_input_data()
        self.data = self.transpose_list(self.data)
        self.fetch_csv_labels()
        self.convert_to_float()

        # open plot config file
        self.plotconfig = self.read_file(
                self.config_folderdirectory, 
                self.plotconfig_name, 
                self.config_format)
        
        # validate the inputs of config files
        check_mainconfig = self.check_config(self.mainconfig_name)
        if not self.check_config(self.plotconfig_name) or not check_mainconfig: sys.exit(0)

    # =============================== Open main config file
    def read_file(self, file_dir, file_name, file_format):
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
        data = self.read_file(
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
    
    # =============================== Convert rows to cols in input data from csv
    def transpose_list(self, data):
        data = list(map(list, zip(*data))) # transpose the self.data: rows -> columns
        return data

###################### GRAPH SETUP CLASS
class graphHandler(AutoPylot):
    # =============================== Initializer / Instance attributes
    def __init__(self, data_handler):
        self.data_handler = data_handler
        self.date = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.figRowCnt = 0
        self.figColCnt = 0
        self.fTxtNoXServer = f"""
{Fore.RED}Your X-server is not running, cannot plot the graph.
Please turn on your X-server first and then hit [enter]"""
        self.guest = []
        self.guestLabels = []
        self.guestLines = []
        self.hostLabels = []
        self.hostLines = []
        self.labelsSum = []
        self.linesSum = []
        self.numOfRow = 0
        self.oneColSpecPlt = False
        self.plotCounter = 0
        self.plotFuncName = ''
        self.snsJntPlot = None

    # =============================== Color the axes for multi-y axes (seaborn) line plots
    def axisColoring(self, colors, colorHost, colorGuest, guestPlotCnt):
        # color host
        self.host[self.figColCnt, self.figRowCnt].yaxis.label.set_color(colors[colorHost])
        self.host[self.figColCnt, self.figRowCnt].yaxis.label.set_alpha(
                self.data_handler.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['dataset' + str(0)]['graph_alpha'])
        # color guests     
        self.guest[guestPlotCnt - 1].yaxis.label.set_color(colors[colorGuest])
        self.guest[guestPlotCnt - 1].yaxis.label.set_alpha(
                self.data_handler.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['dataset' + str(guestPlotCnt)]['graph_alpha'])
    
    # =============================== Graph Configurations
    def graph_configs(self, dataNum, guestPlotCnt, xLabel, yLabel, zLabel, threeD, title, numOfPlots, numData, plotCounter, boxplot_legend, boxplot_legendname):
        self.plotCounter = plotCounter 
        self.dataNum = dataNum # TODO get rid of dataNum in this class. It does not make sense. 
        
        if not self.data_handler.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['graph_type'] in {'box'}:
            self.set_axis_label_scale(threeD)
        if threeD: 
            self.set_azim_elev()
        self.set_axis_limit(threeD)
        self.set_axis_tick(threeD)
        self.set_axis_label(numData, threeD, xLabel, yLabel, zLabel)
        self.set_axis_label_pad(threeD)
        self.set_subtitle(numOfPlots, title)
        self.set_plot_legend(boxplot_legend, boxplot_legendname, guestPlotCnt)
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
    def prepare_graph(self, numOfPlots, threeD):
        if threeD:
            self.host[self.figColCnt, self.figRowCnt].axis('off')
            numOfRow = 2 if numOfPlots > 1 else 1
            self.host[self.figColCnt, self.figRowCnt] = self.fig.add_subplot(
                    math.ceil(numOfPlots / numOfRow), 
                    numOfRow, 
                    self.plotCounter + 1, 
                    projection = '3d')
        else:
            exitLoop = False
            plt.rcParams.update(config_matplotlibrc.parameters) # update matplotlib parameters
            
            while True:
                try:   
                    self.numOfRow = self.data_handler.mainconfig['MAIN']['figure_plotperrow'] if numOfPlots > 1 else 1
                    if (self.data_handler.mainconfig['MAIN']['figure_plotperrow'] == 1 and numOfPlots > 1) and self.data_handler.mainconfig['MAIN']['figure_singlecolumnnarrowplot']:
                        self.numOfRow = 2
                        self.oneColSpecPlt = True
                    else:
                        self.oneColSpecPlt = False

                    if not self.oneColSpecPlt:
                        self.fig, self.host = plt.subplots(
                                math.ceil(numOfPlots / self.numOfRow), 
                                self.numOfRow, 
                                sharex = self.data_handler.mainconfig['MAIN']['figure_sharexaxis'], 
                                sharey = self.data_handler.mainconfig['MAIN']['figure_shareyaxis'], 
                                figsize = (self.data_handler.mainconfig['MAIN']['outputfigure_xdimension'], 
                                self.data_handler.mainconfig['MAIN']['outputfigure_ydimension']), 
                                squeeze = False)
                        if numOfPlots != 1 and numOfPlots % self.numOfRow != 0: # turn off the axes of last unused plot, because there is leftover plot in when total plots are odd
                            for i in range(numOfPlots % self.numOfRow, self.numOfRow):
                                self.host[int(numOfPlots / self.numOfRow), i].axis('off')
                    else:
                        self.fig, self.host = plt.subplots(
                                numOfPlots, 
                                self.numOfRow, 
                                sharex = self.data_handler.mainconfig['MAIN']['figure_sharexaxis'], 
                                sharey = self.data_handler.mainconfig['MAIN']['figure_shareyaxis'], 
                                figsize = (self.data_handler.mainconfig['MAIN']['outputfigure_xdimension'], 
                                self.data_handler.mainconfig['MAIN']['outputfigure_ydimension']), 
                                squeeze = False)
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
    
    # =============================== save figure
    def save_figure(self):
            self.fig.savefig(
            '%s' %self.data_handler.mainconfig['MAIN']['outputfigure_directory'] + os.sep + 
            '%s.%s' %(self.date, self.data_handler.mainconfig['MAIN']['outputfigure_format']), 
            bbox_inches = 'tight', 
            format = self.data_handler.mainconfig['MAIN']['outputfigure_format'])
    
    # =============================== set axis labels
    def set_axis_label(self, numData, threeD, xLabel, yLabel, zLabel):
        self.host[self.figColCnt, self.figRowCnt].set_xlabel(xLabel)
        self.host[self.figColCnt, self.figRowCnt].set_ylabel(yLabel)
        if self.data_handler.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['multipleyaxis']:# and plotSelect in ['line', 'seaborn line']:
            guestCnt = 0
            for i in range(self.data_handler.check_num_dataset(self.plotCounter) - 1):
                if self.data_handler.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['dataset' + str(i + 1)]['yaxis_on']: 
                    self.guest[guestCnt].set_ylabel(self.data_handler.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['dataset' + str(i + 1)]['dataset_ylabel'])
                    guestCnt += 1
        if threeD: self.host[self.figColCnt, self.figRowCnt].set_zlabel(zLabel)

    # =============================== set axis label paddings
    def set_axis_label_pad(self, threeD):
        self.host[self.figColCnt, self.figRowCnt].axes.xaxis.labelpad = self.data_handler.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['plot_xlabel_pad']
        self.host[self.figColCnt, self.figRowCnt].axes.yaxis.labelpad = self.data_handler.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['plot_ylabel_pad']
        if threeD: self.host[self.figColCnt, self.figRowCnt].axes.zaxis.labelpad = self.data_handler.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['plot_zlabel_pad']

    # =============================== set label scales
    def set_axis_label_scale(self, threeD):
        self.host[self.figColCnt, self.figRowCnt].set_xscale(self.data_handler.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['plot_xscale'])
        self.host[self.figColCnt, self.figRowCnt].set_yscale(self.data_handler.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['plot_yscale'])
        if threeD: 
            self.host[self.figColCnt, self.figRowCnt].set_zscale(self.data_handler.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['plot_zscale'])
    
    # =============================== set axis limits
    def set_axis_limit(self, threeD):
        self.host[self.figColCnt, self.figRowCnt].set_xlim(xmin = self.data_handler.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['plot_xlimit_min'],
                xmax = self.data_handler.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['plot_xlimit_max'])
        self.host[self.figColCnt, self.figRowCnt].set_ylim(ymin = self.data_handler.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['plot_ylimit_min'],
                ymax = self.data_handler.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['plot_ylimit_max'])
        if threeD: 
            self.host[self.figColCnt, self.figRowCnt].set_zlim(zmin = self.data_handler.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['plot_zlimit_min'],
                zmax = self.data_handler.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['plot_zlimit_max'])
    
    # =============================== set axis ticks
    def set_axis_tick(self, threeD):
        # set ticks
        if not self.data_handler.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['plot_xticks_distance'] is None: # check if user set spacing for ticks, otherwise don't set up xticks manually
            if self.data_handler.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['plot_xticks_min'] is None or self.data_handler.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['plot_xticks_max'] is None: # get start and end points from ax if user did not define them
                ticksStart, ticksEnd = self.host[self.figColCnt, self.figRowCnt].get_xlim()
                self.host[self.figColCnt, self.figRowCnt].xaxis.set_ticks(np.arange(ticksStart, ticksEnd, self.data_handler.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['plot_xticks_distance']))
            else:
                self.host[self.figColCnt, self.figRowCnt].xaxis.set_ticks(np.arange(self.data_handler.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['plot_xticks_min'], self.data_handler.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['plot_xticks_max'], self.data_handler.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['plot_xticks_distance']))
        if not self.data_handler.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['plot_yticks_distance'] is None:
            if self.data_handler.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['plot_yticks_min'] is None or self.data_handler.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['plot_yticks_max'] is None:
                ticksStart, ticksEnd = self.host[self.figColCnt, self.figRowCnt].get_ylim()
                self.host[self.figColCnt, self.figRowCnt].yaxis.set_ticks(np.arange(ticksStart, ticksEnd, self.data_handler.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['plot_yticks_distance']))
            else:
                self.host[self.figColCnt, self.figRowCnt].yaxis.set_ticks(np.arange(self.data_handler.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['plot_yticks_min'], self.data_handler.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['plot_yticks_max'], self.data_handler.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['plot_yticks_distance']))
        if threeD and not self.data_handler.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['plot_zticks_distance'] is None: 
            if self.data_handler.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['plot_zticks_min'] is None or self.data_handler.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['plot_zticks_max'] is None:
                ticksStart, ticksEnd = self.host[self.figColCnt, self.figRowCnt].get_zlim()
                self.host[self.figColCnt, self.figRowCnt].zaxis.set_ticks(np.arange(ticksStart, ticksEnd, self.data_handler.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['plot_zticks_distance']))
            else:
                self.host[self.figColCnt, self.figRowCnt].zaxis.set_ticks(np.arange(self.data_handler.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['plot_zticks_min'], self.data_handler.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['plot_zticks_max'], self.data_handler.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['plot_zticks_distance']))

    # =============================== set azimuth and elevation angles for 3D plots
    def set_azim_elev(self):
        self.host[self.figColCnt, self.figRowCnt].azim = self.data_handler.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['plot_threed_azimdegree']
        self.host[self.figColCnt, self.figRowCnt].elev = self.data_handler.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['plot_threed_elevdegree']
     
    # =============================== set figure legend
    def set_figure_legend(self):
        self.fig.legend(
                bbox_to_anchor = self.data_handler.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['plotlegend_ncolumn'], 
                loc = self.data_handler.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['plotlegend_location'], 
                mode = self.data_handler.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['plotlegend_mode'], 
                borderaxespad = self.data_handler.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['plotlegend_border_axisPad'], 
                ncol = self.data_handler.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['plotlegend_ncolumn'])
    
    # =============================== set plot legends
    def set_plot_legend(self, boxplot_legend, boxplot_legendname, guestPlotCnt):
        if guestPlotCnt > 0: 
            self.linesSum = self.hostLines + self.linesSum
            self.labelsSum = self.hostLabels + self.labelsSum
            lines_labels_zipped = dict(zip(self.labelsSum, self.linesSum)) # to avoid duplicate labels in legend, taken from https://stackoverflow.com/questions/13588920/stop-matplotlib-repeating-labels-in-legend
            self.guest[guestPlotCnt - 1].legend(lines_labels_zipped.values(), lines_labels_zipped.keys())
        if self.data_handler.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['plotlegend']: # TODO does not make sense,  move it to set_graph_configs
            if self.data_handler.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['graph_type'] in {'box'}: # TODO fix self.dataNum. Does not make sense.
                label_box, legend_box = [], []
                for i in range(len(boxplot_legend)):
                    label_box.append(boxplot_legendname[i])
                    legend_box.append(boxplot_legend[i]['boxes'][0])
                self.host[self.figColCnt, self.figRowCnt].legend(legend_box, label_box, loc = self.data_handler.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['plotlegend_location'])
            elif not self.data_handler.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['multipleyaxis']: 
                if self.data_handler.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['plotlegend_ncolumn'] != None: # TODO is this correct ??? Set up legend only for the last plot
                    self.host[self.figColCnt, self.figRowCnt].legend(
                            bbox_to_anchor = self.data_handler.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['plotlegend_bbox_to_anchor'], 
                            loc = self.data_handler.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['plotlegend_location'], 
                            mode = self.data_handler.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['plotlegend_mode'], 
                            borderaxespad = self.data_handler.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['plotlegend_border_axisPad'], 
                            ncol = self.data_handler.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['plotlegend_ncolumn'])
                else:    
                    self.host[self.figColCnt, self.figRowCnt].legend(
                            bbox_to_anchor = self.data_handler.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['plotlegend_bbox_to_anchor'], 
                            loc = self.data_handler.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['plotlegend_location'], 
                            mode = self.data_handler.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['plotlegend_mode'], 
                            borderaxespad = self.data_handler.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['plotlegend_border_axisPad'], 
                            ncol = self.data_handler.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['plotlegend_ncolumn'])
            self.hostLines, self.hostLabels, self.guestLines, self.guestLabels, self.linesSum, self.labelsSum  = [], [], [], [], [], [] # reinitialize label arrays

    # =============================== set settings for sns joint plot
    def set_snsjoint_setting(self, title):
        # seaborn jointplot specific settings
        if self.data_handler.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['graph_type'] in {'seaborn joint'}:
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
    def show_graph(self, title, numOfPlots):
        if not self.oneColSpecPlt:
            self.fig.suptitle(title) # Main title
        else:
            self.fig.suptitle(title, x = self.data_handler.mainconfig['MAIN']['figure_singlecolumnnarrowplot_xtitlelocation']) # Main title
        if self.data_handler.mainconfig['MAIN']['figurelegend']: 
            self.set_figure_legend()
        self.save_figure()
        self.fig.tight_layout() # to adjust spacing between graphs and labels
        plt.show()

###################### PLOTTER CLASS
class plotHandler(AutoPylot):
    def __init__(self, data_handler, graph_handler):
        self.data_handler = data_handler
        self.graph_handler = graph_handler
        self.boxplot = []
        self.boxplot_legendname = []
        self.colors = ['steelblue', 'sandybrown', 'mediumseagreen', 'indianred', 'dimgrey', 'orchid', 
                'goldenrod', 'darkcyan', 'mediumslateblue', 'darkkhaki'] # Taken from https://matplotlib.org/3.1.0/gallery/color/named_colors.html

    # =============================== Bar graph
    def bar(self, colNumX, colNumY, legendName):
        self.graph_handler.host[self.graph_handler.figColCnt, self.graph_handler.figRowCnt].bar(
                self.data_handler.data[colNumX], 
                self.data_handler.data[colNumY], 
                color = self.colors[self.data_handler.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['BAR']['color']], 
                edgecolor = self.colors[self.data_handler.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['BAR']['edgecolor']],
                linewidth = self.data_handler.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['BAR']['edgewidth'], 
                tick_label = self.data_handler.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['BAR']['label'], 
                capsize = self.data_handler.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['BAR']['capsize'], 
                width = self.data_handler.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['BAR']['width'], 
                bottom = self.data_handler.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['BAR']['bottom'], 
                align = self.data_handler.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['BAR']['align_bar'], 
                label = legendName, 
                alpha = self.data_handler.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['graph_alpha']) 

    # =============================== Box graph
    def box(self, colNumX, legendName):
        boxplot_data = []
        
        if type(colNumX) is list:
            for item in colNumX:
                boxplot_data.append(self.data_handler.data[item])
        else:
            boxplot_data.append(self.data_handler.data[colNumX])
 
        self.boxplot.append(self.graph_handler.host[self.graph_handler.figColCnt, self.graph_handler.figRowCnt].boxplot(
                boxplot_data, 
                positions = self.data_handler.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['BOX']['position'],
                boxprops = dict(facecolor = self.colors[self.data_handler.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['BOX']['boxcolor']], 
                color = self.colors[self.data_handler.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['BOX']['linecolor']]), 
                capprops = dict(color = self.colors[self.data_handler.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['BOX']['capcolor']]), 
                whiskerprops = dict(color = self.colors[self.data_handler.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['BOX']['whiskercolor']]), 
                flierprops = dict(color = self.colors[self.data_handler.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['BOX']['fliercolor']], 
                markeredgecolor = self.colors[self.data_handler.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['BOX']['markeredgecolor']]), 
                medianprops = dict(color = self.colors[self.data_handler.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['BOX']['mediancolor']]), 
                widths = self.data_handler.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['BOX']['width'], 
                labels = self.data_handler.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['BOX']['label'], 
                vert = self.data_handler.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['BOX']['vertical'], 
                notch = self.data_handler.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['BOX']['notched'], 
                whis = self.data_handler.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['BOX']['whiskerreach'], 
                bootstrap = self.data_handler.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['BOX']['bootstrap'], 
                patch_artist = self.data_handler.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['BOX']['patchartist'], 
                zorder = self.data_handler.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['BOX']['zorder']))
        self.boxplot_legendname.append(legendName) 

    # =============================== CDF graph
    def cdf(self, colNumX, legendName):
        bin_edges_list = [] 
        cdfData = []
        data_size = len(self.data_handler.data[colNumX]) # taken from: https://stackoverflow.com/questions/24575869/read-file-and-plot-cdf-in-python
        data_set = sorted(set(self.data_handler.data[colNumX]))
        bins = np.append(data_set, data_set[-1] + 1)
        counts, bin_edges = np.histogram(self.data_handler.data[colNumX], bins = bins, density = False) # Use histogram function to bin data
        counts = counts.astype(float) / data_size
        cdfData = np.cumsum(counts)
        self.graph_handler.host[self.graph_handler.figColCnt, self.graph_handler.figRowCnt].plot(
                bin_edges[0:-1], 
                cdfData, 
                self.colors[self.data_handler.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['CDF']['color']], 
                linewidth = self.data_handler.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['CDF']['width'], 
                linestyle = self.data_handler.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['CDF']['style'], 
                marker = self.data_handler.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['CDF']['markerstyle'], 
                markersize = self.data_handler.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['CDF']['markersize'], 
                label = legendName,   
                alpha = self.data_handler.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['graph_alpha'])
        print(self.graph_handler.host[self.graph_handler.figColCnt, self.graph_handler.figRowCnt].legend())

    # =============================== Errorbar-type graphs
    def errorbar(self, colNumX, colNumY, colNumE, legendName):
        p = []
        if self.data_handler.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['multipleyaxis']: # multiple-axis enabled
            if dataNum == 0:
                self.errorbar_host(p, colNumX, colNumY, colNumE, legendName)
            else:
                if self.data_handler.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['dataset' + str(dataNum)]['yaxis_on']:
                    lines, labels = self.errorbar_guest(p, colNumX, colNumY, colNumE, legendName)
                    self.graph_handler.guestLines += lines
                    self.graph_handler.guestLabels += labels
                    self.guestPlotCnt += 1
                    self.axisOffset += self.data_handler.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['dataset' + str(dataNum)]['yaxis_axisoffset']
                else:
                    self.errorbar_host(p, colNumX, colNumY, colNumE, legendName)
            self.graph_handler.hostLines, self.graph_handler.hostLabels = self.graph_handler.host[self.graph_handler.figColCnt, self.graph_handler.figRowCnt].get_legend_handles_labels()
            self.graph_handler.linesSum = self.graph_handler.hostLines + self.graph_handler.guestLines
            self.graph_handler.labelsSum = self.graph_handler.hostLabels + self.graph_handler.guestLabels
            if self.guestPlotCnt > 0: self.graph_handler.guest[self.guestPlotCnt - 1].legend(self.graph_handler.linesSum, self.graph_handler.labelsSum)
            if self.guestPlotCnt == dataNum - 1: self.graph_handler.axisColoring(
                    self.colors,
                    dataNum, 
                    self.data_handler.plotconfig['LINE']['Plot' + str(0)]['color'], self.data_handler.plotconfig['LINE']['Plot' + str(dataNum)]['color'],
                    self.guestPlotCnt) # color the axes iff each line has a y-axis
        else:
            self.errorbar_host(p, colNumX, colNumY, colNumE, legendName)

    # =============================== Errorbar Plot - Additional y-axes
    def errorbar_guest(self, p, colNumX, colNumY, colNumE, legendName):
        p.append(0) #initialize array entry
        self.graph_handler.guest.append(0) #initialize array entry
        self.graph_handler.guest[self.guestPlotCnt] = self.graph_handler.host[self.graph_handler.figColCnt, self.graph_handler.figRowCnt].twinx() # setup 2nd axis based on the first graph
        p[self.guestPlotCnt] = self.graph_handler.guest[self.guestPlotCnt].errorbar(
                self.data_handler.data[colNumX], 
                self.data_handler.data[colNumY], 
                yerr = self.data_handler.data[colNumE], ecolor = self.colors[self.data_handler.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['ERRORBAR']['color']], 
                elinewidth = self.data_handler.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['ERRORBAR']['width'], 
                fmt = self.data_handler.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['ERRORBAR']['style'], 
                capsize = self.data_handler.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['ERRORBAR']['capsize'], 
                capthick = self.data_handler.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['ERRORBAR']['capthickness'],  
                barsabove = self.data_handler.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['ERRORBAR']['barabove'], 
                label = legendName, 
                alpha = self.data_handler.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['graph_alpha'])
        self.graph_handler.guest[self.guestPlotCnt].set_ylim(
                min(self.data_handler.data[colNumY]) - self.data_handler.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['yaxis_ylimthreshold'], 
                max(self.data_handler.data[colNumY]) + self.data_handler.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['yaxis_ylimthreshold'])
        self.graph_handler.guest[self.guestPlotCnt].grid(False)
        self.graph_handler.guest[self.guestPlotCnt].spines['right'].set_position(('axes', self.axisOffset)) 
        lines, labels = self.graph_handler.guest[self.guestPlotCnt].get_legend_handles_labels()
        return lines, labels

    # =============================== Errorbar Plot - Primary y-axis  
    def errorbar_host(self, p, colNumX, colNumY, colNumE, legendName):
        p.append(0) #initialize array entry
        p[self.guestPlotCnt] = self.graph_handler.host[self.graph_handler.figColCnt, self.graph_handler.figRowCnt].errorbar(
                self.data_handler.data[colNumX], 
                self.data_handler.data[colNumY], 
                yerr = self.data_handler.data[colNumE], 
                ecolor = self.colors[self.data_handler.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['ERRORBAR']['color']], 
                elinewidth = self.data_handler.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['ERRORBAR']['width'], 
                fmt = self.data_handler.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['ERRORBAR']['style'], 
                capsize = self.data_handler.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['ERRORBAR']['capsize'], 
                capthick = self.data_handler.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['ERRORBAR']['capthickness'],  
                barsabove = self.data_handler.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['ERRORBAR']['barsabove'], 
                label = legendName, 
                alpha = self.data_handler.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['graph_alpha'])
    
    # =============================== Histogram graph
    def histogram(self, colNumX, legendName):
        self.bins = np.arange(
            min(self.data_handler.data[colNumX]) - self.data_handler.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['HISTOGRAM']['binres'], 
            max(self.data_handler.data[colNumX]) + self.data_handler.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['HISTOGRAM']['binres'] * 2, 
            self.data_handler.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['HISTOGRAM']['binres']) # TODO get rid of this. Only do number of bins
        self.graph_handler.host[self.graph_handler.figColCnt, self.graph_handler.figRowCnt].hist(
                self.data_handler.data[colNumX], 
                bins = self.bins, 
                color = self.colors[self.data_handler.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['HISTOGRAM']['color']], 
                edgecolor = self.data_handler.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['HISTOGRAM']['edgecolor'], 
                histtype = self.data_handler.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['HISTOGRAM']['type'], 
                density = self.data_handler.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['HISTOGRAM']['density'], 
                cumulative = self.data_handler.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['HISTOGRAM']['cumulative'], 
                bottom = self.data_handler.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['HISTOGRAM']['bottom'], 
                align = self.data_handler.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['HISTOGRAM']['align_histogram'],
                orientation = self.data_handler.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['HISTOGRAM']['orientation'], 
                rwidth = self.data_handler.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['HISTOGRAM']['relativewidth'], 
                stacked = self.data_handler.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['HISTOGRAM']['stacked'],
                label = legendName, 
                alpha = self.data_handler.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['graph_alpha'])  
        self.graph_handler.host[self.graph_handler.figColCnt, self.graph_handler.figRowCnt].set_xticks(self.bins[:-1]) # TODO modify this per ax

    # =============================== Line-type graphs
    def line(self, colNumX, colNumY, colNumE, legendName):
        p = []
        if self.data_handler.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['multipleyaxis']: # multiple-axis enabled
            if self.dataNum == 0:
                self.line_host_withguest(p, colNumX, colNumY, colNumE, legendName)
            else:
                if self.data_handler.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['yaxis_on']:
                    self.line_guest(p, colNumX, colNumY, colNumE, legendName)
                else:
                    self.line_host_withguest(p, colNumX, colNumY, colNumE, legendName)
            if all(self.data_handler.find_keys(self.data_handler.mainconfig, 'yaxis_on')) and self.guestPlotCnt > 0: 
                self.graph_handler.axisColoring(
                        self.colors, 
                        self.data_handler.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(0)]['LINE']['color'], 
                        self.data_handler.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['LINE']['color'],
                        self.guestPlotCnt) # TODO find a solution instead of any() color the axes iff each line has a y-axis
        else:
            self.line_host(p, colNumX, colNumY, colNumE, legendName)
    
    # =============================== Line Plot - Additional y-axes
    def line_guest(self, p, colNumX, colNumY, colNumE, legendName):
        p.append(0) #initialize array entry
        self.graph_handler.guest.append(0) #initialize array entry
        self.graph_handler.guest[self.guestPlotCnt] = self.graph_handler.host[self.graph_handler.figColCnt, self.graph_handler.figRowCnt].twinx() # setup 2nd axis based on the first graph
        p[-1], = self.graph_handler.guest[self.guestPlotCnt].plot(
                self.data_handler.data[colNumX], 
                self.data_handler.data[colNumY], 
                self.colors[self.data_handler.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['LINE']['color']], 
                linewidth = self.data_handler.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['LINE']['width'], 
                linestyle = self.data_handler.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['LINE']['style'], 
                marker = self.data_handler.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['LINE']['markerstyle'], 
                markersize = self.data_handler.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['LINE']['markersize'],  
                label = legendName, 
                alpha = self.data_handler.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['graph_alpha'])
        self.graph_handler.guest[self.guestPlotCnt].set_ylim(
                min(self.data_handler.data[colNumY]) - self.data_handler.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['yaxis_ylimthreshold'], 
                max(self.data_handler.data[colNumY]) + self.data_handler.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['yaxis_ylimthreshold'])
        self.graph_handler.guest[self.guestPlotCnt].grid(False)
        self.graph_handler.guest[self.guestPlotCnt].spines['right'].set_position(('axes', self.axisOffset)) 
        lines, labels = self.graph_handler.guest[self.guestPlotCnt].get_legend_handles_labels()
        self.graph_handler.linesSum += lines
        self.graph_handler.labelsSum += labels
        self.guestPlotCnt += 1
        self.axisOffset += self.data_handler.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['yaxis_axisoffset']

    # =============================== Line Plot
    def line_host(self, p, colNumX, colNumY, colNumE, legendName):
        p.append(0) #initialize array entry
        p[-1], = self.graph_handler.host[self.graph_handler.figColCnt, self.graph_handler.figRowCnt].plot(
                self.data_handler.data[colNumX], 
                self.data_handler.data[colNumY], 
                self.colors[self.data_handler.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['LINE']['color']], 
                linewidth = self.data_handler.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['LINE']['width'], 
                linestyle = self.data_handler.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['LINE']['style'], 
                marker = self.data_handler.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['LINE']['markerstyle'], 
                markersize = self.data_handler.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['LINE']['markersize'],  
                label = legendName,
                alpha = self.data_handler.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['graph_alpha'])
    
    # =============================== Line Plot - Primary y-axis when used with guest plot
    def line_host_withguest(self, p, colNumX, colNumY, colNumE, legendName):
        self.line_host(p, colNumX, colNumY, colNumE, legendName)
        lines, labels = self.graph_handler.host[self.graph_handler.figColCnt, self.graph_handler.figRowCnt].get_legend_handles_labels()
        self.graph_handler.hostLines += lines
        self.graph_handler.hostLabels += labels

    # =============================== Plotter function
    def main(self, plotCounter, numOfPlots, plotSelect, dataNum, colNumX, colNumY, colNumZ, colNumE, legendName):
        self.plotCounter = plotCounter
        self.dataNum = dataNum

        if self.dataNum == 0:
            self.guestPlotCnt = 0
            self.axisOffset = 1
        # Main if clause for plots
        if plotSelect == 'bar':
            self.bar(colNumX, colNumY, legendName)
        elif plotSelect == 'box':
            self.box(colNumX, legendName)
        elif plotSelect == 'cdf':
            self.cdf(colNumX, legendName)
        elif plotSelect == 'histogram':
            self.histogram(colNumX, legendName)
        elif plotSelect in 'line':
            self.line(colNumX, colNumY, colNumE, legendName)
        elif plotSelect in 'errorbar':
            self.errorbar(colNumX, colNumY, colNumE, legendName)
        elif plotSelect == 'snsjointplot':
            self.snsjoint(colNumX, colNumY, legendName)
        elif plotSelect == 'snsline':
            self.snsline(colNumX, colNumY, legendName)
        elif plotSelect == 'threed':
            self.threed(numOfPlots, plotSelect, colNumX, colNumY, colNumZ, legendName)
    
    # =============================== Seaborn Line Graph
    def snsline(self, colNumX, colNumY, legendName):
        if self.data_handler.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['multipleyaxis']: # multiple-axis enabled
            if self.dataNum == 0:
                self.snsline_host_withguest(colNumX, colNumY, legendName)
            else:
                if self.data_handler.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['yaxis_on']:
                    self.snsline_guest(colNumX, colNumY, legendName)
                else:
                    self.snsline_host_withguest(colNumX, colNumY, legendName)
            if all(self.data_handler.find_keys(self.data_handler.mainconfig, 'yaxis_on')) and self.guestPlotCnt > 0: 
                self.graph_handler.axisColoring(
                        self.colors, 
                        self.data_handler.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(0)]['SNSLINE']['color'], 
                        self.data_handler.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['SNSLINE']['color'],
                        self.guestPlotCnt) # TODO find a solution instead of any() color the axes iff each line has a y-axis
        else:
            self.snsline_host(colNumX, colNumY, legendName)
    
    # =============================== Seaborn Line Graph - Additional y-axes
    def snsline_guest(self, colNumX, colNumY, legendName):
        self.graph_handler.guest.append(0) # initialize array entry
        self.graph_handler.guest[self.guestPlotCnt] = self.graph_handler.host[self.graph_handler.figColCnt, self.graph_handler.figRowCnt].twinx() # setup 2nd axis based on the first graph
        sns.lineplot(
                x = self.data_handler.data[colNumX], 
                y = self.data_handler.data[colNumY], 
                color = self.colors[self.data_handler.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['SNSLINE']['color']], 
                linewidth = self.data_handler.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['SNSLINE']['width'], 
                marker = self.data_handler.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['SNSLINE']['markerstyle'],
                markersize = self.data_handler.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['SNSLINE']['markersize'], 
                hue = self.data_handler.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['SNSLINE']['hue'], 
                size = self.data_handler.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['SNSLINE']['size'], 
                style = self.data_handler.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['SNSLINE']['sns_style'], 
                label = legendName, 
                alpha = self.data_handler.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['graph_alpha'],
                ax = self.graph_handler.guest[self.guestPlotCnt]) 
        self.graph_handler.guest[self.guestPlotCnt].lines[0].set_linestyle(self.data_handler.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['SNSLINE']['style'])
        self.graph_handler.guest[self.guestPlotCnt].set_ylim(
                min(self.data_handler.data[colNumY]) - self.data_handler.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['yaxis_ylimthreshold'], 
                max(self.data_handler.data[colNumY]) + self.data_handler.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['yaxis_ylimthreshold'])
        self.graph_handler.guest[self.guestPlotCnt].grid(False)
        self.graph_handler.guest[self.guestPlotCnt].legend_.remove()
        self.graph_handler.guest[self.guestPlotCnt].spines['right'].set_position(('axes', self.axisOffset))
        lines, labels = self.graph_handler.guest[self.guestPlotCnt].get_legend_handles_labels()
        self.graph_handler.linesSum += lines
        self.graph_handler.labelsSum += labels
        self.guestPlotCnt += 1
        self.axisOffset += self.data_handler.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['yaxis_axisoffset']
    
    # =============================== Seaborn Line Graph - Primary y-axis
    def snsline_host(self, colNumX, colNumY, legendName):
        sns.lineplot(
                x = self.data_handler.data[colNumX], 
                y = self.data_handler.data[colNumY], 
                color = self.colors[self.data_handler.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['SNSLINE']['color']], 
                linewidth = self.data_handler.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['SNSLINE']['width'], 
                marker = self.data_handler.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['SNSLINE']['markerstyle'],
                markersize = self.data_handler.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['SNSLINE']['markersize'], 
                hue = self.data_handler.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['SNSLINE']['hue'], 
                size = self.data_handler.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['SNSLINE']['size'], 
                style = self.data_handler.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['SNSLINE']['sns_style'], 
                label = legendName, 
                alpha = self.data_handler.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['graph_alpha'],
                ax = self.graph_handler.host[self.graph_handler.figColCnt, self.graph_handler.figRowCnt])
        self.graph_handler.host[self.graph_handler.figColCnt, self.graph_handler.figRowCnt].lines[-1].set_linestyle(
                self.data_handler.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['SNSLINE']['style'])
        self.graph_handler.host[self.graph_handler.figColCnt, self.graph_handler.figRowCnt].legend_.remove()

    # =============================== Seaborn Line Graph - Primary y-axis when used with guest plot
    def snsline_host_withguest(self, colNumX, colNumY, legendName):
        self.snsline_host(colNumX, colNumY, legendName)
        lines, labels = self.graph_handler.host[self.graph_handler.figColCnt, self.graph_handler.figRowCnt].get_legend_handles_labels()
        self.graph_handler.hostLines += lines
        self.graph_handler.hostLabels += labels

    # =============================== Seaborn Joint Graph
    def snsjoint(self, colNumX, colNumY, legendName):
        sns.jointplot(
                x = self.data_handler.data[colNumX], 
                y = self.data_handler.data[colNumY], 
                kind = self.data_handler.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['SNSJOINT']['kind'], 
                color = self.colors[self.data_handler.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['SNSJOINT']['color']], 
                label = legendName)

    # =============================== 3D graph
    def threed(self, numOfPlots, plotSelect, colNumX, colNumY, colNumZ, legendName):
        self.graph_handler.host[self.graph_handler.figColCnt, self.graph_handler.figRowCnt].plot(
                self.data_handler.data[colNumX], 
                self.data_handler.data[colNumY], 
                self.data_handler.data[colNumZ], 
                self.colors[self.data_handler.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['THREED']['color']], 
                linewidth = self.data_handler.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['THREED']['width'], 
                linestyle = self.data_handler.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['THREED']['style'], 
                marker = self.data_handler.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['THREED']['markerstyle'], 
                markersize = self.data_handler.plotconfig['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['THREED']['markersize'],
                label = legendName, 
                alpha = self.data_handler.mainconfig['PLOT']['Subplot' + str(self.plotCounter)]['dataset' + str(self.dataNum)]['graph_alpha'])
        
autopylot = AutoPylot()
autopylot.MAIN()