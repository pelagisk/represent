import unittest

import numpy as np
from scipy.sparse.linalg import eigsh
import scipy.optimize as opt
import matplotlib.pyplot as plt
from represent.lattice import simple_chain
from represent.bosehubbard import bose_hubbard_hamiltonian
from represent.exact import exact_hamiltonian
from represent.meanfield import mean_field_hamiltonian


class TestBoseHubbard(unittest.TestCase):

    def test_1(self):

        N = 5
        lattice = simple_chain(N)

        def print_fun(x, f, accepted):
            print("at minima %.4f: accepted?: %d" % (f, accepted))

        ts = np.linspace(2, 10, 11)
        energies_exact = np.zeros(len(ts))
        energies_mf = np.zeros(len(ts))
        for i, t in enumerate(ts):
            print("t = ", t)
            h = bose_hubbard_hamiltonian(t=t, u=1, mu=0, truncation=3)

            H = exact_hamiltonian(h, lattice)
            e, v = eigsh(H, k=1, which='SA')
            energies_exact[i] = e

            mf = mean_field_hamiltonian(h, lattice)
            x0 = np.random.rand(2*N)
            res = opt.basinhopping(mf, x0,
                                   minimizer_kwargs={'method': 'powell'},
                                   callback=print_fun,
                                   niter=5)
            energies_mf[i] = res.fun

        plt.plot(ts, energies_exact, label="Exact")
        plt.plot(ts, energies_mf, label="Mean-field")
        plt.legend()
        plt.show()

        # TODO actually test something...
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()
