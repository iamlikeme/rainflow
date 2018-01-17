# coding: utf-8
"""
Implements rainflow cycle counting algorythm for fatigue analysis
according to section 5.4.4 in ASTM E1049-85 (2011).
"""
__version__ = "1.0.1"

from collections import deque, defaultdict


def get_round_function(ndigits=None):
    if ndigits is None:
        def func(x):
            return x
    else:
        def func(x):
            return round(x, ndigits)
    return func


def reversals(series):
    """
    A generator function which iterates over the reversals in the iterable
    *series*. Reversals are the points at which the first
    derivative on the series changes sign. The generator never yields
    the first and the last points in the series.
    """
    series = iter(series)

    x_last, x = next(series), next(series)
    d_last = (x - x_last)

    for x_next in series:
        if x_next == x:
            continue
        d_next = x_next - x
        if d_last * d_next < 0:
            yield x
        x_last, x = x, x_next
        d_last = d_next


def extract_cycles(series):
    """
    A generator function which extracts cycles from the iterable *series*
    according to section 5.4.4 in ASTM E1049 (2011).

    The generator produces tuples (low, high, mult), where low and high
    define cycle amplitude and mult equals to 1.0 for full cycles and 0.5
    for half cycles. Note that low and high are not necessarily ordered,
    so do not rely on low < high.
    """
    points = deque()

    for x in reversals(series):
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
                yield points[-3], points[-2], 0.5
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
            yield points[-2], points[-1], 0.5
            points.pop()


def count_cycles(series, ndigits=None):
    """
    Returns a sorted list containig pairs of cycle magnitude and count.
    One-half cycles are counted as 0.5, so the returned counts may not be
    whole numbers. The cycles are extracted from the iterable *series*
    using the extract_cycles function. If *ndigits* is given the cycles
    will be rounded to the given number of digits before counting.
    """
    counts = defaultdict(float)
    round_ = get_round_function(ndigits)

    for low, high, mult in extract_cycles(series):
        delta = round_(abs(high - low))
        counts[delta] += mult
    return sorted(counts.items())
