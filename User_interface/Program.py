import sys
sys.path.append('GraphesMoleculaires/Inputs_Outputs')
sys.path.append('GraphesMoleculaires/Solving_Methods')
sys.path.append('GraphesMoleculaires/MCIS')

from Inputs_Outputs import Inputs as In
from Inputs_Outputs import Output as Out
from Solving_Methods import BruteForce
from Solving_Methods import Mcis_algo

# plus utilisé?

###
# 1. Type d'execution bruteforce avec plusieurs fichiers
###

def BF_for_any_new_name(min_ordre, max_ordre):
    # recuperation des donnees de tous les fichiers
    (filenames1, filenames2, lst_index, atom_caract, matrice_adja) = In.data_inputs(1)
    
    # test que les fichiers sont bien associés 2 à 2
    filenames1.sort()
    filenames2.sort()
    if filenames1 != filenames2 :
        print("Erreur de lecture de fichiers "+filenames1+" "+filenames2+'\n')
        print("Fichier(s) manquant(s) ou intrus?\n")
        return 1
    
    BF_do_any_new_name(filenames1, lst_index, atom_caract, matrice_adja, min_ordre, max_ordre)
    return 0

def BF_for_any_name(min_ordre, max_ordre):
    # recuperation des donnees de tous les fichiers
    (filenames1, filenames2, lst_index, atom_caract, matrice_adja) = In.data_inputs(1)
    
    # test que les fichiers sont bien associés 2 à 2
    filenames1.sort()
    filenames2.sort()
    if filenames1 != filenames2 :
        print("Erreur de lecture de fichiers "+filenames1+" "+filenames2+'\n')
        print("Fichier(s) manquant(s) ou intrus?\n")
        return 1
    
    BF_do_any_name(filenames1, lst_index, atom_caract, matrice_adja, min_ordre, max_ordre)
    return 0

# imprime et étudie tous les nouveaux noms de fichiers
def BF_do_any_new_name(filenames, lst_index, atom_caract, matrice_adja, min_ordre, max_ordre):
    for name in filenames :
        if In.done(name):
            print(name+" déjà fait "+str(datetime.now().time()))
        else:
            # imprime les données de ce graphes
            Out.Output_data(name, lst_index[name], atom_caract[name], matrice_adja[name])
    
    for name in filenames1 :
        if not In.done(name):
            print(name+" commence "+str(datetime.now().time()))
            
            # sous_graphes isomorphes connexe par methode bruteforce
            (dict_isomorph, dict_stat, lst_ordre, lst_certif) = BruteForce.BruteF(matrice_adja[name], atom_caract[name], min_ordre, max_ordre)
            # calcul le taux de recouvrement
            BruteForce.Taux_recouvert(dict_stat)
            lst_unique = BruteForce.Nombre_unique(lst_ordre, dict_stat)
            
            # imprime les résultats
            Out.Output_final(name, min_ordre, lst_ordre, lst_combi, lst_certif, lst_unique, dict_isomorph, dict_stat)
            
            print(name+" fini "+str(datetime.now().time())+"\n")

# imprime et étudie tous les nouveaux noms de fichiers
def BF_do_any_name(filenames, lst_index, atom_caract, matrice_adja, min_ordre, max_ordre):
    for name in filenames :
        # imprime les données de ce graphes
        Out.Output_data(name, lst_index[name], atom_caract[name], matrice_adja[name])
    for name in filenames :
        print(name+" commence "+str(datetime.now().time()))
        
        # sous_graphes isomorphes connexe par methode bruteforce
        (dict_isomorph, dict_stat, lst_ordre, lst_certif) = BruteForce.BruteF(matrice_adja[name], atom_caract[name], min_ordre, max_ordre)
        # calcul le taux de recouvrement
        BruteForce.Taux_recouvert(dict_stat)
        lst_unique = BruteForce.Nombre_unique(lst_ordre, dict_stat)
        
        # imprime les résultats
        Out.Output_final(name, min_ordre, lst_ordre, lst_combi, lst_certif, lst_unique, dict_isomorph, dict_stat)
        
        print(name+" fini "+str(datetime.now().time())+"\n")

###
# 2. Type d'execution bruteforce avec un fichier
###

def BF_for_one_name(name, min_ordre, max_ordre):
    # recuperation des donnees de tous les fichiers
    (filename1, filename2, lst_index, atom_caract, matrice_adja) = In.data_input(1, name)
    
    if name != filename1 or name != filename2 :
        print("Erreur de lecture de fichiers "+filenames1+" "+filenames2+'\n')
        print("Fichier manquant?\n")
        return 1
    
    BF_do_one_name(name, lst_index, atom_caract, matrice_adja, min_ordre, max_ordre)
    return 0

# imprime et étudie un nom de fichier donné
def BF_do_one_name(name, lst_index, atom_caract, matrice_adja, min_ordre, max_ordre):
    # imprime les données de ce graphes
    Out.Output_data(name, lst_index, atom_caract, matrice_adja)

    print(name+" commence "+str(datetime.now().time()))
    
    # sous_graphes isomorphes connexe par methode bruteforce
    (dict_isomorph, dict_stat, lst_ordre, lst_certif) = BruteForce.BruteF(matrice_adja, atom_caract, min_ordre, max_ordre)
    # calcul le taux de recouvrement
    BruteForce.Taux_recouvert(dict_stat)
    lst_unique = BruteForce.Nombre_unique(lst_ordre, dict_stat)
    
    # imprime les résultats
    Out.Output_final(name, min_ordre, lst_ordre, lst_combi, lst_certif, lst_unique, dict_isomorph, dict_stat)
    
    print(name+" fini "+str(datetime.now().time())+"\n")

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
