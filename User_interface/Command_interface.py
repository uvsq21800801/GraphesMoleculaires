# sera une interface de commande si besoin
import sys
sys.path.append('GraphesMoleculaires/Inputs_Outputs')
sys.path.append('GraphesMoleculaires/Solving_Methods')

from Inputs_Outputs import Inputs
from Solving_Methods import BruteForce

def interface():
    #recuperation des donnees des fichiers
    listindex = []
    atom_caract = []
    Inputs.Input_trad(listindex, atom_caract)
    print(atom_caract)
    print(listindex)
    matriceadja = []
    Inputs.Input_bonds(listindex, matriceadja)
    print(matriceadja)
    print(listindex)

    #methode de resolution -> bruteforce
    resultat = []
    BruteForce.BruteF(listindex, matriceadja, resultat)
    