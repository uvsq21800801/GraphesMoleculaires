from math import comb
from pynauty import *
import networkx as nx
import pynauty
import binascii
import numpy as np

import time

def interize(combi_bool):

    combi_int = np.zeros(len(combi_bool), dtype=int)
    cdef int i
    for i in range(len(combi_int)):
        if combi_bool[i] == True:
            combi_int[i] += 1
        
    return combi_int



####
## 1. Algo principal de regroupement des sous-graphes par certificat canonique
####

def combi_iso(matrice_adja, atom_caract, lst_col, lst_combi, ordre, t_cerif, t_prep_c, t_fill):## 3 last values are test
    ## Structures de stockage :
    # Listes:
    lst_certif = [] #= identifiant : certificat
    lst_id = []  #= [identifiant*]
    # Dictionnaires: 
    # --> on peut revenir à des listes commes les identifiants sont consécutifs
    dict_isomorph = {} #= {identifiant: [combi*]}

    # les deux éléments mis dans ce tableau sont: 
    #     {le nb d'occurence, {nb de fois ou le sommet 1 est couvert, nb de fois ou le sommet 2 est couvert, ...}}
    dict_stat = {}     #= {identifiant: [nb_occurrence,  occurrence_sommet, taux_recouvrement, taux_occupation]}
    
    
    # initialisation le parametres liés à l'ordre du graphe et des sous-graphes
    taille = ordre

    ###### Boucle sur la liste de combinaison ######
    cdef int i
    
    for combi in lst_combi:
        # calcule du certificat de la combinaison
        (certif, t_cerif, t_prep_c) = combi_to_certif(combi, matrice_adja, atom_caract, lst_col, t_cerif, t_prep_c)
        ## ^ 2 last values are test
        time_begin = time.time()
        if certif not in lst_certif:
            lst_certif.append(certif)
            indice = lst_certif.index(certif)
            dict_isomorph[indice] = [interize(combi.copy())]
            dict_stat[indice] = [1,interize(combi.copy())]
            lst_id.append(indice)
        else:
            indice = lst_certif.index(certif)
            dict_isomorph[indice].append(interize(combi.copy()))
            tmp = dict_stat.get(indice)
            for i in range(len(combi)):
                if combi[i] == True:
                    tmp[1][i] += 1 
            dict_stat[indice] = [tmp[0]+1 , tmp[1].copy()]
        t_fill += time.time()-time_begin

    return dict_isomorph, dict_stat, lst_id, lst_certif, t_cerif, t_prep_c, t_fill ## 3 last values are test

###
# 2. Fonctions utiles
###

# Fonction qui génère une signature canonique à partir d'un graphe coloré
#
# La coloration se fera en ajoutant n arrètes à un sommet ayant la couleur
# numéro n.
def combi_to_certif(combi, matrice_adja, atom_caract, lst_col, t_cerif, t_prep_c):## 2 last values are test
    ###### Initialisations ######
    # création d'une liste permettant de renommer les sommets
    # en fonction des sommets non-concernés

    temp_prep_t = time.time()

    # liste [] de la taille de la combinaison contenant dans chaque case,
    # l'indice de l'élément dans la matrice d'adjacence
    ref = []
    cdef int i 
    for i in range(len(combi)):
        if combi[i] != 0:
            ref.append(i)
    
    # création d'un graphe PyNauty
    # g = Graph(len(ref), directed=True) 
    '''faudra probablement le mettre à la fin après'''

    # Pour chaque element pertinent, on va commencer à enregistrer les arcs
    # dans lesquels ils interviennent 
    # sous la forme: [queue de l'arc][liste des têtes de l'arc]
    listes_arcs =  []
    for i in range(len(ref)):
        listes_arcs.append([])

    # de plus pour chaque sommet initial, on a ajouter n arcs pointant vers 
    # un nouveau sommet, n étant l'indice de la couleur du sommet
    # Cela nous permettera de prendre en compte lors de la génération de 
    # signature de PyNauty. (De plus, parait-il, réduire le problème de cette 
    # façon serait moins couteux)
    dict_connex = {}
    num_prochain_sommet = len(ref)
    cdef int j
    for r in ref:
        
        # boucle dans la matrice d'adjacence pour trouver tous les sommets sur
        # lequel i pointe
        list_connex = []
        for j in range(len(matrice_adja)):
            
            if matrice_adja[r][j] != 0 and combi[j] == 1:
                    list_connex.append(ref.index(j))

        # création des nouveaux sommets par couleurs
        temp_couleur = atom_caract[r].split()
        nb_couleur = lst_col.index(temp_couleur[0])+1 # +1 car on veut éviter que la couleur 0 ne crée de confusion
                                                    # (je ne suis pas sûre si cela crucial mais ça ne peut être 
                                                    #  un détriment)
        
        for j in range(nb_couleur):
            list_connex.append(num_prochain_sommet)
            num_prochain_sommet += 1
        
        # ajout de la liste d'arcs dont ref(index) i est la queue dans le dictionnaire
        dict_connex.setdefault(ref.index(r),list_connex)

    # génération du graph
    g = Graph(num_prochain_sommet, directed=True, adjacency_dict=dict_connex) 
    
    t_prep_c += time.time()-temp_prep_t

    temp_t_cert = time.time()
    cf = certificate(g)
    t_cerif += time.time()-temp_t_cert
    return cf, t_cerif, t_prep_c ## ^ 2 last values are test