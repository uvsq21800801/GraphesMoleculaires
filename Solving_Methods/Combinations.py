import math

####
## 1. Algo principal de génération des combinaison de sommet (Brute de force)
####

# génération des combinaisons de sommets connexes de taille ordre
def gen_combi_brute(matrice_adja, ordre):
    # initialisation de la structure des combinaisons
    combi = []
    matrx_len = int(len(matrice_adja))
    for i in range(matrx_len):
        combi.append(0)
    
    # sauvegarde la taille des sous-graphes étudiés
    taille = ordre
    # génération du premier sous-graphe d'ordre minimum
    for k in range(taille):
        combi[k] = 1 

    # initialisation des listes des combinaisons 
    # chaque liste correspond à un ordre entre celui min et max
    lst_combi = []  #= [combi*]

    ###### Algorithme Bruteforce ######
    for i in range(int(math.pow(2,int(matrx_len)))):
        # verification que la combinaison est connexe
        conx = verif_conx(combi, matrice_adja, taille)
        if (conx):
            lst_combi.append(combi.copy())
        # Combinaisons de sommets suivantes
        taille = add_ordonnee(combi, taille)
        # Stop si la taille courante dépasse la taille étudié
        if ordre < taille:
            break
    
    return lst_combi

# génération des combinaisons de sommets connexes de taille entre min et max ordre
def gen_combi_brute_range(matrice_adja, min_ordre, max_ordre):
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
            lst_combi[ordre - min_ordre].append(combi.copy())
        # Combinaisons de sommets suivantes
        ordre = add_ordonnee(combi, ordre)
        if ordre > max_ordre:
            break
    
    #print (dict_isomorph)
    return lst_combi

####
## 2. Fonctions utiles
####

# methode de verification de la connexite d'une combinaison de sommets
def verif_conx(combi, matrice_adja, taille):
    # test de connexité
    listconx = []
    for k in range(taille):
        for i in range(int(len(matrice_adja))):
            if len(listconx) == 0 and combi[i]==1: 
                listconx.append(i)
            if combi[i] == 1 and (i not in listconx):
                for l in listconx:
                    if matrice_adja[l][i] != 0 or matrice_adja[i][l] !=0:
                        listconx.append(i)
                        break

    #print(str(len(listconx))+' '+str(compt))
    if len(listconx) != taille:
        return False
    return True  

# Génère une nouvelle combinaison unique à partir de
# la précédente sans faire de répétition 
def add_ordonnee (combi, taille):
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
            #print("fin taille "+str(taille))
            taille += 1
            if taille >= max:
                taille = max 
            for k in range(taille):
                combi[k] = 1 
            break
    return taille
