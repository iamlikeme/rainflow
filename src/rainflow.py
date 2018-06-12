# coding: utf-8
"""
Implements rainflow cycle counting algorythm for fatigue analysis
according to section 5.4.4 in ASTM E1049-85 (2011).
"""
__version__ = "2.1.1"

from collections import deque, defaultdict
import functools


def _get_round_function(ndigits=None):
    if ndigits is None:
        def func(x):
            return x
    else:
        def func(x):
            return round(x, ndigits)
    return func


def reversals(series, left=False, right=False):
    """Iterate reversal points in the series.

    A reversal point is a point in the series at which the first derivative
    changes sign. Reversal is undefined at the first (last) point because the
    derivative before (after) this point is undefined. The first and the last
    points may be treated as reversals by setting the optional parameters
    `left` and `right` to True.

    Parameters
    ----------
    series : iterable sequence of numbers
    left: bool, optional
        If True, yield the first point in the series (treat it as a reversal).
    right: bool, optional
        If True, yield the last point in the series (treat it as a reversal).

    Yields
    ------
    float
        Reversal points.
    """
    series = iter(series)

    x_last, x = next(series), next(series)
    d_last = (x - x_last)

    if left:
        yield x_last
    for x_next in series:
        if x_next == x:
            continue
        d_next = x_next - x
        if d_last * d_next < 0:
            yield x
        x_last, x = x, x_next
        d_last = d_next
    if right:
        yield x_next


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
def extract_cycles(series, left=False, right=False):
    """Iterate cycles in the series.

    Parameters
    ----------
    series : iterable sequence of numbers
    left: bool, optional
        If True, treat the first point in the series as a reversal.
    right: bool, optional
        If True, treat the last point in the series as a reversal.

    Yields
    ------
    cycle : tuple
        Each tuple contains three floats (low, high, mult), where low and high
        define cycle amplitude and mult equals to 1.0 for full cycles and 0.5
        for half cycles.
    """
    points = deque()

    for x in reversals(series, left=left, right=right):
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


def count_cycles(series, ndigits=None, left=False, right=False):
    """Count cycles in the series.

    Parameters
    ----------
    series : iterable sequence of numbers
    ndigits : int, optional
        Round cycle magnitudes to the given number of digits before counting.
    left: bool, optional
        If True, treat the first point in the series as a reversal.
    right: bool, optional
        If True, treat the last point in the series as a reversal.

    Returns
    -------
    A sorted list containing pairs of cycle magnitude and count.
    One-half cycles are counted as 0.5, so the returned counts may not be
    whole numbers.
    """
    counts = defaultdict(float)
    round_ = _get_round_function(ndigits)

    for low, high, mult in extract_cycles(series, left=left, right=right):
        delta = round_(abs(high - low))
        counts[delta] += mult
    return sorted(counts.items())
