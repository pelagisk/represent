import numpy as np
from scipy.sparse.linalg import eigsh
import scipy.optimize as opt
import matplotlib.pyplot as plt

# TODO finish rewriting the imports this way.
# from .context import represent

from bosehubbard import bose_hubbard_hamiltonian
from exact import exact_hamiltonian

h = bose_hubbard_hamiltonian(t=0.1, u=2, n_sites=5)
matrix = exact_hamiltonian(h, trunc=5)
e, v = eigsh(matrix, k=1, which='SA')
print("Energy of ground state is %g" % e)
