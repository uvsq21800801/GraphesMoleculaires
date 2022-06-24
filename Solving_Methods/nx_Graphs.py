import networkx as nx

## Affichage des matrices d'adjacence des graphes NetworkX

# Matrice d'adjacence du graphe
def print_adj(G):
	s = ''
	for node in G:
		# Sommet d'origine des arcs
		s += str(node)+' { '
		# Sommets de fin des arcs
		for succ in G.neighbors(node):
			s += str(succ)+' '
		s += '}\n'
	print(s)

# Matrice d'adjacence du graphe de compatibilité avec les sommets de compatibilité
def print_adj_compatib(Gc, nodes_comp, option):
	s = ''
	for node in Gc:
		# Sommet d'origine des arcs
		if option :
			s += str(node)+':'+str(nodes_comp[node])+' { '
		else :
			s += str(nodes_comp[node])+' { '
		# Sommets de fin des arcs et label de l'arc
		for succ in Gc.neighbors(node):
			if option :
				s += str(succ)+':'+str(nodes_comp[succ])+'-'+Gc.adj[node][succ]['label']+' '
			else :
				s += str(nodes_comp[succ])+'-'+Gc.adj[node][succ]['label']+' '
		s += '}\n'
	print(s)


# Fonction extrayant un sous-graphe à partir d'une combinaison du graphe original
#
# Entrées : matrice d'adjacence , caractéristique des atomes et combinaisons de sommet du motif
#
# Sorties : matrice d'adjacence et caractéristique des atomes du motif

def extract_sub(matrice_adja, atom_caract, combi):
    # initialise les sorties
    new_adja = []
    new_caract = []
    # pour tous les sommets du graphe original
    for i in range(0, len(combi)):
        # s'il appartienne au sous-graphe
        if combi[i]:
            # copie des caractéristiques
            new_caract.append(atom_caract[i])
            adja_ligne = []
            # copie des liaison avec d'autres sommets du sous-graphe
            for j in range(0, len(combi)):
                if combi[j]:
                    adja_ligne.append(matrice_adja[i][j])
            new_adja.append(adja_ligne)
    return new_adja, new_caract


# Construction d'un digraphe sur NetworkX
def create_digraph(matrice_adja, atom_caract):
	# graphe orienté et label sur les sommets
	G = nx.DiGraph()
	# ajoute les sommets avec leur élément associé
	for i in range(len(atom_caract)):
		G.add_node(i, label=atom_caract[i].split()[0])
	# ajoute les relations de la matrice d'adjacence
	for n in G:
		for m in G:
			if m>n:
				if matrice_adja[n][m] == 1:
					G.add_edge(n,m)
					G.add_edge(m,n)
				elif matrice_adja[n][m] == 2:
					G.add_edge(n,m)
				elif matrice_adja[m][n] == 2:
					G.add_edge(m,n)
	return G

# Construction d'un graphe de compatibilité entre 2 digraphes
def graph_compatibility(A, B):
	# graphe non orienté et label sur les arêtes
	Gc = nx.Graph()
	# sommets du graphes avec tri sur les labels compatibles
	nodes_comp = []
	i = 0
	for a in A:
		for b in B:
			# verifie les label des sommets
			if A.nodes[a]['label'] == B.nodes[b]['label']:
				nodes_comp.append([a, b])
				Gc.add_node(i)
				i+=1
	# ajout des arrêtes strong, floppy et weak
	for x in Gc:
		for y in Gc:
			if y > x:
				xa = nodes_comp[x][0]
				xb = nodes_comp[x][1]
				ya = nodes_comp[y][0]
				yb = nodes_comp[y][1]
				# verifie que les sommets sont compatibles
				if not (xa == ya or xb == yb):
					Test = ['', '']
					# test dans le sens x vers y
					if xa in A.successors(ya) and xb in B.successors(yb):
						Test[0] = 's'
					elif xa not in A.successors(ya) and xb not in B.successors(yb):
						Test[0] = 'w'
					# test dans le sens y vers x
					if ya in A.successors(xa) and yb in B.successors(xb):
						Test[1] = 's'
					elif ya not in A.successors(xa) and yb not in B.successors(xb):
						Test[1] = 'w'
					# catégorisation des liaisons strong (lié symétriquement) et weak (pas de liaison)
					# la catégorie floppy survient si les liaisons dans les 2 sens ne sont pas de même catégorie 
					if Test[0]==Test[1] and Test[0]!='':
						Gc.add_edge(x,y,label=Test[0])
					if (Test[0]=='s' and Test[1]=='w') or (Test[0]=='w' and Test[1]=='s'):
						Gc.add_edge(x,y,label='f')
	return (Gc, nodes_comp)

# Construction du MCIS issus de la clique forte maximale sur le graphe de compatibilité
#
# Entrées : Matrice d'adjacence du sous-graphe de l'index donnée, clique forte du graphe de compatibilité et noms des sommets associés
#
# Sorties : 

def Mcis_by_compatibility(matrice_adja, atom_caract, nodes_comp, clique, index) :
	MCIS = nx.DiGraph()
	# ajoute les sommets avec leur élément associé
	for n in clique:
		num = nodes_comp[n][index]
		MCIS.add_node(num, label=atom_caract[num].split()[0])
	# ajoute les relations de la matrice d'adjacence
	for n in MCIS:
		for m in MCIS:
			if m>n :
				if matrice_adja[n][m] == 1:
					MCIS.add_edge(n,m)
					MCIS.add_edge(m,n)
				elif matrice_adja[n][m] == 2:
					MCIS.add_edge(n,m)
				elif matrice_adja[m][n] == 2:
					MCIS.add_edge(m,n)
	return MCIS

# Recherche des voisins non faible de u sans Gc
#
# Entrées : Graphes de compatibilité et sommet u
# 
# Sorties : ensemble des voisins de u ayant une liaison forte

## à voir


# Line DiGraphes :
# Construction
# DiGraphe <-> LineDiGraphe
# LineDiGraphes -> Gcompatibilité
