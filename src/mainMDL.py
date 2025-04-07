import os
import time
from model.Trajectoire import Trajectoire
from utils.data_manager import DataManager
from algorithms.MDL import MDL

def process_files(stage, source_dir, result_dir, prefix=""):
    """Traite les fichiers JSON pour un certain stade de traitement."""
    
    os.makedirs(result_dir, exist_ok=True)  # Crée le dossier de résultats si inexistant
    json_files = [f for f in os.listdir(source_dir) if f.endswith('.json')]
    
    if not json_files:
        print(f"Pas de trajectoires dans le dossier {stage}, veuillez exécuter mainDataImport.py ou ajouter des fichiers JSON.")
        return

    mdl_instance = MDL()
    json_files_done = set(os.listdir(result_dir))  # Ensemble des fichiers déjà traités
    file_index = 1
    tdebut = time.time()

    for json_file_name in json_files:
        result_file_name = f"{prefix}mdl_{json_file_name}"
        if result_file_name not in json_files_done:
            json_file_path = os.path.join(source_dir, json_file_name)
            print(f"\nChargement du fichier JSON : {json_file_name}...")

            # Charger les trajectoires
            trajectoires = DataManager.load_traj_from_json(json_file_path)
            print(f"Fichier : {json_file_name} contient {len(trajectoires)} trajectoires.")

            resultats = []
            for i, trajectoire in enumerate(trajectoires):
                print(f"Traitement de la trajectoire {i} ({len(trajectoire.points)} points)...")
                mdl_result = mdl_instance.traj_partitionning(trajectoire)  # Applique MDL
                resultats.append(Trajectoire(trajectoire.player_id, mdl_result))

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
    results_dir = os.path.join(base_dir, '..', 'data', 'results', 'mdl')

    stages = {
        "early":  ("early",  "early_"),
        "mid":    ("mid",    "mid_"),
        "end":    ("end",    "end_"),
        "all":    ("all",    "all_")
    }

    for stage, (subdir, prefix) in stages.items():
        source_dir = os.path.join(processed_dir, subdir)
        result_dir = os.path.join(results_dir, subdir)
        process_files(stage, source_dir, result_dir, prefix)

if __name__ == "__main__":
    main()