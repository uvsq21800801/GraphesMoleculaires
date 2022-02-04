from os import listdir
from os.path import isfile, join
import re

#initie la matrice d'adjacence
def Init(matrice, taille):
    for i in range(taille):
        matrice.append([])
        for j in range(taille):
            matrice[i].append(0)

# devra retourner le contenu des fichiers texte
def Input_bonds(li,ma):    
    # recuperation du fichier bonds
    fpath = "Inputs_Outputs/Place_Bonds_file_here/"
    filenames = [f for f in listdir(fpath) if isfile(join(fpath, f))]
    filename = filenames[0]

    #initie la matrice d'adjacence
    Init(ma,len(li))

    # lecture du fichier bonds et transcription dans la matrice d'adjacence
    file = open(fpath+filename, 'r').readlines()
    for line in file:
        splitted = line.split()
        # liaison covalente
        if splitted[0] == '1' and len(splitted) == 3:
            if splitted[1] in li and splitted[2] in li:
                #ajoute un 1 dans la matrice ma de façon symétrique
                print(str(li.index(splitted[1]))+' '+str(li.index(splitted[2])))
                ma[li.index(splitted[1])][li.index(splitted[2])] = 1
                ma[li.index(splitted[2])][li.index(splitted[1])] = 1
            #print(splitted[0]+' '+splitted[1]+' '+splitted[2])
        # liaison hydrogene
        if splitted[0] == '4' and len(splitted) == 4:
            if splitted[1] in li and splitted[2] in li:
                #ajoute un 2 dans la matrice ma de façon asymétrique
                print(str(li.index(splitted[1]))+' '+str(li.index(splitted[2])))
                ma[li.index(splitted[1])][li.index(splitted[2])] = 2
            #print(splitted[0]+' '+splitted[1]+' '+splitted[2])

    print("Inputs.py->Inputs_bonds a completer")
    
def Input_trad(li):
    # recuperation du fichier trad
    fpath = "Inputs_Outputs/Place_Trad_file_here/" 
    filenames = [f for f in listdir(fpath) if isfile(join(fpath, f))]
    filename = filenames[0]
    
    # lecture du fichier bonds et transcription dans la matrice de traduction
    file = open(fpath+filename, 'r').readlines()
    for line in file:
        splitted = line.split()
        if len(splitted) == 3:
            if splitted[1] != 'H':
                li.append(splitted[0])
            #print(splitted[0]+' '+splitted[1]+' '+splitted[2])

            # ajouter les informations des atomes dans une structure


    print("Inputs.py->Inputs_trad a completer")