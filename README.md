# What should I install?

## Virtual environment for Python3
Refer to: https://docs.python.org/3/library/venv.html

Create new envinronment
> python -m venv /path/to/new/virtual/environment

To activate:
> sourve <venv>/bin/activate

## Packages to install for Python3

PyCryptoDome
> pip install pycryptodome

pwntools
> pip install pwntools

## Useful tools 

### Number Field Sieve
Using cado-nfs, one can compute factorisation, dicrete log, ...

Refer to: https://gitlab.inria.fr/cado-nfs/cado-nfs

### Lattice 
https://github.com/josephsurin/lattice-based-cryptanalysis (have not used)
https://github.com/TheBlupper/linineq  (also have not used, but seems can solve linear combination in mod)
https://github.com/kionactf/coppersmith (Coppersmith attack)
