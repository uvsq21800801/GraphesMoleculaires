from os import listdir, remove
from os.path import isfile, join
import re
import numpy as np

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

###
# 2. Fonctions de récupération de données d'atomes
###

# retourne le nombre de sommets qui nous intéresse
def Get_nb_vertex(option, name):
    # récum du fichier
    fpath = "Inputs_Outputs/Place_Trad_file_here/" 
    filename = "trad-atom_"+name+".txt"
    f1 = open(join(fpath,filename), 'r').readlines()
    
    # ajoute +1 pour chaque sommet qui nous intéresse
    cdef int count_verticles = 0
    for line in f1:
        splitted = line.split()
        # test needed to exclude the first like
        if len(splitted) == 3:
            if (option == 1 and splitted[1] != 'H') or (option == 0):
                count_verticles += 1    

    return count_verticles

# Retourne le contenu d'un fichier texte pour un nom donné
def Input_trad(option, name, li, atom_caract):
    # recuperation du fichier trad
    fpath = "Inputs_Outputs/Place_Trad_file_here/" 
    filename = "trad-atom_"+name+".txt"
    # si le nom est bien représenté, on récupère les données
    cdef int i = 0

    if isfile(join(fpath,filename)):
        # lecture du fichier bonds et transcription dans la matrice de traduction
        f1 = open(join(fpath,filename), 'r').readlines()
        for line in f1:
            splitted = line.split()
            if len(splitted) == 3:
                if (option == 1 and splitted[1] != 'H') or (option == 0):
                    #li.append(splitted[0])
                    
                    li[i] = splitted[0]

                    # Liste de traduction suivant le modele '[type atome] [numero]'
                    temp = splitted[2]
                    caracteristiques = splitted[1]+' '+temp[len(splitted[1]):]
                    atom_caract[i] = caracteristiques
                    #print(splitted[0]+' '+splitted[1]+' '+splitted[2])
                    i += 1
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
        f1 = open(join(fpath,filename), 'r').readlines()
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
    filename = "bonds_"+name+".txt"
    # si le nom est bien représenté, on récupère les données
    
    #print('isfile? '+ str(isfile(join(fpath,filename))))

    if isfile(join(fpath,filename)):
        #initie la matrice d'adjacence
        #init_matrice(ma,len(li))

        # lecture du fichier bonds et transcription dans la matrice d'adjacence
        f1 = open(join(fpath,filename), 'r').readlines()
        
        #print(li)
        
        for line in f1:
            splitted = line.split()
            # liaison covalente

            #print('test ?? '+ str(splitted[0] == '1' and len(splitted) == 3))

            if splitted[0] == '1' and len(splitted) == 3:
                #print('AAAAA test 2 ?? '+ str(splitted[1] in li and splitted[2] in li))
                if int(splitted[1]) in li and int(splitted[2]) in li:
                    #print('WIN')
                    #ajoute deux 1 dans la matrice ma de façon symétrique
                    #print('li: '+str(li))
                    #print('int(splitted[1]): '+str(int(splitted[1])))
                    #print('int(splitted[1]): '+str(int(splitted[2])))
                    #print('np.where(li == int(splitted[1]) : '+str(np.where(li == int(splitted[1]))[0][0]))
                    #print('np.where(li == int(splitted[2]) : '+str(np.where(li == int(splitted[2]))[0][0]))
                    ma[np.where(li == int(splitted[1]))[0][0]][np.where(li == int(splitted[2]))[0][0]] = True
                    ma[np.where(li == int(splitted[2]))[0][0]][np.where(li == int(splitted[1]))[0][0]] = True
            # liaison hydrogene
            if splitted[0] == '4' and len(splitted) == 4:
                if int(splitted[1]) in li and int(splitted[2]) in li:
                    if option == 1 : # hydrogène présent
                        #ajoute un 2 de l'atomes donneur vers l'accepteur
                        ma[np.where(li == int(splitted[1]))[0][0]][np.where(li == int(splitted[2]))[0][0]] = True # 2 changé en 1 pour optimiser la matrice en bool
                    elif option == 0 and int(splitted[3]) in li:
                        #ajoute un 2 de l'hydrogène vers l'accepteur
                        ma[np.where(li == int(splitted[3]))[0][0]][np.where(li == int(splitted[2]))[0][0]] = True # 2 changé en 1 pour optimiser la matrice en bool
        #print(ma)
        return name
    else :
        #print(ma)
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
            f1 = open(join(fpath,filename), 'r').readlines()
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
# 5. Fonctions utile à la lecture ou l'écriture de données
###

# Récupère le nom dans les formats type_name.txt
def get_name(filename):
    name1 = filename.split('_',1)
    name2 = name1[1].split('.')
    return name2[0]

# Fichiers déjà existant et donc calcul probablement non utile
def done(name, detail):
    if detail[0] == 1 :
        compl = "_H"
    else :
        compl = ""
    fpath = "Inputs_Outputs/Place_Output_here/"
    filename1 = name+compl+"_data.txt"
    filename2 = name+compl+"_res.txt"
    # tests si les 2 fichiers existes déjà
    if isfile(join(fpath, filename1)) and isfile(join(fpath, filename2)):
        return True
    else:
        return False

# Fichiers déjà existant dans le dossier donné et donc calcul probablement inutile
def done_here(fpath, name, detail):
    if detail[0] == 1 :
        compl = "_H"
    else :
        compl = ""
    filename1 = name+compl+"_data.txt"
    filename2 = name+compl+"_res.txt"
    # tests si les 2 fichiers existes déjà
    if isfile(join(fpath, filename1)) and isfile(join(fpath, filename2)):
        return True
    else:
        return False

# Initie la matrice d'adjacence pour stocker les données
def init_matrice(matrice, taille):
    for i in range(taille):
        matrice.append([])
        for j in range(taille):
            matrice[i].append(0)

