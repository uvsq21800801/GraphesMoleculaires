import networkx as nx
import random
from Solving_Methods import nx_Graphs as nxg

################### DEPRECATED

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
# Entrées: Graphe étudié, ensemble des clique maximum connus et les ensembles de sommets R, P et X
# 			R : ensemble des sommets de la clique courante
# 			P : ensemble des sommets candidats à l'ajout dans la clique (voisin de tous les sommets déjà considérés)
# 			X : ensemble des sommets exclus (déjà traité ou appartenant déjà à une clique maximale)
#
# Sortie: liste des cliques maximales sur le graphe de compatibilité et les ensembles P et X (récursivité)

def BronKerborsch_2(Gc, maxClique, R, P, X):
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
			sNv = strong_neighbors(Gc, v)
			#print('v',v,Nv)
			maxClique = BronKerborsch(Gc, maxClique, R|set([v]), P&sNv, X&Nv)
			P.discard(v)
			X = X|set([v])
	return maxClique

# Fonction retournant les voisins du sommet par des liens strong ou floppy (s ou f)
#
# Entrées : Graphe de compatibilité labélisé sur les arêtes {s, f, w} et un sommet du graphe
#
# Sortie : Renvoie un ensemble de sommet voisin de n par des arêtes labelisées s ou f

def strong_neighbors(Gc, node):
	res = set()
	# ensemble des sommets voisins
	Next = set(nx.neighbors(Gc, node))
	for v in Next:
		if Gc[node][v]['label'] in "sf" :
			res.add([v])
	return res

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


