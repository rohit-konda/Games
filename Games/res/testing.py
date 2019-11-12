#!/usr/bin/env python
"""
Tutorial example for computing price of anarchy for a class of resource allocation games
"""

from computable import *


players = ['Alice', 'Bob', 'Carolyn', 'Dmitri']
res = [4, 9, 2, 5, 8, 7, 9, 3, 6, 7]
n = len(players)
strategies = [[(), ], [(), ], [(), ], [(), ]]
p = .5
w = [1 - (1-p)**j for j in range(n+1)]
f = [0] + [p*(1-p)**(j-1) for range(1, n+1)]



