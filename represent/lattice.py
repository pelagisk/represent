class Lattice:

    def __init__(self, kinds, links):
        self.kinds = kinds
        self.links = links

    def get_dims(self, hamiltonian):
        return [hamiltonian.types[kind].dims for kind in self.kinds]

    def get_coherent_param_sizes(self, hamiltonian):
        return [hamiltonian.types[kind].coherent_parameters for kind in self.kinds]

    def get_links(self, tag):
        return filter(lambda x: tag in x['tags'], self.links)


def simple_chain(N, periodic=False):
    kinds = ['generic' for i in range(N)]
    links = [{'indices': [i], 'tags': set(["onsite"])} for i in range(N)]
    links += [{'indices': [i, i+1], 'tags': set(["nn", "nn_left"])} for i in range(N-1)]
    links += [{'indices': [i+1, i], 'tags': set(["nn", "nn_right"])} for i in range(N-1)]
    if periodic == True:
        links.append({'indices': [N-1, 0], 'tags': set(["nn", "nn_left"])})
        links.append({'indices': [0, N-1], 'tags': set(["nn", "nn_right"])})
    return Lattice(kinds, links)

def unit_cell_chain(cell, N_cells, periodic=False):
    n_cell = len(cell)
    kinds = []
    links = []
    for i in range(N_cells):
        for j, kind in enumerate(cell):
            idx = n_cell*i+j
            kinds.append(kind)
            nn_tag = "nn_" + kind
            links.append({'indices': [idx],
                          'tags': set(["onsite"])})
            links.append({'indices': [idx, idx+1],
                          'tags': set([nn_tag, nn_tag + "_left"])})
            links.append({'indices': [idx+1, idx],
                          'tags': set([nn_tag, nn_tag + "_right"])})
    if periodic == True:
        N = n_cell*N_cells
        kind = cell[-1]
        nn_tag = "nn_" + kind
        links.append({'indices': [N-1, 0], 'tags': set([nn_tag, nn_tag + "_left"])})
        links.append({'indices': [0, N-1], 'tags': set([nn_tag, nn_tag + "_right"])})
    return Lattice(kinds, links)
