from Solving_Methods import Mcis_decl
from Solving_Methods import BronKerborsch.py

'''
######## Etude de la similarité des sous-graphes dans un jeux de combinaison d'un graphe

Perspectives : Généralisé l'étude sur un jeux de motif avec matrice d'adjacences et caractéristiques atomiques associées
'''

# Fonction calculant les valeurs de la table de chaleur sur un ensemble de combinaison unique
#
# Entrées: detail d'exécution, matrice d'adjacence , caractéristique des atomes, liste des identifiants de motif, dict les rassemblant et parametre d'exécution
#
# Sortie: Tableau [x] [y]

def Similarity(matrice_adja, atom_caract, lst_id, dict_iso, detail):
    # Tableau rassemblant les matrice d'adjacence et caractéristique des motifs
    cb = len(lst_id)
    adja_s = [None for x in range(cb)]
    carac_s = [None for x in range(cb)]

    # tableau de sortie
    tab_ord = [[None for y in range(cb)] for x in range(cb)]

    # initialisation des sous-graphes à évaluer
    for i in range(cb):
        getlist = dict_iso[lst_id[i]]
        (adja_s[i], carac_s[i]) = extract_sub(
            matrice_adja, atom_caract, getlist[0])
    
    # boucle sur tous les duo à évaluer selon la méthode choisie et 
    for i in range(cb):
        for j in range(cb):
            if detail[2] == 1 and j>i:
                tab_ord[i][j] = 1 - Mcis_decl.simmilarite(adja_s[i], carac_s[i], adja_s[j], carac_s[j])
                tab_ord[j][i] = tab_ord[i][j]
            if detail[2] == 2 and j>i:
                tab_ord[i][j] = Mcis_decl.sim_raymond(adja_s[i], carac_s[i], adja_s[j], carac_s[j])
                tab_ord[j][i] = tab_ord[i][j]
            if detail[2] == 3 :
                tab_ord[i][j] = Mcis_decl.sim_barth(adja_s[i], carac_s[i], adja_s[j], carac_s[j], i, j)
            if i == j :
                tab_ord[i][i] = 1

    # print(tab_ord)
    return tab_ord

# Fonction calculant les valeurs de la table de chaleur sur une liste d'ensemble de combinaison (taille par taille)
#
# Entrées: matrice d'adjacence , caractéristique des atomes, liste des identifiants de motif par ordre et dict les rassemblant
#
# Sortie: Tableau [ordre - min] [x] [y]

def Similarity_range(matrice_adja, atom_caract, lst_ord, dict_iso, min_ordre, max_ordre, detail):
    # Tableau rassemblant les matrice de chaleur sur les différents ensembles étudiés
    tab_sim = []
    # Etude par ensemble
    for h in range(max_ordre - min_ordre+1):
        tab_sim.append(Similarity(matrice_adja, atom_caract, lst_ord[h], dict_iso, detail))
    return tab_sim


# Distance d'édition
# Metrique de Raymond symétrique
# Metrique de Raymond asymétrique
