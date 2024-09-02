# -*- coding: utf-8 -*-
"""
Created on Mon May  6 23:04:44 2024

@author: dangt
"""

# create a dictionary to store telephone keypad mappings
telephone = {
    '2': ['A', 'B', 'C'],
    '3': ['D', 'E', 'F'],
    '4': ['G', 'H', 'I'],
    '5': ['J', 'K', 'L'],
    '6': ['M', 'N', 'O'],
    '7': ['P', 'Q', 'R', 'S'],
    '8': ['T', 'U', 'V'],
    '9': ['W', 'X', 'Y', 'Z'],
    '0': [' ']
}
frequency = {
    '2': [],
    '3': [],
    '4': [],
    '5': [],
    '6': [],
    '7': [],
    '8': [],
    '9': [],
    '0': []
}
result = ''
s = open('sw2014-ms98-a-trans.txt').read()
s = s.upper()
# count the number of alphabet character in given string
for key in telephone:
    if(key!= '0'):
        for i in range(len(telephone[key])):
            frequency[key].append(s.count(telephone[key][i]))
# Rearrange the alphabet in each key respect to most appearance to least appearance
for key in telephone:
    if(key!= '0'):
        for i in range(len(telephone[key])):
            for j in range(i+1,len(telephone[key])):
                if(frequency[key][j] > frequency[key][i]):
                    frequency[key][i],frequency[key][j] = frequency[key][j],frequency[key][i]
                    telephone[key][i],telephone[key][j] = telephone[key][j],telephone[key][i]
# Transfer the alphabet string to number string
for i in range(len(s)):
    for key in telephone:
        if(s[i] in telephone[key]):
            result = result+key*(telephone[key].index(s[i])+1)
            if(i < len(s)-1): 
                if(s[i+1] in telephone[key]  and key!=0):
                    result = result+'_'
            break       
print(result)
