"""
Walks through a Hamiltonian and processes it to some concrete representation,
works a bit like reduce
"""

from itertools import permutations


def map_hamiltonian(hamiltonian, H, f):
    terms, lattice = hamiltonian
    for term in terms:
        subsets, cnumber, operators = term
        for subset in subsets:
            sites = list(subset.items())
            # for now, just assume that any permutation should be taken
            for permutation in permutations(sites):
                H += cnumber * f(operators, permutation)
    return H
