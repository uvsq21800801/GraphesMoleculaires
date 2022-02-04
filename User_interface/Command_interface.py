# sera une interface de commande si besoin
import sys
sys.path.append('GraphesMoleculaires/Inputs_Outputs')
from Inputs_Outputs import Inputs

def interface():
    listindex = []
    Inputs.Input_trad(listindex)
    print(listindex)
    matriceadja = []
    Inputs.Input_bonds(listindex, matriceadja)
    print(matriceadja)
    
    