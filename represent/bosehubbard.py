from .sitetypes import SiteType
from .operators import AnnihilateBoson, Identity
from .hamiltonian import Hamiltonian


def bose_hubbard_hamiltonian(t=1, u=0, mu=0, truncation=3):
    boson = SiteType("boson", truncation, 2)
    types = {'generic': boson}
    b = AnnihilateBoson(boson)
    n = b.H() * b
    i = Identity(boson)
    interaction = u, [n*(n-i)]
    chem = (-mu), [n]
    nn = t, [b.H(), b]
    terms = {'onsite': [interaction, chem], 'nn': [nn]}
    return Hamiltonian(types, terms)
