# coding: utf-8
"""
Implements rainflow cycle counting algorythm for fatigue analysis
according to section 5.4.4 in ASTM E1049-85 (2011).
"""
from collections import deque, defaultdict


def reversals(series):
    """
    A generator function which iterates over the reversals in the given
    *series* (an iterable). Reversals are the points at which the first
    derivative on the series changes sign. The generator never yields
    the first and the last points in the series.
    """
    series = iter(series)
    
    x_last, x = series.next(), series.next()
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
    Returns two lists: the first one containig full cycles and the second
    containing one-half cycles. The cycles are extracted from the iterable
    *series* according to section 5.4.4 in ASTM E1049 (2011).
    """
    points = deque()
    full, half = [], []

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
                half.append(Y)
                points.popleft()
            else:
                # Count Y as one cycle and discard the peak and the valley of Y
                full.append(Y)
                last = points.pop()
                points.pop()
                points.pop()
                points.append(last)
    else:
        # Count the remaining ranges as one-half cycles
        while len(points) > 1:
            half.append(abs(points[-2] - points[-1]))
            points.pop()
    return full, half



def count_cycles(series, ndigits=None):
    """
    Returns a sorted list containig pairs of cycle magnitude and count.
    One-half cycles are counted as 0.5, so the returned counts may not be
    whole numbers. The cycles are extracted from the iterable *series*
    using the extract_cycles function. If *ndigits* is given the cycles
    will be rounded to the given number of digits before counting.
    """
    full, half = extract_cycles(series)
    
    # Round the cycles if requested
    if ndigits is not None:
        full = (round(x, ndigits) for x in full)
        half = (round(x, ndigits) for x in half)
    
    # Count cycles
    counts = defaultdict(float)
    for x in full:
        counts[x] += 1.0
    for x in half:
        counts[x] += 0.5
    
    return sorted(counts.items())
