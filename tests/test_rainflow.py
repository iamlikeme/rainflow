import unittest, rainflow, random, itertools, pkg_resources


class TestRainflowCounting(unittest.TestCase):
    # Load series and corresponding cycle counts from ASTM E1049-85
    series = [0, -2, 1, -3, 5, -1, 3, -4, 4, -2, 0]
    cycles = [(3, 0.5), (4, 1.5), (6, 0.5), (8, 1.0), (9, 0.5)]
    # tests for nbins argument
    cycles_nbins_1 = [(0.0, 4)]
    cycles_nbins_2 = [(0.0, 2), (4.5, 2)]
    cycles_nbins_5 = [(3, 0.5), (4, 1.5), (6, 0.5), (8, 1.0), (9, 0.5)]
    cycles_nbins_9 = [(0.0, 0), (1.0, 0), (2.0, 0), (3.0, 0.5), (4.0, 1.5),
                        (5.0, 0), (6.0, 0.5), (7.0, 0), (8.0, 1.5)]
    cycles_nbins_10 = [(0.0, 0), (0.9, 0), (1.8, 0), (2.7, 0.5),
                       (3.6, 1.5), (4.5, 0), (5.4, 0.5), (6.3, 0),
                       (7.2, 1.0), (8.1, 0.5)]
    
    # tests for bin_size argument
    cycles_binsize_1 = [(0.0, 0), (1.0, 0), (2.0, 0), (3.0, 0.5), (4.0, 1.5),
                        (5.0, 0), (6.0, 0.5), (7.0, 0), (8.0, 1.5)]
    cycles_binsize_2 = [(0, 0), (2, 0.5), (4, 1.5), (6, 0.5), (8, 1.5)]
    cycles_binsize_3 = [(0, 0), (3, 2.0), (6, 2.0)]
    cycles_binsize_5 = [(0, 2.0), (5, 2.0)]
    cycles_binsize_9 = [(0.0, 4)]
    cycles_binsize_10 = [(0.0, 4)]
    

    def test_lows_and_highs_sorted(self):
        self.assertTrue(all(
            low <= high
            for low, high, mult in rainflow.extract_cycles(self.series)
        ))

    def test_rainflow_counting(self):
        self.assertEqual(
            rainflow.count_cycles(self.series),
            self.cycles,
        )
        self.assertEqual(
            rainflow.count_cycles(self.series[1:-1], left=True, right=True),
            self.cycles,
        )
        self.assertEqual(
            rainflow.count_cycles(self.series[1:], left=True),
            self.cycles,
        )
        self.assertEqual(
            rainflow.count_cycles(self.series[:-1], right=True),
            self.cycles,
        )

    def test_rainflow_ndigits(self):
        series = [x + 0.01 * random.random() for x in self.series]
        self.assertNotEqual(rainflow.count_cycles(series), self.cycles)
        self.assertEqual(rainflow.count_cycles(series, ndigits=1), self.cycles)

    def test_rainflow_nbins(self):
        self.assertEqual(
            rainflow.count_cycles(self.series, left=True, right=True, nbins=1),
            self.cycles_nbins_1,
        )
        self.assertEqual(
            rainflow.count_cycles(self.series, left=True, right=True, nbins=2),
            self.cycles_nbins_2,
        )
        self.assertEqual(
            rainflow.count_cycles(self.series, left=True, right=True, nbins=5),
            self.cycles_nbins_5,
        )
        self.assertEqual(
            rainflow.count_cycles(self.series, left=True, right=True, nbins=9),
            self.cycles_nbins_9,
        )
        self.assertEqual(
            rainflow.count_cycles(self.series, left=True, right=True, nbins=10),
            self.cycles_nbins_10,
        )

    def test_rainflow_binsize(self):
        self.assertEqual(
            rainflow.count_cycles(self.series, left=True, right=True, binsize=1),
            self.cycles_binsize_1,
        )
        self.assertEqual(
            rainflow.count_cycles(self.series, left=True, right=True, binsize=2),
            self.cycles_binsize_2,
        )
        self.assertEqual(
            rainflow.count_cycles(self.series, left=True, right=True, binsize=3),
            self.cycles_binsize_3,
        )
        self.assertEqual(
            rainflow.count_cycles(self.series, left=True, right=True, binsize=5),
            self.cycles_binsize_5,
        )
        self.assertEqual(
            rainflow.count_cycles(self.series, left=True, right=True, binsize=9),
            self.cycles_binsize_9,
        )
        self.assertEqual(
            rainflow.count_cycles(self.series, left=True, right=True, binsize=10),
            self.cycles_binsize_10,
        )

    def test_series_with_zero_derivatives(self):
    	series = itertools.chain(*([x, x] for x in self.series))
    	self.assertEqual(rainflow.count_cycles(series), self.cycles)

    def test_order_of_remaining_halves(self):
        cycle_ref = [0.5, 0.5, 0.5, 1.0, 0.5, 0.5, 0.5, 0.5, 0.5]
        mean_ref = [-1.0, -0.5, -1.0, 1.0, 1.0, 0.5, 0.0, 1.0, -1.0]

        cycles = []
        means = []
        for low, high, mult in rainflow.extract_cycles(self.series, True, True):
            cycles.append(mult)
            mean = 0.5 * (high + low)
            means.append(mean)

        self.assertEqual(cycles, cycle_ref)
        self.assertEqual(means, mean_ref)


class TestDistribution(unittest.TestCase):

    def test_version(self):
        dist = pkg_resources.get_distribution("rainflow")
        self.assertEqual(dist.version, rainflow.__version__)
