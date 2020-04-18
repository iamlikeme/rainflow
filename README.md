Rainflow
========

[![Build Status](https://travis-ci.org/iamlikeme/rainflow.svg?branch=master)](https://travis-ci.org/iamlikeme/rainflow)

`rainflow` is a Python implementation of the ASTM E1049-85 rainflow cycle counting
algorythm for fatigue analysis. Supports both Python 2 and 3.

Installation
------------

`rainflow` is available [on PyPI](https://pypi.org/project/rainflow/):

```
pip install rainflow
```

and [on conda-forge](https://github.com/conda-forge/rainflow-feedstock):

```
conda install rainflow --channel conda-forge
```

Usage
-----

Let's generate a sample time series.
Here we simply generate a list of floats but `rainflow` works
with any sequence of numbers, including numpy arrays and pandas Series.

```python
from math import sin, cos

time = [4.0 * i / 200 for i in range(200 + 1)]
signal = [0.2 + 0.5 * sin(t) + 0.2 * cos(10*t) + 0.2 * sin(4*t) for t in time]
```

Function `count_cycles` returns a sorted list of ranges and the corresponding
number of cycles:

```python
import rainflow

rainflow.count_cycles(signal)
# Output
[(0.04258965150708488, 0.5),
 (0.10973439445727551, 1.0),
 (0.11294628078612906, 0.5),
 (0.2057106991158965, 1.0),
 (0.21467990941625242, 1.0),
 (0.4388985979776988, 1.0),
 (0.48305748051348263, 0.5),
 (0.5286423866535466, 0.5),
 (0.7809330293159786, 0.5),
 (1.4343610172143002, 0.5)]
```

Cycle ranges can be binned or rounded to a specified number of digits
using optional arguments *binsize*, *nbins* or *ndigits*:

```python
rainflow.count_cycles(signal, binsize=0.5)
# Output
[(0.5, 5.5), (1.0, 1.0), (1.5, 0.5)]

rainflow.count_cycles(signal, ndigits=1)
# Output
[(0.0, 0.5),
 (0.1, 1.5),
 (0.2, 2.0),
 (0.4, 1.0),
 (0.5, 1.0),
 (0.8, 0.5),
 (1.4, 0.5)]
```

Full information about each cycle, including mean value, can be obtained
using the `extract_cycles` function:

```python
for rng, mean, count, i_start, i_end in rainflow.extract_cycles(signal): 
    print(rng, mean, count, i_start, i_end) 
# Output             
0.04258965150708488 0.4212948257535425 0.5 0 3
0.11294628078612906 0.38611651111402034 0.5 3 13
...
0.4388985979776988 0.18268137509849586 1.0 142 158
1.4343610172143002 0.3478109852897205 0.5 94 200
```

Running tests
-------------

```
pip install .[dev]
pytest
```
