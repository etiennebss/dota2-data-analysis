import json
import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

from utils.data_manager import DataManager
from model.Trajectoire import Trajectoire
from algorithms.PrefixSpanAnalyser import PrefixSpanAnalyser

def main():

    processed_dir = os.path.join(os.path.dirname(__file__), '..', 'data', 'results', 'kmeans')
    print("Chargement des données JSON..")
    map_image = mpimg.imread("src/map.jpg")

    json_files = [f for f in os.listdir(processed_dir) if f.endswith('.json')]

    if not json_files:
        print("Pas de trajectoires dans le dossier processed, veuillez exécuter mainDataImport.py ou ajouter des fichiers JSON.")
        return

    trajectoires = []

    for json_file_name in json_files:
        json_file_path = os.path.join(processed_dir, json_file_name)
        trajectoireLoad = DataManager.load_traj_from_json(json_file_path)
        print(trajectoireLoad)

        for traj in trajectoireLoad :
            print(traj)
            if traj.player_id == 9 :
                trajectoires.append(traj)


    listePoints = []
    for trajectoire in trajectoires:
        points = [
            (point.get_coords()[0], point.get_coords()[1])
            for point in trajectoire.get_all_points()[:200]
            if point.get_coords()[:2] != (None, None)
        ]
        
        listePoints.append(points)
    
    if listePoints:
        print(len(listePoints))
        pointsMoyens = []
        for trajectoire in listePoints:
            sumx = 0
            sumy = 0
            for elt in trajectoire :
                sumx += elt[0]
                sumy += elt[1]
            pointsMoyens.append((sumx/len(trajectoire), sumy/len(trajectoire)))


        
        sumx = 0
        sumy = 0
        for elt in pointsMoyens :
            sumx += elt[0]
            sumy += elt[1]
        pointsMoyenMoyen = (sumx/len(pointsMoyens), sumy/len(pointsMoyens))



    traj_a_afficher = pointsMoyens

    x_coords = [point[0] for point in points]
    y_coords = [point[1] for point in points]

    # Trajectoire après KMeans sans lignes, juste des marqueurs
    
    plt.figure("Trajectoire partitionning", figsize=(10, 6))
    plt.imshow(map_image, extent=[-50, 1090, -45, 1015])
    plt.scatter(x_coords, y_coords, marker='o', label=f'Points Moyens')
    plt.scatter(pointsMoyenMoyen[0], pointsMoyenMoyen[1], color='red', marker='x', s=100, label='Point Moyen Moyen')

    plt.xlabel('x')
    plt.ylabel('y')
    plt.title(f'Points Moyens')
    plt.legend()
    plt.grid(True)

    plt.show()



            


if __name__ == "__main__":
    main()