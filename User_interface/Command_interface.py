# sera une interface de commande si besoin
import sys
sys.path.append('GraphesMoleculaires/Inputs_Outputs')
sys.path.append('GraphesMoleculaires/Solving_Methods')
sys.path.append('GraphesMoleculaires/MCIS')

from Inputs_Outputs import Inputs as In
from Inputs_Outputs import Output as Out
from Solving_Methods import Combinations as Combi
from Solving_Methods import Isomorph as Iso
from Solving_Methods import Statistic as Stat
from Solving_Methods import Similarity as Simil

from os import listdir, remove, mkdir
from os.path import isfile, isdir, join
from datetime import datetime

Multi_Taille = False
Multi_File = False
File_exist = False

def interface():
    ##### Choix des tailles de sous-graphes
    ordre = input("Taille des sous-graphes : ")
    while not type(ordre)==int and not Multi_Taille :
        if ordre == '*':
            Multi_Taille = True
            min_ordre = input("Taille minimum : ")
            while type(min_ordre)!=int or int(min_ordre)<3 :
                min_ordre = input("(Taille minimum) Entrer un nombre cohérent : ")
            max_ordre = input("Taille maximum : ")
            while type(max_ordre)!=int or int(max_ordre) < min_ordre or int(max_ordre)<3:
                max_ordre = input("(Taille maximum) Entrer un nombre cohérent : ")
        ordre = input("(Taille sous-graphes) Entrer un nombre : ")
    

    ##### Fichiers entrés
    fpath_T = "Inputs_Outputs/Place_Trad_file_here/" 
    fpath_B = "Inputs_Outputs/Place_Bonds_file_here/"
    name = input("Nom fichier entré : ")
    filename_T = "trad-atom_"+name+".txt"
    filename_B = "bonds_"+name+".txt"
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
                name = input("Nom fichier entré : ")
                filename_T = "trad-atom_"+name+".txt"
                filename_B = "bonds_"+name+".txt"

    ##### Création dossier de sortie
    path_O = "Inputs_Outputs/Place_Output_here/"
    dir_O = input("Nom sous-dossier sortant : ")
    ### dossier n'existe pas déjà ?
    if not isdir(join(path_O, dir_O)) :
        ### créé le dossier
        mkdir(join(path_O, dir_O))
    
    ##### Options:
    option = input("Retirer les H et déplacer les liaisons H sur donneur :[0|1]:")
    while type(option)!=int and not (option==0 or option==1) :
        option = input("(atome H) Attend 0 ou 1 : ")
    detail = [option, 0]
    
    ###### Lancement de l'execution du programme
    if not Multi_File :
        filenames = [name]
    for filename in filenames:
            ## Extraction des données
            if Multi_File:
                name = In.get_name(filename)
            lst_index = []
            atom_caract = []
            filename_T = In.Inputs_trad_all(option, name, lst_index, atom_caract)
            matrice_adja = []
            filename_B = In.Inputs_bonds_all(option, name, lst_index, matrice_adja)

            ### déjà exécuté?
            if In.done_here(join(path_O, dir_O), name):
                print(name+" déjà fait")
                test = input("Effacer les précédents résultats? :[0|1]:")
                while type(test)!=int and not (test==0 or test==1) :
                    test = input("(Effacer resultats) Attend 0 ou 1:")
                if test==1 :
                    remove(join(join(path_O, dir_O), name+"_data.txt"))
                    remove(join(join(path_O, dir_O), name+"_res.txt"))
            
            if not In.done_here(join(path_O, dir_O), name):
                ### imprime les données de ce graphe
                Out.Output_data(dir_O, name, detail, lst_index, atom_caract, matrice_adja)

                #### Exécution sur le ou les ordre(s)
                if Multi_Taille :
                    print(name+" commence "+str(datetime.now().time()))
                    # sous_graphe connexe par methode bruteforce
                    lst_combi = Combi.gen_combi_brute_range(matrice_adja, min_ordre, max_ordre)
                    print(name+" combinaisons finis "+str(datetime.now().time()))
                    
                    for i in range(max_ordre - min_ordre + 1):
                        ordre = min_ordre+1
                        (dict_isomorph, dict_stat, lst_id, lst_certif, nb_unique, Tab_sim) = programm(dir_O, name, detail, matrice_adja, atom_caract, lst_combi[i], ordre)
                        print(name+" exécution fini "+str(datetime.now().time()))
                    
                        detail[1] = ordre
                        out(dir_O, name, detail, lst_id, lst_combi[i], lst_certif, nb_unique, dict_stat, dict_isomorph, Tab_sim)
                        print(name+" taille "+ordre+" fini "+str(datetime.now().time())+"\n")
                    
                    print(name+" fini "+str(datetime.now().time())+"\n")
                else : 
                    print(name+" commence "+str(datetime.now().time()))
                    # sous_graphe connexe par methode bruteforce
                    lst_combi = Combi.gen_combi_brute(matrice_adja, ordre)
                    print(name+" combinaisons finis "+str(datetime.now().time()))
                    
                    (dict_isomorph, dict_stat, lst_id, lst_certif, nb_unique, Tab_sim) = programm(dir_O, name, detail, matrice_adja, atom_caract, lst_combi, ordre)
                    print(name+" exécution fini "+str(datetime.now().time()))
                    
                    detail[1] = ordre
                    out(dir_O, name, detail, lst_id, lst_combi, lst_certif, nb_unique, dict_stat, dict_isomorph, Tab_sim)
                    print(name+" fini "+str(datetime.now().time())+"\n")
                
    return 0

def programm (dir_O, name, detail, matrice_adja, atom_caract, lst_combi, ordre):
    (dict_isomorph, dict_stat, lst_id, lst_certif) = Iso.combi_iso(matrice_adja, atom_caract, lst_combi, ordre)
    print(name+" isomorph fini "+str(datetime.now().time()))
                        
    # calcul le taux de recouvrement 
    Stat.Taux_recouvert(dict_stat)

    # tri de lst_id par nombre d'occurence et le nombre de motif unique
    Stat.Tri_indice(lst_id, dict_stat)
    nb_unique = Stat.Nombre_unique(lst_id, dict_stat)

    # MCIS/ Génération des données pour calculer le taux de chaleur
    Tab_sim = Simil.mcis_algo(matrice_adja, atom_caract, lst_id, dict_isomorph, ordre)
    print(name+" mcis fini "+str(datetime.now().time()))
    return (dict_isomorph, dict_stat, lst_id, lst_certif, nb_unique, Tab_sim)
    
def out (dir_O, name, detail, lst_id, lst_combi, lst_certif, nb_unique, dict_stat, dict_isomorph, Tab_sim):                    
    # imprime les matrices de chaleur
    Out.Output_sim(dir_O, name, detail, Tab_sim)
    # imprime les diagrammes
    Out.Output_diagramme(dir_O, name, detail, lst_id, dict_stat)
    # imprime combinaisons
    Out.Output_combi(dir_O, name, detail, lst_id, dict_isomorph)
    # imprime statistique de l'ordre étudié
    Out.Output_stat(dir_O, name, detail, lst_combi, lst_certif, lst_id, nb_unique)
    # imprime les résultats
    Out.Output_result(dir_O, name, detail, lst_certif, lst_id, dict_stat)
