# -*- coding: utf-8 -*-
"""
Created on Fri Dec  3 23:41:48 2021

@author: a66851
"""

## Modules nécessaires

import itertools as it
import random as rnd
import time

## Opérations élémentaires entre 2 entiers $a$ et $b$ avec $a \ge b$

def operations(a, b):
    yield '+', a + b
    if a > b:
        yield '-', a - b
    yield 'x', a * b
    if a % b == 0:
        yield '/', a / b
                
## Solveur (Propose la première solution trouvée ou alors un compte parmi les plus proche)

def LeCompteEstBon(u, code, result, solutions):
    result_temp, code_temp = "", -1000000000
    if(len(solutions)) == 0:
        if len(u) > 1:
            # set(it.combinations(u,2)) attemps to create the pair of elements in list u
            for x, y in set(it.combinations(u,2)): 
                a, b = (x, y) if x >= y else (y, x)
#op represents to operations and result represents for the result after execution operations
                for op, calculation in operations(a, b):  
                    operat = '%d %s %d = %d \n' % (a, op, b, calculation)
                    if calculation == code:
                        result += operat
                        solutions.append(result)
                        stop = time.time()
                        print(result)
                        print('CPU : %9.3f sec.' % (stop-start))
                    elif abs(calculation-code) < abs(code_temp-code):
                        result_temp = result + operat
                        code_temp = calculation
                    else:
                        u1 = u + [calculation]
                        u1.remove(a)
                        u1.remove(b)
                        LeCompteEstBon(u1, code, result + operat, solutions)   

                
## Programme principal

#u, code = jeu()
u = [13,19,29,43,47,53,61]
code = 10921141
print('\nu, code = %s, %d\n' % (u, code))


start = time.time()
solutions = []
LeCompteEstBon(u, code, "", solutions)
if len(solutions) == 0:
    print('There is no solution for this problem')
    ##print('CPU : %9.3f sec.' % (stop-start))
