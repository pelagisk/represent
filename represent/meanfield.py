import numpy as np
from .hamiltonian import map_hamiltonian


def mean_field_hamiltonian(hamiltonian, lattice):

    coh = lattice.get_coherent_param_sizes(hamiltonian)

    def chunk(x, i):
        if i > 0:
            start = sum(coh[:i])
        else:
            start = 0
        end = start + coh[i]
        return x[start:end]

    def mean_field_energy(x):

        def term(operators, link):
            return np.product([op.coherent_representation(chunk(x, i))
                              for (op, i) in zip(operators, link['indices'])])

        energy = np.array([0.0], dtype='complex')
        energy = map_hamiltonian(hamiltonian, lattice, energy, term)
        return np.real(energy)[0]

    return mean_field_energy
