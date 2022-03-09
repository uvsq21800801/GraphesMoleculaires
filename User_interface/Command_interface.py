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
    filename1 = Inputs.Input_trad(listindex, atom_caract)
    #print(listindex)
    #print(atom_caract)
    matriceadja = []
    filename2 = Inputs.Input_bonds(listindex, matriceadja)
    #affiche_adja(matriceadja)
    
    # test que les fichiers sont bien associés
    if filename1 != filename2 :
        print("Erreur de lecture de fichiers "+filename1+" "+filename2)
        return 1
    
    # définition des ordres des sous-graphes
    max_ordre = 8
    min_ordre = 3

    # methode de resolution -> bruteforce
    (isomorph_dict, recouvre_dict, lst_ordre, lst_c) = BruteForce.BruteF(listindex, matriceadja, atom_caract, max_ordre, min_ordre)
    # calcul et ajoute le taux de recouvrement
    BruteForce.Taux_recouvert(recouvre_dict)

    ### fonctions résultats
    '''
    # affiche par ordre le nombre de certif
    print("Ordre - Nb forme canonique")
    for i in range(int(len(lst_ordre))):
        print('  '+str(i+min_ordre)+'   - '+str(len(lst_ordre[i])))*
    '''
    # Affiche les Isomorphes
    #print("ordre certificat nombre_occurence taux_recouvrement exemple recouvrement")
    #affiche_iso(lst_ordre, isomorph_dict, recouvre_dict, lst_c)
    
    # Diagramme taux par nombre d'occurance croissant
    # --> il serait mieux de rassembler les nombre d'occurance et taux de recouvrement par ordre des sous-graphe pour ça
    ## imprime dans un fichier les données trié
    for i in range(int(len(lst_ordre))):
        Inputs.Output_diagramme(filename1, i, min_ordre, lst_ordre, recouvre_dict)
    
    return 0


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
    s = '"'
    for i in range(len(l)):
        s += str(l[i])
    return s+'"'

def affiche_iso(lst_ordre, isomorph_dict, recouvre_dict, lst_c):
    for i in range(len(lst_ordre)):
        iso_uniq = 0
        #print('Ordre '+str(i+3)+' : '+str(len(lst_ordre[i]))+' certificats')
        for indice in lst_ordre[i]:
            tmp1 = isomorph_dict.get(indice)
            tmp2 = recouvre_dict.get(indice)
            if tmp2[0] > 1:
                #     ordre         certificat              nombre_occurence taux_recouvrement exemple recouvrement
                print(str(i+3)+' "'+lst_c[indice].hex()+'" '+str(tmp2[0])+' '+str(tmp2[2])+' '+affiche_liste(tmp1[0])+' '+affiche_liste(tmp2[1]))
            else :
                #iso_uniq += 1
                print(str(i+3)+' "'+lst_c[indice].hex()+'" '+str(tmp2[0])+' '+str(tmp2[2])+' '+affiche_liste(tmp1[0])+' '+affiche_liste(tmp2[1]))
    #print(iso_uniq)
