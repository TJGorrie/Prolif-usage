#!/bin/bash
# Requires openbabel and propka to be in your path...
# Requires the absolute path + base_name of a folder containing a .mol file and an unliganded pdb file (e.g. _apo.pdb)
# E.g. /path/to/folder/filename
# where /path/to/folder/ contains filename.mol and filename_apo.pdb
# Usage ./plip.sh /path/to/folder/filename
prev=$(pwd)
babel -imol $1.mol -omol $1.pmol -p
propka31 $1_apo.pdb
f=$(basename -- $1_apo)
mv $f.propka_input $1.propka_input
mv $f.pka $1.pka
# Run PLIP with file outputs
python plip.py -i $1.mol -p $1.propka_input -m $1.pmol
# Clean up
rm $1.propka_input $1.pka $1.pmol

