from functools import reduce
from represent import map_hamiltonian
import numpy as np


def exact_hamiltonian(hamiltonian, trunc=2, sparse=False):
    """Creates an exact matrix of a many-body Hamiltonian
       from a Hamiltonian.
       TODO: implement sparse!
       TODO: dim should really be specified in the Hamiltonian
    """

    terms, lattice = hamiltonian
    n_sites = len(lattice)
    dim = trunc ** n_sites

    def op(index, o):
        matrix = o.exact_representation(trunc)
        d = matrix.shape[0]
        lst = []
        for i in range(n_sites):
            if i == index:
                lst.append(matrix)
            else:
                # TODO: allow for more generality here
                lst.append(np.identity(d))
        return reduce(np.kron, lst)

    def term(operators, sites):
        return reduce(np.dot, (op(i, o)
                      for (o, (i, _)) in zip(operators, sites)))

    H = np.zeros((dim, dim), dtype='complex')
    return map_hamiltonian(hamiltonian, H, term)
