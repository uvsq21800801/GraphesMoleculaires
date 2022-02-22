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
    #print(listindex)
    #print(atom_caract)
    matriceadja = []
    Inputs.Input_bonds(listindex, matriceadja)
    #affiche_adja(matriceadja)

    #methode de resolution -> bruteforce
    resultat = []
    (isomorph_dict, recouvre_dict) = BruteForce.BruteF(listindex, matriceadja, atom_caract, resultat)
    BruteForce.Taux_recouvert(recouvre_dict)

    ### fonctions résultats
    '''
    # affiche par ordre (minimum à 3) le nombre de certif
    print("Ordre - Nb certif")
    for i in range(int(len(resultat))):
        print('  '+str(i+3)+'   - '+str(len(resultat[i])))*
    '''
    print("Isomorphes")
    print("certificat   nombre_occurence   taux_recouvrement")
    print("premier isomorphe [> apparition par sommets]")
    affiche_iso(resultat, isomorph_dict, recouvre_dict)


### fonctions de débuggage
def affiche_adja(matriceadja):
    r = int(len(matriceadja))
    for i in range(r):
        print(matriceadja[i])

def affiche_adja2(matriceadja):
    r = int(len(matriceadja))
    for i in range(r):
        s = ''
        for j in range(r):
            s += str(matriceadja[i][j])+' '
        print(s)

def affiche_liste(l):
    s = ''
    for i in range(len(l)):
        s += str(l[i])
    return s

def affiche_iso(resultat, isomorph_dict, recouvre_dict):
    for i in range(len(resultat)):
        print('Ordre '+str(i+3)+' : '+str(len(resultat[i]))+' certificats')
        for certif in resultat[i]:
            tmp1 = isomorph_dict.get(certif)
            tmp2 = recouvre_dict.get(certif)
            if tmp2[0] > 1:
                print(certif.hex()+'   '+str(tmp2[0])+'   '+str(tmp2[2]))
                print(affiche_liste(tmp1[0])+' > '+affiche_liste(tmp2[1]))
            ''' n'affiche pas les certificat de sous-graphe connexe unique
            else :
                print(certif.hex()+'   '+str(tmp2[0])+'   '+str(tmp2[2]))
                print(affiche_liste(tmp1[0]))
            '''

