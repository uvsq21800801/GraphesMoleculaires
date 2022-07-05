import math

'''
# explication de l'algorithme
On prends un sommet, on génère tous les sous-graphes connexes qui le contiennent en utilisant la matrice d'adjacense

'''
import numpy as np

#test for exact equality
def arreq_in_list(myarr, list_arrays):
    return next((True for elem in list_arrays if np.array_equal(elem, myarr)), False)

# fonction recursive qui va chercher toutes les combinaisons générables depuis la combinaison précédente
def subgen_rec(matrice_adja, max_ordre, combi_prec, taille_etud, combi_all, sommets_elim):
    if (taille_etud > max_ordre):
        return combi_all

    cdef int len_matrice = len(matrice_adja)
    cdef int i 
    cdef int j
    for i in range(len_matrice):
    
        if combi_prec[i] != 0:
            for j in range(sommets_elim, len_matrice):
                if (matrice_adja[j][i] !=0 or matrice_adja[i][j] !=0) and combi_prec[j] == 0:
                    combi_temp = combi_prec.copy()
                    combi_temp[j] = 1
                    if not arreq_in_list(combi_temp, combi_all[taille_etud]):
                    #if combi_temp not in combi_all[taille_etud]:
                        combi_all[taille_etud].append(combi_temp.copy())
                        subgen_rec(matrice_adja, max_ordre, combi_temp, taille_etud+1, combi_all, sommets_elim)
    return combi_all


# génération de toutes les combinaisons connexes possibles à partir de chaque sommet et pour chaque tailles     
def subgen(matrice_adja, min_ordre, max_ordre):

    cdef int i

    # cette variable est la structure qui contient les graphlet de chaque tailles
    combi_all_ord = []
    #cdef int combi_all_ord[max_ordre+1]
    for i in range(max_ordre+1):
        combi_all_ord.append([])
    
    # remplissage de la matrice de taille 1

    for i in range(len(matrice_adja)):
        temp_matrix = np.zeros(len(matrice_adja), dtype=bool)
        temp_matrix[i] = True
        #combi_all_ord[0].append([])
        #for j in range(len(matrice_adja)):
        #    combi_all_ord[0][i].append(0)
        #combi_all_ord[0][i][i] = 1
        combi_all_ord[0].append(temp_matrix.copy())
    
    # cette variable est la taille étudiée à chaque tour de l'execution, ou à chaque récursions
    taille_etud = 1
    for i in range(len(matrice_adja)):
        # appel de la fonction récursive pour chaque sommets étudiés
        combi_all_ord = subgen_rec(matrice_adja, max_ordre, combi_all_ord[0][i], taille_etud+1, combi_all_ord, i)

    if max_ordre == min_ordre:
        return combi_all_ord[min_ordre].copy()
    else:
        # juste une structure qui ne contient que les tailles qui nous intéresse
        comb_return = []    
        for i in range(max_ordre-min_ordre+1):
            comb_return.append(combi_all_ord[i+min_ordre].copy())

        return comb_return
    


