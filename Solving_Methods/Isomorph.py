from math import comb
from pynauty import *
import networkx as nx
import pynauty
import binascii

####
## 1. Algo principal de regroupement des sous-graphes par certificat canonique
####

def combi_iso(matrice_adja, atom_caract, lst_combi, ordre):
    ## Structures de stockage :
    # Listes:
    lst_certif = [] #= identifiant : certificat
    lst_id = []  #= [identifiant*]
    # Dictionnaires: 
    # --> on peut revenir à des listes commes les identifiants sont consécutifs
    dict_isomorph = {} #= {identifiant: [combi*]}

    # les deux éléments mis dans ce tableau sont: 
    #     {le nb d'occurence, {nb de fois ou le sommet 1 est couvert, nb de fois ou le sommet 2 est couvert, ...}}
    dict_stat = {}     #= {identifiant: [nb_occurrence,  occurrence_sommet, taux_recouvrement, recouvrement, taux_occupation]}
    
    # initialisation du dictionnaire des couleurs
    (dict_couleur, couleur_nb) = init_col(atom_caract)
    
    # initialisation le parametres liés à l'ordre du graphe et des sous-graphes
    taille = ordre

    ###### Boucle sur la liste de combinaison ######
    for combi in lst_combi:
        # calcule du certificat de la combinaison
        certif = combi_to_certif(combi, matrice_adja, atom_caract, dict_couleur)
        #print(certif.hex())
        if certif not in lst_certif:
            lst_certif.append(certif)
            indice = lst_certif.index(certif)
            dict_isomorph[indice] = [combi.copy()]
            dict_stat[indice] = [1,combi.copy()]
            lst_id.append(indice)
        else:
            indice = lst_certif.index(certif)
            dict_isomorph[indice].append(combi.copy())
            tmp = dict_stat.get(indice)
            for i in range(len(combi)):
                tmp[1][i] += combi[i]
            dict_stat[indice] = [tmp[0]+1,tmp[1].copy()]
            #affiche_combi(tmp[1], taille)
    
    #print (dict_isomorph)
    return dict_isomorph, dict_stat, lst_id, lst_certif

###
# 2. Fonctions utiles
###

# Initialisation des couleurs
def init_col(atom_caract):
    couleur_nb = 0
    dict_couleur = {}    
    for i in atom_caract:
        splitted = i.split()
        if splitted[0] not in dict_couleur:
            dict_couleur[splitted[0]] = couleur_nb 
            couleur_nb += 1
    return dict_couleur, couleur_nb

# Fonction qui génère une signature canonique à partir d'un graphe coloré
#
# La coloration se fera en ajoutant n arrètes à un sommet ayant la couleur
# numéro n.
def combi_to_certif(combi, matrice_adja, atom_caract, dict_c):
    ###### Initialisations ######
    # création d'une liste permettant de renommer les sommets
    # en fonction des sommets non-concernés


    # liste [] de la taille de la combinaison contenant dans chaque case,
    # l'indice de l'élément dans la matrice d'adjacence
    ref = []
    for i in range(len(combi)):
        if combi[i] != 0:
            ref.append(i)
    
    # création d'un graphe PyNauty
    g = Graph(len(ref), directed=True) 
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
    for i in ref:
        
        # boucle dans la matrice d'adjacence pour trouver tous les sommets sur
        # lequel i pointe
        list_connex = []
        for j in range(len(matrice_adja)):
            
            if matrice_adja[i][j] != 0 and combi[j] == 1:
                    list_connex.append(ref.index(j))

    #print (matrice_adja)

    return certificate(g)

# Fait et retourne un certificat de graphe à partir d'une 
# combinaison de sommets
# DEPRECATED
def combi_to_certif_broken(combi, matrice_adja, atom_caract, dict_c):
    ###### Initialisations ######
    print('')
    print('combi: '+ str(combi))
    # création d'une liste permettant de renommer les sommets
    # en fonction des sommets non-concernés
    nv_nom = []
    enum = 0
    for i in range(len(combi)):
        if combi[i] == 1:
            nv_nom.append(enum)
            enum += 1
        else:
            nv_nom.append('')

    # initialisation de la liste des sommets classés par couleur
    list_by_colors = []
    for i in range(len(dict_c)):
        list_by_colors.append([])

    # initialisation du graph
    g = Graph(enum, directed=True) ## PYNAUTY
    
    ###### Algo ######
    # remplissage des adjacences
    list_adja = []
    sommet_n = 0
    for i in range(len(combi)):
        listconnex = []
        if combi[i] == 1:
            for j in range(len(combi)):
                if matrice_adja[i][j] != 0 and combi[j] == 1:
                    #print(nv_nom[j])
                    listconnex.append(nv_nom[j])
            #g.connect_vertex(sommet_n, listconnex)
            temp = atom_caract[i].split()
            #dict_c.get(temp)
            list_by_colors[dict_c.get(temp[0])].append(nv_nom[i]) #to int needed maybe
            sommet_n += 1
            g.connect_vertex(nv_nom[i], listconnex)
            list_adja.append(listconnex)

    # coloriage des sommets
    list_sets = []
    for i in range(len(dict_c)):
        list_sets.append(set(list_by_colors[i]))
        
    g.set_vertex_coloring(list_sets)
    
    print(g)
    return certificate(g)

    #print('')

    #print(list_by_colors)
    #print(list_adja)
    #print(g.adjacency_dict)
    #print(g.vertex_coloring)

    #print('')
    #print('colors: '+str(list_by_colors))

    print('canonlabel: '+ str(canon_label(g)))
    print('graph: '+str(g))

    #
    canon_lbl = canon_label(g)
    
    # initialisation du graph canonique
    new_g = Graph(enum, directed=True) ## PYNAUTY

    for i in range(len(canon_lbl)):
        # copie du dictionnaire pour avoir un array de même
        # taille
        new_dict = g.adjacency_dict[i].copy()
        j = 0
        for m in g.adjacency_dict[i]:
            new_dict[canon_lbl.index(m)] = int(m)
            j += 1
        new_g.connect_vertex(i, new_dict)
        
    '''
    i = 0
    for l in canon_lbl:
        new_dict = g.adjacency_dict[l].copy()
        
        j = 0 
        for m in g.adjacency_dict[l]:
            new_dict[j] = int(canon_lbl[m])
            j += 1
        
        new_g.connect_vertex(i, new_dict)
        i += 1
    '''
    list_new_colors = []
    for i in range(len(g.vertex_coloring)):
        new_color = []
        temp_set = g.vertex_coloring[i].copy()
        for elem in temp_set:
            new_color.append(canon_lbl[elem])
        #print('new set: '+str(new_color))
        #print('vert col: '+str(g.vertex_coloring[i]))
        list_new_colors.append(set(new_color))
        

    new_g.set_vertex_coloring(list_new_colors)

    '''
    # initialisation de la liste des sommets classés par couleur
    list_by_colors = []
    for i in range(len(dict_c)):
        list_by_colors.append([])

    
    new_list_sets = []
    for i in range(len(dict_c)):
        new_list_sets.append(set(list_by_colors[canon_lbl[i]]))


    ###### Algo ######
    # remplissage des adjacences
    
    for i in canon_lbl:
        listconnex = []
        if combi[i] == 1:
            for j in range(len(combi)):
                if matrice_adja[i][j] != 0 and combi[j] == 1:
                    #print(nv_nom[j])
                    listconnex.append(nv_nom[j])
            #g.connect_vertex(sommet_n, listconnex)
            temp = atom_caract[i].split()
            #dict_c.get(temp)
            list_by_colors[dict_c.get(temp[0])].append(nv_nom[i]) #to int needed maybe
            sommet_n += 1
            new_g.connect_vertex(nv_nom[i], listconnex)

    list_sets = []
    for i in range(len(dict_c)):
        list_sets.append(set(list_by_colors[i]))
        
    new_g.set_vertex_coloring(list_sets)

    '''
    #print('new colors: '+str(list_by_colors))

    print('new canonlabel: '+ str(canon_label(new_g)))
    print('new graph: '+str(new_g))

    return (str(new_g)).encode('ascii')
