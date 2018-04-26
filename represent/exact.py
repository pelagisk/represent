from operator import mul
from functools import reduce
from .hamiltonian import map_hamiltonian
import numpy as np


def exact_hamiltonian(hamiltonian, lattice):

    dims = lattice.get_dims(hamiltonian)

    def term(operators, link):
        lst = []
        for i, d in enumerate(dims):
            if i in link['indices']:
                idx = link['indices'].index(i)
                matrix = operators[idx].exact_representation()
                assert(matrix.shape[0] == d)
                lst.append(matrix)
            else:
                lst.append(np.identity(d))
        return reduce(np.kron, lst)

    M = reduce(mul, dims)
    H = np.zeros((M, M), dtype='complex')
    return map_hamiltonian(hamiltonian, lattice, H, term)
