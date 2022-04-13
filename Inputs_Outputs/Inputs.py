from os import listdir, remove
from os.path import isfile, join
import re

###
### option : 0 = tout ; 1 = pas les hydrogènes
###

###
# 1. Fonctions de lecture et écriture sur fichiers
###

# recuperation des donnees des fichiers
def data_inputs(option):
    lst_index = {}
    atom_caract = {}
    filenames1 = Inputs_trad_all(option, lst_index, atom_caract)
    matrice_adja = {}
    filenames2 = Inputs_bonds_all(option, lst_index, matrice_adja)
    
    return filenames1, filenames2, lst_index, atom_caract, matrice_adja

# recuperation des donnees d'un type de fichier
def data_input(option, name):
    lst_index = []
    atom_caract = []
    filename1 = Input_trad(option, name, lst_index, atom_caract)
    matrice_adja = []
    filename2 = Input_bonds(option, name, lst_index, matrice_adja)
    
    return filename1, filename2, lst_index, atom_caract, matrice_adja

# impression des resultats pour un graphe
def res_output(name, min_ordre, lst_ordre, lst_combi, lst_certif, lst_unique, dict_isomorph, dict_stat):
    for i in range(int(len(lst_ordre))):
        Output_diagramme(name, i, min_ordre, lst_ordre, dict_stat)
    Output_result(name, min_ordre, lst_certif, lst_ordre, dict_stat)
    Output_combi(name, lst_ordre, dict_isomorph)
    Output_stat(name, min_ordre, lst_combi, lst_certif, lst_ordre, lst_unique)

###
# 2. Fonctions de récupération de données d'atomes
###

# Retourne le contenu d'un fichier texte pour un nom donné
def Input_trad(option, name, li, atom_caract):
    # recuperation du fichier trad
    fpath = "Inputs_Outputs/Place_Trad_file_here/" 
    filenames = [f for f in listdir(fpath) if isfile(join(fpath, f))]
    filename = "trad-atom_"+name+".txt"
    # si le nom est bien représenté, on récupère les données
    if filename in filenames:
        # lecture du fichier bonds et transcription dans la matrice de traduction
        f1 = open(fpath+filename, 'r').readlines()
        for line in f1:
            splitted = line.split()
            if len(splitted) == 3:
                if (option == 1 and splitted[1] != 'H') or (option == 0):
                    li.append(splitted[0])
                    
                    # Liste de traduction suivant le modele '[type atome] [numero]'
                    temp = splitted[2]
                    caracteristiques = splitted[1]+' '+temp[len(splitted[1]):]
                    atom_caract.append(caracteristiques)
                #print(splitted[0]+' '+splitted[1]+' '+splitted[2])
        return name
    else :
        return ""

# Retourne le contenu des fichiers textes en liste
def Inputs_trad_all(option, li, atom_caract):
    # recuperation du fichier trad
    fpath = "Inputs_Outputs/Place_Trad_file_here/" 
    filenames = [f for f in listdir(fpath) if isfile(join(fpath, f))]
    names = []

    for filename in filenames :
        # definie le nom du graphe
        name = get_name(filename)
        names.append(name)
        #initie les listes pour ce graphe (écrase le précédent si 2 noms identiques)
        li[name] = []
        atom_caract[name] = []
        # lecture du fichier bonds et transcription dans la matrice de traduction
        f1 = open(fpath+filename, 'r').readlines()
        for line in f1:
            splitted = line.split()
            if len(splitted) == 3:
                if (option == 1 and splitted[1] != 'H') or (option == 0):
                    li[name].append(splitted[0])
                    
                    # Liste de traduction suivant le modele '[type atome] [numero]'
                    temp = splitted[2]
                    caracteristiques = splitted[1]+' '+temp[len(splitted[1]):]
                    atom_caract[name].append(caracteristiques)
                #print(splitted[0]+' '+splitted[1]+' '+splitted[2])
    return names

###
# 3. Fonctions de récupération de données de liaisons
###

def Input_bonds(option, name, li, ma):    
    # recuperation du fichier bonds
    fpath = "Inputs_Outputs/Place_Bonds_file_here/"
    filenames = [f for f in listdir(fpath) if isfile(join(fpath, f))]
    filename = "bonds_"+name+".txt"
    # si le nom est bien représenté, on récupère les données
    if filename in filenames:

        #initie la matrice d'adjacence
        init_matrice(ma,len(li))

        # lecture du fichier bonds et transcription dans la matrice d'adjacence
        f1 = open(fpath+filename, 'r').readlines()
        for line in f1:
            splitted = line.split()
            # liaison covalente
            if splitted[0] == '1' and len(splitted) == 3:
                if splitted[1] in li and splitted[2] in li:
                    #ajoute deux 1 dans la matrice ma de façon symétrique
                    ma[li.index(splitted[1])][li.index(splitted[2])] = 1
                    ma[li.index(splitted[2])][li.index(splitted[1])] = 1
            # liaison hydrogene
            if splitted[0] == '4' and len(splitted) == 4:
                if splitted[1] in li and splitted[2] in li:
                    if option == 1 : # hydrogène présent
                        #ajoute un 2 de l'atomes donneur vers l'accepteur
                        ma[li.index(splitted[1])][li.index(splitted[2])] = 2
                    elif option == 0 and splitted[3] in li:
                        #ajoute un 2 de l'hydrogène vers l'accepteur
                        ma[li.index(splitted[3])][li.index(splitted[2])] = 2
        return name
    else :
        return ""

# Retourne le contenu des fichiers "bonds" texte en matrice d'adjacence
def Inputs_bonds_all(option, li, ma):    
    # recuperation du fichier bonds
    fpath = "Inputs_Outputs/Place_Bonds_file_here/"
    filenames = [f for f in listdir(fpath) if isfile(join(fpath, f))]
    names = []
    
    matrice = []
    for filename in filenames :
        # definie le nom du graphe
        name = get_name(filename)
        names.append(name)
        #initie la matrice d'adjacence
        matrice = []
        if name in li.keys() :
            l = li.get(name)
            init_matrice(matrice,len(l))

            # lecture du fichier bonds et transcription dans la matrice d'adjacence
            f1 = open(fpath+filename, 'r').readlines()
            for line in f1:
                splitted = line.split()
                # liaison covalente
                if splitted[0] == '1' and len(splitted) == 3:
                    if splitted[1] in l and splitted[2] in l:
                        #ajoute un 1 dans la matrice ma de façon symétrique
                        matrice[l.index(splitted[1])][l.index(splitted[2])] = 1
                        matrice[l.index(splitted[2])][l.index(splitted[1])] = 1
                # liaison hydrogene
                if splitted[0] == '4' and len(splitted) == 4:
                    if splitted[1] in l and splitted[2] in l:
                        if option == 1 : # hydrogène présent
                            #ajoute un 2 de l'atomes donneur vers l'accepteur
                            matrice[l.index(splitted[1])][l.index(splitted[2])] = 2
                        elif option == 0 and splitted[3] in l:
                            #ajoute un 2 de l'hydrogène vers l'accepteur
                            matrice[l.index(splitted[3])][l.index(splitted[2])] = 2
        ma[name] = matrice.copy()

    return names

###
# 4. Fonctions d'impression de données
###

## données de base redirigées dans nos structures
def Output_data(name, lst_index, atom_caract, matrice_adja):
    # création du fichier de sortie
    fpath = "Inputs_Outputs/Place_Output_here/"
    filename = name+"_data.txt"
    if isfile(join(fpath, filename)):
        remove(join(fpath, filename))
    f = open(fpath+filename, 'w')
    
    f.write("Indice IndiceOld Caracteristique atome\n")
    for i in range(len(lst_index)):
        f.write(str(i)+' '+str(lst_index[i])+' '+atom_caract[i]+'\n')
    
    f.write("Matrice Adjacence\n")
    r = int(len(matrice_adja))
    for i in range(r):
        s = ''
        for j in range(r):
            s += str(matrice_adja[i][j])+'  '
        f.write(s+'\n')
    f.close()

## données pour le diagramme des nombre d'occurence et taux de recouvrement
def Output_diagramme(name, ordre, min_ordre, lst_ordre, dict_stat):
    # création du fichier de sortie
    fpath = "Inputs_Outputs/Place_Output_here/"
    filename = name+'_'+str(ordre+min_ordre)+".txt"
    if isfile(join(fpath, filename)):
        remove(join(fpath, filename))
    f = open(fpath+filename, 'w')
    
    # liste des couples de donnée { occurrence : [[indice, taux]] }
    d = {}
    for i in lst_ordre[ordre]:
        tmp = dict_stat.get(i)
        if tmp[0] != 1:
            if tmp[0] not in d.keys():
                d[tmp[0]] = [[i, tmp[2]]]
            else :
                d[tmp[0]].append([i, tmp[2]])
    
    j = 1
    f.write("ordonne nbOccur taux indice\n")
    for k in sorted(d.keys()) :
        tmp = d.get(k)
        for l in sorted(tmp):
            f.write(str(j)+' '+str(k)+' '+str(l[1])+' '+str(l[0])+'\n')
            j += 1
    
    f.close()

## ajoute les données supplémentaires
def Output_stat(name, min_ordre, lst_combi, lst_certif, lst_ordre, lst_unique):
    # ouverture du fichier de sortie
    fpath = "Inputs_Outputs/Place_Output_here/"
    filename = name+"_data.txt"
    if isfile(join(fpath, filename)):
        f = open(fpath+filename, 'a')
    
    cmpt = 0
    for l in lst_combi:
        cmpt += len(l)
    
    f.write("\nNombre de sous-graphes connexes :"+str(cmpt)+"\n")
    f.write("Nombre de certificats différents :"+str(len(lst_certif))+"\n")
    f.write("Ordre Nb_certif Nb_unique Nb_sg :\n")
    for i in range(len(lst_unique)):
        f.write(str(i+min_ordre)+" "+str(len(lst_ordre[i]))+" "+str(lst_unique[i])+" "+str(len(lst_combi[i]))+"\n")
    f.close()

## données de résultats sous un format pouvant rentrer dans un tableaux excel (si l'on retire la dernière ligne)
def Output_result(name, min_ordre, lst_certif, lst_ordre, dict_stat):
    # création du fichier de sortie
    fpath = "Inputs_Outputs/Place_Output_here/"
    filename = name+"_res.txt"
    if isfile(join(fpath, filename)):
        remove(join(fpath, filename))
    f = open(fpath+filename, 'w')
    
    f.write("ordre identifiant nombre_occurrence taux_recouvrement recouvrement certificat\n")
    iso_uniq = 0
    for i in range(len(lst_ordre)):
        for indice in lst_ordre[i]:
            tmp2 = dict_stat.get(indice)
            if tmp2[0] > 1:
                #       ordre               identifiant    nombre_occurrence taux_recouvrement  recouvrement                 certificat                
                f.write(str(i+min_ordre)+' '+str(indice)+' '+str(tmp2[0])+' '+str(tmp2[2])+' \''+str_liste(tmp2[1])+' \''+lst_certif[indice].hex()+'\n')
            else :
                iso_uniq += 1
                #f.write(str(i+min_ordre)+' '+str(indice)+' '+str(tmp2[0])+' '+str(tmp2[2])+' \''+str_liste(tmp2[1])+' \''+lst_certif[indice].hex()+'\n')
    #f.write("Nombre unique "+str(iso_uniq)+'\n')
    
    f.close()

## données des liste de combinaisons
def Output_combi(name, lst_ordre, dict_isomorph):
    # création du fichier de sortie
    fpath = "Inputs_Outputs/Place_Output_here/"
    filename = name+"_combi.txt"
    if isfile(join(fpath, filename)):
        remove(join(fpath, filename))
    f = open(fpath+filename, 'w')
    
    f.write("identifiant liste_combi \n")
    for i in range(len(lst_ordre)):
        for indice in lst_ordre[i]:
            tmp = dict_isomorph.get(indice)
            #       identifiant    liste_combi                
            f.write(str(indice)+' '+str_matrice(tmp)+'\n')
    
    f.close()

###
# 5. Fonctions utile à la lecture ou l'écriture de données
###

# Récupère le nom dans les formats type_name.txt
def get_name(filename):
    name1 = filename.split('_')
    name2 = name1[1].split('.')
    return name2[0]

# Fichiers déjà existant et donc calcul probablement non utile
def done(name):
    fpath = "Inputs_Outputs/Place_Output_here/"
    filename1 = name+"_data.txt"
    filename2 = name+"_res.txt"
    # tests si les 2 fichiers existes déjà
    if isfile(join(fpath, filename1)) and isfile(join(fpath, filename2)):
        return True
    else:
        return False

def str_liste(l):
    s = ''
    for i in range(len(l)):
        s += str(l[i])
    return s

def str_matrice(m):
    s = '[ '
    for l in m:
        s += str(str_liste(l))+' '
    return s+']'


# Initie la matrice d'adjacence pour stocker les données
def init_matrice(matrice, taille):
    for i in range(taille):
        matrice.append([])
        for j in range(taille):
            matrice[i].append(0)

