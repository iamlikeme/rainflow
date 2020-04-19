# coding: utf-8
"""
Implements rainflow cycle counting algorythm for fatigue analysis
according to section 5.4.4 in ASTM E1049-85 (2011).
"""
from __future__ import division
from collections import deque, defaultdict
import math

try:
    from importlib import metadata as _importlib_metadata
except ImportError:
    import importlib_metadata as _importlib_metadata

__version__ = _importlib_metadata.version("rainflow")


def _get_round_function(ndigits=None):
    if ndigits is None:
        def func(x):
            return x
    else:
        def func(x):
            return round(x, ndigits)
    return func


def reversals(series):
    """Iterate reversal points in the series.

    A reversal point is a point in the series at which the first derivative
    changes sign. Reversal is undefined at the first (last) point because the
    derivative before (after) this point is undefined. The first and the last
    points are treated as reversals.

    Parameters
    ----------
    series : iterable sequence of numbers

    Yields
    ------
    Reversal points as tuples (index, value).
    """
    series = iter(series)

    x_last, x = next(series), next(series)
    d_last = (x - x_last)

    yield 0, x_last
    for index, x_next in enumerate(series, start=1):
        if x_next == x:
            continue
        d_next = x_next - x
        if d_last * d_next < 0:
            yield index, x
        x_last, x = x, x_next
        d_last = d_next
    yield index + 1, x_next


def extract_cycles(series):
    """Iterate cycles in the series.

    Parameters
    ----------
    series : iterable sequence of numbers

    Yields
    ------
    cycle : tuple
        Each tuple contains (range, mean, count, start index, end index).
        Count equals to 1.0 for full cycles and 0.5 for half cycles.
    """
    points = deque()

    def format_output(point1, point2, count):
        i1, x1 = point1
        i2, x2 = point2
        rng = abs(x1 - x2)
        mean = 0.5 * (x1 + x2)
        return rng, mean, count, i1, i2

    for point in reversals(series):
        i, x = point
        points.append(point)

        while len(points) >= 3:
            # Form ranges X and Y from the three most recent points
            x1, x2, x3 = points[-3][1], points[-2][1], points[-1][1]
            X = abs(x3 - x2)
            Y = abs(x2 - x1)

            if X < Y:
                # Read the next point
                break
            elif len(points) == 3:
                # Y contains the starting point
                # Count Y as one-half cycle and discard the first point
                yield format_output(points[0], points[1], 0.5)
                points.popleft()
            else:
                # Count Y as one cycle and discard the peak and the valley of Y
                yield format_output(points[-3], points[-2], 1.0)
                last = points.pop()
                points.pop()
                points.pop()
                points.append(last)
    else:
        # Count the remaining ranges as one-half cycles
        while len(points) > 1:
            yield format_output(points[0], points[1], 0.5)
            points.popleft()


def count_cycles(series, ndigits=None, nbins=None, binsize=None):
    """Count cycles in the series.

    Parameters
    ----------
    series : iterable sequence of numbers
    ndigits : int, optional
        Round cycle magnitudes to the given number of digits before counting.
    nbins : int, optional
        Specifies the number of cycle-counting bins
    binsize : int, optional
        Specifies the width of each cycle-counting bin

    ndigits, nbins and binsize are mutually exclusive - only one of the three
    can be specified.

    Returns
    -------
    A sorted list containing pairs of cycle magnitude and count.
    One-half cycles are counted as 0.5, so the returned counts may not be
    whole numbers. If binning is used, the cycle count magnitude corresponds
    to the right edge of the bin.
    """
    if sum(value is not None for value in (ndigits, nbins, binsize)) > 1:
        raise ValueError(
            "Arguments ndigits, nbins and binsize are mutually exclusive"
        )

    counts = defaultdict(float)
    cycles = (
        (rng, count)
        for rng, mean, count, i_start, i_end in extract_cycles(series)
    )

    if binsize is not None:
        for rng, count in cycles:
            n = math.ceil(rng / binsize)
            counts[n * binsize] += count

        rng = binsize
        while rng < max(counts):
            counts.setdefault(rng, 0.0)
            rng += binsize

    elif nbins is not None:
        binsize = (max(series) - min(series)) / nbins
        for rng, count in cycles:
            n = math.ceil(rng / binsize)
            counts[n * binsize] += count

        for i in range(nbins):
            rng = (i + 1) * binsize
            counts.setdefault(rng, 0.0)

    elif ndigits is not None:
        round_ = _get_round_function(ndigits)
        for rng, count in cycles:
            counts[round_(rng)] += count

    else:
        for rng, count in cycles:
            counts[rng] += count

    return sorted(counts.items())
