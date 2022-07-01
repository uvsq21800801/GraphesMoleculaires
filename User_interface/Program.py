###
# 1. Fonctions d'affichage de structures
###

### fonctions d'affichage matrice et liste
def affiche_matrice(m, sep=''):
    r = int(len(m))
    for i in range(r):
        s = ''
        for j in range(r):
            s += str(m[i][j])+sep
        print(s)

def affiche_liste(l, sep=''):
    s = ''
    for i in range(len(l)):
        s += str(l[i])+sep
    print(s)

# affiche les infos sur les motifs (groupes à isomorphismes près)
def affiche_data(min_ordre, lst_ordre, dict_isomorph, dict_stat, lst_certif):
    print("ordre identifiant nombre_occurrence taux_recouvrement recouvrement certificat liste_combi")
    for i in range(len(lst_ordre)):
        iso_uniq = 0
        for indice in lst_ordre[i]:
            tmp1 = dict_isomorph.get(indice)
            tmp2 = dict_stat.get(indice)
            if tmp2[0] > 1:
                #     ordre               identifiant nombre_occurrence taux_recouvrement  recouvrement                 certificat                liste combinaison
                print(str(i+min_ordre)+' '+str(indice)+str(tmp2[0])+' '+str(tmp2[2])+' \''+affiche_liste(tmp2[1])+' \''+lst_certif[indice].hex()+' \''+str(tmp1))
            else :
                iso_uniq += 1
                #print(str(i+min_ordre)+' '+str(indice)+str(tmp2[0])+' '+str(tmp2[2])+' \''+affiche_liste(tmp2[1])+' \''+lst_certif[indice].hex()+' \''+str(tmp1))
    print(iso_uniq)
