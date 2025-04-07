import matplotlib.pyplot as plt
import os
import json
import numpy as np

from algorithms.KMeans import KMeans
from utils.data_manager import DataManager
from model.Trajectoire import Trajectoire
def main():
    processed_dir = os.path.join(os.path.dirname(__file__), '..', 'data', 'results', 'mdl')
    os.makedirs(results_dir, exist_ok=True)  # Crée le dossier de résultats si inexistant
    print("Chargement des données JSON..")
    json_files = [f for f in os.listdir(processed_dir) if f.endswith('.json')]

    if not json_files:
        print("Pas de trajectoires dans le dossier processed, veuillez exécuter mainDataImport.py ou ajouter des fichiers JSON.")
        return
    weights = [0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]
    results = []
    for weigth in weights:
        kmean_instance = KMeans(100, weigth)
        file_index = 1

        # Pour chaque trajectoire, on extrait les points et on applique KMeans
        for json_file_name in json_files:
            
            resultats = []

            json_file_path = os.path.join(processed_dir, json_file_name)
            trajectoires = DataManager.load_traj_from_json(json_file_path)
            

            for i, trajectoire in enumerate(trajectoires):
                points = []
                result = []
                for point in trajectoire.get_all_points():
                    points.append((point.get_coords()[0], point.get_coords()[1], point.tick))

                result.append.comparatorHelper(points)
                #ici traiter cette donnée avant de l'ajouter dans le tableau(ou la traiter a la toute fin, tout depend de la donnée).
            
            results.append(result)


                


        

if __name__ == "__main__":
    main()