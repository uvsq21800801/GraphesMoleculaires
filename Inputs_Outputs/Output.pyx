from os import listdir, remove
from os.path import isfile, join
import matplotlib
import matplotlib.pyplot as plt

import numpy as np

############################## Principale ##############################

# données de base redirigées dans nos structures


def Output_data(dir_O, detail, lst_index, atom_caract, matrice_adja, nb_conf):
    # selon les paramètres
    if detail[0] == True:
        compl = "_NoH"
    else:
        compl = ""

    if detail[3] == True:
        compl += "_Cr"

    compl += "_conf"+str(nb_conf)

    # création du fichier de sortie
    fpath = "Inputs_Outputs/Place_Output_here/"+dir_O+'/'
    filename = dir_O+compl+"_data.txt"
    if isfile(join(fpath, filename)):
        remove(join(fpath, filename))
    f = open(fpath+filename, 'w')

    f.write("Indice IndiceOld Caract_atome\n")
    cdef int i 
    for i in range(len(lst_index)):
        f.write(str(i)+' '+str(lst_index[i])+' '+str(atom_caract[i])+'\n')

    f.write("Matrice Adjacence\n")
    r = int(len(matrice_adja))
    cdef int j
    for i in range(r):
        s = ''
        for j in range(r):
            s += str(matrice_adja[i][j])+'  '
        f.write(s+'\n')
    f.close()

# données pour le diagramme des nombre d'occurence et taux de recouvrement


def Output_diagramme(dir_O, name, detail, lst_id, dict_stat, nb_conf, ordre):
    # selon les paramètres
    compl = "conf"+str(nb_conf)+'_'+str(ordre)

    if detail[0] == True:
        compl+="_H"
    
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
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()

    occur = np.array(plot_occur)
    occur = occur.astype(float)
    recouv = np.array(plot_recouv)
    recouv = recouv.astype(float)

    # Histogrammes
    ax1.hist(occur, plot_indice, c="red")
    ax2.hist(recouv, plot_indice, c="blue")
    '''# Nuage de points
    ax1.scatter(plot_indice, occur,s=3,c="red")
    ax2.scatter(plot_indice, recouv,s=3,c="blue")
    '''

    ax1.set_xlabel("Motifs triés par nombre d'occurrence croissante")
    ax1.set_ylabel("Nombre d'occurrence d'un motif", c="red")
    ax2.set_ylabel("Taux de recouvrement du motif", c="blue")
    
    #plt.title("")
    #plt.show()  
    plt.savefig(fpath+name+compl+"_graph.png")

    plt.clf()

    occup = np.array(plot_occup)
    occup = occup.astype(float)
    plt.scatter(plot_indice, occup,s=3)
    plt.xlabel("Motifs triés par nombre d'occurrence croissante")
    plt.ylabel("Taux d'occupation d'un motif")
    plt.savefig(fpath+name+compl+"_occup.png")
    plt.clf()

# ajoute les données supplémentaires


def Output_stat(dir_O, name, detail, lst_combi, lst_certif, lst_id, nb_unique, nb_conf, ordre):
    # selon les paramètres
    compl = "_conf"+str(nb_conf) 
    if detail[0] == True:
        compl += "_H"
    
    if detail[3] == True:
        compl += "_Cr" 

    # ouverture du fichier de sortie
    fpath = "Inputs_Outputs/Place_Output_here/"+dir_O+'/'
    filename = name+compl+"_data.txt"
    if isfile(join(fpath, filename)):
        f = open(fpath+filename, 'a')

        f.write("\nOrdre : "+str(ordre)+'\n')
        f.write("Nombre de sous-graphes connexes : "+str(len(lst_combi))+'\n')
        f.write("Nombre de certificats différents : "+str(len(lst_certif))+'\n')
        f.write("Nombre de motifs uniques :"+str(nb_unique)+'\n')
        f.write("Indices triés :\n"+str_liste(lst_id, ' ')+'\n')
        f.close() 

# données de résultats sous un format pouvant rentrer dans un tableaux excel

# écrit le fichier [XXX]_res.txt
def Output_result(dir_O, name, detail, lst_certif, lst_id, dict_stat, nb_conf, ordre):
    # selon les paramètres
    compl = "_conf"+str(nb_conf) 
    if detail[0] == True:
        compl += "_H"
    
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
            f.write(str(ordre)+' '+str(indice)+' '+str(i)+' '+str(tmp1[0])+' '+str(
                tmp1[2])+' \''+str_liste(tmp1[1],'')+' \''+str(tmp1[3])+' \''+lst_certif[indice].hex()+'\n')
        else:
            f.write(str(ordre)+' '+str(indice)+' '+str(i)+' '+str(tmp1[0])+' '+str(
                tmp1[2])+' \''+str_liste(tmp1[1],'')+' \''+str(tmp1[3])+' \''+lst_certif[indice].hex()+'\n')
        i += 1
    f.close()

# données des listes de combinaisons


def Output_combi(dir_O, name, detail, lst_id, dict_isomorph, nb_conf, ordre):
    # selon les paramètres
    compl = "_conf"+str(nb_conf)+'_'+str(ordre)
    if detail[0] == 1:
        compl += "_H"
    
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


def Output_sim(dir_O, name, detail, lst_id, Tab_sim, nb_conf, ordre):
    # selon les paramètres
    compl = "_conf"+str(nb_conf)+'_'+str(detail[2])
    if detail[0] == True:
        compl += "_H"
    
    if detail[3] == True:
        compl += "_Cr" 

    nb = 1
    # création du fichier de sortie
    fpath = "Inputs_Outputs/Place_Output_here/"+dir_O+'/'
    filename = name+compl+"_sim_ord_"+str(ordre)+'_'+str(nb)+".txt"
    while isfile(join(fpath, filename)):
        nb += 1
        filename = name+compl+"_sim_ord_"+str(ordre)+'_'+str(nb)+".txt"
    f = open(fpath+filename, 'w')
    
    #print(lst_id)
    for i in range(len(Tab_sim)):
        s = ""
        for j in range(len(Tab_sim)):
            s += str(Tab_sim[i][j])+' '
            #print(' ')
        f.write(s+'\n')
    f.close()
    
    if detail[2] == 1:
        cmap = "hot_r"
    else:
        cmap = "hot"
        
    plt.clf()
    
    
    fig, ax = plt.subplots()
    
    fig.set_size_inches(12.8,9.6)
        
    im = ax.imshow(Tab_sim, cmap=cmap, interpolation='nearest')
    
    cbarlabels = ["distance d'édition", "similarité Raymond", "similarité Raymond asymétrique"]
    cbarlabel = cbarlabels[detail[2]-1]
    
    cbar = ax.figure.colorbar(im, ax=ax, cmap=cmap)
    cbar.ax.set_ylabel(cbarlabel, rotation=-90, va="bottom", fontsize=16)
    
    step = int(len(lst_id)/20) + 1
    
    lst_id[::step]
    np.arange(0,len(lst_id),step)

    ax.set_xticks(np.arange(0,len(lst_id),step), labels=lst_id[::step], fontsize=12)
    ax.set_yticks(np.arange(0,len(lst_id),step), labels=lst_id[::step], fontsize=12)
    ax.tick_params(top=True, labeltop=True, bottom=False, labelbottom=False)

    ax.xaxis.set_label_position("top")
    if detail[2] == 3:
        ax.set_xlabel("MCIS/maxG : Isomorphisme si 1", fontsize=16)
        ax.set_ylabel("MCIS/minG : Inclusion si 1", fontsize=16)
    
    #plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
    
    if len(lst_id) < 20 :
        for i in range(len(lst_id)):
            for j in range(len(lst_id)):
                fontsize = 10
                round_size = 2
                val = round(Tab_sim[i][j],round_size)
                ax.text(j,i, val, ha="center", va="center", color='b', fontsize=fontsize)
    
    titlecompl= str(nb)
    if detail[0] == 1:
        titlecompl = "H "+titlecompl
    ax.set_title("Similarité entre motifs de "+name+" de taille "+str(ordre)+" "+titlecompl, fontsize=20)
    fig.tight_layout()
    plt.savefig(fpath+name+compl+"_heatmap_ord_"+str(ordre)+'_'+str(nb)+".png")   
    plt.clf()  

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