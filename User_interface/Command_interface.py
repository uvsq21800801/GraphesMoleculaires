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



def interface():
    Multi_Taille = False
    Multi_File = False
    File_exist = False

    ##### Choix des tailles de sous-graphes
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
    option = input("Retirer les H et déplacer les liaisons H sur donneur [0|1]: ")
    while (option!='0' and option!='1'):
        option = input("(atome H) Attend 0 ou 1 : ")
    detail = [int(option), 0]
    
    ###### Lancement de l'execution du programme
    if not Multi_File :
        filenames = [name]
    for filename in filenames:
            ## Extraction des données
            if Multi_File:
                name = In.get_name(filename)
            lst_index = []
            atom_caract = []
            filename_T = In.Input_trad(detail[0], name, lst_index, atom_caract)
            matrice_adja = []
            filename_B = In.Input_bonds(detail[0], name, lst_index, matrice_adja)

            # test: taille raisonnable?
            
            if (len(atom_caract)<int(input_num)):
                print('Erreur: Taille entrée trop grande')
                print('Taille maximum:'+str(len(atom_caract)))
                break

            ### déjà exécuté?
            if In.done_here(join(path_O, dir_O), name, detail):
                print(name+" déjà fait")
                test = input("Effacer les précédents résultats? :[y|n]: ")
                while (test!='y' and test!='n') :
                    test = input("(Effacer resultats) Attend y ou n: ")
                if test=='y' :
                    if detail[0] == 1 :
                        compl = "_H"
                    else :
                        compl = ""
                    remove(join(join(path_O, dir_O), name+compl+"_data.txt"))
                    remove(join(join(path_O, dir_O), name+compl+"_res.txt"))
            
            if not In.done_here(join(path_O, dir_O), name, detail):
                ### imprime les données de ce graphe
                Out.Output_data(dir_O, name, detail, lst_index, atom_caract, matrice_adja)

                #### Exécution sur le ou les ordre(s)
                if Multi_Taille :
                    print(name+" commence "+str(datetime.now().time()))
                    # sous_graphe connexe par methode bruteforce
                    lst_combi = Combi.gen_combi_brute_range(matrice_adja, min_ordre, max_ordre)
                    print(name+" combinaisons finis "+str(datetime.now().time()))
                    
                    for i in range(max_ordre - min_ordre + 1):
                        ordre = min_ordre+i
                        detail[1] = ordre
                        (dict_isomorph, dict_stat, lst_id, lst_certif, nb_unique) = programm_1(dir_O, name, detail, matrice_adja, atom_caract, lst_combi[i], ordre)
                        programm_2(dir_O, name, detail, ordre, matrice_adja, atom_caract, lst_id, dict_isomorph)
                    
                        print(name+" taille "+str(ordre)+" fini "+str(datetime.now().time())+"\n")
                    
                    print(name+" fini "+str(datetime.now().time())+"\n")
                else : 
                    print(name+" commence "+str(datetime.now().time()))
                    # sous_graphe connexe par methode bruteforce
                    lst_combi = Combi.gen_combi_brute(matrice_adja, ordre)
                    print(name+" combinaisons finis "+str(datetime.now().time()))
                    
                    detail[1] = ordre
                    (dict_isomorph, dict_stat, lst_id, lst_certif, nb_unique) = programm_1(dir_O, name, detail, matrice_adja, atom_caract, lst_combi, ordre)
                    programm_2(dir_O, name, detail, ordre, matrice_adja, atom_caract, lst_id, dict_isomorph)
                    
                    print(name+" fini "+str(datetime.now().time())+"\n")
                
    return 0

def programm_1 (dir_O, name, detail, matrice_adja, atom_caract, lst_combi, ordre):
    (dict_isomorph, dict_stat, lst_id, lst_certif) = Iso.combi_iso(matrice_adja, atom_caract, lst_combi, ordre)
    
    print(name+" isomorph fini "+str(datetime.now().time()))
                        
    # calcul le taux de recouvrement 
    Stat.Taux_recouvert(dict_stat)
    # tri de lst_id par nombre d'occurence et le nombre de motif unique
    Stat.Tri_indice(lst_id, dict_stat)
    nb_unique = Stat.Nombre_unique(lst_id, dict_stat)
    
    # imprime combinaisons
    Out.Output_combi(dir_O, name, detail, lst_id, dict_isomorph)
    # imprime les diagrammes
    Out.Output_diagramme(dir_O, name, detail, lst_id, dict_stat)
    # imprime statistique de l'ordre étudié
    Out.Output_stat(dir_O, name, detail, lst_combi, lst_certif, lst_id, nb_unique)
    # imprime les résultats
    Out.Output_result(dir_O, name, detail, lst_certif, lst_id, dict_stat)

    print(name+" sortie fini "+str(datetime.now().time()))
    return (dict_isomorph, dict_stat, lst_id, lst_certif, nb_unique)
    
def programm_2 (dir_O, name, detail, ordre, matrice_adja, atom_caract, lst_id, dict_isomorph):
    # MCIS/ Génération des données pour calculer le taux de chaleur
    Tab_sim = Simil.mcis_algo(matrice_adja, atom_caract, lst_id, dict_isomorph, ordre)
    # imprime les matrices de chaleur
    Out.Output_sim(dir_O, name, detail, Tab_sim)
    print(name+" mcis fini "+str(datetime.now().time()))
