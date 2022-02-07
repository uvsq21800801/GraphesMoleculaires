import math

# méthode à appeler pour bruteforcer
def BruteF(listindex, matriceadja, resultat):
    # initialisation de la matrice des combinaisons
    combi = []
    matrx_len = int(len(matriceadja))
    matrx_len *= matrx_len
    for i in range(matrx_len):
        combi.append(0)
    
    # bruteforcage
    for i in range(matrx_len):
        # verification que la combinaison est connexe


        # si connexe -> deja connue oui/non


        # ++
        add_b2(combi)
# btw je compte changer plus tards histoire de pas faire la 
# double boucle matriceadja        


# methode de verification de la connexite d'une combinaison 
# de sommets
#def verif_conx(combi, matriceadja):
    # definition du nb de sommets. utile?

    # si au moins un sommet marque "1" n'est connexe avec
    # aucun autre sommet marque "1" -> break rep faux


#def verif_connu():
    


# addition base 2
def add_b2 (combi):
    for i in combi:
        if combi[i] == 0:
            combi[i] = 1
            break
        else: 
            combi[i] = 0



    