# -*- coding: utf-8 -*-
"""
Created on Mon Dec 10 09:26:51 2018

@author: Geoff
"""

import timeit

def test_1():
    cycles1 = rainflow.count_cycles(dfSmall['SG1'].values, left=True, right=True)
    ranges = [delta for delta, count in cycles1]
    counts = [count for delta, count in cycles1]
    cycles_nph = np.histogram(ranges, weights=counts, bins=37)
    
    
def test_2():
    cycles2 = count_cycles(dfSmall['SG1'].values, left=True, right=True, nbins=37)
    
print(timeit.timeit(test_1, number=1))
print(timeit.timeit(test_2, number=1))
print(timeit.timeit(test_1, number=1))
print(timeit.timeit(test_2, number=1))

# results using consecutive single runs with decimated dfDecStresses:
# test_1: 1.86
# test_2: 1.52
# test_1: 1.84
# test_2: 1.53

# results using consecutive single runs with dfDecStresses:
# test_1: 16.89
# test_2: 12.78
# test_1: 16.98
# test_2: 13.05

# results using consecutive single runs with dfStresses:
# test_1: 238.1
# test_2: 306.4
# test_1: 242.3
# test_2: 301.7
