import networkx as nx
import random
import nx_Graphs as nxg

# Fonction regroupant l'ensemble de la ou des clique(s) maximum(s) (unique ou multiple)
#
# Entrées: Graphe étudié, ensemble des clique maximum connus et les ensembles de sommets R, P et X
# 			R : ensemble des sommets de la clique courante
# 			P : ensemble des sommets candidats à l'ajout dans la clique (voisin de tous les sommets déjà considérés)
# 			X : ensemble des sommets exclus (déjà traité ou appartenant déjà à une clique maximale)
#
# Sortie: liste des cliques maximales sur le graphe de compatibilité et les ensembles P et X (récursivité)

def BronKerborsch(Gc, maxClique, R, P, X):
	if len(P) == 0 and len(X) == 0 :
		if len(maxClique) == 0 :
			maxClique.append(R.copy())
		elif len(R) > len(maxClique[0]) :
			maxClique.insert(0,R.copy())
		else :
			i = 0
			while i < len(maxClique) and len(maxClique[i]) > len(R):
				i += 1
			maxClique.insert(i,R.copy())
		#print("tab :", maxClique)
	else :
		T = P|X
		u = random.choice(list(T))
		Nu = set(nx.neighbors(Gc, u))
		#print('u',u,Nu)
		V = P-Nu
		for v in V:
			Nv = set(nx.neighbors(Gc, v))
			#print('v',v,Nv)
			maxClique = BronKerborsch(Gc, maxClique, R|set([v]), P&Nv, X&Nv)
			P.discard(v)
			X = X|set([v])
	return maxClique

# Fonction regroupant l'ensemble de la ou des clique(s) maximum(s) (unique ou multiple)
#   Utilisant l'heuristique de Johnston adaptée avec les voisinages par arêtes strong ou floppy

### à voir



# Fonction recherchant dans la clique, la plus grande sous-clique possédant un arbre couvrant d'arêtes s ou f.
#
# Entrées : Graphe de compatibilité labélisé sur les arêtes {s, f, w} et clique (liste des sommets)
#
# Sortie : Renvoie la plus grande clique possèdant un arbre couvrant d'arêtes labélisées s ou f dans la clique en entrée

def arbre_strong(Gc, clique):
	res = set()
	# ensemble des sommets à parcourir et arbre formé
	Next = clique.copy()
	Arbre = set()
	# sélection du sommet de départ
	u = Next.pop()
	Arbre.add(u)
	# parcours en profondeur récursif
	marquage_strong(Gc, Arbre, Next, u)
	# tant que l'arbre parcouru est plus grand que le précédent alors il le remplace
	while len(res)<len(Arbre):
		res = Arbre.copy()
		if len(Next) > len(res):
			u = Next.pop()
			Arbre = set()
			Arbre.add(u)
			marquage_strong(Gc, Arbre, Next, u)
	return res

# Fonction de marquage par un parcours en profondeur sur les arêtes s ou f
#
# Entrées : Graphes de compatibilité labélisé sur les arêtes {s, f, w}, ensemble des sommets à parcourir et sommet courant
#
# fonction récursive

def marquage_strong(Gc, Arbre, Next, u):
	V = set(nx.neighbors(Gc,u))&Next
	for v in V:
		if Gc[u][v]['label'] in "sf" and v in Next:
			Next.discard(v)
			Arbre.add(v)
			marquage_strong(Gc, Arbre, Next, v)

# Fonction qui renvoie la clique de plus grande taille possédant un arbre couvrant d'arêtes s ou f
#
# Entrées : Graphes de compatibilité labélisé sur les arêtes {s, f, w} et ensemble des cliques maximales
#
# Sortie : renvoie l'ensemble de sommets constituant la clique maximum ayant un arbre couvrant d'arête s ou f

def MaxStrongClique(Gc, MaxClique):
	res = set()
	# sur les cliques maximales, extrait des arbres d'arêtes s ou f
	for clique in MaxClique :
		if len(clique) > len(res):
			tmp = arbre_strong(Gc, clique)
			if len(tmp) > len(res):
				res = tmp
		else :
# renvoie la plus grande clique possédant un arbre couvrant d'arêtes s ou f
			return res

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
B = nxg.create_digraph(mB, atB)

#Construction LineGraphes


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


'''
G = nx.DiGraph([(1,2),(1,5),(2,3),(2,5),(3,4),(4,5),(4,6)])

'''
