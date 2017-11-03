"""
Represents operators as objects, for convenience.
"""


from operator import add
from operator import mul
from operator import sub
from copy import copy
import numpy as np


class Operator:

    def __init__(self):
        self.type = 'generic'
        self._str = 'O'
        self._conjugated = False

    def conjugate(self):
        new = copy(self)
        new._conjugated = True
        return new

    def conj(self):
        return self.conjugate()

    def exact_representation(trunc):
        raise NotImplementedError

    def coherent_representation(x):
        raise NotImplementedError

    def _map_operation(self, other, op, label):

        if isinstance(other, (int, float, complex)):
            return NotImplementedError

        if self.type != other.type:
            raise ValueError

        o = Operator()

        def exact_representation(trunc):
            f = self.exact_representation
            g = other.exact_representation
            return op(f(trunc), g(trunc))

        def coherent_representation(x):
            f = self.coherent_representation
            g = other.coherent_representation
            return op(f(x), g(x))

        o.exact_representation = exact_representation
        o.coherent_representation = coherent_representation
        o._str = str(self) + label + str(other)
        o.type = self.type
        return o

    def __add__(self, other):
        return self._map_operation(other, add, '+')

    def __sub__(self, other):
        return self._map_operation(other, sub, '-')

    def __mul__(self, other):
        return self._map_operation(other, mul, '*')

    def __str__(self):
        s = self._str
        if self._conjugated is True:
            s += "^H"
        return s

    def __repr__(self):
        return self.__str__()


class Identity(Operator):

    def __init__(self, type):
        self.type = type
        self._str = "I"
        self._conjugated = False

    def conj(self):
        return self

    def exact_representation(self, trunc):
        return np.identity(trunc)

    def coherent_representation(self, x):
        return 1

    def __str__(self):
        return self._str


class Boson(Operator):

    def __init__(self):
        super().__init__()
        self.type = "boson"
        self.mf_input_size = 2
        self._str = "B"

    def exact_representation(self, trunc):
        e = np.diag(np.sqrt(np.arange(1, trunc)), 1)
        if self._conjugated is True:
            return e.conjugate().transpose()
        else:
            return e

    def coherent_representation(self, x):
        assert len(x) == 2
        re, im = x
        if self._conjugated is True:
            return re - 1j*im
        else:
            return re + 1j*im