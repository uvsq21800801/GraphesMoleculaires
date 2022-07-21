
from os import listdir, remove
from os.path import isfile, join
import numpy as np

from Inputs_Outputs import Output



def insert_motifs(motifs, lst_index, dict_isomorph, coloration, signature, nb_sommets, liaison_H, crible):
    for l in lst_index:
        # calcul nombre de liaisons
        # + liste de liaisons 
        # degré min
        # degré max

        # A FAIRE


        
        
        tmp = dict_isomorph.get(l)
        motif = {"temp": tmp[0],
                "signature": signature,
                "coloration": coloration,
                "nombre_sommets": nb_sommets,
                "nombre_laison": "A faire",
                "liste_elements": "A faire",
                "liste_liaiso": "A faire",
                "degré min": "A faire",
                "degré max": "A faire",
                "crible_OW": liaison_H,
                "liason_H": crible}

        motifs.insert_one(motif)
        #for i in range(len(tmp)):
        #    bd_ids[3].append(Output.str_liste(tmp[i],''))

    return motifs