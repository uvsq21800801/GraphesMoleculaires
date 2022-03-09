import math
from pynauty import *


# Explication de l'algorithme
# On initialise la matrice de combinaison à la 1ere combinaison (aucun sommet)
# On vérifie la connexité
# On vérifié l'isomorphisme
# On ajoute dans la matrice résultat
# On incrémente la valeur de la combinaison avec l'addition binaire
# On recommence tout jusqu'à la dernière combinaison
# On retourne les dictionnaires de résultat

# note: On a pas besoin de vérifier qu'un sous-graphe existe déjà car
# ils sont générés de manière à être unique

###
# 1. Principale - Sous-graphes connexe avec certificat canonique
###


# méthode à appeler pour bruteforcer
def BruteF(listindex, matriceadja, atom_caract, max_ordre, min_ordre):
    ###### Initialisations ######
    # initialisation de la matrice des combinaisons
    combi = []
    matrx_len = int(len(matriceadja))
    for i in range(matrx_len):
        combi.append(0)
    
    # initialisation le parametres liés à l'ordre du graphe et des sous-graphes
    ordre = min_ordre
    # on initie le premier sous graphe d'ordre minimum
    for k in range(ordre):
        combi[k] = 1 

    # on initie la structure de stockage des graphes 
    # chaque liste correspond à un ordre entre celui min et max
    lst_ordre = [] #= ordre : [identifiant]
    for k in range(max_ordre - min_ordre +1):
        lst_ordre.append([]) 

    # Structure de stockage pour l'isomorphisme et le recouvrement
    # avec les certificats de lst_c
    # Dictionnaire:
    isomorph_dict = {} #= {identifiant: liste_combi}
    recouvre_dict = {} #= {identifiant: [nb_occurence,  occurence_sommet, taux]}
    lst_c = []     #= identifiant : [certificat]


    # initialisation des couleurs
    couleur_nb = 0
    dict_couleur = {}    
    for i in atom_caract:
        splitted = i.split()
        if splitted[0] not in dict_couleur:
            dict_couleur[splitted[0]] = couleur_nb 
            couleur_nb += 1
        #print(dict_couleur)
    #print(couleur_nb)

    #return 0;

    ###### Algorithme Bruteforce ######
    for i in range(int(math.pow(2,int(matrx_len)))):
        # verification que la combinaison est connexe
        conx = verif_conx(combi, matriceadja, ordre)
        if (conx):
            #print(comb_trad(combi,atom_caract)+" connexe!")
            #affiche_combi(combi, ordre)
            
            # --> test isomorphisme
            # --> recouvrement des sommets
            # --> lst_ordre stocke les indices par ordre
            certif = combi_to_certif(combi, matriceadja, atom_caract, dict_couleur)
            #print(certif.hex())
            if certif not in lst_c:
                lst_c.append(certif)
                isomorph_dict[lst_c.index(certif)] = [combi.copy()]
                recouvre_dict[lst_c.index(certif)] = [1,combi.copy()]
                lst_ordre[ordre - min_ordre].append(lst_c.index(certif))
            else:
                isomorph_dict[lst_c.index(certif)].append(combi.copy())
                tmp = recouvre_dict.get(lst_c.index(certif))
                for i in range(len(combi)):
                    tmp[1][i] += combi[i]
                recouvre_dict[lst_c.index(certif)] = [tmp[0]+1,tmp[1].copy()]
                #affiche_combi(tmp[1], ordre)             
            
        # Combinaisons de sommets suivantes
        ordre = add_magique(combi, ordre)
        if ordre > max_ordre:
            break
    
    #print (isomorph_dict)
    return isomorph_dict, recouvre_dict, lst_ordre, lst_c

# methode de verification de la connexite d'une combinaison 
# de sommets
def verif_conx(combi, matriceadja, ordre):
    # test de connexité
    listconx = []
    for k in range(ordre):
        for i in range(int(len(matriceadja))):
            if len(listconx) == 0 and combi[i]==1: 
                listconx.append(i)
            if combi[i] == 1 and (i not in listconx):
                for l in listconx:
                    if matriceadja[l][i] != 0 or matriceadja[i][l] !=0:
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
def recouvrement(isomorph_dict):
    recouvre_dict = {}
    for indice in isomorph_dict.keys():
        l_iso = isomorph_dict.get(indice)
        recouvre_dict[indice] = [len(l_iso),[]]
        for i in range(len(l_iso)):
            for j in range(len(l_iso[i])):
                if i==0 :
                    recouvre_dict[indice][1].append(0)
                recouvre_dict[indice][1][j]+=l_iso[i][j]
    return recouvre_dict
# renvoie un dictionnaire avec pour chaque certificat le nombre d'occurance
# et le nombre d'apparition de chaque sommet dans ses occurances


# Calcul le taux de recouvrement pour un groupe d'isomorphes
def Taux_recouvert(recouvre_dict):
    for indice in recouvre_dict.keys():
        stat = recouvre_dict.get(indice)
        tot = 0 # cumule des occurences de sommets
        cmpt = 0 # nombre de sommets apparus
        for i in range(len(stat[1])):
            tot += stat[1][i]
            if stat[1][i]>0 :
                cmpt += 1 
        # taux de recouvrement
        recouvre_dict[indice].append(tot/cmpt)

###
# 3. Certificat canonique de sous-graphes par les combinaisons de sommets
###

# Fait et retourne un certificat de graphe à partir d'une 
# combinaison de sommets
def combi_to_certif(combi, matriceadja, atom_caract, dict_c):
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
                if matriceadja[i][j] != 0 and combi[j] == 1:
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
        
        #test #g.set_vertex_coloring([set([1])])
        #g.set_vertex_coloring([set([2])])        
        
    #print(g)
    #print(autgrp(g))
    #print(certificate(g).decode('cp437'))
    #print(certificate(g).decode("utf-16"))
    
    return certificate(g) 

###
# 4. Fonction de bases (affichage et reprise des résultats)
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

# rassemblement des nombres d'occurence    

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
def add_magique (combi, ordre):
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

