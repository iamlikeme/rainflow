import unittest, rainflow

class TestRainflowCounting(unittest.TestCase):
    series = [0, -2, 1, -3, 5, -1, 3, -4, 4, -2, 0]
    cycles = [(3, 0.5), (4, 1.5), (6, 0.5), (8, 1.0), (9, 0.5)]
    
    def test_rainflow_counting(self):
        self.assertItemsEqual(rainflow.count_cycles(self.series), self.cycles)
    