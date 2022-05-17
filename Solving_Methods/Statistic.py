
###
# 1. Recouvrement des sommets du graphes par un type de sous-graphes
###

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
        if cmpt > 0 :
            dict_stat[indice].append(tot/cmpt)
        else :
            dict_stat[indice].append(0)
    
###
# 2. Fonctions utiles
###

# Calcul le nombre de sous-graphes sans équivalent isomorphe (unique)
def Nombre_unique(lst_id, dict_stat):
    cmpt = 0
    for indice in lst_id:
        tmp = dict_stat.get(indice)
        if tmp[0] == 1:
            cmpt += 1 
    return cmpt

# Tri par occurrence et recouvrement croissant
def Tri_indice(lst_id, dict_stat):
    tri_indice = []
    # liste des couples de donnée { occurrence : [[indice, taux]] }
    d = {}
    # pour chaque indice (de certificat/ de motif)
    for i in lst_id:
        tmp = dict_stat.get(i)
        if tmp[0] not in d.keys():
            d[tmp[0]] = [[i, tmp[2]]]
        else :
            d[tmp[0]].append([i, tmp[2]])
    
    # pour tous les nombres d'occurrence triés
    for k in sorted(d.keys()) :
        # récupère la liste des couples [indice, taux]
        tmp = d.get(k)
        # pour tous les couples triés selon le taux
        for l in sorted(tmp, key=second):
            tri_indice.append(l[0])
    
    return tri_indice

# retourne le second terme d'un tableau 
def second(tab):
    return tab[1]
