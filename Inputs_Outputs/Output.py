from os import listdir, remove
from os.path import isfile, join
import re
import matplotlib.pyplot as plt
import numpy as np

############################## Principale ##############################

# impression des resultats pour un graphe
def res_output(name, min_ordre, lst_ordre, lst_combi, lst_certif, lst_unique, dict_isomorph, dict_stat):
    for i in range(int(len(lst_ordre))):
        Output_diagramme(name, i, min_ordre, lst_ordre, dict_stat)
    Output_result(name, min_ordre, lst_certif, lst_ordre, dict_stat)
    Output_combi(name, lst_ordre, dict_isomorph)
    Output_stat(name, min_ordre, lst_combi, lst_certif, lst_ordre, lst_unique)

############ Isomorphisme

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
    # pour tous les nombre d'occurrence trié
    for k in sorted(d.keys()) :
        # récupère la liste des couples [indice, taux]
        tmp = d.get(k)
        # pour tous les couples triés (ATTENTION : est-ce que c'est bien trié?)
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

######## Similarité

# données de similarité de "motifs"
def res_sim(name, min_ordre, max_ordre, Tab_sim):

    for h in range(max_ordre-min_ordre+1):
    
        # création du fichier de sortie
        fpath = "Inputs_Outputs/Place_Output_here/"
        filename = name+"_sim_ord_"+str(h+min_ordre)+".txt"
        if isfile(join(fpath, filename)):
            remove(join(fpath, filename))
        f = open(fpath+filename, 'w')
        plt.imshow(Tab_sim[h], cmap='hot_r', interpolation='nearest')
        #plt.show()
        plt.savefig(fpath+name+"_heatmap_ord_"+str(h+min_ordre)+".png")
        for i in range(len(Tab_sim[h])):
            

            s =""

            for j in range(len(Tab_sim[h])):
                s+=str(Tab_sim[h][i][j])+' '
                print(' ')

            f.write(s+'\n')
        f.close()
