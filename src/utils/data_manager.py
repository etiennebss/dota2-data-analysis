import json
import pandas as pd

from model.Point import Point
from model.Trajectoire import Trajectoire

class DataManager :
    """Classe pour gérer les données : export de trajectoires en JSON, chargement des csvé"""

    @staticmethod
    def _create_point(x, y, vec_x, vec_y, tick):
        """Permet de créer un point a partir des données brutes 
        Utile dans load_data_from_csv
        
        @return: un point avec des coordonnées normalisées entre 0 et 1000
        """
        #Calculer les coordonnées exactes
        new_x = 256*x + vec_x
        new_y = 256*y + vec_y

        # Récupération des valeurs min/max depuis le dictionnaire
        min_x = 66
        max_x = 188
        min_y = 72
        max_y = 186

            #Normalisation des coordonnées
        new_x = 1000 * ((new_x - 256*min_x) / (256*max_x - 256*min_x))
        new_y = 1000 * ((new_y - 256*min_y) / (256*max_y - 256*min_y))

            #Création du point
        point = Point(new_x, new_y, tick)

        return point



    @staticmethod
    def  load_data_from_csv(file_path):
        """Permet de créer une liste des 9 trajectoires situées dans un fichier csv"""
        trajectoires = []

        data = pd.read_csv(file_path)

        #print(min_max_values)

        for i in range(10):
            points = []
            # Iloc permet d'accéder à un dataframe de façon numérique
            for _, row in data.iloc[1:].iterrows(): #data.iloc[1:] pour enlever la première ligne du csv de la traj

                # Coordonnées
                x = row.get(f'x{i}', None)   # Si non présent None
                y = row.get(f'y{i}', None)
                # Vecs
                vec_x = row.get(f'vec_x{i}', 0)  # Si non présent 0
                vec_y = row.get(f'vec_y{i}', 0)
                #Tick
                tick = row.get("tick", 0)

                if x is not None and x >= 66 and y >=73 and y is not None:  
                    # Crée un point seulement si les coordonnées x et y existent
                    pt = DataManager._create_point(x, y, vec_x, vec_y, tick)
                    if(pt.get_coords()[0] >= 0 and pt.get_coords()[1] >= 0):
                        points.append(pt)

            traj = Trajectoire(i, points)
            trajectoires.append(traj)
        return trajectoires

    @staticmethod
    def cutFromDate(trajectoires):
        earlys = []
        mids = []
        ends = []
        for trajectoire in trajectoires:
            early = []
            mid = []
            end = []
            for i in range(len(trajectoire.get_all_points())):
                if i < 1200:
                    early.append(trajectoire.get_all_points()[i])
                elif i < 2400:
                    mid.append(trajectoire.get_all_points()[i])
                else:
                    end.append(trajectoire.get_all_points()[i])
            trajEarly = Trajectoire(trajectoire.player_id, early)
            trajMid = Trajectoire(trajectoire.player_id, mid)
            trajEnd = Trajectoire(trajectoire.player_id, end)

            earlys.append(trajEarly)
            mids.append(trajMid)
            ends.append(trajEnd)
        return earlys, mids, ends



    @staticmethod
    def export_trajectories_to_json(trajectoires, file_path):
        """Exporte les trajectoires dans un fichier JSON spécifié"""
        # Préparation des données à exporter
        data_to_export = [
            {
                'player_id': traj.player_id,
                'points': [{'x': point.x, 'y': point.y, 'tick': point.tick} for point in traj.points]
            }
            for traj in trajectoires
        ]
        # Exportation dans le fichier JSON
        with open(file_path, 'w') as f:
            json.dump(data_to_export, f, indent=4)
    
    @staticmethod
    def load_traj_from_json(file_path):
        trajectoires = []
        
        # Ouvrir le fichier JSON et charger les données
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        # Parcours des trajectoires dans les données
        for traj_data in data:
            player_id = traj_data['player_id']
            points = []

            # Parcours des points de chaque trajectoire
            for point_data in traj_data['points']:
                x = float(point_data["x"])
                y = float(point_data["y"])
                tick = float(point_data["tick"])
                point = Point(x, y, tick)
                points.append(point)

            
            # Création de la trajectoire
            traj = Trajectoire(player_id, points)
            trajectoires.append(traj)

        return trajectoires

    @staticmethod
    def load_trajs_from_json(file_path):
        trajectoires = []
        with open(file_path, 'r') as f:
            data = json.load(f)
        for traj_data in data:
            player_id = traj_data['player_id']
            points = [Point(float(pt["x"]), float(pt["y"]), float(pt["tick"])) for pt in traj_data['points']]
            trajectoires.append(Trajectoire(player_id, points))
        return trajectoires

    @staticmethod
    def export_patterns_to_json(patterns, dest_path):
        data_to_export = [
            {
                'count': pattern[0],
                'points': [{'x': point[0], 'y': point[1]} for point in pattern[1]]
            }
            for pattern in patterns
        ]
        # Exportation dans le fichier JSON
        with open(dest_path, 'w') as f:
            json.dump(data_to_export, f, indent=4)

    @staticmethod
    def load_patterns_from_json(file_path):
        patterns = []
        
        # Ouvrir le fichier JSON et charger les données
        with open(file_path, 'r') as f:
            data = json.load(f)
            i=0
            for pattern in data:
                i+=1
                print(f"Traitement du {i}ème pattern")
                count = pattern['count']
                points = []
                for point in pattern['points']:
                    x = float(point["x"])
                    y = float(point["y"])
                    points.append((x, y))
                patterns.append((count ,points))
        return patterns