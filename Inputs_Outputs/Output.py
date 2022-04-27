from os import listdir, remove
from os.path import isfile, join
import re
import matplotlib.pyplot as plt
import numpy as np


def res_sim(name, min_ordre, max_ordre, Tab_sim):

    for h in range(max_ordre-min_ordre+1):
    
        # création du fichier de sortie
        fpath = "Inputs_Outputs/Place_Output_here/"
        filename = name+"_sim_ord_"+str(h+min_ordre)+".txt"
        if isfile(join(fpath, filename)):
            remove(join(fpath, filename))
        f = open(fpath+filename, 'w')
        plt.imshow(Tab_sim[h], cmap='hot_r', interpolation='nearest')
        #plt.show()
        plt.savefig(fpath+name+"_heatmap_ord_"+str(h+min_ordre)+".png")
        for i in range(len(Tab_sim[h])):
            

            s =""

            for j in range(len(Tab_sim[h])):
                s+=str(Tab_sim[h][i][j])+' '
                print(' ')

            f.write(s+'\n')
        f.close()