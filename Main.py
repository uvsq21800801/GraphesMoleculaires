# Python[version]
# Main, File to execute
import sys, os
GraphesMoleculaires = os.getcwd()
path = os.path.dirname(GraphesMoleculaires)
sys.path.append('GraphesMoleculaires/UserInterface')
from User_interface import Command_interface

def main():
    Command_interface.interface()
    
if __name__=="__main__":
    main()
