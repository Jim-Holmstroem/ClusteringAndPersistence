from __future__ import print_function, division

from functools import partial
from abc import abstractmethod, ABCMeta

import numpy as np

def distance_matrix(distance, a, b):
    return map(distance, product(a, b))

SingeltonSet = partial(map, lambda x: {x})

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
        return np.min(distance_matrix(self.distance, A, B))
class CL(SetDistance):
    def __call__(self, A, B):
        return np.max(distance_matrix(self.distance, A, B))
class AL(SetDistance):
    def __call__(self, A, B):
        return np.mean(distance_matrix(self.distance, A, B))
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
        X : [block : {x : object}]

        Returns
        -------
        clustering : [(distance : float, [block : {x : object}])]
        """



X = SingeltonSet(range(5))
print(HC(SL)(X))
