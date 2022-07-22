
from os import listdir, remove
from os.path import isfile, join
from bson import ObjectId
import numpy as np

def insert_motifs(motifs, occurs, bd_ids, nb_conf, matrice_adja, atom_caract, lst_index, dict_isomorph, dict_stat, lst_certif, nb_sommets, liaison_H, crible):
    for l in lst_index:
        # signature
        signature = str(lst_certif[l])
        while signature[0] == "0":
            signature = signature[1:]
        
        # Si motif déjà présent?
        if motifs.count_documents({"signature": signature, "coloration": bd_ids[1]}) > 0 :
            result = motifs.find_one({"signature": signature, "coloration": bd_ids[1]})
            motif_id = result["_id"]
        else :
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
            
            motif = {
                    "signature": signature,
                    "coloration": bd_ids[1],
                    "nombre_sommets": nb_sommets,
                    "nombre_liaison": nb_liaison,
                    "liste_elements": lst_caract,
                    "liste_liaison": lst_link,
                    "degre_min": degre_min,
                    "degre_max": degre_max,
                    "elem_OW": bool_OW,
                    "liaison_H": bool_H
                    }

            result = motifs.insert_one(motif)
            motif_id = result.inserted_id

        # Occurrence avec cette config
        # Si déjà présent?
        if occurs.count_documents({"motif": ObjectId(motif_id), "interf":  ObjectId(bd_ids[0]), "config": nb_conf }) > 0 :
            result = occurs.find_one({"motif": ObjectId(motif_id), "interf":  ObjectId(bd_ids[0]), "config": nb_conf })
            # Comparer les résultats
        else :
            stats = dict_stat.get(l)
            
            occur = {
                "motif": ObjectId(motif_id),
                "interf":  ObjectId(bd_ids[0]),
                "config": nb_conf,
                "valeur": stats[0], #multiplier par le nombre d'apparition de la conf
                "t_rec": stats[2],
                "t_occ": stats[3]
                }
            # créé l'occurrence
            result = occurs.insert_one(occur)

    return True