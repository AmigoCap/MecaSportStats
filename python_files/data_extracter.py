#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 21 16:33:44 2019

@author: gabin
"""

import json

def json_extracter(data): #data should be a string like : 'data.json', the function returns data and events
    with open(data) as json_file:  
        data = json.load(json_file)
        events=data['events']
    return(data,events)