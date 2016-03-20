import unittest, rainflow
from math import sin, cos

def f(x):
    return 0.2 + 0.5 * sin(x) + 0.2 * sin(4*x) + 0.8 * cos(10*x)

x = [0.01 * i for i in range(250)]
y = map(f, x)

# Expected local peaks to be observed in y
peaks = [1.010, -0.258, 1.411, -0.313, 1.286, -0.104, 1.665, -0.084, 1.180]

# Expected half-cycles to be extracted from y
halfcycles = [
    (peaks[0] - peaks[1]),
    (peaks[1] - peaks[6]),
    (peaks[2] - peaks[3]),
    (peaks[3] - peaks[2]),
    (peaks[4] - peaks[5]),
    (peaks[5] - peaks[4]),
    (peaks[6] - peaks[7]),
    (peaks[7] - peaks[8]),
    ]

# Expected full cycles to be extracted from y
cycles = [1.268, 1.390, 1.724, 1.923]



class TestLocalExtrema(unittest.TestCase):
    def test_local_extrema(self):
        for expected, i in zip(peaks, rainflow.local_extrema(y)):
            actual = y[i]
            self.assertAlmostEqual(expected, actual, delta=0.001)
    

class TestExtractHalfCycles(unittest.TestCase):    
    def test_extract_half_cycles(self):
        _expected = sorted(halfcycles)
        _actual = sorted(rainflow.extract_halfcycles(y))
        for expected, actual in zip(_expected, _actual):
            self.assertAlmostEqual(expected, actual, delta=0.001)
        

class TestCombineHalfCycles(unittest.TestCase):
    def test_combine_halfcycles(self):
        halfcycles = [-2.5, -2.1, -1.5, -1.0, 1.2, 1.5, 2.5]
        expected_full = [1.5, 2.5]
        expected_residual = [-2.1, -1.0, 1.2]
        actual_full, actual_residual = rainflow.combine_halfcycles(halfcycles)
        self.assertEqual(2, len(actual_full))
        self.assertEqual(3, len(actual_residual))
        for expected, actual in zip(expected_full, sorted(actual_full)):
            self.assertEqual(expected, actual)
        for expected, actual in zip(expected_residual, sorted(actual_residual)):
            self.assertEqual(expected, actual)
            
        
class TestConvertHalfCycles(unittest.TestCase):
    def test_convert_residual_halfcycles(self):
        residual = [-3.2, 3.1, -2.5, 2.6, -1.3]
        combined = rainflow.convert_residual_halfcycles(residual)
        self.assertEqual(3, len(combined))
        for expected, actual in zip([1.3, 2.6, 3.2], sorted(combined)):
            self.assertEqual(expected, actual)


class TestExtractCycles(unittest.TestCase):
    def test_extract_cycles(self):
        extracted = rainflow.extract_cycles(y)
        self.assertEqual(4, len(extracted))
        for expected, actual in zip(cycles, sorted(extracted)):
            self.assertAlmostEqual(expected, actual, delta=0.001)

