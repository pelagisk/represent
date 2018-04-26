class Hamiltonian:

    def __init__(self, types, terms):
        self.types = types
        self.terms = terms

def map_hamiltonian(hamiltonian, lattice, H, term):
    for tag, tag_terms in hamiltonian.terms.items():
        for (cnumber, operators) in tag_terms:
            for link in lattice.get_links(tag):
                H += cnumber * term(operators, link)
    return H
