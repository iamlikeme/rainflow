# coding: utf-8
"""
Implements rainflow cycle counting algorythm for fatigue analysis
according to section 5.4.4 in ASTM E1049-85 (2011).
"""
from __future__ import division
from collections import deque, defaultdict
import functools
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


def _sort_lows_and_highs(func):
    "Decorator for extract_cycles"
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        for low, high, mult in func(*args, **kwargs):
            if low < high:
                yield low, high, mult
            else:
                yield high, low, mult
    return wrapper


@_sort_lows_and_highs
def extract_cycles(series):
    """Iterate cycles in the series.

    Parameters
    ----------
    series : iterable sequence of numbers

    Yields
    ------
    cycle : tuple
        Each tuple contains three floats (low, high, mult), where low and high
        define cycle amplitude and mult equals to 1.0 for full cycles and 0.5
        for half cycles.
    """
    points = deque()

    for index, x in reversals(series):
        points.append(x)
        while len(points) >= 3:
            # Form ranges X and Y from the three most recent points
            X = abs(points[-2] - points[-1])
            Y = abs(points[-3] - points[-2])

            if X < Y:
                # Read the next point
                break
            elif len(points) == 3:
                # Y contains the starting point
                # Count Y as one-half cycle and discard the first point
                yield points[0], points[1], 0.5
                points.popleft()
            else:
                # Count Y as one cycle and discard the peak and the valley of Y
                yield points[-3], points[-2], 1.0
                last = points.pop()
                points.pop()
                points.pop()
                points.append(last)
    else:
        # Count the remaining ranges as one-half cycles
        while len(points) > 1:
            yield points[0], points[1], 0.5
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
    counts = defaultdict(float)
    round_ = _get_round_function(ndigits)

    try:
        max_range = max(series) - min(series)
        if max_range == 0:
            return []
    except ValueError:
        return []

    # check for mutually exclusive options: ndigits, nbins, binsize
    if (ndigits is not None) and ((nbins is not None) or (binsize is not None)) :
        raise ValueError("Specify only one option from ndigits, nbins or binsize")
    if (nbins is not None) and (binsize is not None) :
        raise ValueError("Specify only one option from nbins or binsize")

    # if neither nbins nor binsize is specified
    if (nbins is None) and (binsize is None):
        for low, high, mult in extract_cycles(series):
            delta = round_(abs(high - low))
            counts[delta] += mult
    else:
        # if nbins is specified
        if nbins is not None:
            # if number of bins for range hase been defined, 
            # then group the count data accordingly
            binsize = max_range / nbins
        # else binsize is specified
        else:
            nbins = int(math.ceil(max_range / binsize))
        # save cycle counts to dictionary where key is the bin index, not range
        counts_ix = defaultdict(int)
        for i in range(nbins):
            counts_ix[i] = 0
        for low, high, mult in extract_cycles(series):
            binIndex = int(abs(high - low) / binsize)
            # handle possibility of range equaliing max range
            if binIndex == nbins:
                binIndex = nbins - 1
            counts_ix[binIndex] += mult
        # save count data to dictionary where key is the range
        counts = dict(((k+1)*binsize,v) for k,v in counts_ix.items())

    return sorted(counts.items())
