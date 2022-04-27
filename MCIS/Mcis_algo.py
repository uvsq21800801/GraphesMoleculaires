
from MCIS import Mcis_decl

#extraction d'un sous-graphe à partir d'une combinaison du graphe original
def extract_sub(matrice_adja,atom_caract,combi, taille):

    #new_adja = [[None for y in range(taille)] for x in range(taille)]
    #new_caract = [None for x in range(taille)]
    new_adja = []
    new_caract = []

    for i in range(0,len(combi)):
        cnt_i = 0
        if (combi[i] != 0):
            new_caract.append(atom_caract[i])    
            #adja_ligne = [None for x in range(taille)]
            adja_ligne = []
            cnt_j = 0
            for j in range(0,len(combi)):
                if (combi[j] != 0):
                    #adja_ligne[cnt_j] = matrice_adja[i][j]
                    adja_ligne.append(matrice_adja[i][j]) 
                    
                    cnt_j+=1
            new_adja.append(adja_ligne)
            #new_caract.append(carac_ligne)
            cnt_i+=1
        

    return new_adja,new_caract
    #print('MCIS/Mcis_algo: rien pour l\'instant')

# Fonction calculant les valeurs de la table de chaleur
#
# Entrées:
#
# Sortie: Tableau [ordre] [x] [y]
def mcis_algo(matrice_adja,atom_caract, lst_combi,min_ordre, max_ordre):
    
    # tableau 3D [ordre][nb_occurence de cet ordre][nb_occurence de cet ordre]
    tab_sim = []
    
    for h in range(0, max_ordre - min_ordre):
        cb = len(lst_combi[h])
        adja_s = [None for x in range(cb)]
        carac_s = [None for x in range(cb)]

        # tableau intermédiaire à append
        #d = [ [ None for y in range( 2 ) ] for x in range( 2 ) ]
        tab_ordre = [[None for y in range(cb)] for x in range(cb)]
        #tab_ordre = [len(lst_combi[h])][len(lst_combi[h])]
        
        # initialisation des sous-graphes à évaluer
        for i in range(0, len(lst_combi[h])):
            adja_s[i], carac_s[i] = extract_sub(matrice_adja, atom_caract, lst_combi[h][i], h+min_ordre)
        
        for i in range(0, len(lst_combi[h])):
            for j in range(0, len(lst_combi[h])):
                tab_ordre[i][j] = Mcis_decl.simmilarite(adja_s[i], carac_s[i], adja_s[j], carac_s[j])

                #print('MCIS/Mcis_algo: Pas fini')
        tab_sim.append(tab_ordre)
    
    for h in range(0, max_ordre - min_ordre):
    
        print(tab_sim[h])

    return tab_sim