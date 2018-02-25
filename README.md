Rainflow
========

Rainflow is a Python implementation of the rainflow cycle counting algorythm
for fatigue analysis according to ASTM E1049-85. No dependencies beside Python's
standard library. Supports both Python 2 and 3.

Usage
-----
Let's generate a sample time series of some load. Here we create a numpy array but any iterable of numbers would work:
```python
>>> import numpy as np
>>> x = np.linspace(0, 4, 200)
>>> y = 0.2 + 0.5 * np.sin(x) + 0.2 * np.cos(10*x) + 0.2 * np.sin(4*x)
```

Function `count_cycles` returns a sorted list of the load ranges and the corresponding
number of cycles:
```python
>>> import rainflow
>>> rainflow.count_cycles(y)
    [(0.11022406179686783, 1.0), (0.11316419853821802, 0.5), (0.20607635324664902, 1.0),
     (0.2148070281383265, 0.5), (0.36749670533564682, 0.5), (0.4389628182518176, 0.5),
     (0.48294318988133728, 0.5), (0.52799626197601901, 0.5), (0.78150280937784777, 0.5),
     (1.102640610792428, 0.5)]
```

Not interested in all the decimals? Use *ndigits*:
```python
>>> rainflow.count_cycles(y, ndigits=2)
    [(0.11, 1.5), (0.21, 1.5), (0.37, 0.5), (0.44, 0.5), (0.48, 0.5), (0.53, 0.5),
     (0.78, 0.5), (1.1, 0.5)]
```

If you need more detailed output, like cycle lows, highs or means, use `extract_cycles`:
```python
>>> for low, high, mult in rainflow.extract_cycles(y):
...     mean = 0.5 * (high + low)
...     rng = high - low
```

Running tests
-------------
```
python -m unittest tests/*.py
```
