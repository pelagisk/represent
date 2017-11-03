# Automatic generation of different representations of discrete quantum systems

## Goals

The goal is to be able to represent a quantum Hamiltonian of discrete degrees of freedom, and to be able to automatically conveert this representation into a form suitable for:

- exact diagonalization
- mean-field theory
- tensor methods (DMRG, TEBD)
- etc.

Code is on the idea stage and will be heavily edited later.

## Ideas

- Dict of nodes represents the lattice.
- Sublists of this list are:
  - Singletons: references one-site terms
  - Pairs: two-body terms
  - etc..
  - does it have to be ordered? How does this affect Hamiltonians?
  - each site can only have one type of operators defined!
- One can classify the sublists into different types, each with a label.

- Hamiltonians are a function from a possible list of variable arguments,
  to a list of terms, where each term is:
  - a reference to a type of sublist
  - a c-number variable: here the variable arguments come in
  - a list of references to operators,
    matching the shape of the type of sublist

- Operators are:
  - a label
  - additional info and description
  - different representations: mean-field, DMRG, exact diagonalization.
  - would be nice if it was possible to multiply and add them?
  - best to work with objects for this?

- How should the relation between node "type" (local Hilbert space) and operators be interpreted?

## Setup

Written for Python 3. Requires installing the following Python packages:

- `numpy`
- `scipy`
- `matplotlib`

## License

GNU GPL v3

## Author

Axel Gagge, 2017
