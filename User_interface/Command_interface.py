# sera une interface de commande si besoin
import sys
sys.path.append('GraphesMoleculaires/Input_Outputs')
from Inputs_Outputs import Inputs

def interface():
    Inputs.Input_bonds()
    Inputs.Input_trad()
    