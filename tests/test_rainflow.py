import unittest, rainflow, random, itertools, pkg_resources, numpy


class TestRainflowCounting(unittest.TestCase):
    # Load series and corresponding cycle counts from ASTM E1049-85
    series = [0, -2, 1, -3, 5, -1, 3, -4, 4, -2, 0]
    cycles = [(3, 0.5), (4, 1.5), (6, 0.5), (8, 1.0), (9, 0.5)]

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

    def test_series_with_zero_derivatives(self):
    	series = itertools.chain(*([x, x] for x in self.series))
    	self.assertEqual(rainflow.count_cycles(series), self.cycles)

    def test_remaining_halfs(self):
        refcase = [0.60727647, 0.14653493, 0.19643957, 0.56821631, 0.88833878, 0.29612997,
                   0.59539649, 0.6996683, 0.10524973, 0.12334626, 0.68401331, 0.85985292,
                   0.73141117, 0.36808646, 0.94015761, 0.85626572, 0.76956161, 0.49777263,
                   0.54066458, 0.45931667, 0.82204694, 0.76816398, 0.66417278, 0.62238591,
                   0.61302659, 0.0158001, 0.35254166, 0.54150519, 0.14868205, 0.91848263,
                   0.8989403, 0.90866213, 0.831834, 0.48128077, 0.60999729, 0.78850529,
                   0.67725795, 0.76098028, 0.96626931, 0.91693159, 0.19347573, 0.4920361,
                   0.16060596, 0.10603582, 0.0017221, 0.6250337, 0.43623379, 0.54612575,
                   0.00411415, 0.91371242, 0.08600793, 0.77993431, 0.89695114, 0.43309567,
                   0.70051438, 0.05484055, 0.0673957, 0.68068416, 0.12452928, 0.00811467,
                   0.33861137, 0.61719287, 0.49407856, 0.8300253, 0.29934456, 0.7107892,
                   0.38225825, 0.02715285, 0.0189073, 0.68926121, 0.46134276, 0.25709821,
                   0.46942654, 0.68086762, 0.3117921, 0.89299606, 0.43332419, 0.04576419,
                   0.09044587, 0.28137508, 0.365343, 0.94461639, 0.48949621, 0.03472242,
                   0.79210514, 0.94612641, 0.25696703, 0.61546048, 0.04270415, 0.6681445,
                   0.79452558, 0.41156153, 0.4671666, 0.01783284, 0.8529705, 0.56580293,
                   0.62133836, 0.74723755, 0.28597705, 0.7421038]

        cycle_ref = [0.5000, 1.0000, 0.5000, 1.0000, 0.5000, 1.0000,
                     1.0000, 0.5000, 1.0000, 1.0000, 1.0000, 1.0000,
                     0.5000, 1.0000, 0.5000, 1.0000, 1.0000, 1.0000,
                     1.0000, 1.0000, 1.0000, 1.0000, 1.0000, 1.0000,
                     1.0000, 1.0000, 1.0000, 1.0000, 1.0000, 1.0000,
                     1.0000, 1.0000, 0.5000, 0.5000, 0.5000, 0.5000,
                     0.5000, 0.5000]

        amp_ref = [0.2304, 0.2018, 0.3709, 0.2459, 0.3915, 0.0214,
                   0.1814, 0.4175, 0.1964, 0.0049, 0.0556, 0.2186,
                   0.4622, 0.1493, 0.4752, 0.0549, 0.3105, 0.1337,
                   0.4055, 0.3129, 0.0616, 0.2057, 0.1845, 0.2161,
                   0.4056, 0.4236, 0.4528, 0.4549, 0.1792, 0.0278,
                   0.3759, 0.0907, 0.4823, 0.4722, 0.4641, 0.4176,
                   0.2835, 0.2281]

        mean_ref = [0.3769, 0.4979, 0.5174, 0.6140, 0.4968, 0.5192,
                    0.6407, 0.5227, 0.3451, 0.9038, 0.7329, 0.6999,
                    0.4780, 0.3428, 0.4910, 0.4912, 0.3146, 0.5668,
                    0.4915, 0.3678, 0.5556, 0.5051, 0.4963, 0.4732,
                    0.4245, 0.4694, 0.4609, 0.4897, 0.4362, 0.4394,
                    0.4186, 0.6565, 0.4840, 0.4739, 0.4820, 0.4354,
                    0.5695, 0.5140]

        cycles = []
        amps = []
        means = []
        for low, high, mult in rainflow.extract_cycles(refcase, True, True):
            cycles.append(mult)
            amp = numpy.round(high - 0.5 * (high + low), 4)
            amps.append(amp)
            mean = numpy.round(0.5 * (high + low), 4)
            means.append(mean)

        assert numpy.array_equal(cycles, cycle_ref)
        assert numpy.array_equal(amps, amp_ref)
        assert numpy.array_equal(means, mean_ref)


class TestDistribution(unittest.TestCase):

    def test_version(self):
        dist = pkg_resources.get_distribution("rainflow")
        self.assertEqual(dist.version, rainflow.__version__)
