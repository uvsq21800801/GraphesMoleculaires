from pynauty import *

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

# Fait et retourne un certificat de graphe à partir d'une 
# combinaison de sommets
def combi_to_certif(combi, matrice_adja, atom_caract, dict_c):
    ###### Initialisations ######
    
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

    # coloriage des sommets
    list_sets = []
    for i in range(len(dict_c)):
        list_sets.append(set(list_by_colors[i]))
        
    g.set_vertex_coloring(list_sets)
        
    return certificate(g) ## PYNAUTY
