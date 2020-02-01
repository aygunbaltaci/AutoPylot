#!/usr/bin/env python3

import os
import sys
from colorama import Fore, Back, init # colored output on the terminal
import csv
import numpy as np
sys.path.append('lib' + os.sep)
import config_main as config
import plotFuncs
init(autoreset = True) # turn off colors after each print()
   
###################### USER INTERACTIONS
class userInteractions:
    # =============================== Initializer
    def __init__(self):
        self.counter_acceptUserInput = 0
        self.csvData = True
        self.data = []
        self.defaultBinRes = 1
        self.defaultErrorBar = False
        self.defaultFetchColX = 0
        self.defaultFetchColY = 1
        self.defaultFetchColZ = 2
        self.defaultFetchErrorBar = 2
        self.defaultLabels = [] 
        self.defaultMinX = 1
        self.defaultMaxX = 100
        self.defaultNumOfPlots = 1
        self.defaultResX = 1
        self.defaultThreeD = False
        self.defaultX = np.arange(float(self.defaultMinX), float(self.defaultMaxX), float(self.defaultResX))
        self.defaultY = self.defaultX ** 2
        self.defaultZ = self.defaultY ** 2
        self.defaultE = np.random.random_sample(len(self.defaultX))
        self.df = []
        self.errorBar = []
        self.fetchColX = []
        self.fetchColY = []
        self.fetchColZ = []
        self.fetchColE = []
        self.fetchXFunc = False
        self.fetchXFunc2 = False
        self.fetchYFunc = False
        self.fetchYFunc2 = False
        self.fetchZFunc = False
        self.fetchZFunc2 = False
        self.inputFile = config.defaultInputFile
        self.legendName = []
        self.plotTypes = ['bar', 'box', 'cdf', 'histogram', 'line||scatter||line+scatter', '3d', 'seaborn line', 'seaborn jointplot']
        self.maxNumXAxis = 0 # I don't know whether this is a right value to take, might cause errors. DOUBLE CHECK
        self.maxPlotType = len(self.plotTypes) 
        self.maxPlotPlotType = 6
        self.minColNum = 0
        self.minPlotType = 1
        self.minPlotPlotType = 1
        self.moreData = False
        self.nextFunc = 'askInputFileName'
        self.numData = 0
        self.plotSelect = ''
        self.plotPlotSelect = []
        self.plotPyt = None
        self.prevCallFunc = False
        self.prevCallFunc_askPlotType = False
        self.prevCallFunc_errorBar = False
        self.prevCallFunc_E = False
        self.prevCallFunc_plotPlotType = False
        self.prevCallFunc_xLabel = False
        self.prevCallFunc_Y = False
        self.prevCallFunc_yLabel = False
        self.prevCallFunc_Z = False
        self.prevPlotSelect = ''
        self.printFailure = 'f'
        self.printQuestion = 'q'
        self.printSuccess = 's'
        self.printVars = []
        self.printWelcomeTxt = True
        self.undoCommands = ['undo', 'UNDO']
        self.yDataCounter = 0
        self.yLabel = []
        
        # Set default values
        self.binRes = self.defaultBinRes
        self.e = self.defaultE
        self.minX = self.defaultMinX
        self.maxX = self.defaultMaxX
        self.numOfPlots = self.defaultNumOfPlots
        self.resX = self.defaultResX
        self.threeD = self.defaultThreeD
        self.title = config.defaultTitle
        self.x = self.defaultX
        self.xLabel = config.defaultXLabel
        self.y = self.defaultY
        self.z = self.defaultZ
        self.zLabel = config.defaultZLabel
        
        # Print messages
        self.qTxtFileName = f"""
\n\n{Back.BLUE}PYTHON3 PLOTTER{Back.BLACK}
Plot your data without writing scripts!  
Type [{Fore.YELLOW}exit{Fore.WHITE} || {Fore.YELLOW}EXIT{Fore.WHITE} || {Fore.YELLOW}quit{Fore.WHITE} || {Fore.YELLOW}QUIT{Fore.WHITE}] to terminate the program at any step.
Type [{Fore.YELLOW}undo{Fore.WHITE} || {Fore.YELLOW}UNDO{Fore.WHITE}] to go to previous question at any step. \n
{Fore.MAGENTA}>>>{Fore.WHITE} Enter the name of your data file (located in the same directory of program)."""
        self.qTxtTypeOfPlot = """
GRAPH #: %d

What type of graph do you want to plot? \nOptions:"""
        self.qTxtTypeOfPlotPlot = """
Select the plot type for this data set: 

1. Line
2. Scatter
3. Line+Scatter
4. Line w/ ErrorBar
5. Scatter w/ ErrorBar
6. Line+Scatter w/ ErrorBar

Enter the number of the plot [1-6]:"""
        self.qTxtDefault = f"""
Just hit [{Fore.YELLOW}enter{Fore.WHITE}] for default: ({Fore.CYAN}%s{Fore.WHITE})"""
        self.qTxtSelectYN = f"""
{Fore.MAGENTA}>>>{Fore.WHITE} Please select [{Fore.YELLOW}yY{Fore.WHITE}] or [{Fore.YELLOW}nN{Fore.WHITE}]."""
        self.qTxtNumOfPlots = f"""
{Fore.MAGENTA}>>>{Fore.WHITE} How many graphs do you want to plot?"""
        self.qTxtSkipCsvDataFetch = f"""
If you want to derive data ONLY from a function, you may skip this part by typing [{Fore.YELLOW}sS{Fore.WHITE}] \n\n"""
        self.qTxtDataFromFunction = f"""
If you want to derive data from a function, please type [{Fore.YELLOW}fF{Fore.WHITE}] \n\n"""
        self.qTxtFetchCol = f"""
{Fore.MAGENTA}>>>{Fore.WHITE} What is the column number in your input data for %s-axis?"""
        self.qTxtFetchErrorCol = f"""
{Fore.MAGENTA}>>>{Fore.WHITE} What is the column number of errorbar data?"""
        self.qTxtMoreData = f"""
{Fore.MAGENTA}>>>{Fore.WHITE} Do you want to add more dataset to the plot? [{Fore.YELLOW}y/N{Fore.WHITE}]"""
        self.qTxtMinMaxResX = f"""
Please enter the min, max. and resolution of x-axis."""
        self.qTxtEnterFormula = f"""
{Fore.MAGENTA}>>>{Fore.WHITE} Enter the formula %s(%s). You may type 
{Fore.MAGENTA}numpy (np.*){Fore.WHITE} and {Fore.YELLOW}math (math.*) {Fore.WHITE}functions in your formula."""
        self.qTxtBinResolution = f"""
{Fore.MAGENTA}>>>{Fore.WHITE} What is the bin resolution for dataset {Fore.CYAN}%d{Fore.WHITE}? (e.g. resolution of your data)"""
        self.qTxtMultiGraph = f"""
{Fore.MAGENTA}>>>{Fore.WHITE} Do you want to plot multiple graphs? ({Fore.YELLOW}y/N{Fore.WHITE})"""
        self.qTxtMultiXAxis = f"""
{Fore.MAGENTA}>>>{Fore.WHITE} Do you want to use different x-axis for each subplot? ({Fore.YELLOW}y/N{Fore.WHITE})"""
        self.qTxtThreeDGraph = f"""
{Fore.MAGENTA}>>>{Fore.WHITE} Do you want to plot the graph in 3D? ({Fore.YELLOW}y/N{Fore.WHITE})"""    
        self.qTxtNumColXAxis = f"""
{Fore.MAGENTA}>>>{Fore.WHITE} How many columns are x-axes data in your input csv file?"""
        self.qTxtFetchXAxisColNum = f"""
{Fore.MAGENTA}>>>{Fore.WHITE} What is the column number of x-axis for your dataset %d?"""
        self.qTxtLegendName = f"""
{Fore.MAGENTA}>>>{Fore.WHITE} What is the %s name for dataset %d? """ 
        self.qTxtLabelName = f"""
{Fore.MAGENTA}>>>{Fore.WHITE} What is the label name of %s-axis? """    
        self.qTxtTitleName = f"""
{Fore.MAGENTA}>>>{Fore.WHITE} What is the title name of the subplot? """
        self.qTxtMainTitleName = f"""
{Fore.MAGENTA}>>>{Fore.WHITE} What is the main title name of the graph? """
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
Please type an integer or float. 
Make sure that Max. x > Min. x and Res. x > 0"""
        self.fTxtTypeCorrFormula = """
Please type a valid formula or function from 
numpy (np.*) or math (math.*) libraries. \n\n """
        self.fTxtNumXAxes = f"""
Please enter a number between {Fore.YELLOW}%d{Fore.WHITE} and {Fore.YELLOW}%d{Fore.WHITE} """
        self.fTxtDataSizeNoMatch = """
Please make sure that x and y data sizes match! """
        self.yTxtPlotType = f"""
{Fore.GREEN}Selected plot type is: {Fore.CYAN}%s """
        self.yTxtNumOfPlots = f"""
{Fore.GREEN}Number of plots to be graphed: {Fore.CYAN}%d """
        self.yTxtFileName = f"""
{Fore.GREEN}Your input file: {Fore.CYAN}%s {Fore.GREEN}is found. """
        self.yTxtFetchCol= f"""
{Fore.GREEN}Selected column for %s-axis: {Fore.CYAN}%s """
        self.yTxtEFetchCol= f"""
{Fore.GREEN}Selected column for errorbar: {Fore.CYAN}%s """
        self.yTxtDataFromFunction = f"""
{Fore.GREEN}Your inputs are accepted: \n\n %s: {Fore.CYAN}%s"""
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
        files = os.listdir(os.getcwd() + os.sep + config.defaultInputDir)
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
        elif self.processType == 'plotPlotType':
            print(self.qTxtTypeOfPlotPlot + self.qTxtDefault %printVal)
        elif self.processType == 'moreData':
            print(self.qTxtMoreData + self.qTxtDefault %printVal)
        elif self.processType == 'fetchInputData':
            print(self.qTxtFileName + self.qTxtDefault %printVal + self.qTxtSkipCsvDataFetch)
        elif self.processType == 'numOfPlots':
            print(self.qTxtNumOfPlots + self.qTxtDefault %printVal)
        elif self.processType == 'fetchColX':
            if printVal[0] == 0: # first run, do not ask whether user want to plot any more data
                print(self.qTxtFetchCol %'x' + self.fTxtTypeBetween %(self.minColNum, self.numData - 1) + self.qTxtDefault %printVal[1] + self.qTxtDataFromFunction)
            else:
                print(self.qTxtFetchCol %'x' + self.fTxtTypeBetween %(self.minColNum, self.numData - 1) + self.qTxtDefault %printVal[1] + self.qTxtDataFromFunction)
        elif self.processType == 'fetchColY':
            print(self.qTxtFetchCol %'y'+ self.fTxtTypeBetween %(self.minColNum, self.numData - 1) + self.qTxtDataFromFunction)
        elif self.processType == 'fetchColZ':
            print(self.qTxtFetchCol %'z' + self.fTxtTypeBetween %(self.minColNum, self.numData - 1) + self.qTxtDataFromFunction)
        elif self.processType == 'fetchErrorBar':
            print(self.qTxtFetchErrorCol + self.fTxtTypeBetween %(self.minColNum, self.numData - 1) + self.qTxtDataFromFunction)
        elif self.processType == 'getFuncXFromUser':
            if printVal[0] == 0: # first run, do not ask whether user want to plot any more data
                print(self.qTxtMinMaxResX + self.qTxtDefault %printVal[1:])
        elif self.processType == 'getFuncYFromUser':
            print(self.qTxtEnterFormula %('y', 'x') + self.qTxtDefault %printVal)
        elif self.processType == 'getFuncZFromUser':
            print(self.qTxtEnterFormula %('z', 'x, y')+ self.qTxtDefault %printVal)
        elif self.processType == 'getFuncEFromUser':
            print(self.qTxtEnterFormula %('e', 'x') + self.qTxtDefault %printVal)
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
        elif self.processType == 'getLegendNames':
            print(self.qTxtLegendName %(printVal[2], printVal[0]) + self.qTxtDefault %printVal[1])
        elif self.processType == 'getLabelX':
            print(self.qTxtLabelName %'x' + self.qTxtDefault %printVal)
        elif self.processType == 'getLabelY':
                print(self.qTxtLabelName %'y' + self.qTxtDefault %printVal)
                if self.plotSelect in {'line', 'scatter', 'line+scatter'}:
                    self.prevPlotSelect = self.plotSelect
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
        elif self.processType in 'plotPlotType':
            print(self.fTxtNotValid + self.fTxtTypeBetween %(self.minPlotPlotType, self.maxPlotPlotType) + self.fTxtDefault %printVal)
        elif self.processType == 'moreData':
            print(self.fTxtNotValid + self.qTxtSelectYN + self.fTxtDefault %printVal)
        elif self.processType == 'fetchInputData':
            print(self.fTxtNotValid + self.fTxtDefault %printVal)
        elif self.processType == 'fetchColX':
            print(self.fTxtNotValid + self.fTxtTypeBetween %(self.minColNum, self.numData - 1))
        elif self.processType == 'fetchColY':
            print(self.fTxtNotValid + self.fTxtDataSizeNoMatch + self.fTxtTypeBetween %(self.minColNum, self.numData - 1) + self.qTxtDataFromFunction)
        elif self.processType == 'fetchColZ':
            print(self.fTxtNotValid + self.fTxtDataSizeNoMatch + self.fTxtTypeBetween %(self.minColNum, self.numData - 1) + self.qTxtDataFromFunction)
        elif self.processType == 'fetchErrorBar':
            print(self.fTxtNotValid + self.fTxtDataSizeNoMatch + self.fTxtTypeBetween %(self.minColNum, self.numData - 1))
        elif self.processType in ['getFuncXFromUser', 'numOfPlots']:
            print(self.fTxtNotValid + self.fTxtTypeIntOrFloat + self.fTxtDefault %printVal)
        elif self.processType in 'getFuncYFromUser':
            print(self.fTxtNotValid + self.fTxtTypeCorrFormula + self.fTxtDefault %'x**2')
        elif self.processType in 'getFuncZFromUser':
            print(self.fTxtNotValid + self.fTxtTypeCorrFormula + self.fTxtDefault %'y**2')
        elif self.processType in 'getFuncEFromUser':
            print(self.fTxtNotValid + self.fTxtTypeCorrFormula + self.fTxtDefault %'np.random.random_sample(x)')
        elif self.processType in 'checkNumXAxis':
            print(self.fTxtNotValid + self.fTxtNumXAxes %(self.defaultNumXAxis, self.maxNumXAxis) + self.fTxtDefault %self.defaultNumXAxis)
        elif self.processType in 'fetchXAxisColNum':
            print(self.fTxtNotValid + self.fTxtNumXAxes %(0, self.numData - 1) + self.fTxtDefault % 0)
        elif self.processType in 'checkMultiGraph' or self.processType in 'checkMultiXAxis' or self.processType == 'checkThreeDGraph':
            print(self.fTxtNotValid + self.qTxtSelectYN + self.fTxtDefault %printVal)
    
    # =============================== Success messages on the terminal
    def printText_success(self, printType, printVal):
        if not printVal in self.undoCommands:     
            if self.processType == 'plotType':   
                print(self.yTxtPlotType %(printVal))
            elif self.processType == 'plotPlotType':   
                print(self.yTxtPlotType %(printVal))
            elif self.processType == 'numOfPlots':   
                print(self.yTxtNumOfPlots %printVal)
            elif self.processType == 'fetchInputData':
                print(self.yTxtFileName %printVal)
            elif self.processType == 'fetchColX':
                print(self.yTxtFetchCol %('x', printVal))
            elif self.processType == 'fetchColY':
                print(self.yTxtFetchCol %('y', printVal))
            elif self.processType == 'fetchColZ':
                print(self.yTxtFetchCol %('z', printVal))
            elif self.processType == 'fetchErrorBar':
                print(self.yTxtEFetchCol %printVal)
            elif self.processType in 'getFuncXFromUser':
                print(self.yTxtDataFromFunction %('x', printVal))
            elif self.processType in 'getFuncYFromUser':
                print(self.yTxtDataFromFunction %('y', printVal))
            elif self.processType in 'getFuncZFromUser':
                print(self.yTxtDataFromFunction %('z', printVal))
            elif self.processType in 'getFuncEFromUser':
                print(self.yTxtDataFromFunction %('e', printVal))
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
        else:
            pass
    # =============================== Print messages on the terminal
    def printText(self, printType, printVal):
    
        if printType == self.printQuestion:
            self.printText_question(printType, printVal)
        elif printType == self.printFailure:
            self.printText_failure(printType, printVal)
        elif printType == self.printSuccess:
            self.printText_success(printType, printVal)
        return 0
            
    # =============================== Incrementer to accept correct values for xmin, xmax and xres in x-axis of function plots
    def adjust_xInput_func(self): 
        self.counter_acceptUserInput += 1
        if self.counter_acceptUserInput == 3:
            self.counter_acceptUserInput = 0
    
    # =============================== Validate input data given by the user
    def checkUserInput(self, input):
        if self.processType == 'fetchColY' and input == '': # return default y column from csv if user pressed Enter
            input = self.defaultFetchColY
        try: 
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
    def fetchDefLabels(self, plots): 
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
        with open(config.defaultInputDir + os.sep + self.inputFile, 'r', encoding = config.defaultEncoding) as csvfile: 
            plots = csv.reader(csvfile, delimiter = config.defaultDelimeter)
            # Fetch data from each row
            for row in plots:
                self.data.append(row)
            self.transposeData()
            self.fetchDefLabels(plots)
            self.convDataToFloat()
    
    # =============================== Ask input file name from user      
    def askInputFileName(self):
        self.data = []
        # Get input file name from user
        self.printText(self.printQuestion, config.defaultInputFile)
        self.inputFile = self.acceptUserInput(config.defaultInputFile)
        if not self.inputFile in self.undoCommands:
            if not self.inputFile in ['s', 'S']:
                self.printText(self.printSuccess, self.inputFile)
                self.fetchInputData() # Fetch self.data from .csv file
            else:
                self.csvData = False
        self.nextFunc = 'askNumOfPlots'
        
    # =============================== Ask number of plots from user   
    def askNumOfPlots(self):
        # Ask num of plots type from user
        self.processType = 'numOfPlots'
        self.printText(self.printQuestion, self.defaultNumOfPlots)
        self.numOfPlots = self.acceptUserInput(self.defaultNumOfPlots)
        if not self.numOfPlots in self.undoCommands:
            self.nextFunc = 'askPlotType'
            self.printText(self.printSuccess, self.numOfPlots)
        else:
            self.numOfPlots = self.defaultNumOfPlots
            self.inputFile = config.defaultInputFile
            self.nextFunc = 'askInputFileName'
        
    # =============================== Reinitialize some variables  
    def main_reinitializeVars(self):
        # Reinitialize some vars
        self.yDataCounter = 0
        self.threeD = False
        self.fetchColX = []
        self.fetchColY = []
        self.fetchColZ = []
        self.legendName = []
        self.yLabel = []
        
    # =============================== Ask plot type from user      
    def askPlotType(self, i):
        # Select plot type
        self.processType = 'plotType'
        printVal = [i + 1, config.defaultPlotSelect]
        self.printText(self.printQuestion, printVal)
        self.plotSelect = self.acceptUserInput(config.defaultPlotSelect)
        if not self.plotSelect in self.undoCommands:
            self.prevCallFunc_askPlotType = False
            if not self.plotSelect == config.defaultPlotSelect:
                self.plotSelect = self.plotTypes[int(self.plotSelect) - 1] # - 1 to map user input to correct entry inside self.plotTypes[]. E.g. user input '3' will be mapped to '2' which corresponds to 'line' graph
            self.printText(self.printSuccess, self.plotSelect)
            self.threeD = True if self.plotSelect == '3d' else False
            if self.plotSelect == 'line||scatter||line+scatter':
                self.nextFunc = 'askPlotPlotType'
            else:
                self.nextFunc = 'askXData_csv'
        else:
            self.numOfPlots = self.defaultNumOfPlots
            self.plotSelect = ''
            self.nextFunc = 'askNumOfPlots'
            self.prevCallFunc_askPlotType = True
            self.plotPyt.resetPlot()
        prevCallFunc_plotPlotType = False
        
    # =============================== Ask plot type for each data set from user if line||scatter||line+scatter plot selected
    def askPlotPlotType(self):
        # Select plot type
        self.processType = 'plotPlotType'
        printVal = [config.defaultPlotPlotSelect]
        self.printText(self.printQuestion, printVal)
        userInput = self.acceptUserInput(config.defaultPlotPlotSelect)
        if userInput in self.undoCommands:
            self.nextFunc = 'askPlotType'
        else:
            self.plotPlotSelect.append(int(userInput))
            self.errorBar.append(True) if self.plotPlotSelect[-1] > 3 else self.errorBar.append(False) # Enable/disable errorBar
            self.nextFunc = 'askXData_csv'
            self.printText(self.printSuccess, self.plotPlotSelect)
        prevCallFunc_plotPlotType = True
        
    # =============================== Ask x-axis csv data from user      
    def askXData_csv(self):
        self.processType = 'fetchColX'
        printVal = [self.yDataCounter, self.defaultFetchColX]
        self.printText(self.printQuestion, printVal)
        self.fetchColX.append(self.acceptUserInput(self.defaultFetchColX))
        if self.plotSelect in ['box', 'cdf', 'histogram']: self.yDataCounter += 1
        if self.fetchColX[-1] in self.undoCommands:
            if self.prevCallFunc_plotPlotType: 
                self.nextFunc = 'askPlotType'
                self.plotSelect = ''
            else:
                self.nextFunc = 'askPlotPlotType'
                self.plotPlotSelect.pop()
                self.errorBar.pop()
            self.fetchColX.pop()
            if self.plotSelect in ['box', 'cdf', 'histogram']: self.yDataCounter -= 1
        else:
            if not self.fetchColX[-1] in ['f', 'F'] or not self.nextFunc == 'minX':
                self.nextFunc = 'askYZEData_csv'
                self.printText(self.printSuccess, self.fetchColX)
                if self.plotSelect in ['histogram']: # do not accept more than 1 x-axis data, no y-axis data needed
                    return True
            if self.fetchColX[-1] in ['f', 'F'] or self.nextFunc == 'minX':
                self.nextFunc = 'askXData_func'
                self.fetchColX.pop()
                self.fetchXFunc = True    
                self.fetchXFunc2 = True 
        
    # =============================== Ask y-, z-axis and errorbar csv data from user      
    def askYZEData_csv(self):
        if self.fetchXFunc is False:
            if not self.plotSelect in ['box', 'cdf', 'histogram']: # no need for y-axis data for bar plot
                self.processType = 'fetchColY'
                self.fetchCol_YZE(self.processType)
                if self.plotSelect == 'line||scatter||line+scatter' and self.errorBar[-1] == True: 
                    self.processType = 'fetchErrorBar'
                    self.fetchCol_YZE(self.processType)
            else:
                self.nextFunc = 'askLegendNames'
            if self.plotSelect == '3d':
                self.processType = 'fetchColZ'
                self.fetchCol_YZE(self.processType)
            self.prevCallFunc = False
            
    # =============================== Logic to fetch column number for y-, z-axis and errorbars 
    def fetchCol_YZE(self, processType):
        self.processType = processType
        if processType == 'fetchColY':
            self.prevCallFunc_E = False
            self.prevCallFunc_Y = True
            self.prevCallFunc_Z = False
            self.printText(self.printQuestion, self.defaultFetchColY)
            self.fetchColY.append(self.acceptUserInput(self.defaultFetchColY))
            self.yDataCounter += 1
            if self.fetchColY[-1] in self.undoCommands:
                self.nextFunc = 'askXData_csv'
                self.fetchColX.pop()
                self.fetchColY.pop()
                self.yDataCounter -= 1
                return None
            else:
                self.nextFunc = 'askLegendNames'
        elif processType == 'fetchColZ':
            self.prevCallFunc_E = False
            self.prevCallFunc_Y = False
            self.prevCallFunc_Z = True
            self.printText(self.printQuestion, self.defaultFetchColZ)
            self.fetchColZ.append(self.acceptUserInput(self.defaultFetchColZ))
            if self.fetchColZ[-1] in self.undoCommands:
                self.nextFunc = 'askXData_csv'
                self.fetchColX.pop()
                self.fetchColZ.pop()
                return None
            else:
                self.nextFunc = 'askLegendNames'
        else: # processType == 'fetchErrorBar':
            self.prevCallFunc_E = True
            self.prevCallFunc_Y = False
            self.prevCallFunc_Z = False
            self.printText(self.printQuestion, self.defaultFetchErrorBar)
            self.fetchColE.append(self.acceptUserInput(self.defaultFetchErrorBar))
            if self.fetchColE[-1] in self.undoCommands:
                self.nextFunc = 'askXData_csv'
                self.fetchColX.pop()
                self.fetchColE.pop()
                return None
            else:
                self.nextFunc = 'askLegendNames'
        if (processType in ['fetchColY', 'fetchErrorBar']) and (self.fetchColY[-1] in ['f', 'F']) or (self.fetchColE and self.fetchColE[-1] in ['f', 'F']):
            self.fetchColY.pop() if processType == 'fetchColY' else self.fetchColE.pop()
            self.fetchYFunc = True
            self.fetchYFunc2 = True
            self.nextFunc = 'askYEData_func'
            self.yDataCounter -= 1
        elif processType == 'fetchColZ' and self.fetchColZ[-1] in ['f', 'F']:
            self.fetchColZ.pop()
            self.fetchZFunc = True
            self.fetchZFunc2 = True
            self.nextFunc = 'askZData_func'
        else:
            if processType == 'fetchColY':
                self.printText(self.printSuccess, self.fetchColY) 
            elif processType == 'fetchColZ':
                self.printText(self.printSuccess, self.fetchColZ) 
            else:
                self.printText(self.printSuccess, self.fetchColE) 
        
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
            if self.nextFunc == 'askXData_func' or self.nextFunc == 'minX':
                print("Min. x: ")
                self.minX = self.acceptUserInput(self.defaultMinX)
                if self.minX in self.undoCommands:
                    if prevCallFunc_plotPlotType: 
                        self.nextFunc = 'askPlotType'
                        self.plotSelect = ''
                    else:
                        self.nextFunc = 'askPlotPlotType'
                        self.plotPlotSelect.pop()
                        self.errorBar.pop()
                    self.minX = self.defaultMinX
                else:
                    self.nextFunc = 'maxX'
                if self.minX in ['q', 'Q']:
                    return True
            if self.nextFunc == 'maxX':
                print("Max. x: ")
                self.maxX = self.acceptUserInput(self.defaultMaxX)
                if self.maxX in self.undoCommands:
                    self.nextFunc = 'minX'
                    self.minX = self.defaultMinX
                    self.maxX = self.defaultMaxX
                else:
                    self.nextFunc = 'resX'
            if self.nextFunc == 'resX':
                print("Res. x: ")
                self.resX = self.acceptUserInput(self.defaultResX)
                if self.resX in self.undoCommands:
                    self.nextFunc = 'maxX'
                    self.maxX = self.defaultMaxX
                    self.resX = self.defaultResX
                else:
                    self.nextFunc = 'computeX'
            if self.nextFunc == 'computeX':
                self.nextFunc = 'askYEData_func'
                self.x = np.arange(self.minX, self.maxX, self.resX)
                self.printText(self.printSuccess, self.x)
                self.data.append(self.x)
                self.fetchColX.append(len(self.data) - 1) # record at which index you saved the x data in self.data matrix
                if self.plotSelect in ['box', 'cdf', 'histogram']: self.yDataCounter += 1
                if self.plotSelect in ['histogram']: # do not accept more than 1 x-axis data, no y-axis data needed
                    return True
                if self.fetchColX[-1] in ['q', 'Q']:
                    self.fetchColX.pop()
                    if (self.plotSelect == '3d' and self.yDataCounter < 2):
                        print(f"{Fore.RED}You need to enter at least 2 data sets in order to plot 3D plot")
                    else:
                        return True
                return False

    # =============================== Ask y-axis func data from user      
    def askYEData_func(self):
        self.fetchYFunc = True
        self.fetchYFunc2 = True
        if not self.plotSelect in ['box', 'cdf', 'histogram'] and self.processType != 'fetchColZ': # no need for y-axis data for bar plot
            self.processType = 'getFuncYFromUser'
            self.fetchFunc_YE(self.processType)
            if (self.plotSelect == 'line||scatter||line+scatter' and self.errorBar[-1] == True):
                self.processType = 'getFuncEFromUser'
                self.fetchFunc_YE(self.processType)
                
    # =============================== Logic to fetch function for y-axis and errorbars 
    def fetchFunc_YE(self, processType):
        printVal = 'x**2' if processType == 'getFuncYFromUser' else 'np.random.random_sample(x)'
        self.printText(self.printQuestion, printVal)
        print("y(x): ") if processType == 'getFuncYFromUser' else 'e(x)'
        if processType == 'getFuncYFromUser':
            self.prevCallFunc_errorBar = False
            self.y = self.acceptUserInput(self.defaultY)
            if not self.y in self.undoCommands:
                self.nextFunc = 'askZData_func'
                self.printText(self.printSuccess, self.y)
                self.data.append(self.y)
                self.fetchColY.append(len(self.data) - 1) # record at which index you saved the x data in self.data matrix
                self.yDataCounter += 1
            else:
                self.nextFunc = 'resX'
                self.resX = self.defaultResX
                self.x = self.defaultX
                self.y = self.defaultY
                self.data.pop()
                self.fetchColX.pop()
                
        else: # errorbar function
            self.prevCallFunc_errorBar = True
            self.e = self.acceptUserInput(self.defaultE)
            if not self.e in self.undoCommands:
                self.nextFunc = 'askZData_func'
                self.printText(self.printSuccess, self.e)
                self.data.append(self.e)
                self.fetchColE.append(len(self.data) - 1) # record at which index you saved the x data in self.data matrix
            else: 
                self.nextFunc = 'resX'
                self.resX = self.defaultResX
                self.x = self.defaultX
                self.e = self.defaultE
                self.data.pop()
                self.fetchColX.pop()
        
    # =============================== Ask z-axis func data from user      
    def askZData_func(self):
        self.fetchZFunc = True
        self.fetchZFunc2 = True
        self.prevCallFunc = True
        if self.plotSelect == '3d':
            self.processType = 'getFuncZFromUser'
            printVal = 'y**2'
            self.printText(self.printQuestion, printVal)
            print("z(x, y): ")
            self.z = self.acceptUserInput(self.defaultZ)
            if not self.z in self.undoCommands:
                self.nextFunc = 'askLegendNames'
                self.printText(self.printSuccess, self.z)
                self.data.append(self.z)
                self.fetchColZ.append(len(self.data) - 1) # record at which index you saved the x data in self.data matrix
            else:
                self.nextFunc = 'askYEData_func'
                self.z = self.defaultZ
                self.data.pop()
                if self.prevCallFunc_errorBar:
                    self.e = self.defaultE
                    self.fetchColE.pop()
                else:
                    self.y = self.defaultY
                    self.fetchColY.pop()
                    self.yDataCounter -= 1
        else:
            self.nextFunc = 'askLegendNames'
    
    # =============================== Ask legend names of fetched data from user      
    def askLegendNames(self, i):
        # Fetch legend name(s)
        self.processType = 'getLegendNames'
        if self.plotSelect in ['box']:
            printVal = [i + 1, config.defaultLegendNames[i], 'xtick']
            self.printText(self.printQuestion, printVal) # send i instead of legend name to be able to print dataset # in printText()
            self.legendName.append(self.acceptUserInput(config.defaultLegendNames[i]))
            if self.legendName[-1] in self.undoCommands:
                self.legendName.pop()
                if self.prevCallFunc:
                    self.nextFunc = 'askYEData_func'
                    self.y = self.defaultY
                    self.data.pop()
                    self.fetchColY.pop()
                    self.yDataCounter -= 1
                else:
                    self.nextFunc = 'askYZEData_csv'
                    if self.prevCallFunc_E:
                        self.fetchColE.pop()
                    elif self.prevCallFunc_Y:
                        self.fetchColY.pop()
                        self.yDataCounter -= 1
                    elif self.prevCallFunc_Z: 
                        self.fetchColZ.pop()
            else:
                self.nextFunc = 'askMoreData'
                self.printText(self.printSuccess, self.legendName)
        elif self.plotSelect == '3d': 
            printVal = [i + 1, config.defaultLegendNames[i], 'legend']
            self.printText(self.printQuestion, printVal) # send i instead of legend name to be able to print dataset # in printText()
            self.legendName.append(self.acceptUserInput(config.defaultLegendNames[i]))
            if self.legendName[-1] in self.undoCommands:
                self.legendName.pop()
                if self.prevCallFunc:
                    self.nextFunc = 'askZData_func'
                    self.z = self.defaultZ
                    self.data.pop()
                    self.fetchColZ.pop()
                else:
                    self.nextFunc = 'askYZEData_csv'
                    if self.prevCallFunc_E:
                        self.fetchColE.pop()
                    elif self.prevCallFunc_Y:
                        self.fetchColY.pop()
                        self.yDataCounter -= 1
                    elif self.prevCallFunc_Z: 
                        self.fetchColZ.pop()
            else:
                self.nextFunc = 'askMoreData'
                self.printText(self.printSuccess, self.legendName)
        else:
            printVal = [i + 1, config.defaultLegendNames[i], 'legend']
            self.printText(self.printQuestion, printVal) # send i instead of legend name to be able to print dataset # in printText()
            self.legendName.append(self.acceptUserInput(config.defaultLegendNames[i]))
            if self.legendName[-1] in self.undoCommands:
                self.legendName.pop()
                if self.prevCallFunc:
                    self.nextFunc = 'askYEData_func'
                    self.y = self.defaultY
                    self.data.pop()
                    self.fetchColY.pop()
                    self.yDataCounter -= 1
                else:
                    self.nextFunc = 'askYZEData_csv'
                    if self.prevCallFunc_E:
                        self.fetchColE.pop()
                    elif self.prevCallFunc_Y:
                        self.fetchColY.pop()
                        self.yDataCounter -= 1
                    elif self.prevCallFunc_Z: 
                        self.fetchColZ.pop()
            else:
                self.nextFunc = 'askMoreData'
                self.printText(self.printSuccess, self.legendName)
        self.fetchXFunc = False
        self.fetchYFunc = False
        self.fetchZFunc = False
        
    # =============================== Ask whether user want to add more data to the plot
    def askMoreData(self):
        self.processType = 'moreData'
        printVal = [config.defaultMoreData]
        self.printText(self.printQuestion, printVal)
        self.moreData = self.acceptUserInput(config.defaultMoreData)
        if self.moreData in self.undoCommands:
            self.nextFunc = 'askLegendNames'
            self.moreData = True
            self.legendName.pop()
        elif self.plotSelect == 'line||scatter||line+scatter' and self.moreData:
            self.nextFunc = 'askPlotPlotType'
        elif self.moreData:
            self.nextFunc = 'askXData_csv'
        else:
            self.nextFunc = 'askXLabel'
        return self.moreData
            
    # =============================== Ask x-axis label name from user
    def askXLabel(self):    
        # Fetch x-label
        self.processType = 'getLabelX'
        if self.plotSelect == 'box':
            self.printText(self.printQuestion, config.defaultXLabel) # send i instead of legend name to be able to print dataset # in printText()
            self.xLabel = (self.acceptUserInput(config.defaultXLabel))
            if not self.xLabel in self.undoCommands:
                self.nextFunc = 'askBinRes'
                self.printText(self.printSuccess, self.xLabel)
                self.prevCallFunc_xLabel = False
            else:
                self.nextFunc = 'askMoreData'
                self.xLabel = config.defaultXLabel
                self.prevCallFunc_xLabel = True
        else:
            if not self.csvData or self.fetchXFunc2:
                self.printText(self.printQuestion, config.defaultXLabel) # send i instead of legend name to be able to print dataset # in printText()
                self.xLabel = (self.acceptUserInput(config.defaultXLabel))
            else:
                self.printText(self.printQuestion, self.defaultLabels[self.fetchColX[-1]]) 
                self.xLabel = self.acceptUserInput(self.defaultLabels[self.fetchColX[-1]])
            if not self.xLabel in self.undoCommands:
                self.nextFunc = 'askBinRes'
                self.printText(self.printSuccess, self.xLabel)
                self.prevCallFunc_xLabel = False
            else:
                self.nextFunc = 'askMoreData'
                self.xLabel = config.defaultXLabel
                self.prevCallFunc_xLabel = True
                
    # =============================== Ask bin resolution for histogram graphs from user
    def askBinRes(self):
        if (self.plotSelect == 'histogram'):
            self.processType = 'binResolution'
            self.printText(self.printQuestion, self.defaultBinRes)
            self.binRes = self.acceptUserInput(self.defaultBinRes)
            if not self.binRes in self.undoCommands:
                self.nextFunc = 'askYZLabel'
                self.printText(self.printSuccess, self.binRes)
                self.prevCallFunc_yLabel = False
            else:
                self.nextFunc = 'askXLabel'
                self.binRes = self.defaultBinRes
                self.xLabel = config.defaultXLabel
        else:
            self.nextFunc = 'askYZLabel'
            
        if self.prevCallFunc_yLabel == True:
            self.nextFunc = 'askXLabel'
            self.prevCallFunc_yLabel = False
        
    # =============================== Ask y- and z-axis label names from user
    def askYZLabel(self):
        if self.plotSelect in ['cdf', 'histogram', 'box']: config.multipleAxis = False
        if self.plotSelect == 'cdf':
            self.yLabel.append(config.cdfDefaultLabel)
            if self.yLabel[-1] in self.undoCommands:
                self.nextFunc = 'askBinRes'
                self.yLabel.pop()
                self.binRes = self.defaultBinRes
                self.prevCallFunc_yLabel = True
            else:
                self.nextFunc = 'askSubplotTitle'
                self.printText(self.printSuccess, self.yLabel)
        elif self.plotSelect == 'histogram':
            self.yLabel.append(config.histDefaultLabel)
            if self.yLabel[-1] in self.undoCommands:
                self.nextFunc = 'askBinRes'
                self.yLabel.pop()
                self.binRes = self.defaultBinRes
                self.prevCallFunc_yLabel = True
            else:
                self.nextFunc = 'askSubplotTitle'
                self.printText(self.printSuccess, self.yLabel)
        elif self.plotSelect == 'box':
            self.processType = 'getLabelY'
            if not self.csvData or self.fetchYFunc2:
                self.printText(self.printQuestion, config.defaultXLabel) # send i instead of legend name to be able to print dataset # in printText()
                self.yLabel.append(self.acceptUserInput(config.defaultXLabel)) # fetch x label to the y-axis
            else:
                self.printText(self.printQuestion, self.defaultLabels[self.fetchColX[-1]]) 
                self.yLabel.append(self.acceptUserInput(self.defaultLabels[self.fetchColX[-1]]))
            if self.yLabel[-1] in self.undoCommands:
                self.nextFunc = 'askBinRes'
                self.yLabel.pop()
                self.binRes = self.defaultBinRes
                self.prevCallFunc_yLabel = True
            else:
                self.nextFunc = 'askSubplotTitle'
                self.printText(self.printSuccess, self.yLabel)
        
        if not self.plotSelect in ['cdf', 'histogram', 'box']:
            # Fetch y-label
            config.multipleAxis = True if self.yDataCounter  > 1 and config.multipleAxis else False
            self.processType = 'getLabelY'
            if not config.multipleAxis:
                if not self.csvData or self.fetchYFunc2:
                    self.printText(self.printQuestion, config.defaultYLabel) # send i instead of legend name to be able to print dataset # in printText()
                    self.yLabel.append(self.acceptUserInput(config.defaultYLabel))
                else:
                    self.printText(self.printQuestion, self.defaultLabels[self.fetchColY[-1]]) 
                    self.yLabel.append(self.acceptUserInput(self.defaultLabels[self.fetchColY[-1]]))
                if self.yLabel[-1] in self.undoCommands:
                    self.nextFunc = 'askBinRes'
                    self.yLabel.pop()
                    self.binRes = self.defaultBinRes
                    self.prevCallFunc_yLabel = True
                else:
                    self.nextFunc = 'askSubplotTitle'
                    self.printText(self.printSuccess, self.yLabel)
            else: # Fetch y-label for the additional y-axes
                for j in range(self.yDataCounter):
                    if not self.csvData or self.fetchYFunc2:
                        self.printText(self.printQuestion, config.defaultYLabel) # send j instead of legend name to be able to print dataset # in printText()
                        self.yLabel.append(self.acceptUserInput(config.defaultYLabel)) # fetch x label to the y-axis
                    else:
                        self.printText(self.printQuestion, self.defaultLabels[self.fetchColY[j]]) 
                        self.yLabel.append(self.acceptUserInput(self.defaultLabels[self.fetchColY[j]]))
                    if self.yLabel in self.undoCommands:
                        self.nextFunc = 'askBinRes'
                        self.yLabel.pop()
                        self.binRes = self.defaultBinRes
                        self.prevCallFunc_yLabel = True
                    else:
                        self.nextFunc = 'askSubplotTitle'
                        self.printText(self.printSuccess, self.yLabel)
            if self.plotSelect == '3d':
                # set z-axis label
                self.processType = 'getLabelZ'
                if not self.csvData or self.fetchZFunc2:
                    self.printText(self.printQuestion, config.defaultZLabel) # send i instead of legend name to be able to print dataset # in printText()
                    self.zLabel = self.acceptUserInput(config.defaultZLabel)
                else:
                    self.printText(self.printQuestion, self.defaultLabels[self.fetchColZ[-1]]) 
                    self.zLabel = self.acceptUserInput(self.defaultLabels[self.fetchColZ[-1]])
                if self.zLabel in self.undoCommands:
                    self.nextFunc = 'askBinRes'
                    self.zLabel = 'z'
                    self.binRes = self.defaultBinRes
                    self.prevCallFunc_yLabel = True
                else:
                    self.nextFunc = 'askSubplotTitle'
                    self.printText(self.printSuccess, self.zLabel)
            self.fetchXFunc2 = False
            self.fetchYFunc2 = False
            self.fetchZFunc2 = False
            
    # =============================== Ask subplot title name from user
    def askSubplotTitle(self, i):
        if self.numOfPlots > 1: 
            # Fetch title name from user
            self.processType = 'getTitleName'
            mainTitle = False
            printVar = [mainTitle, config.defaultSubTitleNames[i]]
            self.printText(self.printQuestion, printVar) 
            self.title = self.acceptUserInput(config.defaultSubTitleNames[i])
            if not self.title in self.undoCommands:
                self.nextFunc = 'subplotDone'
                self.printText(self.printSuccess, self.title)
            else:
                self.nextFunc = 'askYZLabel'
                self.title = config.defaultSubTitleNames[i]
                if self.plotSelect == '3d':
                    self.zLabel = 'z'
                else:
                    self.yLabel.pop()
        else:
            self.nextFunc = 'subplotDone'
            
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
        while True: 
            if self.nextFunc == 'askInputFileName':
                self.processType = 'fetchInputData'
                self.askInputFileName()
                #print("progress a: %s" %self.nextFunc)
            elif self.nextFunc == 'askNumOfPlots':
                self.askNumOfPlots()
            elif self.nextFunc == 'askPlotType':
                self.initiatePlotter() # Initiate the plotter class
                self.plotPyt.prepPlot(self.numOfPlots) # prepare the plot environment
                self.main_reinitializeVars()
                #print("progress b: %s" %self.nextFunc)
                # main plot loop
                for i in range(self.numOfPlots):
                    while True: 
                        if self.nextFunc == 'askPlotType':
                            self.askPlotType(i)
                            #print("progress c: %s" %self.nextFunc)
                            if self.prevCallFunc_askPlotType: # go back to askNumOfPlots
                                break
                            # data generation loop
                        elif self.nextFunc in ['askXData_csv', 'askPlotPlotType', 'askMoreData']: 
                            while True:
                                if self.yDataCounter != 0 and self.nextFunc == 'askMoreData':
                                    if not self.askMoreData():
                                        break
                                if self.nextFunc == 'askPlotPlotType':
                                    self.askPlotPlotType()
                                    if self.nextFunc == 'askPlotType':
                                        break
                                        #print("progress d: %s" %self.nextFunc)
                                if self.csvData and self.nextFunc == 'askXData_csv':
                                    self.askXData_csv()
                                    #print("progress e: %s" %self.nextFunc)
                                if self.nextFunc == 'askYZEData_csv': 
                                    self.askYZEData_csv()
                                    #print("progress f: %s" %self.nextFunc)
                                if ((not self.csvData or self.fetchXFunc or self.fetchYFunc or self.fetchZFunc) and self.nextFunc in ['askXData_func', 'askYEData_func', 'askZData_func']) or (self.nextFunc == 'minX' or self.nextFunc == 'resX'): # generate data from function
                                    self.askXData_func()
                                    if self.nextFunc == 'askYEData_func':
                                        self.askYEData_func()
                                        #print("progress g: %s" %self.nextFunc)
                                    if self.nextFunc == 'askZData_func':
                                        self.askZData_func()
                                        #print("progress h: %s" %self.nextFunc)
                                if self.nextFunc == 'askLegendNames':
                                    self.askLegendNames(self.yDataCounter - 1)
                                    #print("progress i: %s, y data counter: %d" %(self.nextFunc, self.yDataCounter))
                        elif self.nextFunc == 'askXLabel':
                            self.askXLabel()
                            #print("progress k: %s" %self.nextFunc)
                        elif self.nextFunc == 'askBinRes':
                            self.askBinRes()
                            #print("progress l: %s" %self.nextFunc)
                        elif self.nextFunc == 'askYZLabel':
                            self.askYZLabel()
                            #print("progress m: %s" %self.nextFunc)
                        elif self.nextFunc == 'askSubplotTitle':
                            self.askSubplotTitle(i)
                            #print("progress n: %s" %self.nextFunc)
                            plotCounter = i
                        elif self.nextFunc == 'subplotDone': 
                            self.plotPyt.mainPlotter(plotCounter, self.numOfPlots, self.plotSelect, self.plotPlotSelect, self.yDataCounter, self.fetchColX, self.fetchColY, self.fetchColZ, self.fetchColE, self.legendName, self.binRes, self.data) # TODO: Why do I send self.numOfPlots???
                            self.plotPyt.plotConfigs(self.xLabel, self.yLabel, self.zLabel, self.threeD, self.title, self.numOfPlots, plotCounter, self.plotSelect, self.yDataCounter)
                            self.main_reinitializeVars()
                            #print("progress o: %s" %self.nextFunc)
                            if not self.nextFunc == 'askYZLabel':
                                if i == (self.numOfPlots - 1):
                                    self.nextFunc = 'askMainTitle'
                                else:
                                    self.nextFunc = 'askPlotType'
                                break
                        elif self.prevCallFunc_askPlotType: # go back to askNumOfPlots
                                break
            elif self.nextFunc == 'askMainTitle':     
                # Fetch title name from user
                self.askMainTitle()
                self.plotPyt.showPlot(self.title, self.numOfPlots)
                break
       
    # =============================== Initiate and Run the PlotPython Class
    def initiatePlotter(self):
        self.plotPyt = plotFuncs.plotPython()

# #################################### MAIN
task = userInteractions()
task.main() # Fetch self.data-related info from user
task.initiatePlotter()  