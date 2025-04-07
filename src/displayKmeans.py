import json
import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

from utils.data_manager import DataManager
from model.Trajectoire import Trajectoire


def main():

    processed_dir = os.path.join(os.path.dirname(__file__), '..', 'data', 'results', 'kmeans', 'all')
    print("Chargement des données JSON..")

    json_files = [f for f in os.listdir(processed_dir) if f.endswith('.json')]

    if not json_files:
        print("Pas de trajectoires dans le dossier processed, veuillez exécuter mainDataImport.py ou ajouter des fichiers JSON.")
        return

    trajectoires = []

    for json_file_name in json_files:

        json_file_path = os.path.join(processed_dir, json_file_name)
        trajectoirelist = DataManager.load_traj_from_json(json_file_path)
        
        for trajectoire in trajectoirelist:
            trajectoires.append(trajectoire)
    




    listePoints = []
    for trajectoire in trajectoires:
        points = [
            (point.get_coords()[0], point.get_coords()[1])
            for point in trajectoire.get_all_points()
            if point.get_coords()[:2] != (None, None)
        ]
        
        listePoints.append(points)
    

    traj_a_afficher = trajectoires[0].points

    #Affichage traj partitionnée
    x_coords = [point.x for point in traj_a_afficher]
    y_coords = [point.y for point in traj_a_afficher]
    
    map_image = mpimg.imread("src/map.jpg")

    plt.figure("Trajectoire partitionning", figsize=(10,6))

    plt.imshow(map_image, extent=[-50, 1090, -45, 1015])

    plt.plot(x_coords, y_coords, marker='o', label=f'Exemple trajectoire Joueur après kmeans', linestyle='-')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title(f'Trajectoire du Joueur après kmeans et arrondi')
    plt.legend()
    plt.grid(True)


    plt.show()

if __name__ == "__main__":
    main()