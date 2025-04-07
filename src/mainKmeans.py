import os
import time
from algorithms.KMeans import KMeans
from utils.data_manager import DataManager
from model.Trajectoire import Trajectoire

def process_files(stage, source_dir, result_dir, kmeans_instance, prefix=""):
    """Traite les fichiers JSON pour un certain stade de traitement."""
    
    os.makedirs(result_dir, exist_ok=True)  # Crée le dossier de résultats si inexistant
    json_files = [f for f in os.listdir(source_dir) if f.endswith('.json')]
    
    if not json_files:
        print(f"Pas de trajectoires dans le dossier {stage}, veuillez exécuter mainDataImport.py ou ajouter des fichiers JSON.")
        return

    json_files_done = set(os.listdir(result_dir))  # Ensemble des fichiers déjà traités
    file_index = 1
    tdebut = time.time()

    for json_file_name in json_files:
        result_file_name = f"kmeans_{json_file_name}"
        if result_file_name not in json_files_done:
            json_file_path = os.path.join(source_dir, json_file_name)
            print(f"\nChargement du fichier JSON : {json_file_name}...")

            # Charger les trajectoires
            trajectoires = DataManager.load_traj_from_json(json_file_path)
            print(f"Fichier : {json_file_name} contient {len(trajectoires)} trajectoires.")

            resultats = []
            for i, trajectoire in enumerate(trajectoires):
                print(f"Traitement de la trajectoire {i} ({len(trajectoire.points)} points)...")
                points = [(point.get_coords()[0], point.get_coords()[1], point.get_tick()) for point in trajectoire.get_all_points()]
                if points:
                    kmeans_instance.fit(points)
                    result = Trajectoire(trajectoire.player_id, kmeans_instance.prepare_data_for_prefixspan())
                    resultats.append(result)

            # Sauvegarde des résultats
            result_file_path = os.path.join(result_dir, result_file_name)
            DataManager.export_trajectories_to_json(resultats, result_file_path)
            print(f"Résultats enregistrés dans {result_file_path}")
        else:
            print(f"Fichier {json_file_name} déjà traité")

        print(f"\n{file_index} fichiers traités en {time.time() - tdebut:.2f} secondes")
        file_index += 1

    print(f"\nTraitement {stage} terminé en {int(time.time() - tdebut)}s.")

def main():
    base_dir = os.path.dirname(__file__)
    
    # Définition des répertoires
    processed_dir = os.path.join(base_dir, '..', 'data', 'processed')
    results_dir = os.path.join(base_dir, '..', 'data', 'results', 'kmeans')

    stages = {
        "early":  ("early",  "early_"),
        "mid":    ("mid",    "mid_"),
        "end":    ("end",    "end_"),
        "all":    ("all",    "all_")
    }

    kmeans_instance = KMeans(100)

    for stage, (subdir, prefix) in stages.items():
        source_dir = os.path.join(processed_dir, subdir)
        result_dir = os.path.join(results_dir, subdir)
        process_files(stage, source_dir, result_dir, kmeans_instance, prefix)

if __name__ == "__main__":
    main()
