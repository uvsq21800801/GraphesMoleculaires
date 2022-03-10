import math
from pynauty import *


# Explication de l'algorithme générale
#   Génération d'une liste de combinaison de sommets = sous-graphe 
#       combi[i] = 1 si sommet i appartient au sous-graphe
#                = 0 sinon
#   Si le sous-graphe est connexe, alors il est sauvegarder dans dict_combi
#       la clé du dictionnaire est l'ordre du sous-graphe
#   On génère le certificat (canonique) des sous-graphes
#   Si il est inconnu :
#       On ajoute le certificat à la liste de certificat lst_certif
#       On ajoute l'indice du certificat dans 
#           le dictionnaire des indices par ordre lst_ordre
#   S'il est connu ou non :
#       Pour l'identifiant du certificat
#       Dans le dictionnaire des isomorphes dict_isomorph,
#           On ajoute la combinaison de sommets à la liste 
#       Dans le dictionnaire des données statistiques dict_stat,
#           En [0], On incrémente le nombre d'occurence du sous-graphe
#           En [1], On incrémente le nombre d'apparition des sommets

# Le calcul du taux de recouvrement est calculer comme :
#   Le nombre moyen d'apparition dans les sous-graphes 
#       si le sommets apparait au moins 1 fois

# La génération de combinaison bruteforce se fait par une forme d'addition binaire
# On note qu'il n'est pas nécessaire de vérifier si le sous-graphes 
#   a déjà été vu par l'algorithme de génération bruteforce

###
# 1. Principale - Sous-graphes connexe avec certificat canonique
###

# méthode générale (génération et test combiné)
def BruteF(matrice_adja, atom_caract, min_ordre, max_ordre):
    ###### Initialisations ######
    # initialisation de la matrice des combinaisons
    combi = []
    matrx_len = int(len(matrice_adja))
    for i in range(matrx_len):
        combi.append(0)
    
    # initialisation le parametres liés à l'ordre du graphe et des sous-graphes
    ordre = min_ordre
    # on initie le premier sous graphe d'ordre minimum
    for k in range(ordre):
        combi[k] = 1 

    # Structures de stockage :
    # Listes:
    lst_certif = [] #= identifiant : certificat
    lst_ordre = []  #= ordre-min_ordre : [identifiant*]
    lst_combi = []  #= ordre-min_ordre : [combi*]
    # Dictionnaires: 
    # --> on peut revenir à des listes commes les identifiants sont consécutifs
    dict_isomorph = {} #= {identifiant: [combi*]}
    dict_stat = {}     #= {identifiant: [nb_occurrence,  occurrence_sommet, taux]}
    
    # Initialisation des listes par ordre 
    for k in range(max_ordre - min_ordre +1):
        lst_ordre.append([]) 
        lst_combi.append([]) 
    # chaque liste correspond à un ordre entre celui min et max
    
    # initialisation du dictionnaire des couleurs
    (couleur_nb, dict_couleur) = init_col(atom_caract)

    ###### Algorithme Bruteforce ######
    for i in range(int(math.pow(2,int(matrx_len)))):
        # verification que la combinaison est connexe
        conx = verif_conx(combi, matrice_adja, ordre)
        if (conx):
            #print(comb_trad(combi,atom_caract)+" connexe!")
            #affiche_combi(combi, ordre)
            
            # --> test isomorphisme
            # --> recouvrement des sommets
            # --> lst_ordre stocke les indices par ordre
            certif = combi_to_certif(combi, matrice_adja, atom_caract, dict_couleur)
            #print(certif.hex())
            if certif not in lst_certif:
                lst_certif.append(certif)
                dict_isomorph[lst_certif.index(certif)] = [combi.copy()]
                dict_stat[lst_certif.index(certif)] = [1,combi.copy()]
                lst_ordre[ordre - min_ordre].append(lst_certif.index(certif))
            else:
                dict_isomorph[lst_certif.index(certif)].append(combi.copy())
                tmp = dict_stat.get(lst_certif.index(certif))
                for i in range(len(combi)):
                    tmp[1][i] += combi[i]
                dict_stat[lst_certif.index(certif)] = [tmp[0]+1,tmp[1].copy()]
                #affiche_combi(tmp[1], ordre)             
            
        # Combinaisons de sommets suivantes
        ordre = add_ordonnee(combi, ordre)
        if ordre > max_ordre:
            break
    
    #print (dict_isomorph)
    return dict_isomorph, dict_stat, lst_ordre, lst_certif

# génération des combinaisons de sommets connexes
def gen_combi_brute(matrice_adja, atom_caract, min_ordre, max_ordre):
    ###### Initialisations ######
    # initialisation de la structure des combinaisons
    combi = []
    matrx_len = int(len(matrice_adja))
    for i in range(matrx_len):
        combi.append(0)
    
    # initialisation le parametres liés à l'ordre du graphe et des sous-graphes
    ordre = min_ordre
    # génération du premier sous-graphe d'ordre minimum
    for k in range(ordre):
        combi[k] = 1 

    # initialisation des listes des combinaisons 
    # chaque liste correspond à un ordre entre celui min et max
    lst_combi = []  #= ordre-min_ordre : [combi*]
    for k in range(max_ordre - min_ordre +1):
        lst_combi.append([]) 

    ###### Algorithme Bruteforce ######
    for i in range(int(math.pow(2,int(matrx_len)))):
        # verification que la combinaison est connexe
        conx = verif_conx(combi, matrice_adja, ordre)
        if (conx):
            lst_combi[ordre].append(combi.copy())
        # Combinaisons de sommets suivantes
        ordre = add_ordonnee(combi, ordre)
        if ordre > max_ordre:
            break
    
    #print (dict_isomorph)
    return lst_combi

def combi_iso(matrice_adja, atom_caract, lst_combi, min_ordre, max_ordre):
    ###### Initialisations ######

    # Structures de stockage :
    # Listes:
    lst_certif = [] #= identifiant : certificat
    lst_ordre = []  #= ordre-min_ordre : [identifiant*]
    # Dictionnaires: 
    # --> on peut revenir à des listes commes les identifiants sont consécutifs
    dict_isomorph = {} #= {identifiant: [combi*]}
    dict_stat = {}     #= {identifiant: [nb_occurrence,  occurrence_sommet, taux]}
    
    # initialisation des listes par ordre (entre le min et le max)
    for k in range(max_ordre - min_ordre +1):
        lst_ordre.append([]) 
    
    # initialisation du dictionnaire des couleurs
    (couleur_nb, dict_couleur) = init_col(atom_caract)
    
    # initialisation le parametres liés à l'ordre du graphe et des sous-graphes
    ordre = min_ordre

    ###### Boucle sur la liste de combinaison ######
    for liste in lst_combi:
        for combi in liste :            
            # calcule du certificat de la combinaison
            certif = combi_to_certif(combi, matrice_adja, atom_caract, dict_couleur)
            #print(certif.hex())
            if certif not in lst_certif:
                lst_certif.append(certif)
                indice = lst_certif.index(certif)
                dict_isomorph[indice] = [combi.copy()]
                dict_stat[indice] = [1,combi.copy()]
                lst_ordre[ordre - min_ordre].append(indice)
            else:
                indice = lst_certif.index(certif)
                dict_isomorph[indice].append(combi.copy())
                tmp = dict_stat.get(indice)
                for i in range(len(combi)):
                    tmp[1][i] += combi[i]
                dict_stat[indice] = [tmp[0]+1,tmp[1].copy()]
                #affiche_combi(tmp[1], ordre)
    
    #print (dict_isomorph)
    return dict_isomorph, dict_stat, lst_ordre, lst_certif

# methode de verification de la connexite d'une combinaison 
# de sommets
def verif_conx(combi, matrice_adja, ordre):
    # test de connexité
    listconx = []
    for k in range(ordre):
        for i in range(int(len(matrice_adja))):
            if len(listconx) == 0 and combi[i]==1: 
                listconx.append(i)
            if combi[i] == 1 and (i not in listconx):
                for l in listconx:
                    if matrice_adja[l][i] != 0 or matrice_adja[i][l] !=0:
                        listconx.append(i)
                        break

    #print(str(len(listconx))+' '+str(compt))
    if len(listconx) != ordre:
        return False
    return True   

###
# 2. Recouvrement des sommets du graphes par un type de sous-graphes
###


# Calcul les recouvrements
# (sommets par sommets pour chaque isomorphe)
def recouvrement(dict_isomorph):
    dict_stat = {}
    for indice in dict_isomorph.keys():
        l_iso = dict_isomorph.get(indice)
        dict_stat[indice] = [len(l_iso),[]]
        for i in range(len(l_iso)):
            for j in range(len(l_iso[i])):
                if i==0 :
                    dict_stat[indice][1].append(0)
                dict_stat[indice][1][j]+=l_iso[i][j]
    return dict_stat

# Calcul le taux de recouvrement pour un groupe d'isomorphes
def Taux_recouvert(dict_stat):
    for indice in dict_stat.keys():
        stat = dict_stat.get(indice)
        tot = 0 # cumule des occurrences de sommets
        cmpt = 0 # nombre de sommets apparus
        for i in range(len(stat[1])):
            tot += stat[1][i]
            if stat[1][i]>0 :
                cmpt += 1 
        # taux de recouvrement
        dict_stat[indice].append(tot/cmpt)

# Calcul le nombre de sous-graphes sans équivalent isomorphe (unique)
def Nombre_unique(lst_ordre, dict_stat):
    cmpt = []
    for i in range(len(lst_ordre)):
        cmpt.append(0)
        for indice in lst_ordre[i]:
            tmp = dict_stat.get(indice)
            if tmp[0] == 1:
                cmpt[i] += 1 
    return cmpt

###
# 3. Certificat canonique de sous-graphes par les combinaisons de sommets
###

# initialisation des couleurs
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
    g = Graph(enum)
    
    ###### Algo ######
    # remplissage des vertex
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
        
    return certificate(g) 

###
# 4. Fonctions d'affichage
###

# affichage de la combinaison en suite de 1 et de 0 (fonction de débuggage)
def affiche_combi(combi, ordre):
    s = "combi: "
    for i in range(len(combi)):
        s += str(combi[i])+''
    s += ' ordre: ' + str(ordre)
    print(s)

# traduction de la combinaison (fonction de débuggage)
def comb_trad(combi,atom_caract):
    s = ''
    for i in range(len(combi)):
        if combi[i] == 1:
           s+= atom_caract[i]+', ' 
    return s   

###
# 5. Gestion des combinaisons de sommets du graphes
###

# addition base 2
def add_b2 (combi):
    for i in range(len(combi)):
        if combi[i] == 0:
            combi[i] = 1
            break
        else: 
            combi[i] = 0

# Une façon d'obtenir une nouvelle combinaison unique à partir de
# la précédente et qui permet de suivre l'ordre du sous-graphe 
def add_ordonnee (combi, ordre):
    compt_end = 0
    end_full = True
    max = len(combi)
    for i in range(max):
        if combi[max - 1 - i] == 1: 
            if (end_full):
                compt_end+=1
                combi[max - 1 - i] = 0
            else:
                combi[max - 1 - i] = 0
                for j in range(compt_end + 1):
                    combi[max + j - i] = 1 
                break
        else:
            end_full = False
        if i == max - 1:
            ordre += 1
            if ordre >= max:
                ordre = max 
            for k in range(ordre):
                combi[k] = 1 
            break
    return ordre

