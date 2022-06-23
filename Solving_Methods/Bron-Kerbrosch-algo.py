import networkx as nx

#Construction digraphes avec combinaisons
def combi_to_digraph(combi, matrice_adja, atom_caract):
	# graphe orienté et label sur les sommets
	G = nx.DiGraph()
	# ajoute les sommets avec leur élément associé
	for i in range(len(combi)):
		if combi[i]:
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
					# la catégorie floppy survient si par la liaison entre les sommets n'est que dans un sens
					if Test[0]==Test[1] and Test[0]!='':
						Gc.add_edge(x,y,label=Test[0])
					if (Test[0]=='s' and Test[1]=='w') or (Test[0]=='w' and Test[1]=='s'):
						Gc.add_edge(x,y,label='f')
	return (Gc, nodes_comp)

def print_adj(G):
	s = ''
	for node in G:
		s += str(node)+' { '
		for succ in G.neighbors(node):
			s += str(succ)+' '
		s += '}\n'
	print(s)

def print_adj_compatib(Gc, nodes_comp, option):
	s = ''
	for node in Gc:
		if option :
			s += str(node)+':'+str(nodes_comp[node])+' { '
		else :
			s += str(nodes_comp[node])+' { '
		for succ in Gc.neighbors(node):
			if option :
				s += str(succ)+':'+str(nodes_comp[succ])+'-'+Gc.adj[node][succ]['label']+' '
			else :
				s += str(nodes_comp[succ])+'-'+Gc.adj[node][succ]['label']+' '
		s += '}\n'
	print(s)

def BronKerborsch(Gc, maxClique, R, P, X):
	if len(P) == 0 and len(X) == 0 :
		#print("max : ",R)
		if len(maxClique) == 0 or len(R) < len(maxClique[0]):
			maxClique.append(R.copy())
		else :
			maxClique.insert(0,R.copy())
	else :
		T = P|X
		u = T.pop()
		Nu = nx.neighbors(Gc, u)
		#print(u,list(Nu))
		for v in P - set(Nu):
			Nv = nx.neighbors(Gc, v)
			BronKerborsch(Gc, maxClique, set(R)|set([v]), P&set(Nv), X&set(Nv))
			P.discard(v)
			X = X|set([v])
	return maxClique

def arbre_strong(Gc, clique):
	Next = clique.copy()
	#print("init", set(Next))
	u = Next.pop()
	#print(set(Next))
	marquage_strong(Gc, Next, u)
	if len(Next):
		return False
	else :
		return True


def marquage_strong(Gc, Next, u):
	V = set(nx.neighbors(Gc,u))&Next
	for v in V:
		if Gc[u][v]['label'] in "sf" and v in Next:
			Next.discard(v)
			#print(set(Next))
			marquage_strong(Gc, Next, v)


def MaxStrongClique(Gc, MaxClique):
	# sur les cliques maximals tester l'existence d'arbre couvrant strong ou floppy
	for clique in MaxClique :
		if arbre_strong(Gc, clique):
			return Gc.subgraph(clique)


#combinaisons
combi_A = [0,0,1,1,1,1]
combi_B = [1,1,1,0,1,0]

#data
atom_caract = ["O 1","O 2","Si 1","O 3","O 4","Si 2"]
matrice_adja = [[0,0,2,0,0,0],[0,0,2,0,0,0],[0,0,0,2,1,0],[0,0,0,0,0,2],[0,0,1,0,0,2],[0,0,0,0,0,0]]

#Construction graphes
A = combi_to_digraph(combi_A, matrice_adja, atom_caract)
B = combi_to_digraph(combi_B, matrice_adja, atom_caract)

#Construction graphe compatibilité
(Gc, nodes_comp) = graph_compatibility(A,B)

print_adj_compatib(Gc,nodes_comp, 1)


MaxClique = BronKerborsch(Gc, [], set(), set(range(len(Gc))), set())
print(MaxClique)


'''
print(MCIS[0].nodes)
print_adj(MCIS[0])
print(MCIS[1].nodes)
print_adj(MCIS[1])
'''
