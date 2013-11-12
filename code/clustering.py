from __future__ import print_function, division

from itertools import combinations, product
from functools import partial, wraps
from abc import abstractmethod, ABCMeta

import numpy as np

def distances(distance, a, b):
    return list(starmap(distance, product(a, b)))

def apply(f, *args, **kwargs):  # NOTE overwrites depricated builtin
    return f(*args, **kwargs)

def composition(f, *g):
    if g:
        return lambda *x: f(composition(*g)(*x))
    else:
        return f

def min_with_arg_by(f, ABs):
    min_, min_arg = min(starmap(lambda a, b: (f(a, b), (a, b)), ABs))
    return min_arg, min_

SingeltonSet = composition(frozenset, partial(map, lambda x: frozenset([x, ])))

filter_non_equal = partial(filter, lambda (x_i, x_j) : x_i == x_j)

def symmetric_lazy(f):  # TODO breakout the lazy parts of the code
    """See lazy, adds the fact f(i, j) == f(j, i)
    Will be associated with a SetDistance class,
    the Distance.distance function is included in the key.
    Is currently only made to be used with SetDistance.
    """
    @wraps(f)
    def _f(self, i, j):
        distance_function = self.distance.__call__.im_func
        key = (distance_function, i, j)
        key_transpose = (distance_function, j, i)
        if not (key in _f.__cache or key_transpose in _f.__cache):
            _f.__cache[key] = f(self, i, j)

        value = _f.__cache[key] if key in _f.__cache else _f.__cache[key_transpose]

        return value

    _f.__cache = dict()

    return _f

class Distance(object):
    __metaclass__ = ABCMeta
    @abstractmethod
    def __call__(self, a, b):
        """
        Parameters
        ----------
        a : object
        b : object

        Returns
        -------
        distance : float
        """
        pass

class PointDistance(Distance): pass

class SetDistance(Distance):
    def __init__(self, distance):
        assert(isinstance(distance, PointDistance))
        self.distance = distance

class EuclideanDistance(PointDistance):
    def __call__(self, x_i, x_j):
        return np.sqrt((x_i - x_j)**2)

class SL(SetDistance):
    def __call__(self, A, B):
        return np.min(
            distances(self.distance, A, B)
        )
class CL(SetDistance):
    def __call__(self, A, B):
        return np.max(
            distances(self.distance, A, B)
        )
class AL(SetDistance):
    def __call__(self, A, B):
        return np.mean(
            distances(self.distance, A, B)
        )
class HL(SetDistance):
    def __call__(self, A, B):
        raise NotImplementedError('HL not implemented yet, needs housendorf distance')  # TODO does it need another type of `distance_matrix`?!

class HC(object):
    def __init__(self, distance):
        assert(isinstance(distance, SetDistance))
        self.distance = distance

    def __call__(self, X):
        """
        Parameters
        ----------
        X : {(block : {(x : object)})}

        Returns
        -------
        clustering : [(distance : float, {(block : {(x : object)}})]
        """
        #  TODO recursive, flatten it with a trampoline
        assert(len(X) not in (0,))  # TODO handle these cases gracefully and consistently

        if len(X) == 1:
            return []

        (A, B), min_distance = min_with_arg_by(
            self.distance,
            combinations(X, r=2)
        )

        # NOTE doesn't handle multiple linkage, return more AB and link/remove all below in a more general form (A, B)-> As higher order union = partial(reduce, union) and X-As #min_with_arg_by returns (frozenset, float)

        return [
            (min_distance, X)  # NOTE if intended to return something else here is the spot
        ] + (
            self(
                (X - {A, B}) | {A | B}
            )
        )

X = SingeltonSet([1, 2.1, 3.2, 4.4, 5.8])
for set_distance in starmap(apply, product([SL, CL, AL], [EuclideanDistance()])):
    map(print, HC(set_distance)(X))
    print()
