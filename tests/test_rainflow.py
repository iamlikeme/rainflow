import itertools
import pytest
import rainflow
import random
import math

try:
    from importlib import metadata as importlib_metadata
except ImportError:
    import importlib_metadata as importlib_metadata

# A test case is a tuple containing the following items:
#  - a list representing a time series
#  - a list of tuples, each containing:
#    cycle range, cycle mean, count (0.5 or 1.0), start index, end index
#  - a list of tuples, each containing: cycle range, cycles
#  - a boolean that indicates whether range and mean values
#    are approximate (True) or exact (False)
TEST_CASE_1 = (
    [-2, 1, -3, 5, -1, 3, -4, 4, -2],
    [
        (3, -0.5, 0.5, 0, 1),
        (4, -1.0, 0.5, 1, 2),
        (4, 1.0, 1.0, 4, 5),
        (8, 1.0, 0.5, 2, 3),
        (9, 0.5, 0.5, 3, 6),
        (8, 0.0, 0.5, 6, 7),
        (6, 1.0, 0.5, 7, 8),
    ],
    [
        (3, 0.5),
        (4, 1.5),
        (6, 0.5),
        (8, 1.0),
        (9, 0.5),
    ],
    False,
)
TEST_CASE_2 = (
    [
        -1.5, 1.0, -3.0, 10.0, -1.0, 3.0, -8.0, 4.0, -2.0, 6.0,
        -1.0, -4.0, -8.0, 2.0, 1.0, -5.0, 0.0, 2.5, -4.0, 1.0,
        0.0, 2.0, -0.5,
    ],
    [
        (2.5, -0.25, 0.5, 0, 1),
        (4.0, -1.00, 0.5, 1, 2),
        (4.0, 1.00, 1.0, 4, 5),
        (13.0, 3.50, 0.5, 2, 3),
        (6.0, 1.00, 1.0, 7, 8),
        (14.0, -1.00, 1.0, 6, 9),
        (7.0, -1.50, 1.0, 13, 15),
        (1.0, 0.50, 1.0, 19, 20),
        (18.0, 1.00, 0.5, 3, 12),
        (10.5, -2.75, 0.5, 12, 17),
        (6.5, -0.75, 0.5, 17, 18),
        (6.0, -1.00, 0.5, 18, 21),
        (2.5, 0.75, 0.5, 21, 22),
    ],
    [
        (1.0, 1.0),
        (2.5, 1.0),
        (4.0, 1.5),
        (6.0, 1.5),
        (6.5, 0.5),
        (7.0, 1.0),
        (10.5, 0.5),
        (13.0, 0.5),
        (14.0, 1.0),
        (18.0, 0.5),
    ],
    False,
)
TEST_CASE_3 = (
    [
        0.8 * math.sin(0.01 * math.pi * i) + 0.2 * math.sin(0.032 * math.pi * i)
        for i in range(1001)
    ],
    [
        (0.09020631993390904, 0.638796382297327, 1.0, 26, 45),
        (0.7841230166856958, 0.3920615083428479, 0.5, 0, 70),
        (0.02555985050659182, -0.556567582861063, 1.0, 122, 134),
        (1.6512875405599494, -0.04152075359427887, 0.5, 70, 166),
        (1.7986374238678868, 0.03215418805968978, 0.5, 166, 261),
        (1.906532656127566, -0.02179342807014989, 0.5, 261, 357),
        (1.9722034009805518, 0.011041944356343036, 0.5, 357, 452),
        (0.025559850506592485, 0.5565675828610637, 1.0, 866, 878),
        (0.09020631993390937, -0.6387963822973273, 1.0, 955, 974),
        (1.9942872896932382, -5.551115123125783e-17, 0.5, 452, 548),
        (1.9722034009805514, -0.01104194435634337, 0.5, 548, 643),
        (1.906532656127565, 0.021793428070149834, 0.5, 643, 739),
        (1.7986374238678864, -0.032154188059689504, 0.5, 739, 834),
        (1.6512875405599488, 0.04152075359427937, 0.5, 834, 930),
        (0.7841230166856932, -0.39206150834284836, 0.5, 930, 1000),
    ],
    [
        (0.025559850506591708, 1.0),
        (0.025559850506592263, 1.0),
        (0.09020631993390904, 1.0),
        (0.09020631993390937, 1.0),
        (0.7841230166856958, 0.5),
        (0.7841230166856961, 0.5),
        (1.6512875405599488, 0.5),
        (1.651287540559949, 0.5),
        (1.798637423867886, 0.5),
        (1.7986374238678877, 0.5),
        (1.9065326561275655, 0.5),
        (1.9065326561275668, 0.5),
        (1.9722034009805516, 0.5),
        (1.9722034009805522, 0.5),
        (1.9942872896932382, 0.5)
    ],
    True,
)


def test_version():
    # Ensure that rainflow.__version__ is the same as version set in pyproject.toml
    assert rainflow.__version__ == importlib_metadata.version("rainflow")


@pytest.mark.parametrize(
    ("series", "cycles", "counts", "approx"),
    [TEST_CASE_1, TEST_CASE_2, TEST_CASE_3],
)
def test_count_cycles(series, cycles, counts, approx):
    result = rainflow.count_cycles(series)
    if approx:
        expected = [(pytest.approx(rng), count) for rng, count in counts]
    else:
        expected = counts
    assert result == expected


@pytest.mark.parametrize(
    ("series", "cycles", "counts", "approx"),
    [TEST_CASE_1, TEST_CASE_2],
)
def test_count_cycles_ndigits(series, cycles, counts, approx):
    series = [x + 0.01 * random.random() for x in series]
    assert rainflow.count_cycles(series) != counts
    assert rainflow.count_cycles(series, ndigits=1) == counts


def test_count_cycles_nbins():
    series = TEST_CASE_1[0]
    assert rainflow.count_cycles(series, nbins=1) == [(9, 4.0)]
    assert rainflow.count_cycles(series, nbins=2) == [
        (4.5, 2.0),
        (9.0, 2.0),
    ]
    assert rainflow.count_cycles(series, nbins=5) == [
        (1.8, 0.0),
        (3.6, 0.5),
        (5.4, 1.5),
        (7.2, 0.5),
        (9.0, 1.5),
    ]
    assert rainflow.count_cycles(series, nbins=9) == [
        (1.0, 0.0),
        (2.0, 0.0),
        (3.0, 0.5),
        (4.0, 1.5),
        (5.0, 0.0),
        (6.0, 0.5),
        (7.0, 0.0),
        (8.0, 1.0),
        (9.0, 0.5),
    ]
    assert rainflow.count_cycles(series, nbins=10) == [
        (0.9, 0.0),
        (1.8, 0.0),
        (2.7, 0.0),
        (3.6, 0.5),
        (4.5, 1.5),
        (5.4, 0.0),
        (6.3, 0.5),
        (7.2, 0.0),
        (8.1, 1.0),
        (9.0, 0.5),
    ]


def test_count_cycles_binsize_case_1():
    series = TEST_CASE_1[0]
    assert rainflow.count_cycles(series, binsize=10) == [(10, 4.0)]
    assert rainflow.count_cycles(series, binsize=9) == [(9, 4.0)]
    assert rainflow.count_cycles(series, binsize=5) == [
        (5, 2.0),
        (10, 2.0),
    ]
    assert rainflow.count_cycles(series, binsize=3) == [
        (3, 0.5),
        (6, 2.0),
        (9, 1.5),
    ]
    assert rainflow.count_cycles(series, binsize=2) == [
        (2, 0.0),
        (4, 2.0),
        (6, 0.5),
        (8, 1.0),
        (10, 0.5),
    ]
    assert rainflow.count_cycles(series, binsize=1) == [
        (1, 0.0),
        (2, 0.0),
        (3, 0.5),
        (4, 1.5),
        (5, 0.0),
        (6, 0.5),
        (7, 0.0),
        (8, 1.0),
        (9, 0.5),
    ]


def test_count_cycles_binsize_case_3():
    series = TEST_CASE_3[0]
    result = rainflow.count_cycles(series, binsize=0.2)
    expected = [
        (pytest.approx(rng), count)
        for rng, count in [
            (0.2, 4.0),
            (0.4, 0.0),
            (0.6, 0.0),
            (0.8, 1.0),
            (1.0, 0.0),
            (1.2, 0.0),
            (1.4, 0.0),
            (1.6, 0.0),
            (1.8, 2.0),
            (2.0, 2.5),
        ]
    ]
    assert result == expected


@pytest.mark.parametrize(
    ("series", "cycles", "counts", "approx"),
    [TEST_CASE_1, TEST_CASE_2, TEST_CASE_3],
)
def test_count_cycles_series_with_zero_derivatives(series, cycles, counts, approx):
    series = list(itertools.chain.from_iterable([x, x] for x in series))
    result = rainflow.count_cycles(series)
    if approx:
        expected = [(pytest.approx(rng), count) for rng, count in counts]
    else:
        expected = counts
    assert result == expected


def test_count_cycles_exclusive_arguments():
    series = TEST_CASE_1[0]

    with pytest.raises(ValueError):
        rainflow.count_cycles(series, nbins=1, binsize=1)

    with pytest.raises(ValueError):
        rainflow.count_cycles(series, nbins=1, ndigits=1)

    with pytest.raises(ValueError):
        rainflow.count_cycles(series, binsize=1, ndigits=1)


@pytest.mark.parametrize(
    ("series", "cycles", "counts", "approx"),
    [TEST_CASE_1, TEST_CASE_2, TEST_CASE_3],
)
def test_extract_cycles(series, cycles, counts, approx):
    result = list(rainflow.extract_cycles(series))
    if approx:
        expected = [
            (pytest.approx(rng), pytest.approx(mean), count, i, j)
            for (rng, mean, count, i, j) in cycles
        ]
    else:
        expected = cycles
    assert result == expected


@pytest.mark.parametrize(
    ("series", "cycles"),
    [
        ([], []),
        ([1], []),
        ([1, 2], []),
        ([1, 2, 3], [(2, 2.0, 0.5, 0, 2)]),
    ]
)
def test_extract_cycles_small_series(series, cycles):
    assert list(rainflow.extract_cycles(series)) == cycles


@pytest.mark.parametrize(
    ("series", "cycles", "counts", "approx"),
    [TEST_CASE_1, TEST_CASE_2, TEST_CASE_3],
)
def test_reversals_yield_value(series, cycles, counts, approx):
    for index, value in rainflow.reversals(series):
        assert value == series[index]


@pytest.mark.parametrize(
    ("series", "reversals"),
    [
        ([], []),
        ([1], []),
        ([1, 2], [(0, 1)]),
        ([1, 2, 3], [(0, 1), (2, 3)]),
    ]
)
def test_reversals_small_series(series, reversals):
    assert list(rainflow.reversals(series)) == reversals


def test_num_bins():
    # This test checks for a bug reported in issue #60 where the
    # returned number of bins was different than the nbins argument
    # due to floating point accuracy.
    series = [
        0,
        3517.860166127188,
        -3093.4966492094213,
        0,
    ]
    nbins = 100
    result = rainflow.count_cycles(series, nbins=nbins)
    assert len(result) == nbins
