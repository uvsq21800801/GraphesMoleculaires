import sys
from os import listdir, remove
from os.path import isfile, join
import re
import networkx as nx
import matplotlib.pyplot as plt
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

    filename = name+'_'+ordre+"_combi.txt"

    ##### indice du graphe qui nous intéresse
    indice = input("indice du sous-graphe(indiqué sur les axes de la matrice de chaleur) : ")

    #####
    # 1 - Extraction de la combi  
    #####
    f = open(fpath+"/"+filename, "r")
    lines=f.readlines()
    for i in range(len(lines)):
        splitted = lines[i].split()
        if (splitted[0] == indice):
            combi = splitted[1] 
            break            
    f.close()

    #####
    # 2 - caractéristiques du graphe et matrice adja
    #####
    option = input("Retirer les H et déplacer les liaisons H sur donneur [0|1]: ")
    while (option!='0' and option!='1'):
        option = input("(atome H) Attend 0 ou 1 : ")
    option = int(option)    

    filename1, filename2, lst_index, atom_caract, matrice_adja = Inputs.data_input(option, name)

    #print(matrice_adja)
    #print(atom_caract)
    
    #####
    # 3 - construction du graph avec nx
    #####
    temp = []
    for i in range(len(combi)):
        temp.append(int(combi[i]))
    combi = temp
    new_adja, new_carac = Similarity.extract_sub(matrice_adja, atom_caract, combi, ordre)

    g = nx.Graph()

    g_len = int(len(new_adja))
    for i in range(g_len):
        for j in range(g_len):
            if(new_adja[i][j] == 1):
                g.add_edges_from([(new_carac[i], new_carac[j])] , color="blue" )
            if(new_adja[i][j] == 2):
                g.add_edges_from([(new_carac[i], new_carac[j])] , color="red" )

    edges = g.edges()
    colors = [g[u][v]['color'] for u,v in edges]
    
    #####
    # 4 - dessin
    #####
    nx.draw(g,with_labels = True,edge_color=colors)
    #plt.show()  
    plt.savefig("Inputs_Outputs/Draw_Graph/draw_"+name+"_"+str(ordre)+"_"+str(indice)+".png")
    print("dessin sauvegardé dans Inputs_Outputs/Draw_Graph"
            +"en tant que : "+name+"_"+str(ordre)+"_"+str(indice)+".png")

def main():
    interface()
    
if __name__=="__main__":
    main()
