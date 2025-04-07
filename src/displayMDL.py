import os
import time

import matplotlib.pyplot as plt

from model.Trajectoire import Trajectoire
from utils.data_manager import DataManager
from algorithms.MDL import MDL
import matplotlib.image as mpimg

def main():

    tdebut = time.time()

    # Chemin contenant les data
    processed_dir = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed', 'all')

    # Récupère les fichiers JSON dans le répertoire 'processed'
    json_files = [f for f in os.listdir(processed_dir) if f.endswith('.json')]

    if json_files:
        # Prendre uniquement le premier fichier JSON
        json_file_name = json_files[0]
        json_file_path = os.path.join(processed_dir, json_file_name)

        print(f"Chargement du fichier JSON : {json_file_name}...")

        # Charger les trajectoires depuis le fichier JSON
        trajectoires = DataManager.load_traj_from_json(json_file_path)

        # Affichage des trajectoires trouvées dans le fichier
        print(f"\nFichier : {json_file_name} :")

        for i, trajectoire in enumerate(trajectoires):
            print(f"Trajectoire {i}: {len(trajectoire.points)} points")

        tinter = time.time()
        print(f"Temps pour charger les trajectoires : {str(int(tinter - tdebut))}s")


        #Application de la MDL sur la première trajectoire du premier fichier
        mdl_instance = MDL()

        traj_pour_mdl = trajectoires[0]
        mdl = Trajectoire(traj_pour_mdl.player_id, mdl_instance.traj_partitionning(traj_pour_mdl))

        print(f"Avant la MDL {len(traj_pour_mdl.points)} points")
        print(f"Après la MDL {len(mdl.points)} points")

        tfin = time.time()
        print(f"Temps pour MDL de la trajectoire : {str(int(tfin - tdebut))}s")



        # Affichage traj initiale
        x_coords = [point.x for point in traj_pour_mdl.points]
        y_coords = [point.y for point in traj_pour_mdl.points]

        map_image = mpimg.imread("src/map.jpg")

        plt.figure("Trajectoire", figsize=(10, 6))

        plt.imshow(map_image, extent=[-50, 1090, -45, 1015])

        plt.plot(x_coords, y_coords, marker='o', label=f'Trajectoire Joueur {traj_pour_mdl.player_id}', linestyle='-')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.title(f'Trajectoire du Joueur {traj_pour_mdl.player_id}')
        plt.legend()
        plt.grid(True)


        #Affichage traj partitionnée
        x_coords = [point.x for point in mdl.points]
        y_coords = [point.y for point in mdl.points]
        

        plt.figure("Trajectoire partitionning", figsize=(10,6))

        plt.imshow(map_image, extent=[-50, 1090, -45, 1015])

        plt.plot(x_coords, y_coords, marker='o', label=f'Trajectoire Joueur {traj_pour_mdl.player_id}', linestyle='-')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.title(f'Trajectoire du Joueur {traj_pour_mdl.player_id}')
        plt.legend()
        plt.grid(True)


        plt.show()

    else :
        print("Pas de trajectoires dans le fichier processed, veuillez run mainDataImport.py ou en ajouter par vous même avant")



if __name__ == "__main__":
    main()



    #coord_4070746269.json sur traj 8 pour test (pq mdl ça prend du temps ?)