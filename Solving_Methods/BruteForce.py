import math

# Explication de l'algorithme
# On initialise la matrice de combinaison à la 1ere combinaison (aucun sommet)
# On vérifie la connexité
# On vérifié l'isomorphisme
# On ajoute dans la matrice résultat
# On incrémente la valeur de la combinaison avec l'addition binaire
# On recommence tout jusqu'à la dernière combinaison
# On retourne la matrice de résultat

# méthode à appeler pour bruteforcer
def BruteF(listindex, matriceadja, atom_caract, resultat):
    # initialisation de la matrice des combinaisons
    combi = []
    matrx_len = int(len(matriceadja))
    for i in range(matrx_len):
        combi.append(0)
    

    # bruteforcage
    for i in range(int(math.pow(2,int(matrx_len)))):
        # verification que la combinaison est connexe
        conx = verif_conx(combi, matriceadja)
        if (conx):
            print(comb_trad(combi,atom_caract)+" connexe!")
            affiche_combi(combi)
        
        # si connexe -> deja connue oui/non


        # ++
        #affiche_combi(combi)
        add_b2(combi)
# btw je compte changer plus tards histoire de pas faire la 
# double boucle matriceadja                  


# methode de verification de la connexite d'une combinaison 
# de sommets
def verif_conx(combi, matriceadja):
    # compte le nb de sommets de la combi
    compt = 0 
    for i in range(len(combi)):
        if combi[i] == 1:
            compt+=1
    #print(compt)

    # test de connexité
    listconx = []
    for k in range(compt):
        for i in range(int(len(matriceadja))):
            if len(listconx) == 0 and combi[i]==1: 
                listconx.append(i)
            if combi[i] == 1 and (i not in listconx):
                for l in listconx:
                    if matriceadja[l][i] != 0 or matriceadja[i][l] !=0:
                        listconx.append(i)

                    #for j in range(int(len(matriceadja))):
                        #if matriceadja[l][j] != 0 or matriceadja[j][l] != 0:
                            #if combi[j] == 1 and (i not in listconx): 
                                #listconx.append(i)
    
    if len(listconx) != compt:
        return False
    return True   

    # definition du nb de sommets. utile?

    # si au moins un sommet marque "1" n'est connexe avec
    # aucun autre sommet marque "1" -> break rep faux

# affichage de la combinaison en suite de 1 et de 0 (fonction de débuggage)
def affiche_combi(combi):
    s = "combi: "
    for i in range(len(combi)):
        #if (combi[i] == 1):
        s += str(combi[i])+''
    print(s)
#def verif_connu():
    


# addition base 2
def add_b2 (combi):
    for i in range(len(combi)):
        if combi[i] == 0:
            combi[i] = 1
            break
        else: 
            combi[i] = 0

# traduction de la combinaison (fonction de débuggage)
def comb_trad(combi,atom_caract):
    s = ''
    for i in range(len(combi)):
        if combi[i] == 1:
           s+= atom_caract[i]+', ' 
    return s
    #print(s)


    