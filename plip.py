import argparse
import os
import glob
import prolif as plf
from rdkit import Chem
from prolif.plotting.network import LigNetwork

def generatePLIP(mol, propka, pmol):
    root_fn = mol.replace('.mol', '')
    output = f'{root_fn}_plip.html'
    pdb_mol = Chem.MolFromPDBFile(propka, removeHs=False)
    prot = plf.Molecule.from_rdkit(pdb_mol)
    net_mol = Chem.MolFromMolFile(mol, removeHs=False)
    lig_mol = Chem.MolFromMolFile(pmol, removeHs=False)
    lig = plf.Molecule.from_rdkit(lig_mol)
    print('Fingerprinting')
    fp = plf.Fingerprint(interactions='all')
    ifp = fp.generate(lig, prot, return_atoms=True)
    ifp["Frame"] = 0
    print('Network')
    df = plf.to_dataframe([ifp], fp.interactions.keys(), return_atoms=True)
    net = LigNetwork.from_ifp(df, net_mol, kind="frame", frame=0)
    net.save(output)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i",
        "--input",
        help="Input file",
        required=True
    )
    parser.add_argument(
        "-m",
	"--babelmol",
        help="Input file",
        required=True
    )
    parser.add_argument(
        "-p",
	"--propka",
        help="Input file",
        required=True
    )
    args = vars(parser.parse_args())
    file = args["input"]
    babel = args["babelmol"]
    propka = args["propka"]
    generatePLIP(mol=file, propka=propka, pmol=babel)
