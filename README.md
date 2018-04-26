# Automatic generation of different representations of discrete quantum systems

## Goals

The goal is to be able to represent a quantum Hamiltonian of discrete degrees of freedom, and to be able to automatically convert this representation into a form suitable for:

- exact diagonalization
- mean-field theory
- tensor methods (DMRG, TEBD)
- etc.

Code is on the idea stage and will be heavily edited later.

## Description

- `SiteType`: holds information about local Hilbert space dimension and the dimension required for a coherent-state representation.
- `Lattice`: consists of a set of sites, each of a certain "kind". There are also "links" between the sites which can have a number of "tags". "Kinds" and "tags" are useful for addressing.
- `Operator`: an abstract local operator. Can be represented in many concrete ways.
- `Hamiltonian`: essentially a labelling of a `Lattice`: each "kind" is designated a `SiteType` and each "tag" of links correspond to a product of local operators.

The idea is then that a lattice and a Hamiltonian can be defined independently, and transformed to concrete matrices when needed.

See tests!

## Setup

Written for Python 3. Requires installing the following Python packages:

- `numpy`
- `scipy`
- `matplotlib`

Run test(s) from the root directory:

`python3 -m unittest discover`

## License

GNU GPL v3

## Author

Axel Gagge, 2017
