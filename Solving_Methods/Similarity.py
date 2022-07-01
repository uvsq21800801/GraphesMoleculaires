import networkx as nx
from Solving_Methods import nx_Graphs as nxg

'''
######## Etude de la similarité des sous-graphes dans un jeux de combinaison d'un graphe

Perspectives : Généralisé l'étude sur un jeux de motif avec matrice d'adjacences et caractéristiques atomiques associées
'''

# Fonction calculant les valeurs de la table de chaleur sur un ensemble de combinaison unique
#
# Entrées: nombre de motifs, tableau des graphes asoociés et parametre d'exécution
#
# Sortie: Tableau [x] [y]

def Similarity_sansMcis(tab_sg, detail):
    nb = len(tab_sg)
    
    # tableau de sortie
    Tab_sim = [[None for y in range(nb)] for x in range(nb)]
    
    # boucle sur tous les duo à évaluer selon la méthode choisie
    for i in range(nb):
        for j in range(nb):
            if j>i and detail[2] == 1 :
                Tab_sim[i][j] = distance_edition(tab_sg[i], tab_sg[j])
                Tab_sim[j][i] = Tab_sim[i][j]
            
    # print(Tab_sim)
    return Tab_sim


# Fonction calculant les valeurs de la table de chaleur sur un ensemble de combinaison unique
#
# Entrées: nombre de motifs, tableau des graphes associés, semi-matrice des MCIS et parametre d'exécution
#
# Sortie: Tableau [x] [y]

def Similarity_avecMcis(tab_sg, tab_mcis, detail):
    nb = len(tab_sg)
    
    # tableau de sortie
    Tab_sim = [[None for y in range(nb)] for x in range(nb)]
    
    # boucle sur tous les duo à évaluer selon la méthode choisie et 
    for i in range(nb):
        for j in range(nb):
            if i>j:
                if detail[2] == 2 :
                    Tab_sim[i][j] = sim_raymond(tab_mcis[i-1][j], tab_sg[i], tab_sg[j])
                    Tab_sim[j][i] = Tab_sim[i][j]
                if detail[2] == 3 :
                    Tab_sim[i][j] = sim_barth(tab_mcis[i-1][j], tab_sg[i], tab_sg[j], i, j)
                    Tab_sim[j][i] = sim_barth(tab_mcis[i-1][j], tab_sg[j], tab_sg[i], j, i)
            if i == j :
                Tab_sim[i][i] = 1
    return Tab_sim

# Distance d'édition
def distance_edition(sgA, sgB):
    return nx.graph_edit_distance(sgA,sgB,node_match=nxg.colors_match,edge_match=nxg.edge_col_match)

# Metrique de Raymond symétrique
def sim_raymond(g_mcis, g_a, g_b):
    if g_mcis == -1 :
        return 0
    else:
        # calcul similarité de raymond
        res = g_mcis.number_of_edges() + g_mcis.number_of_nodes()
        res *= res
        val_a = g_a.number_of_edges()+g_a.number_of_nodes()
        val_b = g_b.number_of_edges()+g_b.number_of_nodes()
        res /= (val_a*val_b)
        return res

# Metrique de Raymond asymétrique
def sim_barth(g_mcis, g_a, g_b, x , y):
    # cas de la comparaison avec soi-même
    if (x==y):
        return 1
    # cas où il n'y a pas de mcis
    elif g_mcis == -1 :
        return 0
    else :
        # calcul similarité de raymond
        res = g_mcis.number_of_edges() + g_mcis.number_of_nodes()
        val_a = g_a.number_of_edges()+g_a.number_of_nodes()
        val_b = g_b.number_of_edges()+g_b.number_of_nodes()
        if (x>y):
            res /= min(val_a,val_b)
        else:
            res /= max(val_a,val_b)
        return res

# Construit le tableau des MCIS 
#   forme triangulaire : pour t[i][j] existe, i >= j
#   les indices des graphes sont décrémentés de 1 dans la première dimension
#
# Entrées : tableau de graphes
#
# Sortie : tableau triangulaire des MCIS

def tab_mcis(tab_sg):
    nb = len(tab_sg)
    tab_mcis = [[None for y in range(x+1)] for x in range(nb-1)]
    
    for x in range(nb-1):
        for y in range(x+1):
            tab_mcis[x][y] = nxg.construct_mcis(tab_sg[x+1], tab_sg[y])
    
    return tab_mcis