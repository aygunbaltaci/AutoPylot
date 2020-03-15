#!/usr/bin/env python3

import configparser


config = configparser.ConfigParser()

config.read('config.ini')
print(config.sections())
print(config.options('PLOT'))
print(config.get('DEFAULT', 'deneme'))
print(config.get('PLOT2', 'nasilsin'))
a = config.get('PLOT2', 'nasilsin').split(',')
print(a)