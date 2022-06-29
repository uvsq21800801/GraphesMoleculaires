import networkx as nx
import nx_Graphs as nxg

########################################################################
########################### Experimentations ###########################
########################################################################

#combinaisons
combi_A = [0,0,1,1,1,1]
combi_B = [1,1,1,0,1,0]

#data
atom_caract = ["O 1","O 2","Si 1","O 3","O 4","Si 2"]
matrice_adja = [[0,0,2,0,0,0],[0,0,2,0,0,0],[0,0,0,2,1,0],[0,0,0,0,0,2],[0,0,1,0,0,2],[0,0,0,0,0,0]]

# extraction données
(mA, atA) = nxg.extract_sub(matrice_adja, atom_caract, combi_A)
print(mA)
print(atA)
(mB, atB) = nxg.extract_sub(matrice_adja, atom_caract, combi_B)

#Construction DiGraphes
A = nxg.create_digraph(mA, atA)
#B = nxg.create_digraph(mB, atB)
print(A.nodes(data=True))
print(A.edges)

#Construction LineGraphes
lA = nx.line_graph(A, create_using=nx.DiGraph)
print(lA.nodes(data=True))
print(lA.edges)
#lB = nxg.create_line_digraph(B)
#print(lB.nodes(data=True))


#Abis = nxg.inverse_line_digraph(lA)

'''
#Construction du graphe de compatibilité
(Gc, nodes_comp) = nxg.graph_compatibility(A,B)

nxg.print_adj_compatib(Gc, nodes_comp, 1)

#Recherche des cliques maximales possédant un arbre couvrant fort (à opti)
MaxClique = BronKerborsch(Gc, [], set(), set(range(len(Gc))), set())
print(MaxClique)

#Récupération des sommets de la clique maximale avec arbre couvrant fort
MCIS_nodes = MaxStrongClique(Gc, MaxClique)
print(MCIS_nodes)

#Construction du MCCIS sur le Graphe de compatibilité des LineDiGraphes
C = Gc.subgraph(MCIS_nodes)
MCIS_0 = nxg.Mcis_by_compatibility(mA, atA, nodes_comp, MCIS_nodes, 0)
MCIS_1 = nxg.Mcis_by_compatibility(mB, atB, nodes_comp, MCIS_nodes, 1)

print(MCIS_0.nodes(data=True))
nxg.print_adj(MCIS_0)

#test d'isomorphisme entre les 2 MCCIS issus du duo
IsoM = nx.isomorphism.DiGraphMatcher(MCIS_0, MCIS_1)
print(IsoM.is_isomorphic())

# Convertion en MCCI sur les DiGraphes depuis celui des LineDiGraphes



G = nx.DiGraph([(1,2),(1,5),(2,3),(2,5),(3,4),(4,5),(4,6)])

'''

