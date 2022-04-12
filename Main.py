# Python[version]
# Main, File to execute
import sys, os
from os import listdir, remove
from os.path import isfile, join
import re
sys.path.append('MCIS/analysis')

from analysis import mcis
    
def main():

    SiO_caract = ['Si 1', 'O 2']

    SiO_adja = [[0,1],[1,0]]

    SiO4_caract = ['Si 1', 'O 2', 'O 3', 'O 4', 'O 5']

    SiO4_adja = [[0,1,0,1,1],
                [1,0,1,0,1],
                [1,1,0,1,1],
                [0,0,1,0,1],
                [1,1,0,1,0]]
    
    mcis.mcis_algo(SiO4_adja,SiO4_caract,SiO_adja,SiO_caract)


if __name__=="__main__":
    main()




