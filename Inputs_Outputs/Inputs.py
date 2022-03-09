from os import listdir, remove
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
    
    ##print(filename)

    #initie la matrice d'adjacence
    Init(ma,len(li))

    # lecture du fichier bonds et transcription dans la matrice d'adjacence
    f1 = open(fpath+filename, 'r').readlines()
    for line in f1:
        splitted = line.split()
        # liaison covalente
        if splitted[0] == '1' and len(splitted) == 3:
            if splitted[1] in li and splitted[2] in li:
                #ajoute un 1 dans la matrice ma de façon symétrique
                #print(str(li.index(splitted[1]))+' '+str(li.index(splitted[2])))
                ma[li.index(splitted[1])][li.index(splitted[2])] = 1
                ma[li.index(splitted[2])][li.index(splitted[1])] = 1
            #print(splitted[0]+' '+splitted[1]+' '+splitted[2])
        # liaison hydrogene
        if splitted[0] == '4' and len(splitted) == 4:
            if splitted[1] in li and splitted[2] in li:
                #ajoute un 2 dans la matrice ma de façon asymétrique
                #print(str(li.index(splitted[1]))+' '+str(li.index(splitted[2])))
                ma[li.index(splitted[1])][li.index(splitted[2])] = 2
            #print(splitted[0]+' '+splitted[1]+' '+splitted[2])
        
    name1 = filename.split('_')
    name2 = name1[1].split('.')
    
    return name2[0]
    
def Input_trad(li, atom_caract):
    # recuperation du fichier trad
    fpath = "Inputs_Outputs/Place_Trad_file_here/" 
    filenames = [f for f in listdir(fpath) if isfile(join(fpath, f))]
    filename = filenames[0]
    
    # lecture du fichier bonds et transcription dans la matrice de traduction
    f1 = open(fpath+filename, 'r').readlines()
    for line in f1:
        splitted = line.split()
        if len(splitted) == 3:
            if splitted[1] != 'H':
                li.append(splitted[0])
                
                # Liste de traduction suivant le modele '[type atome] [numero]'
                temp = splitted[2]
                caracteristiques = splitted[1]+' '+temp[len(splitted[1]):]
                atom_caract.append(caracteristiques)
            #print(splitted[0]+' '+splitted[1]+' '+splitted[2])
        
    name1 = filename.split('_')
    name2 = name1[1].split('.')
    
    return name2[0]

def Output_diagramme(name, ordre, min_ordre, lst_ordre, data):
    # création du fichier de sortie
    fpath = "Inputs_Outputs/Place_Output_here/"
    filename = name+'_'+str(ordre+min_ordre)+".txt"
    if isfile(join(fpath, filename)):
        remove(join(fpath, filename))
    f = open(fpath+filename, 'w')
    
    # liste des couples de donnée { occurance : [taux] }
    d = {}
    for i in lst_ordre[ordre]:
        tmp = data.get(i)
        if tmp[0] != 1:
            if tmp[0] not in d.keys():
                d[tmp[0]] = [tmp[2]]
            else :
                d[tmp[0]].append(tmp[2])
    
    j = 1
    f.write("ordonne nbOccur taux\n")
    for k in sorted(d.keys()) :
        tmp = d.get(k)
        for l in sorted(tmp):
            f.write(str(j)+' '+str(k)+' '+str(l)+'\n')
            j += 1
    
    f.close()
