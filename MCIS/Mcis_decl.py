from os import listdir, remove
from os.path import isfile, join
import re
from signal import valid_signals
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import scipy as sp

# pour vérifier la coloration de noeuds
def colors_match(n1_attrib,n2_attrib):
    '''returns False if either does not have a color or if the colors do not match'''
    try:
        return n1_attrib['color']==n2_attrib['color']
    except KeyError:
        print('pas normal')
        return False

# pour vérifier la coloration d'arrêtes (pas sure que c'est au point)
def edge_col_match(n1_attrib,n2_attrib):
    '''returns False if either does not have a color or if the colors do not match'''
    try:
        return n1_attrib['color']==n2_attrib['color']
    except KeyError:
        print('pas normal')
        return False

# vieille fonction pour retrouver le MCIS de deux graphes
# (inachevée et sera potentiellement supprimée si elle ne sert à rien)
def sim_raymond(a_adja, a_car, b_adja, b_car):
    # declaration de graph a et graph b
    g_a = nx.Graph()
    g_b = nx.Graph()

    # affichages
    #print(a_car)
    #print(a_adja)

    
    a_len = int(len(a_adja))
    for i in range(a_len):
        splitted = a_car[i].split()
        color = splitted[0]
        g_a.add_nodes_from([(i, {"color": color})])
        for j in range(a_len):
            if(a_adja[i][j] == 1):
                g_a.add_edges_from([(i, j)] , color="blue" )
            if(a_adja[i][j] == 2):
                g_a.add_edges_from([(i, j)] , color="red" )

    b_len = int(len(b_adja))
    for i in range(b_len):
        splitted = b_car[i].split()
        color = splitted[0]
        g_b.add_nodes_from([(i, {"color": color})])
        for j in range(b_len):
            if(b_adja[i][j] == 1):
                g_b.add_edges_from([(i, j)] , color="blue" )
            if(b_adja[i][j] == 2):
                g_b.add_edges_from([(i, j)] , color="red")


    # MCIS
    
    ismags = nx.isomorphism.ISMAGS(g_a,g_b,node_match=colors_match, edge_match=edge_col_match)
    largest_common_sub = list(ismags.largest_common_subgraph())
    
    # affichages
    #  print('classic')
    #  print(g_a.nodes)
    #  print(g_b)
    #  print('ismag:')
    #  print(ismags.graph)
    #  print(largest_common_sub)
    
    if(largest_common_sub != []):
        #  
        ls_nodes_mcis = largest_common_sub[0].keys()
        g_mcis = g_a.subgraph(ls_nodes_mcis)
        #  print('newg')
        #  print(g_mcis)

        # calcul simmilarité de raymond
        res = g_mcis.number_of_edges() + g_mcis.number_of_nodes()
        res *= res
        res /= ((g_a.number_of_edges()+g_a.number_of_nodes())*
                (g_b.number_of_edges()+g_b.number_of_nodes()))
        #  print(res)
        return res


    #affichages
    #print(g_a)
    #print(g_b)
    #print(largest_common_subgraph)

    # cas ou il n'y à pas de mcis
    return 0


# vieille fonction pour retrouver le MCIS de deux graphes
# (inachevée et sera potentiellement supprimée si elle ne sert à rien)
def sim_barth(a_adja, a_car, b_adja, b_car, x , y):

    # declaration de graph a et graph b
    g_a = nx.Graph()
    g_b = nx.Graph()

    #print(a_car)
    #print(a_adja)

    
    a_len = int(len(a_adja))
    for i in range(a_len):
        splitted = a_car[i].split()
        color = splitted[0]
        g_a.add_nodes_from([(i, {"color": color})])
        for j in range(a_len):
            if(a_adja[i][j] == 1):
                g_a.add_edges_from([(i, j)] , color="blue" )
            if(a_adja[i][j] == 2):
                g_a.add_edges_from([(i, j)] , color="red" )

    # cas où on à la comparaison d'un graphe avec lui-même
    if (x==y):
        return 1#g_a.number_of_nodes()

    b_len = int(len(b_adja))
    for i in range(b_len):
        splitted = b_car[i].split()
        color = splitted[0]
        g_b.add_nodes_from([(i, {"color": color})])
        for j in range(b_len):
            if(b_adja[i][j] == 1):
                g_b.add_edges_from([(i, j)] , color="blue" )
            if(b_adja[i][j] == 2):
                g_b.add_edges_from([(i, j)] , color="red")


    # MCIS
    
    ismags = nx.isomorphism.ISMAGS(g_a,g_b,node_match=colors_match, edge_match=edge_col_match)
    largest_common_sub = list(ismags.largest_common_subgraph())


    #  print('classic')
    #  print(g_a.nodes)
    #  print(g_b)
    #  print('ismag:')
    #  print(ismags.graph)
    #  print(largest_common_sub)



    if(largest_common_sub != []):
        #  
        ls_nodes_mcis = largest_common_sub[0].keys()
        g_mcis = g_a.subgraph(ls_nodes_mcis)
        #  print('newg')
        #  print(g_mcis)

        # calcul simmilarité de raymond
        res = g_mcis.number_of_edges() + g_mcis.number_of_nodes()
        #res *= res
        val_a = g_a.number_of_edges()+g_a.number_of_nodes()
        val_b = g_b.number_of_edges()+g_b.number_of_nodes()
        if (x>y):
            if (val_a > val_b):
                res /= val_b
            else:
                res /= val_a
        else:
            if (val_a <= val_b):
                res /= val_b
            else:
                res /= val_a
            
        #  print(res)
        return res


    #affichages
    #print(g_a)
    #print(g_b)
    #print(largest_common_subgraph)

    # cas ou il n'y à pas de mcis
    return 0


# Calcule la simmilarité entre deux graphes.
# Plus le score est élevé, plus il y à besoin d'étapes
# pour passer d'un graphe entré à l'autre
#
# Entrée: Matrice d'adjacence et tableau de caractéristiques
# des deux graphes à comparer
#
# Sortie: Score de simmilarité
def simmilarite(a_adja, a_car, b_adja, b_car):
    # declaration de graph a et graph b
    g_a = nx.Graph()
    g_b = nx.Graph()

    '''affichages'''
    #print(a_car)
    #print(a_adja)

    # création d'un dictionnaire à couleurs


    # génération des deux graphes colorés
    a_len = int(len(a_adja))
    for i in range(a_len):
        splitted = a_car[i].split()
        col = splitted[0]
        g_a.add_node(i)
        g_a.nodes[i]['color'] = col
        #print(g_a.nodes[i])
        #print(g_a)
        for j in range(a_len):
            #g_a.add_edge(i,j)
            if(a_adja[i][j] == 1):
                g_a.add_edge(i,j, color = 'blue')
                #g_a[i][j]['color'] = "blue"

            if(a_adja[i][j] == 2):
                g_a.add_edge(i,j, color = 'red')
                #g_a[i][j]['color'] = "red"

            #print(g_a[i][j])

    #print('space ')
    b_len = int(len(b_adja))
    for i in range(b_len):
        splitted = b_car[i].split()
        col = splitted[0]
        g_b.add_node(i)
        g_b.nodes[i]['color'] = col
        
        #print(g_b.nodes[i])
        #print(g_b)
        for j in range(b_len):
            #g_b.add_edge(i,j)
            if(b_adja[i][j] == 1):
                #g_b[i][j]['color'] = "blue"
                g_b.add_edge(i,j, color = 'blue')
            if(b_adja[i][j] == 2):
                #g_b[i][j]['color'] = "red"
                g_b.add_edge(i,j, color = 'red')

            #print(g_b[i][j])
    
    #print(g_a[0])
    #print(g_a[1])


    # simmilarité
    score_sim = nx.graph_edit_distance(g_b,g_a,node_match=colors_match,edge_match=edge_col_match)
    
    #print(score_sim)

    '''
    J'ai une petite suspicion sur le fonctionnement de cette partie
    du programme ou de ce qui est donné en entrée car on ne devrait
    pas obtenir de simmilarité 0 hors de la diagonale. Donc ou;
    - il y à une erreur/ manque de coloration ici
    - les sous-graphes donnés en entrée ont des isomorphes entre eux
    '''

    return score_sim