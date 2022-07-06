import sys, os
GraphesMoleculaires = os.getcwd()
path = os.path.dirname(GraphesMoleculaires)
sys.path.append('GraphesMoleculaires/UserInterface')
from User_interface import Compare_interface as CI

def main():
    CI.interface()
    
if __name__=="__main__":
    main()
