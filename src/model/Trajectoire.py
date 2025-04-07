#import time

import numpy as np

from model.Point import Point

class Trajectoire:
    """Classe qui gère les trajectoires"""

    def __init__(self, player_id, points):
        self.player_id = player_id
        self.points = points



    def sub_trajectories(self):
        """
        Divise la trajectoire en segments (pour compression ou analyse).
        Chaque segment est défini par une paire de points consécutifs de la trajectoire.
        
        @return: Une liste de segments. Chaque segment est une paire de tuples ((x1, y1), (x2, y2)).
        """
        segments = []  # Initialise une liste vide pour stocker les segments

        # Parcourt tous les points de la trajectoire sauf le dernier (car on regarde des paires de points)
        for i in range(len(self.points) - 1):
            # Point de départ du segment
            start = self.points[i]

            # Point de fin du segment
            end = self.points[i + 1]

            # Récupère les coordonnées des points de départ et de fin sous forme de tuple (x, y)
            segment = (start.get_coords(), end.get_coords())

            # Ajoute le segment à la liste des segments
            segments.append(segment)

        # Retourne la liste complète des segments
        return segments



    def get_partial_segments(self, start_index=0, end_index=None):
        """
        Retourne une partie des segments entre deux indices donnés.
        
        @param start_index: Indice de départ pour les segments (inclusif).
        @param end_index: Indice de fin pour les segments (exclusif). Si None, va jusqu'à la fin.
        @return: Liste des segments sélectionnés.
        
        @raise ValueError: Si les indices sont hors des limites de la trajectoire.
        """
        if end_index is None:
            end_index = len(self.points) - 1
        if start_index < 0 or end_index > len(self.points) - 1:
            raise ValueError("Indices hors des limites de la trajectoire.")
        segments = self.sub_trajectories()
        return segments[start_index:end_index]


    def get_segments(self, start_index, end_index):
        """
        Retourne une liste des segments de la trajectoire sous forme de tuples (vecteur, longueur).
        
        @return: Liste des segments, chaque segment étant un tuple (vecteur, longueur).
        """
        segments = []
        for i in range(start_index, end_index):
            debut = self.points[i].get_coords()
            fin = self.points[i + 1].get_coords()
            vec = np.array(fin) - np.array(debut)
            length = np.linalg.norm(vec)
            segments.append(((self.points[i].get_coords(), self.points[i + 1].get_coords()), length))
        return segments



    def get_point(self, index):
        """
        Retourne le point à un indice donné de la trajectoire.
        
        @param index: L'indice du point à récupérer.
        @return: Le point à l'indice spécifié.
        """
        return self.points[index]


    def get_all_points(self):
        """
        Retourne tout les points de la trajectoire.
        
        @return: La liste de points self.points.
        """
        return self.points
    
    def to_list(self):
        """Convertit la trajectoire en une liste de tuples (x, y)."""
        return [point.get_coords() for point in self.points]


    def __str__(self):
        """
        Retourne une chaîne de caractères représentant la trajectoire.
        
        @return: La chaîne de caractères représentant la trajectoire du joueur.
        """
        return f"Trajectoire joueur {self.player_id} : {len(self.points)} points"