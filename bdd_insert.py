
from os import listdir, remove
from os.path import isfile, join
import numpy as np

def insert_motifs(motifs, coloration, matrice_adja, atom_caract, lst_index, dict_isomorph, dict_stat, lst_certif, nb_sommets, liaison_H, crible):
    for l in lst_index:
        
        # récupère les informations du motif
        stat = dict_stat.get(l)
        
        # reconstruit une occurrence du motif
        tmp = dict_isomorph.get(l)
        # liste des éléments et liaisons
        lst_caract = []
        lst_link = []
        # autres valeurs
        nb_liaison = 0
        degre_min = -1
        degre_max = -1
        # pour tous les sommets du graphe original
        for i in range(0, len(tmp[0])):
            # s'il appartienne au sous-graphe
            if tmp[0][i]:
                degre = 0
                # copie des caractéristiques
                splitted = atom_caract[i].split()
                lst_caract.append(splitted[0])
                # copie des liaisons avec d'autres sommets du sous-graphe
                for j in range(0, len(tmp[0])):
                    if tmp[0][j]:
                        if matrice_adja[i][j]:
                            if i < j and matrice_adja[j][i]:
                                lst_link.append([1,i,j])
                                degre += 1
                                nb_liaison += 1
                            elif not matrice_adja[j][i]:
                                lst_link.append([2,i,j])
                                degre += 1
                                nb_liaison += 1
                if degre < degre_min or degre_min == -1:
                    degre_min = degre
                if degre > degre_max or degre_max == -1:
                    degre_max = degre
        
        # test si un element OW
        bool_OW = "OW" in lst_caract
        # test si une liaison H
        bool_H = False
        for link in lst_link:
            if 2 in link :
                bool_H = True
        
        # signature
        #signature = lst_certif[l]
        signature = "A faire"
       
        motif = {
                "signature": signature,
                "coloration": coloration,
                "nombre_sommets": nb_sommets,
                "nombre_liaison": nb_liaison,
                "liste_elements": lst_caract,
                "liste_liaison": lst_link,
                "degre_min": degre_min,
                "degre_max": degre_max,
                "elem_OW": bool_OW,
                "liaison_H": bool_H
                }

        motifs.insert_one(motif)
        #for i in range(len(tmp)):
        #    bd_ids[3].append(Output.str_liste(tmp[i],''))

    return motifs