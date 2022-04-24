from os import listdir, remove
from os.path import isfile, join
import re
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def mcis(a_adja, a_car, b_adja, b_car):
    # declaration de graph a et graph b
    g_a = nx.Graph()
    g_b = nx.Graph()

    print(a_car)
    print(a_adja)

    
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
    ismags = nx.isomorphism.ISMAGS(g_b,g_a)
    largest_common_subgraph = list(ismags.largest_common_subgraph())




    #affichages

    print("Pas encore impémenté le calcul de simmilarité")

    print(g_a)

    print(g_b)

    print(largest_common_subgraph)

    return 0