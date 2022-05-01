
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
def mcis_algo(matrice_adja, atom_caract, lst_ord, dict_iso,min_ordre, max_ordre):
    
    # tableau 3D [ordre][nb_occurence de cet ordre][nb_occurence de cet ordre]
    tab_sim = []
    
    for h in range(max_ordre - min_ordre+1):
        cb = len(lst_ord[h])
        adja_s = [None for x in range(cb)]
        carac_s = [None for x in range(cb)]

        # tableau intermédiaire à append
        #d = [ [ None for y in range( 2 ) ] for x in range( 2 ) ]
        tab_ord_h = [[None for y in range(cb)] for x in range(cb)]
        #tab_ordre = [len(lst_combi[h])][len(lst_combi[h])]
        
        # initialisation des sous-graphes à évaluer
        for i in range(cb):
            getlist = dict_iso[lst_ord[h][i]]
            adja_s[i], carac_s[i] = extract_sub(matrice_adja, atom_caract, getlist[0], h+min_ordre)
        
        for i in range(cb):
            for j in range(cb):
                '''ce qui est en commentaire ci-dessous, c'est les différentes façons de calculer la simmilarité'''
                #tab_ord_h[i][j] = Mcis_decl.simmilarite(adja_s[i], carac_s[i], adja_s[j], carac_s[j])
                #tab_ord_h[i][j] = Mcis_decl.sim_raymond(adja_s[i], carac_s[i], adja_s[j], carac_s[j])
                tab_ord_h[i][j] = Mcis_decl.sim_barth(adja_s[i], carac_s[i], adja_s[j], carac_s[j], i, j)

                #print('MCIS/Mcis_algo: Pas fini')
        tab_sim.append(tab_ord_h)
    
    '''for h in range( max_ordre - min_ordre +1):
    
        print(tab_sim[h])
'''
    return tab_sim
