Rainflow
========

Rainflow is a Python implementation of the rainflow cycle counting algorythm.

Basic usage:
```python
# Generate sample data
import numpy as np
x = np.linspace(0, 10, 200)
y = 0.2 + 0.5 * np.sin(x) + 0.8 * np.cos(10*x) + 0.2 * np.sin(4*x)

# Extract cycles from y
import rainflow
cycles = rainflow.extract_cycles(y)
```
