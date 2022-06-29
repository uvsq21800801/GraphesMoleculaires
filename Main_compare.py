import sys
from os import listdir, remove
from os.path import isfile, join
import re
import networkx as nx
sys.path.append('GraphesMoleculaires/Inputs_Outputs')
sys.path.append('GraphesMoleculaires/Solving_Methods')
from Solving_Methods import Similarity
from Inputs_Outputs import Inputs

'''
Ce main permet d'afficher le dessin d'un sous graphe à partir de:
- le nom du sous-dossier
- un nom de graphe
- la taille étudiée
- son indice (indiqué dans la matrice de chaleur)
'''
def interface():

    ##### Sous dossier
    fpath = "Inputs_Outputs/Place_Output_here/" 
    s_dossier = input("Nom sous-dossier entré (ne rien entrer si il n'est pas dans un sous-dossier): ")
    if (s_dossier != ''):
        fpath += '/'+s_dossier
    
    ##### Nom du graphe
    # l'ordre qui nous intéresse
    ordre = input("taille de sous-graphe : ")
    # nom
    name = input("Nom fichier entré : ")

    option = input("Retirer les H et déplacer les liaisons H sur donneur [0|1]: ")
    while (option!='0' and option!='1'):
        option = input("(atome H) Attend 0 ou 1 : ")
    option = int(option)   
    s = ''
    if(option):
        s+='_H'

    filename = name+'_'+ordre+s+"_combi.txt"

    ##### indices des grapheq qui nous intéressent
    set_id = set()
    error = False
    while len(set_id) == 0:
        user_input = input("indice des sous-graphe : ")
        splited = user_input.split(',')
        for part in splited :
            if '-' in part :
                part = part.split('-')
                if len(part)!=2 :
                    error = True
                else :
                    if part[0].isnumeric() and part[1].isnumeric():
                        for i in range(int(part[0]), int(part[1])+1):
                            set_id.add(i)
                    else :
                        error = True
            else :
                if part.isnumeric() :
                    set_id.add(int(part))
                else :
                    error = True
        if error:
            set_id.clear()
    set_id.sort()
    
    #####
    # 1 - Extraction des combi  
    #####
    dict_combi = {}
    f = open(fpath+"/"+filename, "r")
    lines=f.readlines()
    for i in range(0,len(lines)-1):
        splitted = lines[i+1].split()
        if (i in set_id):
            dict_combi[i] = splitted[1] 
    f.close()

    #####
    # 2 - caractéristiques du graphe et matrice adja (recherche des infos sur les motifs)
    ##### 
    filename1, filename2, lst_index, atom_caract, matrice_adja = Inputs.data_input(option, name)

    
    #####
    # 3 - comparaisons des sous-graphes (sauvegarde des MCIS)
    #####
    
    # construction des graphes networkx
    
    # comparaison 2 à 2 pour les MCIS
    
    # rempli la matrice avec la métrique sélectionné
    
    # dessine la matrice de chaleur
    
    

def main():
    interface()
    
if __name__=="__main__":
    main()
