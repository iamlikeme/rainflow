import numpy as np
from itertools import izip, izip_longest


class HalfCycle:
    """
    Calculates a running minimum of a 1D array *a* starting at index *i*.
    It is required that a[i] is positive. The running minimum terminates at the end
    of the array or at an index *j* where a[j] is greater than the absolute value
    of the running minimum.

    Indices of *a* where the runinng minimum changes its value are stored in
    self.index and the corresponding values are stored in self.values.
    """
    def __init__(self, a, i):
        top = a[i]
        bottom = top
        index = [i]
        if top < 0:
            raise ValueError("Value at index *i* is not positive")
        for j, value in enumerate(a[i:], i):
            if value > 0 and -value < bottom < 0:
                index.append(j)
                break
            if value < bottom:
                index.append(j)
                bottom = value
        else:
            if index[-1] != j:
                index.append(j)        
        self.index = np.array(index)
        self.values = np.array([a[i] for i in index])
        self.values[-1] = bottom


    def __call__(self, i):
        """
        Returns the value of half-cycle at index i.
        Returns None if i out of range.
        """
        if i < self.index[0] or i > self.index[-1]:
            return None
        return self.values[self.index <= i][-1]
        
    @property
    def magnitude(self):
        "Returns the range of values (first minus last)"
        return self.values[0] - self.values[-1]
    
    def clip(self, other):
        """
        Clips the half-cycle *self* at an index i where self(i) <= other(i) if
        *other* started before *self*. If clipping occurs the last index of self
        becomes i and the last value of self becomes other(i). Returns True
        if clipping occured and False otherwise.
        """
        if not (other.index[0] < self.index[0]):
            # other half-cycle started later than self
            return False
        if other.index[-1] <= self.index[0]:
            # self and other do not overlap
            return False
        for i, value in izip(self.index, self.values):
            other_value = other(i-1)
            if other_value > 0 or other_value is None:
                continue
            elif value <= other_value:
                ix = (self.index <= i)
                self.index = self.index[ix]
                self.values = self.values[ix]
                self.values[-1] = other_value
                return True



def local_extrema(a, recursive=True, indices=None):
    """
    Returns indices at which array *a* has positive maxima and
    negative minima. If *indices* are provided the function will
    look for extrema only among a[indices]. If *recursive* is True
    then the function will be called recursively until the remaining
    extrema have alternating signs (i.e. each maximum is followed by
    a minimum and vice-versa).
    """
    if indices is None:
        indices = np.arange(len(a))
    x = np.array(a)[indices]
    left  = np.r_[x[1], x[:-1]]
    right = np.r_[x[1:], x[-2]]
    minima = (x < 0) & (x < left) & (x < right)
    maxima = (x > 0) & (x > left) & (x > right)
    ix = minima | maxima
    indices = indices[ix]
    if recursive and not all(ix):
        return local_extrema(a, recursive=True, indices=indices)
    else:
        return indices



def extract_halfcycles(a, magnitude=True, which="all"):
    """
    Returns a list half-cycle magnitudes extracted from 1D array *a*.
    Argument *which* should be one of the following strings:
      - 'positive' to extract half-cycles starting at positive values of *a*
      - 'negative' to extract half-cycles starting at negative values of *a*
      - 'all' (default) to extract all half-cycles
    If *magnitude* is False then a list of HalfCycle instances is returned.
    """
    if which not in ("all", "positive", "negative"):
        raise ValueError("Argument *which* must one of: 'all', 'positive', 'negative'")
    halfcycles = []
    a = np.array(a)
    a = a[local_extrema(a)]

    if which in ("all", "positive"):
        # Find half-cycles starting at positive peaks of *a*
        clippers = []
        for i in np.where(a > 0)[0]:
            hc = HalfCycle(a, i)
            if len(hc.index) == 1:
                continue
            for earlier in clippers:
                hc.clip(earlier)
            clippers = filter(lambda hc: hc.index[-1] > i, clippers)
            clippers.append(hc)
            halfcycles.append(hc)
    if which in ("all", "negative"):
        # Find half-cycles starting at negative peaks of *a*
        # by running the function again for -a
        for hc in extract_halfcycles(-a, magnitude=False, which="positive"):
            hc.values = -hc.values
            halfcycles.append(hc)
    if magnitude:
        # Retain only magnitude from each half-cycle
        halfcycles = [hc.magnitude for hc in halfcycles]
    return halfcycles
    


def combine_halfcycles(magnitudes):
    """
    Combines half-cycles of equal absolute magnitude and opposite sign into
    full cycles. Some residual, unmatched half-cycles may remain.
    
    Argument *magnitude* is a sequence of half-cycle magnitudes (positive and
    negative). Returns two lists: the first containing (positive) magnitudes
    of full cyles and the second one containing magnitudes of residual
    half-cycles (positive or negative).
    """
    full, residual = [], []
    positive = sorted(x for x in magnitudes if x > 0)
    negative = sorted((x for x in magnitudes if x < 0), reverse=True)
    while positive and negative:
        pos, neg = positive[-1], negative[-1]
        if pos + neg == 0:
            full.append(pos)
            positive.pop()
            negative.pop()
        elif pos > -neg:
            residual.append(pos)
            positive.pop()
        else:
            residual.append(neg)
            negative.pop()
    residual.extend(positive)
    residual.extend(negative)
    return full, residual



def convert_residual_halfcycles(magnitudes):
    """
    Combines half-cycles of similar magnitude and opposite sign into
    full cycles. Half-cycles are divided into positive and negative ones
    and then sorted by absolute value. Full cycles are created by taking the
    maximum absolute value for each pair of a positive and a negative
    half-cycle. Returns a list of (positive) magnitudes of full cycles.
    """
    positive = sorted([x for x in magnitudes if x > 0], reverse=True)
    negative = sorted([-x for x in magnitudes if x < 0], reverse=True)
    return map(max, izip_longest(positive, negative, fillvalue=0.0))
    
    

def extract_cycles(a):
    """
    Extracts full cycles from a 1D array *a* using rainflow-counting
    algorythm. Residual half-cycles, if any, are converted to full cycles and
    included in the returned list. Returns an unsorted list of cycle magnitudes
    (positive).
    """
    halfcycles = extract_halfcycles(a, magnitude=True, which="all")
    full, residual = combine_halfcycles(halfcycles)
    return full + convert_residual_halfcycles(residual)

