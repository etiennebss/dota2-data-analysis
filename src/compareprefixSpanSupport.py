import os
import time
import json

from utils.data_manager import DataManager

from algorithms.PrefixSpanAnalyser import PrefixSpanAnalyser
import matplotlib.image as mpimg

def main():
        processed_dir = os.path.join(os.path.dirname(__file__), '..', 'data', 'results', 'kmeans')
        dest_dir = os.path.join(os.path.dirname(__file__), '..', 'data', 'results', 'prefixSpan')
        result_file_path = os.path.join(dest_dir, f"prefixSpanResults.json")
        print("Chargement des données JSON..")

        kmeans_files = [f for f in os.listdir(processed_dir) if f.endswith('.json')]

        if not kmeans_files:
            print("Pas de trajectoires dans le dossier processed, veuillez exécuter mainDataImport.py ou ajouter des fichiers JSON.")
            return

        trajectoires = []

        for json_file_name in kmeans_files:

            json_file_path = os.path.join(processed_dir, json_file_name)
            trajectoire = DataManager.load_traj_from_json(json_file_path)[1]    
            trajectoires.append(trajectoire)

        listePoints = []
        for trajectoire in trajectoires:
            points = [
                (point.get_coords()[0], point.get_coords()[1])
                for point in trajectoire.get_all_points()
                if point.get_coords()[:2] != (None, None)
            ]
            
            listePoints.append(points)
        
        if listePoints:
            supports = [5,10,15,20,25,30,35,40,45,50]
            results = []
            for support in supports:
                psa = PrefixSpanAnalyser(support, listePoints)
                results.append(psa.getLenMotif())

if __name__ == "__main__":
    main()