# GraphesMoleculaires
> Projet de TER sur les graphes moléculaires

## Organisation
* Dossier **User_interface** : Organisation des parametrages utilisateur
  * *Program*.py : archive des fonctions d'execution selon des conditions différentes
  * *Command_interface_old*.py : archive de l'exécution des algorithmes dans des conditions fixées
  * *Command_interface*.py : Exécution conditionnel des algorithmes avec entrées sur le terminal
* Dossier **Solving_Methods** : Algorithmes de résolutions 
  * *BruteForce*.py : ancien fichier des algo de *Combination*.py et *Isomorph*.py
  * *Combination*.py : Génération sous-graphes
  * *Isomorph*.py : Isomorphisme, certificat canonique
  * *Statistic*.py : Fonction pour le taux de recouvrement, le nombre de motif unique et le tri des indices
  * *Similarity*.py : Similarité selon les différentes méthodes [à revoir]
  * *Mcis_decl*.py : méthodes nécessaire pour la similarité [à revoir]
* Dossier **Inputs_Outputs** : Methodes de lecture et d'écriture de fichiers
  * Dossier *Place_Bonds_file_here* : fichiers d'entrée de liaison des sommets (1 covalent et 4 liaison H)
  * Dossier *Place_Trad_file_here* : fichiers d'entrée de caractéristique des sommets (nom de l'atome)
  * Dossier *Place_Output_here* : rassemble les fichiers de sortie
  * *Inputs*.py : lecture des fichiers d'entrée
  * *Output*.py : écriure des fichiers de sortie

## Fichiers utilisés
### Entrée
**bonds_[name].txt**
```
  1
  1 [numero_sommet] [numero_sommet]
  4 [numero_donneur] [numero_accepteur] [numero_H]
```
Les liaisons covalentes sont indiqués par un 1 et les liaisons hydrogènes par un 4 avec en premier le sommet donneur puis celui accepteur de le liaison hydrogène.

**trad-atom_[name].txt**
```
  [nombre de sommets]
  [indice][nom_atome][nom_dessin]
```
Le deuxième nom d'atome est celui utilisé dans les dessins du graphes.

### Sortie
Différents fichier de sortie sont généré à la suite du programme :
- *[name]_data.txt* : information sur le graphe analysé avec matrice et résumé des résultats
- *[name]_res.txt* : résultat isomorphisme et recouvrement résumé
- *[name]_combi.txt* : liste des combinaisons de sommets à isomorphisme près
- *[name]_sim_ord_[taille].txt* et *[name]_heatmap_ord_[taille].png* : matrice de chaleur

## Terminologie

combi
ordre
isomorph
...

## Dépendences:
Avant de lancer l'application, entrez cela dans le terminal depuis le dossier contenant ce Readme:
``` bash
  pip install -r requirement.txt
```

Après avoir ajouté de nouvelles dépendences au projet (afin que d'autres personnes travaillant sur le projet puisse installer les bonnes librairies):
``` bash
  pip freeze > requirement.txt
```
