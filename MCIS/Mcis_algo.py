
from MCIS import Mcis_decl

#extraction d'un sous-graphe à partir d'une combinaison du graphe original
def extract_sub(matrice_adja,atom_caract,combi, taille):

    new_adja = [taille]
    new_caract = [taille]

    
    for i in range(0,combi.len()):
        cnt_i = 0
        if (combi[i] != 0):
            adja_ligne = [taille]
            carac_ligne = [taille]    
            cnt_j = 0
            for j in range(0,combi.len()):
                if (combi[j] != 0):
                    adja_ligne[cnt_i][cnt_j] = matrice_adja[i][j]
                    carac_ligne[cnt_i][cnt_j] = atom_caract[i][j]
                    cnt_j+=1
            new_adja.append(adja_ligne)
            new_caract.append(carac_ligne)
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
    tab_sim = [max_ordre-min_ordre]
    
    for h in range(0, max_ordre - min_ordre):
        adja_s = [lst_combi[h].len()]
        carac_s = [lst_combi[h].len()]

        # tableau intermédiaire à append
        tab_ordre = [lst_combi[h].len()][lst_combi[h].len()]
        
        # initialisation des sous-graphes à évaluer
        for i in range(0, lst_combi[h].len()):
            adja_s[i], carac_s[i] = extract_sub(matrice_adja, atom_caract, lst_combi[h][i], h+min_ordre)
        
        for i in range(0, lst_combi[h].len()):
            for j in range(0, lst_combi[h].len()):
                tab_ordre[i][j] = Mcis_decl.mcis(adja_s[i], carac_s[i], adja_s[j], carac_s[j])

                print('MCIS/Mcis_algo: Pas fini')
        tab_sim[h].append(tab_ordre)


    return tab_sim