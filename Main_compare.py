import sys
from os import listdir, remove
from os.path import isfile, isdir, join
from datetime import datetime
import re
import networkx as nx

sys.path.append('GraphesMoleculaires/Inputs_Outputs')
sys.path.append('GraphesMoleculaires/Solving_Methods')
sys.path.append('GraphesMoleculaires/User_interface')
from Solving_Methods import Similarity as Sim
from Solving_Methods import nx_Graphs as nxg
from Inputs_Outputs import Inputs, Output

'''
Ce main permet de lancer la comparaison entre des sous-graphes à partir :
- du nom du sous-dossier
- du nom de la structure
- la taille étudiée
- son indice (dans une figure)
'''
def interface():

    ##### nom du dossier
    fpath = "Inputs_Outputs/Place_Output_here/" 
    
    ##### Construction du nom de fichier source
    s_dossier = input("Nom sous-dossier entré (ne rien entrer si il n'est pas dans un sous-dossier): ")
    if (s_dossier != ''):
        fpath += s_dossier
    print(fpath)
    if not isdir(fpath):
        print(fpath+" n'est pas un dossier existant.")
        exit(1)
    
    ##### parametres
    # nom
    name = input("Nom fichier entré : ")
    # l'ordre qui nous intéresse
    ordre = input("taille de sous-graphe : ")

    option = input("Retirer les H et déplacer les liaisons H sur donneur [0|1]: ")
    while (option!='0' and option!='1'):
        option = input("(atome H) Attend 0 ou 1 : ")
    detail = [int(option), ordre]
    s = ''
    if(detail[0]):
        s+='_H'

    ##### test sur l'existence du fichier source des combinaisons
    filename = name+'_'+ordre+s+"_combi.txt"
    if not isfile(fpath+"/"+filename):
        print("Le fichier "+filename+" n'existe pas.")
        exit(1)
    
    ##### Lecture du fichier source des combinaisons
    f = open(fpath+"/"+filename, "r")
    lines=f.readlines()
    f.close()
    
    ##### indices des graphes qui nous intéressent
    set_id = set()
    error = False
    while len(set_id) == 0:
        user_input = input("indice des sous-graphe : ")
        splited = user_input.replace(' ', '').split(',')
        for part in splited :
            if '-' in part :
                part = part.split('-')
                if len(part)!=2 :
                    error = True
                else :
                    if part[0].isnumeric() and part[1].isnumeric():
                        if int(part[0]) >= 0 and int(part[1]) < len(lines)-1 and int(part[0]) < int(part[1]):
                            for i in range(int(part[0]), int(part[1])+1):
                                set_id.add(i)
                        else :
                            error = True
                    else :
                        error = True
            else :
                if part == '*':
                    for i in range(len(lines)+1):
                        set_id.add(i)
                elif part.isnumeric() and int(part)<len(lines)-1:
                    set_id.add(int(part))
                else :
                    error = True
            if error:
                break
        if error:
            set_id.clear()
        print(set_id)
    set_id = sorted(set_id)
    
    #####
    # 1 - Extraction des données  
    #####
    
    ##### dictionnaire des combinaisons d'intérêt
    dict_combi = {}
    
    for i in range(0,len(lines)-1):
        splitted = lines[i+1].split()
        if (i in set_id):
            dict_combi[i] = splitted[1] 

    ##### Récupération des données du graphe général
    filename1, filename2, lst_index, atom_caract, matrice_adja = Inputs.data_input(detail[0], name)

    
    #####
    # 2 - comparaisons des sous-graphes (sauvegarde des MCIS)
    #####
    
    ##### Construction des sous-graphes
    # Tableau rassemblant les matrice d'adjacence et caractéristique des motifs
    lst_id = list(set_id)
    nb = len(lst_id)
    tab_sg = [None for x in range(nb)]

    # initialisation des sous-graphes à évaluer
    for i in range(nb):
        (adja_tmp, carac_tmp) = nxg.extract_sub(
            matrice_adja, atom_caract, dict_combi[lst_id[i]])
        tab_sg[i] = nxg.create_graph(adja_tmp, carac_tmp)
    
    # Choix du type de Similarite
    print("Quel type de similarite étudier? ")
    print("\t 1 : similarité par cout d'édition ")
    print("\t 2 : similarité par calcul de Raymond sur MCIS ")
    print("\t 3 : similarité par calcul asymétrique sur MCIS ")
    print("\t 0 : les 3 types de similarité ")
    option = input("(Similarité) Attend entre 0 et 3 : ")
    while (option!='0' and option!='1' and option!='2' and option!='3'):
        option = input("(Similarité) Attend entre 0 et 3 : ")
    detail.append(int(option))
    if detail[2] == 0:
        multi = True
        mcis = True
    else :
        multi = False
        if detail[2] >= 2:
            mcis = True
        else :
            mcis = False
    
    tab_mcis = -1
    if mcis :
        tab_mcis = Sim.tab_mcis(tab_sg)
    
    ##### Rempli la matrice avec la(les) métrique(s) sélectionnée(s)
    print(str(name)+" calcul commence "+str(datetime.now().time()))
    if multi :
        Tab_sim = []
        for i in range(3):
            detail[2] += 1
            Tab_sim.append([])
            # Similarité avec MCIS ou non
            if detail[2] >= 2 :
                Tab_sim[i] = Sim.Similarity_avecMcis(tab_sg,tab_mcis,detail)
            else :
                Tab_sim[i] = Sim.Similarity_sansMcis(tab_sg,detail)
            print(name+" calcul "+str(detail[2])+" fini "+str(datetime.now().time()))
        detail[2] = 0
    else :
        # Similarité avec MCIS ou non
        if detail[2] >= 2 :
            Tab_sim = Sim.Similarity_avecMcis(tab_sg,tab_mcis,detail)
        else :
            Tab_sim = Sim.Similarity_sansMcis(tab_sg,detail)
        # imprime les matrices de chaleur
        print(name+" calcul "+str(detail[2])+" fini "+str(datetime.now().time()))
    
    
    #####
    # 3 - fichiers de sortie
    #####
    
    # stocke les mcis générés
    if mcis :
        print("Je stocke les MCIS")
    
    # stocke la matrice dans un fichier et dessine la matrice de chaleur
    if multi :
        for i in range(3):
            detail[2] += 1
            Output.Output_sim(s_dossier, name, detail, lst_id, Tab_sim[i])
        detail[2] = 0
    else :
        Output.Output_sim(s_dossier, name, detail, lst_id, Tab_sim)
    print(name+" écriture "+str(detail[2])+" fini "+str(datetime.now().time()))
    
    exit(0)

def main():
    interface()
    
if __name__=="__main__":
    main()
