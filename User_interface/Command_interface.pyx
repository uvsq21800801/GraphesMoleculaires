# sera une interface de commande si besoin
import sys
sys.path.append('GraphesMoleculaires/Inputs_Outputs')
sys.path.append('GraphesMoleculaires/Solving_Methods')
sys.path.append('GraphesMoleculaires/User_interface')

from Inputs_Outputs import Inputs as In
from Inputs_Outputs import Output as Out
from Solving_Methods import Combinations as Combi
from Solving_Methods import SmartSubGenerator as SSG
from Solving_Methods import OrderedSubGen as OSG
from Solving_Methods import Isomorph as Iso
from Solving_Methods import Statistic as Stat
from Solving_Methods import Similarity as Simil
import bdd_insert

import pymongo as pm
from bson.objectid import ObjectId
from User_interface import mongo_connection as mc
from User_interface import commande_terminal as ct

from os import listdir, remove, mkdir
from os.path import isfile, isdir, join
from datetime import datetime

cimport cython
cimport numpy as np
import numpy as np

import time

def interface():
    ##### VARIABLES 
    # de l'interface
    cdef bint Multi_Taille = True
    cdef bint Multi_Conf = False
    cdef bint Conf_exist = False
    # de la taille
    cdef int max_ordre
    cdef int min_ordre
    # les options :
    #      0 : Hydrogène retiré?
    #      1 : Oxygène de l'eau présent?
    #      2 : Taille traitée
    #      3 : Update?
    options = [False, False, 0, False]
    # les identifiants de la BDD (format str ou _id)
    #      0 : interface (_id)
    #      1 : coloration (_id)
    #      2 : configs [] (_id)
    bd_ids = ["","",[]]
    # la hierarchie de fichiers
    path_I = "Inputs_Outputs/Place_Folder_here/"
    path_O = "Inputs_Outputs/Place_Output_here/"
    interf_name = ""
    color_name = ""
    conf_num = []

    ##### Connection à la BDD 
    client = mc.mongodb_connect()
    # base de données
    db = client.graphetarium
    # tables
    interfs = db.interfaces
    configs = db.configurations
    colors = db.colorations
    motifs = db.motifs
    occurs = db.occurrences

    ##### Fichiers d'informations à traiter
    # récupère le nom de l'interface et test son existance
    namefolder_check = False
    dir_I = ''
    cdt_folder_name = False
    while namefolder_check == False:
        interf_name = input("Quel est le nom de l'interface traité? ")
        list_dir = listdir(path_I)
        for l in list_dir:
            if interf_name in l and isdir(join(path_I, l)): # folder ayant 'interf_name' dans son nom trouvé!
                if namefolder_check == True and cdt_folder_name == False: # cas où 2 folders ont la même particule choisie par l'utilisateur
                                                # dans ce cas, on force l'utilisateur à entrer le nom complet du dossier
                    print('Erreur, il y à plusieurs fichiers de ce nom')
                    while cdt_folder_name == False: #(not isdir(join(path_I, dir_I))) or dir_I == "":
                        dir_I = input("Quel est le nom complet du dossier des fichiers d'entrés? ")
                        if isdir(join(path_I, dir_I)):
                            cdt_folder_name = True
                            interf_name = dir_I
                        else: 
                            print("Erreur, le dossier n'existe pas")
                        
                namefolder_check = True
                dir_I = l
        if namefolder_check == False: 
            print('erreur, aucun dossier contenant \"'+str(interf_name)+"\" dans son n'a été"
                                                        +" trouvé dans le dossier des inputs")  
    # test sur la BDD si l'interface est connu ou non
    tmp_colors = []
    # tmp_configs = []
    if interfs.count_documents({"name":interf_name}) > 0 :
        result = interfs.find_one({"name":interf_name}) 
        res = dict(result)
        print(res)
        bd_ids[0] =  str(res["_id"])
        # info déjà lié à l'interface ?
        tmp_colors = list(res["colors"])
    else :
        # créer l'interface
        bd_ids[0] = str(interfs.insert_one({"name":interf_name, "colors":list()}).inserted_id)
    if len(tmp_colors)>0:
        colors_names = []
        for _id in tmp_colors:
            result = colors.find_one({"_id":_id})
            res = dict(result)
            colors_names.append(res["name"])
        print("Coloration(s) déjà connue(s) pour l'interface :",colors_names)
    
    ##### Type de traitement
    # Coloration ?
    # créé ou existante
    question = "Doit_on utiliser une coloration existante?"
    if ct.terminal_question_On(question, "", "Oui", True):
        question = "Quel est le nom de la coloration que l'on utilise? "
        color_name = input(question)
        # demande le nom de la coloration
        while colors.count_documents({"name":color_name}) == 0 :
            color_name = input(color_name+" n'exites pas. Autre nom :")
        result = colors.find_one({"name":color_name})
        bd_ids[1] = str(result["_id"])
        list_color = list(result["elem"])
        options[0] = result["hydro"]
        print(list_color)
    else :
        #création du dictionnaire des couleurs
        color_name = input("Comment est appelé la nouvelle couleurs? ")
        while colors.count_documents({"name":color_name}) > 0 :
            color_name = input(color_name+" exites déjà. Autre nom :")
        # la liste des elements (index +1 pour les numéros réels)
        count = ct.terminal_input_num("Combien d'éléments ?","")
        list_color = []
        element = "temp"
        while element != "":
            element = input("Quel est le nom de l'élément (ne rien rentrer pour finir)? ")
            list_color.append(str(element))
        # Hydrogène ou non ?
        if "H" in list_color:
            print("Les Hydrogènes sont présents.")
            options[0] = False
        else:
            question = "Doit-on retirer les Hydrogène et déplacer les liaisons H ?"
            options[0] = ct.terminal_question_On(question, "", "Oui", True)
        color = {"name": color_name,
            "elem": list_color,
            "hydro": options[0]}
        # insertion dans la bdd
        result = colors.insert_one(color)
        bd_ids[1] = result.inserted_id
        print(result)
    
    ## ajouter la coloration sur l'interface
    ########################## A Faire
    
    ## choisi les configurations
    # recherche les fichiers liées
    files_T, files_B, conf_num = recherche_files_conf(path_I, dir_I)
    conf_num = list(conf_num)
    if len(conf_num)>1 :
        Multi_Conf = True
    else :
        Multi_Conf = False

    # voir dans la BDD pour les conf
    for i in sorted(conf_num):
        if configs.count_documents({"interf":ObjectId(bd_ids[0]), "num": i}) > 0 :
            result = configs.find_one({"interf":ObjectId(bd_ids[0]), "num": i})
            bd_ids[2].append(result["_id"])
        else :
            result = configs.insert_one({"interf":ObjectId(bd_ids[0]), "num": i})
            bd_ids[2].append(result.inserted_id)
    
    # Taille des motifs étudiés
    question = "Quelles sont les bornes de taille des motifs à enregistrer?"
    min_ordre, max_ordre = ct.terminal_input_bornes_range(question, 2, 10)
    if max_ordre == 0:
        print("Erreur impossible sur les limites de taille")
        return 0
    if min_ordre == max_ordre :
        Multi_Taille = False
    
    # Type de génération de sous-graphes  
    question = "Ne générons-nous que des graphlets avec au moins un OW?"
    options[1] = ct.terminal_question_On(question, "Motifs avec OW", "non", True)
    ##### Création dossier de sortie
    #dir_O = interf_name
    ### dossier n'existe pas déjà ?
    if not isdir(join(path_O, dir_I)) :
        ### créé le dossier
        mkdir(join(path_O, dir_I))
    
    ##### Lancement de l'execution du programme
    print(conf_num)
    for i in conf_num:
        exec_for_one_conf(min_ordre, max_ordre, files_T[i], files_B[i], path_I, 
                        dir_I, options, path_O, Multi_Taille, i, bd_ids, list_color, motifs, occurs)
    return 1

def exec_for_one_conf(min_ordre, max_ordre, filename_T, filename_B, path_I, 
                        dir_I, options, path_O, Multi_Taille, nb_conf, bd_ids, lst_col, motifs, occurs):  
    filename1, filename2, lst_index, atom_caract, matrice_adja = In.data_input(options[1], dir_I, filename_T, filename_B)
    
    #if not In.done_here(join(path_O, dir_I), dir_I, options):
    ### imprime les données de ce graphe
    Out.Output_data(dir_I, options, lst_index, atom_caract, matrice_adja, nb_conf)

    #### Exécution sur le ou les ordre(s)
    if Multi_Taille :
        print(dir_I+" commence "+str(datetime.now().time()))
        '''
        # sous_graphe connexe par methode bruteforce
        lst_combi = Combi.gen_combi_brute_range(matrice_adja, min_ordre, max_ordre)
        '''
        # sous_graphes connexes par notre méthode de parcour d'un arbre de combi de la matrice d'adja
        lst_combi = SSG.subgen(matrice_adja, min_ordre, max_ordre)
        #lst_combi = OSG.subgen_deg_decroiss(matrice_adja, atom_caract, min_ordre, max_ordre, crible)
        
        print(dir_I+" combinaisons finis "+str(datetime.now().time()))
        
        for i in range(max_ordre - min_ordre + 1):
            ordre = min_ordre+i
            #options[1] = ordre ######### a voir ce que cette délétion change
            (dict_isomorph, dict_stat, lst_id, lst_certif, nb_unique) = programm_1(dir_I, dir_I, 
                    options, matrice_adja, atom_caract, lst_col, lst_combi[i], nb_conf, ordre, bd_ids, motifs, occurs)
            ## DEPLACER ICI LES ECRITURES SUR BDD?
            #programm_2(dir_O, name, detail, matrice_adja, atom_caract, lst_id, dict_isomorph)

            print(dir_I+" taille "+str(ordre)+" fini "+str(datetime.now().time())+"\n")
        
        print(dir_I+" fini "+str(datetime.now().time())+"\n")
    else : 
        print(dir_I+" commence "+str(datetime.now().time()))
        '''
        # sous_graphe connexe par methode bruteforce
        lst_combi = Combi.gen_combi_brute(matrice_adja, ordre)
        '''
        # sous_graphes connexes par notre méthode de parcour d'un arbre de combi de la matrice d'adja
        lst_combi = SSG.subgen(matrice_adja, max_ordre, max_ordre)
        #lst_combi = OSG.subgen_deg_decroiss(matrice_adja, atom_caract, ordre, ordre, crible)

        print(dir_I+" combinaisons finis "+str(datetime.now().time()))
        
        #options[1] = max_ordre ######### a voir ce que cette délétion change
        (dict_isomorph, dict_stat, lst_id, lst_certif, nb_unique) = programm_1(dir_I, dir_I,
                     options, matrice_adja, atom_caract, lst_col, lst_combi, nb_conf, max_ordre, bd_ids, motifs, occurs)
        
        #programm_2(dir_O, name, detail, matrice_adja, atom_caract, lst_id, dict_isomorph)
        
        print(dir_I+" fini "+str(datetime.now().time())+"\n")

    return 1    
    
    for i in range(min_ordre, max_ordre):
        exec_for_one_size()
    return 1

def programm_1 (dir_O, name, detail, matrice_adja, atom_caract, lst_col, lst_combi, nb_conf, ordre, bd_ids, motifs, occurs):
    t_cerif = 0 ## test
    t_prep_c = 0 ## test
    t_fill = 0 ## test
    time_temp = time.time()## test
    (dict_isomorph, dict_stat, lst_id, lst_certif, t_cerif, t_prep_c, t_fill) = Iso.combi_iso(matrice_adja, atom_caract, lst_col, lst_combi, detail[1], t_cerif, t_prep_c, t_fill)
    ## ^ 3 last values are test
    print('exec of the whole combi iso: '+str(time.time()-time_temp)+' seconds') ## test
    print('exec of the dict filling: '+str(t_fill)+' seconds') ## test
    print('exec of the prep for pynauty: '+str(t_prep_c)+' seconds') ## test
    print('exec of the pynauty: '+str(t_cerif)+' seconds') ## test

    print(name+" isomorph fini "+str(datetime.now().time()))
                        
    # calcul le taux de recouvrement 
    Stat.Taux_recouvert(dict_stat)
    # tri de lst_id par nombre d'occurence et le nombre de motif unique
    lst_id = Stat.Tri_indice(lst_id, dict_stat)
    nb_unique = Stat.Nombre_unique(lst_id, dict_stat)

    # insère les motifs dans la bdd
    # def insert_motifs(coll_motifs, coll_occurs, bd_ids, matrice_adja, atom_caract, lst_index, dict_isomorph, dict_stat, coloration, lst_certif, nb_sommets, liaison_H, crible):
    bdd_insert.insert_motifs(motifs, occurs, bd_ids, nb_conf, matrice_adja, atom_caract, lst_id, dict_isomorph, dict_stat, lst_certif, ordre, detail[0], False)    

    # imprime combinaisons
    Out.Output_combi(dir_O, name, detail, lst_id, dict_isomorph, nb_conf, ordre)
    # imprime les diagrammes
    Out.Output_diagramme(dir_O, name, detail, lst_id, dict_stat, nb_conf, ordre)
    # imprime statistique de l'ordre étudié
    Out.Output_stat(dir_O, name, detail, lst_combi, lst_certif, lst_id, nb_unique, nb_conf, ordre)
    # imprime les résultats
    Out.Output_result(dir_O, name, detail, lst_certif, lst_id, dict_stat, nb_conf, ordre)

    print(name+" sortie fini "+str(datetime.now().time()))
    return (dict_isomorph, dict_stat, lst_id, lst_certif, nb_unique)


def exec_for_one_size():

    return 1
"""
Pour la suite : ATTENTION!!!
- changement des structures des options
- utilisation d'un unique duo max_ordre et min_ordre à enregistrer
- utilisation des listes de _id de la BDD dans la sauvegarde
- ATTENTION a bien utiliser list_color pour le certificat ou a traduire list_color en dict_color
- définir les formats des collections et de leur attributs
- ne pas oublier d'ajouter les couleurs et les configs associés à une interface (sauf si on utilise jamais ces listes)

- Il serait plus logique de déplacer les fonctions en bas dans Inputs.pyx et de supprimer les anciennes fonctions
- Bien entendu il faudra optimiser cette nouvelle interface (je pourrais aussi le faire Chloé)

- Bon courage pour reprendre la suite du programme qui est pour le moment en commentaire
"""

# Recherche des fichiers des configurations
#
# Entrées : path d'entré et dossier de l'interface
#
# Sorties : liste des fichier de trad-atom, de bonds et des numéros de configurations

def recherche_files_conf (path_I, dir_I):
    files_T = {}
    files_B = {}
    conf_num = []
    # demande si toutes les conf ou désigné(s)
    question = "Quels sont les configurations étudiées?"
    res = ct.terminal_ensemble_num(question)
    if -1 in res:
        #tous les duos trouvés
        for f in extrait_files(path_I, dir_I, "bonds"):
            part = f.split("conf")
            part = part[1].split('.')
            if part[0].isnumeric():
                i = int(part[0])
                t_name = "trad-atom_conf"+str(i)+".txt"
                b_name = "bonds_conf"+str(i)+".txt"
                # si le deuxième existe alors on ajoute la conf à la liste
                if isfile(join(path_I,dir_I,t_name)):
                    conf_num.append(i)
                    files_T[i] = t_name
                    files_B[i] = b_name
    else :
        conf_num = list(res)
        # les duos désignés
        # recherche chaque numéro et les ajoute aux sorties un à un
        for i in conf_num:
            t_name = "trad-atom_conf"+str(i)+".txt"
            b_name = "bonds_conf"+str(i)+".txt"
            # si les deux fichiers existent alors on les ajoute aux listes
            if isfile(join(path_I,dir_I,t_name)) and isfile(join(path_I,dir_I,b_name)):
                files_T[i] = t_name
                files_B[i] = b_name
            else :
                conf_num.remove(i)
    conf_num.sort()
    print(conf_num)
    print("files_T"+str(files_T))
    return files_T, files_B, conf_num

# Fonction qui extrait la liste des noms de fichier
# contenant la partie en paramètre

def extrait_files(path, dir, part_name):
    files = []
    for f in listdir(join(path,dir)):
        if isfile(join(path,dir,f)) and part_name in f:
            files.append(f)
    return files