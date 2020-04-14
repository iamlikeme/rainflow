import itertools
import pytest
import rainflow
import random


@pytest.fixture
def series():
    return [-2, 1, -3, 5, -1, 3, -4, 4, -2]


@pytest.fixture
def counts():
    return [(3, 0.5), (4, 1.5), (6, 0.5), (8, 1.0), (9, 0.5)]


def test_count_cycles(series, counts):
    result = rainflow.count_cycles(series)
    assert result == counts


def test_count_cycles_ndigits(series, counts):
    series = [x + 0.01 * random.random() for x in series]
    assert rainflow.count_cycles(series) != counts
    assert rainflow.count_cycles(series, ndigits=1) == counts


def test_count_cycles_nbins(series):
    assert rainflow.count_cycles(series, nbins=1) == [(9, 5.0)]
    assert rainflow.count_cycles(series, nbins=2) == [
        (4.5, 3.0),
        (9.0, 2.0),
    ]
    assert rainflow.count_cycles(series, nbins=5) == [
        (1.8, 0.0),
        (3.6, 1.5),
        (5.4, 1.5),
        (7.2, 0.5),
        (9.0, 1.5),
    ]
    assert rainflow.count_cycles(series, nbins=9) == [
        (1.0, 0.0),
        (2.0, 0.0),
        (3.0, 1.0),
        (4.0, 0.5),
        (5.0, 1.5),
        (6.0, 0.0),
        (7.0, 0.5),
        (8.0, 0.0),
        (9.0, 1.5),
    ]
    assert rainflow.count_cycles(series, nbins=10) == [
        (0.9, 0.0),
        (1.8, 0.0),
        (2.7, 1.0),
        (3.6, 0.5),
        (4.5, 1.5),
        (5.4, 0.0),
        (6.3, 0.5),
        (7.2, 0.0),
        (8.1, 1.0),
        (9.0, 0.5),
    ]


def test_count_cycles_binsize(series):
    assert rainflow.count_cycles(series, binsize=10) == [(10, 5.0)]
    assert rainflow.count_cycles(series, binsize=9) == [(9, 5.0)]
    assert rainflow.count_cycles(series, binsize=5) == [
        (5, 3.0),
        (10, 2.0),
    ]
    assert rainflow.count_cycles(series, binsize=3) == [
        (3, 1.0),
        (6, 2.0),
        (9, 2.0),
    ]
    assert rainflow.count_cycles(series, binsize=2) == [
        (2, 0.0),
        (4, 1.5),
        (6, 1.5),
        (8, 0.5),
        (10, 1.5),
    ]
    assert rainflow.count_cycles(series, binsize=1) == [
        (1, 0.0),
        (2, 0.0),
        (3, 1.0),
        (4, 0.5),
        (5, 1.5),
        (6, 0.0),
        (7, 0.5),
        (8, 0.0),
        (9, 1.5),
    ]


def test_count_cycles_series_with_zero_derivatives(series, counts):
    series = list(itertools.chain.from_iterable([x, x] for x in series))
    assert rainflow.count_cycles(series) == counts


def test_extract_cycles_low_high_is_sorted(series):
    assert all(
        low <= high
        for low, high, mult in rainflow.extract_cycles(series)
    )


def test_extract_cycles_order_of_half_cycles(series):
    result = [
        (0.5 * (high + low), mult)
        for low, high, mult in rainflow.extract_cycles(series)
    ]
    expected = [
        (-1.0, 0.5),
        (-0.5, 0.5),
        (-1.0, 0.5),
        (1.0, 1.0),
        (1.0, 0.5),
        (0.5, 0.5),
        (0.0, 0.5),
        (1.0, 0.5),
        (-1.0, 0.5),
    ]
    assert result == expected
