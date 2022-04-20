import os
import math
import sys

INF = math.inf

# Algorithme de Floyd-Warshall
def floyd_warshall(nb_vertices, matrix, log):
    distance = list(map(lambda p: list(map(lambda q: q, p)), matrix))
    # Adding vertices individually
    for i in range(nb_vertices):
        for j in range(nb_vertices):
            for k in range(nb_vertices):
                distance[j][k] = min(distance[j][k], distance[j][i] + distance[i][k]) # Minimum entre le chemin courrant et le prochain chemin
                if (j == k) :
                    if (distance[j][k] > 0):
                        distance[j][k] = 0
            k = 0
        log.write("Itération " + str(i + 1) + ":\n")
        pretty_print(distance, len(distance), log);

    absorbing_circle(distance, log)


# Detection de circuit absorbant
def absorbing_circle(distance, log):
    nb_neg_on_diag = -1
    for i in range (len(distance)):                                                   # Detection de négatifs sur la diagonale
        if(distance[i][i] != INF and distance[i][i] < 0) :
            nb_neg_on_diag = i

    if(nb_neg_on_diag != -1):                                                         # Nombre négatif trouvé
        print("Il y a un circuit absorbant dans le graphe dans la diagonale de la ligne " + str(nb_neg_on_diag) + "\n\n")
        log.write("Il y a un circuit absorbant dans le graphe dans la diagonale de la ligne " + str(nb_neg_on_diag) + "\n\n")

    else:                                                                             # Pas de nombre négatif trouvé
        print("Il n'y a pas de circuit absorbant dans le graphe\nMatrice des plus courts chemins:\n")
        pretty_print(distance, len(distance), sys.stdout)
        log.write("Il n'y a pas de circuit absorbant dans le graphe\nMatrice des plus courts chemins:\n")
        pretty_print(distance, len(distance), log)


# Affichage dans un fichier
def pretty_print(matrix, nb_vertices, file):
    # Taille maximal des nombres de la matrice
    max = 0
    for i in range(nb_vertices):
        for j in range(nb_vertices):
            if len(str(matrix[i][j])) > max:
                max = len(str(matrix[i][j]))

    # Affichage du nom des sommets horizontalement
    file.write('\n')
    for i in range(len(str(nb_vertices))):
        file.write(' ')
    for i in range(0, nb_vertices):
        for j in range(max - len(str(i))):
            file.write(' ')
        file.write("  " + str(i))
    file.write("\n")

    # Affichage de "_"
    for i in range(len(str(nb_vertices)) + 2):
        file.write(' ')
    for i in range(nb_vertices * (max + 2) - 1):
        file.write('_')
    file.write('\n')

    # Affichage de la matrice
    for i in range(0, nb_vertices):
        # Affichage du nom des sommets verticalement
        for j in range(len(str(nb_vertices)) - len(str(i))):
            file.write(' ')
        file.write(str(i) + " |");
        # Affichage de la matrice
        for j in range(0, nb_vertices):
            for k in range(max - len(str(matrix[i][j]))):
                file.write(' ')
            if (matrix[i][j] == INF):
                file.write("INF")
            else:
                file.write(str(matrix[i][j]))
            file.write("  ")
        # Retour à la ligne si fin de ligne de la matrice
        if (i != nb_vertices - 1):
            file.write('\n')
    file.write('\n\n\n')


# Remplit la matrice en lisant le fichier
def fill_matrix(matrix, file, nb_edges, nb_vertices):
    edges = file.readline()                                                           # Lecture prealable de la ligne
    len = []
    for i in range(0, nb_edges):                                                      # Boucle sur tous les arcs
        line = edges.split(" ")                                                       # Decoupage de la ligne
        matrix[int(line[0])][int(line[1])] = int(line[2])                             # Rematrixplacematrixent de la valeur dans la matrixatrice
        len.append(int(line[2]))
        edges = file.readline()                                                       # Lecture de la prochaine ligne


# Initialisation de la matrice
def init_matrix(file, log):
    nb_vertices = int(file.readline())                                                # Nombre de sommet
    nb_edges = int(file.readline())                                                   # Nombre d'arc

    matrix = [[INF for i in range(0, nb_vertices)] for i in range(0, nb_vertices)]    # Creation de la matrice
    fill_matrix(matrix, file, nb_edges, nb_vertices)                                  # Remplissage de la matrice
    log.write("\n----------- Matrice d'adjacence combinée à matrice de valeurs -----------")
    pretty_print(matrix, nb_vertices, log)                                       # Remplissage du fichier de log

    return matrix, nb_edges, nb_vertices


# Choix du prochain graphe à étudier
def choose_graph(files_open, path):
    index_file = ""
    files = ""

    # Tant que la saisie n'est pas un numéro qui correspond à un fichier non visité
    while (not index_file.isdigit() or not os.path.isfile(files)):
        index_file = input("Numéro du graphe: ")
        files = path + "/E5_graphe" + index_file + ".txt"

    return index_file, files


# Choix de continuer le programme ou de s'arreter
def continue_program():
    answer = ""
    while (answer != "Y" and answer != "N"):
        answer = input("Continue? (Y/N): ")
    if (answer == "Y"):
        return True
    return False


# Fonction principale
def main(path):
    log_path = path + "/E5_log.txt"
    if not (os.path.isfile(log_path)):                                                # Si le fichier de log n'existe pas, le créer
        log = open(str(log_path), "x")
    else:                                                                             # Sinon l'écraser
        log = open(str(log_path), "w")

    files_open = []                                                                   # Liste des fichiers ouverts
    graph_open = []                                                                   # Matrices des fichiers ouverts
    next_graph = True                                                                 # Condition de sortie du programme

    while(next_graph):
        # Liste tous les fichiers du dossier
        for files in os.listdir(path):
            if (files != "E5_log.txt"):
                print(files)

        index_file, file_chosen = choose_graph(files_open, path)                      # Choix du prochain graphe

        # Si le fichier n'a pas été lu
        if (index_file not in files_open):
            current_file = open(file_chosen, "r")                                     # Ouverture du fichier
            log.write("______________________________________________________\
_______________________________________________________\nFichier en cours: " \
+ current_file.name + '\n')
            matrix, nb_edges, nb_vertices = init_matrix(current_file, log)            # Transformation du fichier en matrice de graphe
            current_file.close()                                                      # Fermeture du fichier
            files_open.append(index_file)                                             # Ajout du fichier
            graph_open.append(matrix)                                                 # Ajout de la matrice

        # Si le fichier a été lu
        else:
            current_file = path + "/E5_graphe" + index_file + ".txt"
            log.write("______________________________________________________\
_______________________________________________________\nFichier en cours: " \
+ current_file + '\n')
            matrix = graph_open[files_open.index(index_file)]
            nb_vertices = len(matrix)

        print("\n----------- Matrice d'adjacence combinée à matrice de valeurs -----------")
        pretty_print(matrix, nb_vertices, sys.stdout)
        log.write("----------- Floyd_Warshall Warshall: -----------\n")
        floyd_warshall(nb_vertices,matrix, log)                                       # Appel à l'algorithme de Floyd-Warshall

        next_graph = continue_program()                                               # Continuer le programme

    log.close()

# Appel de la fonction principale
main("C:/Users/matte/Desktop/Projets/Projet Graph/E5_TestGraphe")
