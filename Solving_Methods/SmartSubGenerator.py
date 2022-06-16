import math

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
            for j in range(len(matrice_adja)):
                if (matrice_adja[j][i] !=0 or matrice_adja[i][j] !=0) and combi_prec[j] == 0:
                    combi_temp = combi_prec.copy()
                    combi_temp[j] = 1
                    if combi_temp not in combi_all[taille_etud]:
                        combi_all[taille_etud].append(combi_temp.copy())
                        subgen_rec(matrice_adja, max_ordre, combi_temp, taille_etud+1, combi_all)
    return combi_all


# génération de toutes les combinaisons connexes possibles à partir de chaque sommet et pour chaque tailles     
def subgen(matrice_adja, min_ordre, max_ordre):


    # cette variable est la structure qui contient les graphlet de chaque tailles
    combi_all_ord = []
    for i in range(max_ordre+1):
        combi_all_ord.append([])
    
    # remplissage de la matrice de taille 1
    for i in range(len(matrice_adja)):

        combi_all_ord[0].append([])
        for j in range(len(matrice_adja)):
            combi_all_ord[0][i].append(0)
        combi_all_ord[0][i][i] = 1


    # cette variable est la taille étudiée à chaque tour de l'execution, ou à chaque récursions
    taille_etud = 1
    for i in range(len(matrice_adja)):
        # appel de la fonction récursive pour chaque sommets étudiés
        combi_all_ord = subgen_rec(matrice_adja, max_ordre, combi_all_ord[0][i], taille_etud+1, combi_all_ord)

    if max_ordre == min_ordre:
        return combi_all_ord[min_ordre].copy()
    else:
        # juste une structure qui ne contient que les tailles qui nous intéresse
        comb_return = []    
        for i in range(max_ordre-min_ordre+1):
            comb_return.append(combi_all_ord[i+min_ordre].copy())

        return comb_return
    


