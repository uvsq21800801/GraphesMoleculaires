import math
import threading
from copy import copy, deepcopy

'''
# explication de l'algorithme
On prends un sommet, on génère tous les sous-graphes connexes qui le contiennent en utilisant la matrice d'adjacense

'''


# fonction recursive qui va chercher toutes les combinaisons générables depuis la combinaison précédente
def subgen_rec(matrice_adja, max_ordre, combi_prec, taille_etud, combi_all):
    if (taille_etud > max_ordre):
        return combi_all

    for i in range(len(matrice_adja)):
    
        if combi_prec[i] != 0:
            for j in range(0, len(matrice_adja)):
                if (matrice_adja[j][i] !=0 or matrice_adja[i][j] !=0) and combi_prec[j] == 0:
                    combi_temp = combi_prec.copy()
                    combi_temp[j] = 1
                    if combi_temp not in combi_all[taille_etud]:
                        combi_all[taille_etud].append(combi_temp.copy())
                        subgen_rec(matrice_adja, max_ordre, combi_temp, taille_etud+1, combi_all)
    return combi_all

# fonction recursive qui va parcourir tous les sommets de manière croissante
def choix_rec(matrice_adja, max_ordre, combi_prec, taille_etud, combi_all, degres):

    print(1)


# génération de toutes les combinaisons connexes possibles à partir de chaque sommet (dans l'ordre croissant) 
# et pour chaque tailles     
def subgen_deg_decroiss(matrice_adja, min_ordre, max_ordre):
    taille = len(matrice_adja)

    # tri des sommets par degré
    degres = [] # degrés [1, n]
    for i in range(10):
        degres.append([])

    # liste temporaire pour stocker les degrés
    temp_list = []
    copy_adja = deepcopy(matrice_adja)

    # ajout des degrés dans la liste
    for i in range(0, taille):
        count = 0
        for j in range(0, taille):
            if matrice_adja[i][j]>0 or matrice_adja[j][i] > 0:
                count += 1
        temp_list.append(count)

    # ajout de la liste dans la structure de degrés
    for i in range(taille):
        degres[10-temp_list[i]-1].append(i)


    # cette variable est la structure qui contient les graphlet de chaque tailles
    combi_all_ord = []
    for i in range(max_ordre+1):
        combi_all_ord.append([])
    
    # remplissage de la matrice de taille 1
    for i in range(taille):

        combi_all_ord[0].append([])
        for j in range(taille):
            combi_all_ord[0][i].append(0)
        combi_all_ord[0][i][i] = 1
    '''
    # appel de la fonction de choix des sommets (récursif)
    combi_all_ord = choix_rec(matrice_adja, max_ordre, combi_all_ord[0][i], taille_etud+1, combi_all_ord, degres)

    #future truc à supprimer
    # cette variable est la taille étudiée à chaque tour de l'execution, ou à chaque récursions
    taille_etud = 1
    for i in range(len(matrice_adja)):
        # appel de la fonction récursive pour chaque sommets étudiés
        combi_all_ord = subgen_rec(matrice_adja, max_ordre, combi_all_ord[0][i], taille_etud+1, combi_all_ord, i)
    '''
    taille_etud = 1
    i = 0
    while i < 10:
        if degres[i]:
            combi_all_ord = subgen_rec(copy_adja, max_ordre, combi_all_ord[0][degres[i][0]], taille_etud+1, combi_all_ord)
            for j in range(taille):
                
                if copy_adja[j][degres[i][0]] != 0 or copy_adja[degres[i][0]][j] != 0:
                    copy_adja[j][degres[i][0]] = 0 
                    copy_adja[degres[i][0]][j] = 0
                    for k in range(10):
                        if j in degres[9-k]:
                            degres[9-k].remove(j)
                            if k > 0:
                                degres[9-k+1].append(j)
                
            del degres[i][0]
            i = i - 1
            if i < 0:
                i = 0
        else :
            i += 1

    if max_ordre == min_ordre:
        return combi_all_ord[min_ordre].copy()
    else:
        # juste une structure qui ne contient que les tailles qui nous intéresse
        comb_return = []    
        for i in range(max_ordre-min_ordre+1):
            comb_return.append(combi_all_ord[i+min_ordre].copy())

        return comb_return
    


