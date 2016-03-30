import unittest, rainflow, random, itertools

class TestRainflowCounting(unittest.TestCase):
    # Load series and corresponding cycle counts from ASTM E1049-85
    series = [0, -2, 1, -3, 5, -1, 3, -4, 4, -2, 0]
    cycles = [(3, 0.5), (4, 1.5), (6, 0.5), (8, 1.0), (9, 0.5)]
    
    def test_rainflow_counting(self):
        self.assertEqual(rainflow.count_cycles(self.series), self.cycles)
    
    
    def test_rainflow_ndigits(self):
        series = [x + 0.01 * random.random() for x in self.series]
        self.assertNotEqual(rainflow.count_cycles(series), self.cycles)
        self.assertEqual(rainflow.count_cycles(series, ndigits=1), self.cycles)
	
    def test_series_with_zero_derivatives(self):
    	series = itertools.chain(*([x, x] for x in self.series))
    	self.assertEqual(rainflow.count_cycles(series), self.cycles)
    	
