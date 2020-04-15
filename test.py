#!/usr/bin/env python3

import json
import toml 
import yaml

class ParentClass(object):

    def __init__(self):
        self.x = [1,2,3]

    def test(self):
        print('Im in parent class')
    
    def openFile(self):
        try:
            with open('config/' + 'mainconfig.' + 'yaml', 'r') as input_data:
                data = yaml.safe_load(input_data)
        except FileNotFoundError:
            print("File does not exist")
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


class ChildClass(ParentClass):

    def test(self):
        super(ChildClass, self).test()
        print("Value of x = %s" %self.x)


x = ChildClass()
x.test()
y = ParentClass()
print(y.openFile())