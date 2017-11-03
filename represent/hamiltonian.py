import numpy as np
import scipy.sparse as sp
from scipy.sparse.linalg import eigsh
from itertools import permutations
from functools import reduce
from operators import *


"""

TODO what should be the structure of sites, site-types and so on?
TODO: allow lattice to be more general... decouple from model?
TODO is DMRG representation even possible?
TODO docstrings
TODO testing
TODO spin 1/2 hamiltonian
"""

class Site:

    def __init__(self):
        self.type = "generic"

    def __str__(self):
        return self.type + " site"

    def __repr__(self):
        return self.__str__()


class BosonSite(Site):

    def __init__(self):
        self.type = "boson"
        self.meanfield_dof = 2
        self.exact_dof = None


class Lattice(list):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def sites(self):
        return [{k: v} for k, v in enumerate(self)]

    def nearest_neighbors(self, start=0, mod=1):
        nn = [{k: self[k], (k+1): self[k+1]} for k in range(len(self)-1)]
        return nn[start::mod]


class Term:

    def __init__(self, subsets=[], cnumber=1, operators=[]):
        self.subsets = subsets
        self.cnumber = cnumber
        self.operators = operators

    def realize(self, realization):
        H = 0
        for subset in self.subsets:
            # TODO write more elegantly using zip?
            sites = list(subset.items())
            # for now, just assume that any permutation should be taken
            for permutation in permutations(sites):
                H += self.cnumber * realization(self.operators, permutation)
        return H


class Hamiltonian:

    def __init__(self, name="generic", lattice=Lattice(), terms=[]):
        self.name = name
        self.lattice = lattice
        self.terms = terms
        self._mf_sizes = [site.meanfield_dof for site in self.lattice]

    def realize(self, realization):
        return sum(term.realize(realization) for term in self.terms)

    def meanfield_energy(self, x):

        def mf_term(operators, sites):
            j = 0
            val = 1
            assert sites != []
            for operator, (i, site) in zip(operators, sites):
                assert operator.type == site.type
                if i == 0:
                    start = 0
                else:
                    start = int(np.product(self._mf_sizes[:i]))
                stop = start + self._mf_sizes[i]
                val *= operator.coherent_representation(x[start:stop])
                i += self._mf_sizes[i]
            return val

        energy = self.realize(mf_term)
        return np.real(energy)

    def anneal(self, **kwargs):
        size = int(np.product(self._mf_sizes))
        x0 = np.random.rand(size)
        res = opt.basinhopping(self.meanfield_energy, x0, **kwargs)
        return res

    def matrix(self, trunc=2, sparse=False):

        def op(index, o):
            matrix = o.exact_representation(trunc)
            d = matrix.shape[0]
            if sparse is True:
                matrix = sp.csr_matrix(matrix)
            lst = []
            for i, site in enumerate(self.lattice):
                if i == index:
                    lst.append(matrix)
                else:
                    if sparse is True:
                        lst.append(sp.identity(d))
                    else:
                        lst.append(np.identity(d))
            if sparse is True:
                return reduce(sp.kron, lst)
            else:
                return reduce(np.kron, lst)

        def exact_term(operators, sites):
            assert sites != 0
            return reduce(np.dot,
                          (op(i, o) for (o, (i, _))
                           in zip(operators, sites)))

        return self.realize(exact_term)

    def diagonalize(trunc=2, sparse=sparse, eigenvalues=False):
        m = self.matrix(trunc=trunc, sparse=sparse)
        if eigenvalues is False:
            eigenvalues = m.shape[0]
        return eigsh(m, k=eigenvalues)

    def __str__(self):
        return (self.name +
                " defined on %d sites" % len(self.lattice))

    def __repr__(self):
        return self.__str__()


class BoseHubbardHamiltonian(Hamiltonian):
    """Constructs a Bose Hubbard model
    """

    def __init__(self, t=1, u=0, n_sites=1):
        lattice = Lattice()
        for i in range(n_sites):
            lattice.append(BosonSite())
        b = Boson()
        i = Identity(b.type)
        n = b.conj() * b
        hopping = Term(lattice.nearest_neighbors(),
                       cnumber=t,
                       operators=[b.conj(), b])
        onsite = Term(lattice.sites(),
                      cnumber=u,
                      operators=[n*(n-i)])
        self.name = "Bose Hubbard Hamiltonian (t=%g, U=%g)" % (t, u)
        self.lattice = lattice
        self.terms = [hopping, onsite]


bh = BoseHubbardHamiltonian(t=1, u=1, n_sites=2)
e = bh.meanfield_energy([2, 0, 0, 0])
print(e)
print(bh.matrix(2, sparse=False))
