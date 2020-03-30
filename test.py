#!/usr/bin/env python3

import json
import toml 
import yaml

# Read YAML file
with open("config\config.yaml", 'r') as stream:
    data_loaded = yaml.safe_load(stream)

print(data_loaded['AWS']['Resources']['EC1']['hi'])
print(len(data_loaded['AWS']))
'''
with open("config\config.json") as json_data_file:
    data = json.load(json_data_file)
print(data['mysql']['host'])

config = configparser.ConfigParser()
configFolder = 'config' + os.sep
config.read(configFolder + 'config.ini')
#print(config.sections())
#print(config.options(config.sections()[1]))
#print(config['PLOT2']['nasilsin'])
#print(config.get('PLOT2', 'nasilsin'))
#print(config.get('PLOT2', 'nasilsin'))
plotType, plotNum = [], []


for i in range(1, len(config.sections()) - 1):
    plotType.append(config['PLOT' + str(i + 1)]['deneme'])
    plotNum.append(config['PLOT' + str(i + 1)]['nasilsin'])

print(plotType)
print(plotType[0].split(','))
print(plotType[1].split(','))
print(plotNum)
print(plotNum[0].split(','))
print(plotNum[1].split(','))
print(plotNum[1].split(',')[3])
print(plotNum[1][4])
'''