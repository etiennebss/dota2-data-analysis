import os
import time

import matplotlib.pyplot as plt
import matplotlib.image as mpimg

import tkinter as tk

from model.Trajectoire import Trajectoire
from utils.data_manager import DataManager
from algorithms.MDL import MDL
from random import randint
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import pandas as pd

def main():

    # Chemin contenant les data
    processed_dir = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed', 'all')

    # Récupère les fichiers JSON dans le répertoire 'processed'
    json_files = [f for f in os.listdir(processed_dir) if f.endswith('.json')]

    processed_dir_kmean = os.path.join(os.path.dirname(__file__), '..', 'data', 'results', 'kmeans', 'all')
    json_files_kmeans = [f for f in os.listdir(processed_dir_kmean) if f.endswith('.json')]

    processed_dir_mdl = os.path.join(os.path.dirname(__file__), '..', 'data', 'results', 'mdl', 'all')
    json_files_mdl = [f for f in os.listdir(processed_dir_mdl) if f.endswith('.json')]

    fenetre = tk.Tk()
    fenetre.title("Affichage des trajectoires")

    fig, ax = plt.subplots(figsize=(10, 6))

    map_image = mpimg.imread("src/map.jpg")
    ax.imshow(map_image, extent=[-50, 1090, -45, 1015])

    compteur = 1
    generate = False
    numeroJoueur = 0
    listeFichiers = []
    nombreJoueurs = 0
    param_affichage = "brute"
    x = None
    y = None
    couleurs = ['b', 'orange', 'g', 'r', 'purple', 'brown', 'pink', 'gray', 'yellow', 'cyan']
    mdl_instance = MDL()

    def ajoutFichier(n):
        nonlocal listeFichiers
        if n < 0:
            for _ in range(abs(n)):  
                if listeFichiers:
                    listeFichiers.pop()
                else:
                    break 
        else:
            for _ in range(n):
                if len(listeFichiers) >= 10:
                    break
                fichier = {}
                fichier["numero"] = randint(0, len(json_files) - 1)
                fichier["nom"] = json_files[fichier["numero"]]
                fichier["chemin"] = os.path.join(processed_dir, fichier["nom"])
                fichier["trajectoires"] = DataManager.load_traj_from_json(fichier["chemin"])
                fichier["x_coords"] = []
                fichier["y_coords"] = []
                fichier["mdl"] = []
                fichier["x_coords_mdl"] = []
                fichier["y_coords_mdl"] = []
                fichier["kmeans"] = []
                fichier["x_coords_kmean"] = []
                fichier["y_coords_kmean"] = []
                
                for i in range(10):
                    fichier["x_coords"].append([point.x for point in fichier["trajectoires"][i].points])
                    fichier["y_coords"].append([point.y for point in fichier["trajectoires"][i].points])
                    mdl_file = f'all_mdl_{fichier["nom"]}'
                    if mdl_file in json_files_mdl:
                        mdl_trajectoires = DataManager.load_traj_from_json(os.path.join(processed_dir_mdl, mdl_file))
                        fichier["mdl"].append(mdl_trajectoires)
                        for i in range(min(10, len(mdl_trajectoires))):
                            fichier["x_coords_mdl"].append([point.x for point in mdl_trajectoires[i].points])
                            fichier["y_coords_mdl"].append([point.y for point in mdl_trajectoires[i].points])
                    kmeans_file = f'kmeans_all_mdl_{fichier["nom"]}'
                    if kmeans_file in json_files_kmeans:
                        kmeans_trajectoires = DataManager.load_traj_from_json(os.path.join(processed_dir_kmean, kmeans_file))
                        fichier["kmeans"].append(kmeans_trajectoires)

                        for i in range(min(10, len(kmeans_trajectoires))):
                            fichier["x_coords_kmean"].append([point.x for point in kmeans_trajectoires[i].points])
                            fichier["y_coords_kmean"].append([point.y for point in kmeans_trajectoires[i].points])

                
                fichier["couleur"] = couleurs[len(listeFichiers)]
                listeFichiers.append(fichier)
        update()


    def ajoutJoueur(n):
        nonlocal nombreJoueurs
        nombreJoueurs = max(0, min(9, nombreJoueurs + n))
        update()

    def update(param = None):
        nonlocal listeFichiers, x, y, param_affichage
        ax.lines.clear()

        if (param in ["brute", "mdl", "kmean"]):
            param_affichage = param
            label2.config(text="mode : " + param_affichage)

        if (param_affichage == "mdl"):
            x = "x_coords_mdl"
            y = "y_coords_mdl"
        elif (param_affichage == "kmean"):
            x = "x_coords_kmean"
            y = "y_coords_kmean"
        else:
            x = "x_coords"
            y = "y_coords"

        for fichier in listeFichiers:
            if len(listeFichiers) == 1:
                ax.set_title(f'Trajectoire du fichier numero {fichier["nom"]}')
                for joueur in range(nombreJoueurs + 1):
                    ax.plot(fichier[x][joueur][0:compteur], fichier[y][joueur][0:compteur], marker='o', label=f'Joueur {joueur}', linestyle='-', color=couleurs[joueur])
                    ax.legend()
            else:
                ax.set_title(f'Trajectoire des joueurs numero {numeroJoueur}')
                ax.plot(fichier[x][numeroJoueur][0:compteur], fichier[y][numeroJoueur][0:compteur], marker='o', label=f'Fichier {fichier["numero"]}', linestyle='-', color=fichier["couleur"])
                ax.legend()
        canvas.draw()



    if json_files:
        for fichier in listeFichiers:
        
            ax.plot(fichier["x_coords"][0][0:compteur], fichier["y_coords"][0][0:compteur], marker='o', label=f'Fichier {fichier["numero"]}', linestyle='-', color=fichier["couleur"])

            ax.set_xlabel('x')
            ax.set_ylabel('y')
            ax.set_title(f'Trajectoire du Joueur {fichier["trajectoires"][numeroJoueur].player_id}')
            ax.legend()
            ax.grid(True)

        canvas = FigureCanvasTkAgg(fig, master=fenetre)
        canvas.draw()
        canvas.get_tk_widget().pack()

        ajoutFichier(1)

        def avancement(pas, play=False):
            nonlocal compteur
            if (pas == "reset"):
                compteur = 1
                update()
            elif (pas == "max"):
                compteur = 3000
                update()
            else:       
                compteur += pas
                update()
                if play:
                    fenetre.after(10, lambda: avancement(pas, True))
            label1.config(text="compteur : " + str(compteur))

        frame_boutons = tk.Frame(fenetre)
        frame_boutons.pack()
        
        bouton1 = tk.Button(frame_boutons, text="-", command=lambda: avancement(-1))
        bouton1.pack(side=tk.LEFT, padx=5)
        bouton2 = tk.Button(frame_boutons, text="--", command=lambda: avancement(-10))
        bouton2.pack(side=tk.LEFT, padx=5)
        bouton3 = tk.Button(frame_boutons, text="---", command=lambda: avancement(-50))
        bouton3.pack(side=tk.LEFT, padx=5)
        bouton4 = tk.Button(frame_boutons, text="◀", command=lambda: avancement(-1, True))
        bouton4.pack(side=tk.LEFT, padx=5)
        bouton5 = tk.Button(frame_boutons, text="▶", command=lambda: avancement(1, True))
        bouton5.pack(side=tk.LEFT, padx=5)
        bouton6 = tk.Button(frame_boutons, text="+", command=lambda: avancement(1))
        bouton6.pack(side=tk.LEFT, padx=5)
        bouton7 = tk.Button(frame_boutons, text="++", command=lambda: avancement(10))
        bouton7.pack(side=tk.LEFT, padx=5)
        bouton8 = tk.Button(frame_boutons, text="+++", command=lambda: avancement(50))
        bouton8.pack(side=tk.LEFT, padx=5)
        boutonReset = tk.Button(frame_boutons, text="Reset", command=lambda: avancement("reset"))
        boutonReset.pack(side=tk.LEFT, padx=5)
        boutonReseta = tk.Button(frame_boutons, text="Max", command=lambda: avancement("max"))
        boutonReseta.pack(side=tk.LEFT, padx=5)

        frame_boutons_fichier = tk.Frame(fenetre)
        frame_boutons_fichier.pack()
        bouton9 = tk.Button(frame_boutons_fichier, text="Ajout d'un fichier \U0001F5C2", command=lambda: ajoutFichier(1))
        bouton9.pack(side=tk.LEFT, padx=5)
        bouton10 = tk.Button(frame_boutons_fichier, text="Retrait d'un fichier \U0001F5C2", command=lambda: ajoutFichier(-1))
        bouton10.pack(side=tk.LEFT, padx=5)
        bouton11 = tk.Button(frame_boutons_fichier, text="Ajout d'un joueur \U0001F579", command=lambda: ajoutJoueur(1))
        bouton11.pack(side=tk.LEFT, padx=5)
        bouton12 = tk.Button(frame_boutons_fichier, text="Retrait d'un joueur \U0001F579", command=lambda: ajoutJoueur(-1))
        bouton12.pack(side=tk.LEFT, padx=5)

        frame_boutons_methode = tk.Frame(fenetre)
        frame_boutons_methode.pack()
        bouton13 = tk.Button(frame_boutons_methode, text="BRUTE \U0001F579", command=lambda: update("brute"))
        bouton13.pack(side=tk.LEFT, padx=5)
        bouton14 = tk.Button(frame_boutons_methode, text="MDL \U0001F579", command=lambda: update("mdl"))
        bouton14.pack(side=tk.LEFT, padx=5)
        bouton15 = tk.Button(frame_boutons_methode, text="KMEAN \U0001F579", command=lambda: update("kmean"))
        bouton15.pack(side=tk.LEFT, padx=5)

        frame_labels= tk.Frame(fenetre)
        frame_labels.pack()
        label1 = tk.Label(frame_labels, text="compteur : " + str(compteur))
        label1.pack(side=tk.LEFT, padx=5)
        label2 = tk.Label(frame_labels, text="mode : " + param_affichage)
        label2.pack(side=tk.LEFT, padx=5)

        fenetre.mainloop()

    else :
        print("Pas de trajectoires dans le fichier processed, veuillez run mainDataImport.py ou en ajouter par vous même avant")



if __name__ == "__main__":
    main()

    