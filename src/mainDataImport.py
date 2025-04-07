import sys
import os
import time

from utils.data_manager import DataManager

# Ajouter 'src' au sys.path pour que Python trouve les modules dans 'src/'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

def main():
    
    tdebut = time.time()

    #Chemin contenant les data
    raw_dir = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw')
    processed_dir = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed')
    all_dir = os.path.join(processed_dir,"all")
    early_dir = os.path.join(processed_dir,"early")
    mid_dir = os.path.join(processed_dir,"mid")
    end_dir = os.path.join(processed_dir,"end")

    # Récupère les fichiers JSON dans le répertoire 'processed'
    json_files_all = [f for f in os.listdir(all_dir) if f.endswith('.json')]
    json_files_early = [f for f in os.listdir(early_dir) if f.endswith('.json')]
    json_files_mid = [f for f in os.listdir(mid_dir) if f.endswith('.json')]
    json_files_end = [f for f in os.listdir(end_dir) if f.endswith('.json')]


    if not json_files_all :
            # Si aucun fichier JSON n'existe, on charge les fichiers CSV et on les exporte en JSON
            print(f"Chargement de tous les fichiers CSV dans le répertoire {raw_dir}")
            
            # Vérifier s'il y a des fichiers CSV dans le répertoire 'raw'
            csv_files = [f for f in os.listdir(raw_dir) if f.endswith('.csv')]
            
            if not csv_files:
                print("Aucun fichier CSV trouvé dans le répertoire.")
                return

            # Itérer sur chaque fichier CSV pour charger les trajectoires
            for file_index, file_name in enumerate(csv_files):
                file_path = os.path.join(raw_dir, file_name)
                print(f"\nFichier {file_index + 1} : {file_name}")

                # Charger les données à partir du fichier CSV
                trajectoires = DataManager.load_data_from_csv(file_path)
                
                # Affichage des trajectoires chargées
                for i, trajectoire in enumerate(trajectoires):
                    print(f"Trajectoire {i}: {len(trajectoire.points)} points")
                
                # Créer le chemin pour le fichier JSON de sortie
                json_file_name = file_name.replace('.csv', '.json')
                json_file_path = os.path.join(all_dir, json_file_name)

                # Exporter les trajectoires dans un fichier JSON
                DataManager.export_trajectories_to_json(trajectoires, json_file_path)
                print(f"Export des trajectoires vers {json_file_path} effectué.")

                tinter = time.time()
                print(str(int(tinter - tdebut)) + "s")

    json_files_all = [f for f in os.listdir(all_dir) if f.endswith('.json')]
    
    if json_files_all :
        if not json_files_early and not json_files_mid and not json_files_end:
            # Si des fichiers JSON existent, on charge et affiche les trajectoires de chaque fichier
            print(f"Chargement des fichiers JSON dans {all_dir} pour découpage...")
            

            for file_index, file_name in enumerate(json_files_all):

                json_file_path = os.path.join(all_dir, file_name)

                early_path = os.path.join(early_dir, 'early'+file_name)
                mid_path = os.path.join(mid_dir, 'mid'+file_name)
                end_path = os.path.join(end_dir, 'end'+file_name)



                # Charger les trajectoires depuis le fichier JSON
                early, mid, end = DataManager.cutFromDate(DataManager.load_traj_from_json(json_file_path))
                
                DataManager.export_trajectories_to_json(early, early_path)
                DataManager.export_trajectories_to_json(mid, mid_path)
                DataManager.export_trajectories_to_json(end, end_path)

                tinter = time.time()
                print(f"{str(int(tinter - tdebut))}s : {file_index} fichiers traités")



    
    tfin = time.time()
    print("Temps total d'exécution : " + str(int(tfin - tdebut)) + "s") # 24sec avec JSON, 426sec en CSV 

if __name__ == "__main__":
    main()
