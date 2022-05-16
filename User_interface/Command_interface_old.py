# sera une interface de commande si besoin
import sys
sys.path.append('GraphesMoleculaires/Inputs_Outputs')
sys.path.append('GraphesMoleculaires/Solving_Methods')
sys.path.append('GraphesMoleculaires/MCIS')

from Inputs_Outputs import Inputs
from Inputs_Outputs import Output
from Solving_Methods import BruteForce
from Solving_Methods import Mcis_algo

from datetime import datetime

def interface():
    # définition des ordres (inclus) des sous-graphes
    min_ordre = 3
    max_ordre = 6
    
    # recuperation des donnees de tous les fichiers
    (filenames1, filenames2, lst_index, atom_caract, matrice_adja) = Inputs.data_inputs(1)
    
    # test que les fichiers sont bien associés 2 à 2
    filenames1.sort()
    filenames2.sort()
    if filenames1 != filenames2 :
        print("Erreur de lecture de fichiers "+filenames1+" "+filenames2+'\n')
        print("Fichier(s) manquant(s) ou intrus?\n")
        return 1
    
    for name in filenames1 :
        if Inputs.done(name):
            print(name+" déjà fait "+str(datetime.now().time()))
        else:
            # imprime les données de ce graphes
            Output.Output_data(name, lst_index[name], atom_caract[name], matrice_adja[name])
    
    for name in filenames1 :
        if not Inputs.done(name):
            print(name+" commence "+str(datetime.now().time()))
            
            # sous_graphes isomorphes connexe par methode bruteforce
            lst_combi = BruteForce.gen_combi_brute(matrice_adja[name], atom_caract[name], min_ordre, max_ordre)
            print(name+" combinaisons finis "+str(datetime.now().time()))
            (dict_isomorph, dict_stat, lst_ordre, lst_certif) = BruteForce.combi_iso(matrice_adja[name], atom_caract[name], lst_combi, min_ordre, max_ordre)
            
            # calcul le taux de recouvrement et les sommets uniques
            BruteForce.Taux_recouvert(dict_stat)
            lst_unique = BruteForce.Nombre_unique(lst_ordre, dict_stat)

            # tri de lst_ordre par nombre d'occurence
            #new_list = []
            for i in range(max_ordre - min_ordre + 1):

                #new_liste_ordre_x = lst_ordre[i]
                BruteForce.Tri_indice(i, lst_ordre, dict_stat)
                #new_list.append(new_liste_ordre_x)
            #lst_ordre = new_list
             

            # MCIS/ Génération des données pour calculer le taux de chaleur
            Tab_sim = Mcis_algo.mcis_algo(matrice_adja[name], atom_caract[name], lst_ordre, dict_isomorph, min_ordre, max_ordre)
            print(name+" mcis finis "+str(datetime.now().time()))
            
            # imprime les matrices de chaleur
            Output.res_sim(name, min_ordre, max_ordre, Tab_sim)

            # imprime les résultats
            Output.res_output(name, min_ordre, lst_ordre, lst_combi, lst_certif, lst_unique, dict_isomorph, dict_stat)
            
            print(name+" fini "+str(datetime.now().time())+"\n")
    return 0

###
# 3. Fonctions d'affichage de structures
###

### fonctions d'affichage matrice et liste
def affiche_matrice(m):
    r = int(len(m))
    for i in range(r):
        print(m[i])

def affiche_matrice2(m):
    r = int(len(m))
    for i in range(r):
        s = ''
        for j in range(r):
            s += str(m[i][j])+' '
        print(s)

def affiche_liste(l):
    s = ''
    for i in range(len(l)):
        s += str(l[i])
    return s+''

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
