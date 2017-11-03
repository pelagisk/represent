from operators import Boson, Identity


def bose_hubbard_hamiltonian(t=1, u=0, n_sites=2):
    lattice = dict((i, {'type': 'boson'}) for i in range(n_sites))
    singletons = [{k: v} for k, v in lattice.items()]
    nearest_neighbors = [{k: lattice[k], (k+1): lattice[k+1]}
                         for k in range(len(lattice)-1)]
    b = Boson()
    i = Identity(b.type)
    n = b.conj() * b
    hopping = [nearest_neighbors, t, [b.conj(), b]]
    onsite_energy = [singletons, u, [n*(n-i)]]
    return [hopping, onsite_energy], lattice
