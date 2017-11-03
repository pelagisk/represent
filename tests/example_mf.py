import numpy as np
import scipy.optimize as opt
import matplotlib.pyplot as plt
from bosehubbard import bose_hubbard_hamiltonian
from meanfield import mean_field_hamiltonian

# TODO finish rewriting the imports this way.
# from .context import represent

def print_fun(x, f, accepted):
    print("at minima %.4f accepted %d" % (f, int(accepted)))


n_sites = 4

# mf = mean_field_hamiltonian(bose_hubbard_hamiltonian(t=0, u=1, n_sites=2))
# print(mf([2,0,0,0]))

ts = np.linspace(0, 2, 11)
energies = np.zeros(len(ts))
for i, t in enumerate(ts):
    h = bose_hubbard_hamiltonian(t=t, u=1, n_sites=n_sites)
    mf = mean_field_hamiltonian(h)
    x0 = np.random.rand((2*n_sites))
    res = opt.basinhopping(mf, x0,
                           minimizer_kwargs={'method': 'powell'},
                           callback=print_fun,
                           niter=1)
    energies[i] = res.fun
plt.plot(ts, energies)
plt.show()
