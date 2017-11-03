import numpy as np
from represent import map_hamiltonian


def mean_field_hamiltonian(hamiltonian):
    """Constructs a mean-field energy functional from a Hamiltonian.
    """

    terms, lattice = hamiltonian
    n_sites = len(lattice)

    def mean_field_energy(x):

        def term(operators, sites):
            # TODO: now it only works with complex numbers...
            return np.product([
                o.coherent_representation(x[i] + 1j*x[n_sites+i])
                for (o, (i, _)) in zip(operators, sites)])

        energy = np.array([0.0], dtype='complex')
        energy = map_hamiltonian(hamiltonian, energy, term)
        return np.real(energy)

    return mean_field_energy
