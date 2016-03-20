import unittest
import rainflow


class TestHalfCycle(unittest.TestCase):
    a = [1, -1, 2, -2, 2, -3, 2]
    
    def test_init(self):
        hc = rainflow.HalfCycle(self.a, 0)
        self.assertEqual(hc.index[-1], 2,
            msg="Half-cycle should terminate at a greater positive peak")
        self.assertEqual(hc.values[0], 1)
        self.assertEqual(hc.values[-1], -1)
    
    def test_terminates_at_input_end(self):
        hc = rainflow.HalfCycle(self.a, 2)
        self.assertEqual(hc.index[-1], 6,
            msg="Half-cycle should terminate at the end of the input list")
        self.assertEqual(hc.values[0], 2)
        self.assertEqual(hc.values[-1], -3)
    
    def test_start_positive(self):
        self.assertRaises(ValueError, rainflow.HalfCycle, self.a, 1)
    
    def test_clip(self):
        hc1 = rainflow.HalfCycle(self.a, 2)
        hc2 = rainflow.HalfCycle(self.a, 4)
        clipped = hc2.clip(hc1)
        self.assertTrue(clipped)
        self.assertEqual(hc2.index[-1], 5)
        self.assertEqual(hc2.values[0], 2)
        self.assertEqual(hc2.values[-1], -2)
