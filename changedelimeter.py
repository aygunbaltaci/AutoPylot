#!/usr/bin/env python3
import csv

reader = list(csv.reader(open('inputFiles/input.csv', "rU"), delimiter='\t'))
writer = csv.writer(open('inputFiles/input2.csv', 'w'), delimiter=',')
writer.writerows(row for row in reader)