import math

# Explication de l'algorithme
# On initialise la matrice de combinaison à la 1ere combinaison (aucun sommet)
# On vérifie la connexité
# On vérifié l'isomorphisme
# On ajoute dans la matrice résultat
# On incrémente la valeur de la combinaison avec l'addition binaire
# On recommence tout jusqu'à la dernière combinaison
# On retourne la matrice de résultat

# note: On à pas besoin de vérifier qu'un sous-graphe existe déjà car
# ils sont générés de manière à être unique

# méthode à appeler pour bruteforcer
def BruteF(listindex, matriceadja, atom_caract, resultat):
    # initialisation de la matrice des combinaisons
    combi = []
    matrx_len = int(len(matriceadja))
    for i in range(matrx_len):
        combi.append(0)
    
    # initialisation des parametres liés à l'ordre du graphe et des sous-graphes
    # on limite la recherche à une fenetre d'ordre (entre 3 et 8 sommets)
    max_ordre = 8
    min_ordre = 3
    ordre = min_ordre
    # on initie le premier sous graphe d'ordre 3
    for k in range(ordre):
        combi[k] = 1 

    # on initie la structure de stockage des graphes 
    # chaque liste correspond à un ordre entre celui min et max
    for k in range(max_ordre - min_ordre +1):
        resultat.append([]) 

    # bruteforcage
    for i in range(int(math.pow(2,int(matrx_len)))):
        # verification que la combinaison est connexe
        conx = verif_conx(combi, matriceadja, ordre)
        if (conx):
            #print(comb_trad(combi,atom_caract)+" connexe!")
            affiche_combi(combi, ordre)
            
            # --> test isomorphisme
            # --> calcul couverture et nb occurrance
            # --> stockage couverture en tableau de nombre d'apparition par sommet
            # --> stockage nombre d'occurance du sous-graphe (isomorphe) par un compteur

            # stockage
            resultat[ordre - min_ordre].append(combi)
        
        # ++ il y à plusieurs façons d'obtenir toutes les combinaisons
        #add_b2(combi)
        ordre = add_magique(combi, ordre)
        if ordre > max_ordre:
            break

# methode de verification de la connexite d'une combinaison 
# de sommets
def verif_conx(combi, matriceadja, ordre):
    # compte le nb de sommets de la combi
    #compt = 0
    #for i in range(len(combi)):
    #    if combi[i] == 1:
    #        compt+=1

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

# affichage de la combinaison en suite de 1 et de 0 (fonction de débuggage)
def affiche_combi(combi, ordre):
    s = "combi: "
    for i in range(len(combi)):
        s += str(combi[i])+''
    s += ' ordre: ' + str(ordre)
    print(s)


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

# traduction de la combinaison (fonction de débuggage)
def comb_trad(combi,atom_caract):
    s = ''
    for i in range(len(combi)):
        if combi[i] == 1:
           s+= atom_caract[i]+', ' 
    return s
    