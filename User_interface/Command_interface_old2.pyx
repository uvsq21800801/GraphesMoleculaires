# sera une interface de commande si besoin
import sys
sys.path.append('GraphesMoleculaires/Inputs_Outputs')
sys.path.append('GraphesMoleculaires/Solving_Methods')
sys.path.append('GraphesMoleculaires/MCIS')

from Inputs_Outputs import Inputs as In
from Inputs_Outputs import Output as Out
from Solving_Methods import Combinations as Combi
from Solving_Methods import SmartSubGenerator as SSG
from Solving_Methods import OrderedSubGen as OSG
from Solving_Methods import Isomorph as Iso
from Solving_Methods import Statistic as Stat
from Solving_Methods import Similarity as Simil

from os import listdir, remove, mkdir
from os.path import isfile, isdir, join
import os
from datetime import datetime

cimport cython
cimport numpy as np
import numpy as np

import time

def interface():
    cdef bint Multi_Taille = True
    cdef bint Multi_File = False
    cdef bint File_exist = False

    ##### Choix des tailles de sous-graphes
    cdef int min_ordre
    cdef int max_ordre
    cdef int ordre

    input_num = input("Taille des sous-graphes : ")
    while not Multi_Taille and not input_num.isnumeric():
        if input_num == '*':
            Multi_Taille = True
        else :
            input_num = input("(Taille sous-graphes) Entrer un nombre : ")
    if not Multi_Taille and input_num.isnumeric():
        ordre = int(input_num)
    if Multi_Taille :
        input_num = input("Taille minimum : ")    
        while not input_num.isnumeric()  :
            input_num = input("(Taille minimum) Entrer un nombre : ")
        if input_num.isnumeric():
            min_ordre = int(input_num)
        input_num = input("Taille maximum : ")    
        while not input_num.isnumeric()  :
            input_num = input("(Taille maximum) Entrer un nombre : ")
        if input_num.isnumeric():
            max_ordre = int(input_num)
        if min_ordre > max_ordre :
            tmp = min_ordre
            min_ordre = max_ordre
            max_ordre = tmp
        
    crible = input("Crible (y/n default: no) : ")
    while not (crible == 'y' or crible == 'n' or crible == ''):
        crible = input("Crible (y/n default: no) : ")
    if crible == 'y':
        crible = True
    else:
        crible = False
    
    if min_ordre == max_ordre:
        Multi_Taille = False
    if not Multi_Taille and input_num.isnumeric():
        ordre = int(input_num)
        
    ##### Fichiers entr??s
    fpath = "Inputs_Outputs/Place_Folder_here/"
    #name = input("Nom complet du dossier entr?? : ")
    #fpath_T = "Inputs_Outputs/Place_Trad_file_here/" 
    #fpath_B = "Inputs_Outputs/Place_Bonds_file_here/"
    #filename_T = "trad-atom_"+name+".txt"
    #filename_B = "bonds_"+name+".txt"
    
    # On cherche ?? r??cup la partie du nom du dossier qui nous int??resse
    img_name = ''
    while img_name == '':
        name = input("Nom complet du dossier entr?? : ")
        name_particles = name.split("_")
        for i in range(len(name_particles)):
            if "img" in name_particles[i]:
                img_name = name_particles[i]
        if img_name == '':
            print("dossier ayant une syntaxe incorrecte (pas de \"img\")")
        if not os.path.isdir(join(fpath, name)):
            print("le dossier "+str(join(fpath, name))+" n'existe pas")
            img_name = ''
    

    # iterate over files in
    # that directory
    # A METTRE LE CODE CI DESSOUS DANS UNE GROSSE BOUCLE DE GESTION D ERREUR
    filename_T = ''
    filename_B = ''
    for filename in os.listdir(join(fpath,name)):
        if "trad" in filename:
            filename_T = filename
        if "bonds" in filename:
            filename_B = filename       

    
    #if isfile(join(fpath,filename_T) and join(fpath,filename_B)):

    #else :

    # L'id??e du Multifile est possiblement obselete, si on utilise le nouveau sys
    # de fichier, mais dans le doute, je garde ??a en comms
    ''' 
    while not Multi_File and not File_exist :
        if name == '*':
            Multi_File = True
            print("Tous les fichiers.")
            filenames = [f for f in listdir(fpath_T) if isfile(join(fpath_T, f))]
        else :
            if isfile(join(fpath_T, filename_T)) and isfile(join(fpath_B, filename_B)):
                File_exist = True
                print("Execution sur les fichiers %s et/ou %s."%(filename_T, filename_B))
            else :
                print("Les fichiers %s et/ou %s n'existent pas ou ne sont pas aux bons endroits."%(filename_T, filename_B))
                name = input("Nom fichier entr?? : ")
                filename_T = "trad-atom_"+name+".txt"
                filename_B = "bonds_"+name+".txt"
    '''
    ##### Cr??ation dossier de sortie
    path_O = "Inputs_Outputs/Place_Output_here/"
    #dir_O = input("Nom sous-dossier sortant : ")
    dir_O = name
    ### dossier n'existe pas d??j?? ?
    if not isdir(join(path_O, dir_O)) :
        ### cr???? le dossier
        mkdir(join(path_O, dir_O))
    
    ##### Options:
    option = input("Retirer les H et d??placer les liaisons H sur donneur [0|1]: ")
    while (option!='0' and option!='1'):
        option = input("(atome H) Attend 0 ou 1 : ")
    detail = [int(option), 0]
    
    # Choix du type de Similarite
    '''
    print("Quel type de similarite ??tudier? ")
    print("\t 1 : similarit?? par cout d'??dition ")
    print("\t 2 : similarit?? par calcul de Raymond sur MCIS ")
    print("\t 3 : similarit?? par calcul asym??trique sur MCIS ")
    print("\t 0 : les 3 types de similarit?? ")
    option = input("(Similarit??) Attend entre 0 et 3 : ")
    while (option!='0' and option!='1' and option!='2' and option!='3'):
        option = input("(Similarit??) Attend entre 0 et 3 : ")
    detail.append(int(option))
    '''
    detail.append(0) #

    detail.append(crible)
    
    ###### Lancement de l'execution du programme
    if not Multi_File :
        filenames = [name]
    for filename in filenames:
        
        # appel fonction
        exec_for_one_file(filename, detail, Multi_Taille, Multi_File, ordre, min_ordre, max_ordre, input_num, dir_O, path_O, fpath+name, filename_B, filename_T, name)
        
    return 1

# permet de d??graisser une boucle de l'interface, execute tout pour un fichier
def exec_for_one_file(filename, detail, Multi_Taille, Multi_File, ordre, min_ordre, max_ordre, input_num, dir_O, path_O, cfpath, filename_B, filename_T, name):
    ## Extraction des donn??es
    if Multi_File:
        name = In.get_name(filename)
    
    
    # nombre de sommets utile ?? l'initialisation des plus grosses structures
    cdef int nb_sommet = In.Get_nb_vertex(detail[0], join(cfpath, filename_T))
    atom_caract = np.empty((nb_sommet,), dtype='<U32')
    cdef np.ndarray[np.int32_t, ndim=1] lst_index = np.empty(nb_sommet, dtype=np.int32)

    filename_T = In.Input_trad(detail[0], cfpath, lst_index, atom_caract, filename_T)
    matrice_adja = np.zeros((nb_sommet,nb_sommet),dtype=bool)

    #matrice_adja[0][0] = True

    filename_B = In.Input_bonds(detail[0], cfpath, lst_index, matrice_adja, filename_B)

    #print('#################################################################')
    #print(matrice_adja)
    #print('#################################################################')
    
    # test: taille raisonnable ou non
    if (len(atom_caract)<int(input_num)):
        print('Erreur: Taille entr??e trop grande')
        print('Taille maximum:'+str(len(atom_caract)))
        return 0

    ### d??j?? ex??cut???
    if In.done_here(join(path_O, dir_O), name, detail):
        print(name+" d??j?? fait")
        test = input("Effacer les pr??c??dents r??sultats? :[y|n]: ")
        while (test!='y' and test!='n') :
            test = input("(Effacer resultats) Attend y ou n: ")
        if test=='y' :
            if detail[0] == 1 :
                compl = "_H"
            else :
                compl = ""
            remove(join(join(path_O, dir_O), name+compl+"_data.txt"))
            remove(join(join(path_O, dir_O), name+compl+"_res.txt"))
    
    cdef int i 
    if not In.done_here(join(path_O, dir_O), name, detail):
        ### imprime les donn??es de ce graphe
        Out.Output_data(dir_O, name, detail, lst_index, atom_caract, matrice_adja)

        #### Ex??cution sur le ou les ordre(s)
        if Multi_Taille :
            print(name+" commence "+str(datetime.now().time()))
            '''
            # sous_graphe connexe par methode bruteforce
            lst_combi = Combi.gen_combi_brute_range(matrice_adja, min_ordre, max_ordre)
            '''
            # sous_graphes connexes par notre m??thode de parcour d'un arbre de combi de la matrice d'adja
            lst_combi = SSG.subgen(matrice_adja, min_ordre, max_ordre)
            #lst_combi = OSG.subgen_deg_decroiss(matrice_adja, atom_caract, min_ordre, max_ordre, crible)
            
            print(name+" combinaisons finis "+str(datetime.now().time()))
            
            for i in range(max_ordre - min_ordre + 1):
                ordre = min_ordre+i
                detail[1] = ordre
                (dict_isomorph, dict_stat, lst_id, lst_certif, nb_unique) = programm_1(dir_O, name, detail, matrice_adja, atom_caract, lst_combi[i])
                #programm_2(dir_O, name, detail, matrice_adja, atom_caract, lst_id, dict_isomorph)
            
                print(name+" taille "+str(ordre)+" fini "+str(datetime.now().time())+"\n")
            
            print(name+" fini "+str(datetime.now().time())+"\n")
        else : 
            print(name+" commence "+str(datetime.now().time()))
            '''
            # sous_graphe connexe par methode bruteforce
            lst_combi = Combi.gen_combi_brute(matrice_adja, ordre)
            '''
            # sous_graphes connexes par notre m??thode de parcour d'un arbre de combi de la matrice d'adja
            lst_combi = SSG.subgen(matrice_adja, ordre, ordre)
            #lst_combi = OSG.subgen_deg_decroiss(matrice_adja, atom_caract, ordre, ordre, crible)

            print(name+" combinaisons finis "+str(datetime.now().time()))
            
            detail[1] = ordre
            (dict_isomorph, dict_stat, lst_id, lst_certif, nb_unique) = programm_1(dir_O, name, detail, matrice_adja, atom_caract, lst_combi)
            
            #programm_2(dir_O, name, detail, matrice_adja, atom_caract, lst_id, dict_isomorph)
            
            print(name+" fini "+str(datetime.now().time())+"\n")

    return 1    

def programm_1 (dir_O, name, detail, matrice_adja, atom_caract, lst_combi):
    t_cerif = 0 ## test
    t_prep_c = 0 ## test
    t_fill = 0 ## test
    time_temp = time.time()## test
    (dict_isomorph, dict_stat, lst_id, lst_certif, t_cerif, t_prep_c, t_fill) = Iso.combi_iso(matrice_adja, atom_caract, lst_combi, detail[1], t_cerif, t_prep_c, t_fill)
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
    
    # imprime combinaisons
    Out.Output_combi(dir_O, name, detail, lst_id, dict_isomorph)
    # imprime les diagrammes
    Out.Output_diagramme(dir_O, name, detail, lst_id, dict_stat)
    # imprime statistique de l'ordre ??tudi??
    Out.Output_stat(dir_O, name, detail, lst_combi, lst_certif, lst_id, nb_unique)
    # imprime les r??sultats
    Out.Output_result(dir_O, name, detail, lst_certif, lst_id, dict_stat)

    print(name+" sortie fini "+str(datetime.now().time()))
    return (dict_isomorph, dict_stat, lst_id, lst_certif, nb_unique)

'''
def programm_2 (dir_O, name, detail, matrice_adja, atom_caract, lst_id, dict_isomorph):
    # MCIS/ G??n??ration des donn??es pour calculer le taux de chaleur
    if detail[2] == 0:
        for i in range(3):
            detail[2] = i+1
            Tab_sim = Simil.mcis_algo(detail, matrice_adja, atom_caract, lst_id, dict_isomorph)
            # imprime les matrices de chaleur
            Out.Output_sim(dir_O, name, detail, Tab_sim)
            print(name+" mcis "+str(detail[2])+" fini "+str(datetime.now().time()))
        detail[2] = 0
    else :
        Tab_sim = Simil.mcis_algo(detail, matrice_adja, atom_caract, lst_id, dict_isomorph)
        # imprime les matrices de chaleur
        Out.Output_sim(dir_O, name, detail, Tab_sim)
        print(name+" mcis fini "+str(datetime.now().time()))
'''
