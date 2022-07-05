from os import listdir, remove
from os.path import isfile, join
import matplotlib.pyplot as plt
import numpy as np

############################## Principale ##############################

# données de base redirigées dans nos structures


def Output_data(dir_O, name, detail, lst_index, atom_caract, matrice_adja):
    # selon les paramètres
    if detail[0] == 1:
        compl = "_H"
    else:
        compl = ""

    if detail[3] == True:
        compl += "_Cr" 

    # création du fichier de sortie
    fpath = "Inputs_Outputs/Place_Output_here/"+dir_O+'/'
    filename = name+compl+"_data.txt"
    if isfile(join(fpath, filename)):
        remove(join(fpath, filename))
    f = open(fpath+filename, 'w')

    f.write("Indice IndiceOld Caract_atome\n")
    for i in range(len(lst_index)):
        f.write(str(i)+' '+str(lst_index[i])+' '+str(atom_caract[i])+'\n')

    f.write("Matrice Adjacence\n")
    r = int(len(matrice_adja))
    for i in range(r):
        s = ''
        for j in range(r):
            s += str(matrice_adja[i][j])+'  '
        f.write(s+'\n')
    f.close()

# données pour le diagramme des nombre d'occurence et taux de recouvrement


def Output_diagramme(dir_O, name, detail, lst_id, dict_stat):
    # selon les paramètres
    if detail[0] == 1:
        compl = '_'+str(detail[1])+"_H"
    else:
        compl = '_'+str(detail[1])

    if detail[3] == True:
        compl += "_Cr" 

    # création du fichier de sortie
    fpath = "Inputs_Outputs/Place_Output_here/"+dir_O+'/'
    filename = name+compl+".txt"
    if isfile(join(fpath, filename)):
        remove(join(fpath, filename))
    f = open(fpath+filename, 'w')

    f.write("ordonne nbOccur taux indice\n")
    # pour les indices des la liste (trié au préalable)
    plot_indice = []
    plot_occur = []
    plot_recouv = []
    plot_occup = []
    for i in range(len(lst_id)):
        # récupère les stats
        tmp = dict_stat.get(lst_id[i])
        f.write(str(i)+' '+str(tmp[0])+' '+str(tmp[2])+' '+str(lst_id[i])+'\n')
        plot_indice.append(int(i))
        plot_occur.append(float(tmp[0]))
        plot_recouv.append(float(tmp[2]))
        plot_occup.append(float(tmp[3]))
    f.close()


    plt.clf()
    occur = np.array(plot_occur)
    occur = occur.astype(np.float)
    plt.scatter(plot_indice, occur,s=3)
    #plt.title("")
    plt.xlabel("Indices triés par occurrence croissance")
    plt.ylabel("Nombre d'occurrence d'un motif")
    #plt.show()  
    plt.savefig(fpath+name+compl+"_occur.png")

    plt.clf()
    recouv = np.array(plot_recouv)
    recouv = recouv.astype(np.float)
    
    plt.scatter(plot_indice, recouv,s=3)
    
    #plt.title("")
    plt.xlabel("Indices triés par occurrence croissance")
    plt.ylabel("Taux de recouvrement d'un motif")
    #plt.show()  
    plt.savefig(fpath+name+compl+"_recouv.png")
    plt.clf()

    occup = np.array(plot_occup)
    occup = occup.astype(np.float)
    plt.scatter(plot_indice, occup,s=3)
    plt.xlabel("Indices triés par occurrence croissance")
    plt.ylabel("Taux d'occupation d'un motif")
    plt.savefig(fpath+name+compl+"_occup.png")
    plt.clf()

# ajoute les données supplémentaires


def Output_stat(dir_O, name, detail, lst_combi, lst_certif, lst_id, nb_unique):
    # selon les paramètres
    if detail[0] == 1:
        compl = "_H"
    else:
        compl = ""

    if detail[3] == True:
        compl += "_Cr" 
    
    # ouverture du fichier de sortie
    fpath = "Inputs_Outputs/Place_Output_here/"+dir_O+'/'
    filename = name+compl+"_data.txt"
    if isfile(join(fpath, filename)):
        f = open(fpath+filename, 'a')

        f.write("\nOrdre : "+str(detail[1])+'\n')
        f.write("Nombre de sous-graphes connexes : "+str(len(lst_combi))+'\n')
        f.write("Nombre de certificats différents : "+str(len(lst_certif))+'\n')
        f.write("Nombre de motifs uniques :"+str(nb_unique)+'\n')
        f.write("Indices triés :\n"+str_liste(lst_id, ' ')+'\n')
        f.close() 

# données de résultats sous un format pouvant rentrer dans un tableaux excel

# écrit le fichier [XXX]_res.txt
def Output_result(dir_O, name, detail, lst_certif, lst_id, dict_stat):
    # selon les paramètres
    if detail[0] == 1:
        compl = "_H"
    else:
        compl = ""

    if detail[3] == True:
        compl += "_Cr" 
    
    # création du fichier de sortie
    fpath = "Inputs_Outputs/Place_Output_here/"+dir_O+'/'
    filename = name+compl+"_res.txt"
    if not isfile(join(fpath, filename)):
        f = open(fpath+filename, 'w')
        f.write("ordre id_c id_t nb_occurrence taux_recouvrement recouvrement taux_occupation certificat\n")
    else :
        f = open(fpath+filename, 'a')
        
    i = 0
    for i in range(len(lst_id)):
        indice = lst_id[i]
        tmp1 = dict_stat.get(indice)
        if tmp1[0] > 1:
            f.write(str(detail[1])+' '+str(indice)+' '+str(i)+' '+str(tmp1[0])+' '+str(
                tmp1[2])+' \''+str_liste(tmp1[1],'')+' \''+str(tmp1[3])+' \''+lst_certif[indice].hex()+'\n')
        else:
            f.write(str(detail[1])+' '+str(indice)+' '+str(i)+' '+str(tmp1[0])+' '+str(
                tmp1[2])+' \''+str_liste(tmp1[1],'')+' \''+str(tmp1[3])+' \''+lst_certif[indice].hex()+'\n')
        i += 1
    f.close()

# données des listes de combinaisons


def Output_combi(dir_O, name, detail, lst_id, dict_isomorph):
    # selon les paramètres
    if detail[0] == 1:
        compl = '_'+str(detail[1])+"_H"
    else:
        compl = '_'+str(detail[1])
    
    if detail[3] == True:
        compl += "_Cr" 
    
    # création du fichier de sortie
    fpath = "Inputs_Outputs/Place_Output_here/"+dir_O+'/'
    filename = name+compl+"_combi.txt"
    if isfile(join(fpath, filename)):
        remove(join(fpath, filename))
    f = open(fpath+filename, 'w')

    f.write("identifiant liste_combi \n")
    for i in range(len(lst_id)):
        tmp = dict_isomorph.get(lst_id[i])
        #       identifiant    liste_combi
        f.write(str(lst_id[i])+' '+str_liste(tmp[0],'')+' '+str_matrice_combi(tmp)+'\n')

    f.close()

# Similarité

# données de similarité de "motifs" et matrice de chaleur


def Output_sim(dir_O, name, detail, Tab_sim):
    # selon les paramètres
    if detail[0] == 1:
        compl = "_H_"+str(detail[2])
    else:
        compl = "_"+str(detail[2])
    
    if detail[3] == True:
        compl += "_Cr" 

    # création du fichier de sortie
    fpath = "Inputs_Outputs/Place_Output_here/"+dir_O+'/'
    filename = name+compl+"_sim_ord_"+str(detail[1])+".txt"
    if isfile(join(fpath, filename)):
        remove(join(fpath, filename))
    f = open(fpath+filename, 'w')
    plt.clf()
    plt.xlabel("Indices des motifs triés dans l'ordre d'occurrence")
    plt.ylabel("Indices des motifs triés dans l'ordre d'occurrence")
    plt.imshow(Tab_sim, cmap='hot', interpolation='nearest')
    # plt.show()
    plt.savefig(fpath+name+compl+"_heatmap_ord_"+str(detail[1])+".png")
    plt.clf()
    for i in range(len(Tab_sim)):
        s = ""
        for j in range(len(Tab_sim)):
            s += str(Tab_sim[i][j])+' '
            #print(' ')
        f.write(s+'\n')
    f.close()

# Fonctions utiles


def str_liste(l, sep):
    s = ''
    for i in range(len(l)):
        s += str(l[i])+sep
    return s


def str_matrice(m):
    s = '[ '
    for l in m:
        s += str_liste(l,' ')
    return s+']'

def str_matrice_combi(m):
    s = '[ '
    for l in m:
        s += str_liste(l,'') +' '
    return s+']'