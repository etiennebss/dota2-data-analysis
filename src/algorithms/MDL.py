import numpy as np

from model.Trajectoire import Trajectoire
from model.Point import Point


class MDL:
    """Classe permettant d'exécuter l'algorithme MDL sur une trajectoire"""

    def _perpendicular_distance(self, l1, l2):
        """
        Calcule la distance perpendiculaire entre deux segments de longueur l1 et l2.
        
        @param l1: Longueur du premier segment.
        @param l2: Longueur du second segment.
        @return: La distance perpendiculaire entre les segments.
        """
        if l1 + l2 == 0:
            return 0
        return (l1**2 + l2**2) / (l1 + l2)



    def _angular_distance(self, segment_i, segment_j):
        """
        Calcule la distance angulaire entre deux segments.
        
        @param segment_i: Le premier segment sous forme de tuple ((x1, y1), (x2, y2)).
        @param segment_j: Le second segment sous forme de tuple ((x3, y3), (x4, y4)).
        @return: La distance angulaire entre les deux segments.
        """
        (x1, y1), (x2, y2) = segment_i
        (x3, y3), (x4, y4) = segment_j

        vec1 = np.array([x2 - x1, y2 - y1])
        vec2 = np.array([x4 - x3, y4 - y3])

        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)

        if norm1 == 0 or norm2 == 0:
            return 0

        cos_theta = np.dot(vec1, vec2) / (norm1 * norm2)
        theta = np.arccos(np.clip(cos_theta, -1, 1))
        theta_deg = np.degrees(theta)

        if 0 <= theta_deg < 90:
            return norm2 * np.sin(theta)

        return norm2


    def _calculer_distances(self, segments):
        """
        Calcule les distances perpendiculaires et angulaires entre les segments de la trajectoire.
        
        @return: Deux listes : distances perpendiculaires et distances angulaires.
        """
        distances_perp = []
        distances_theta = []

        for i in range(len(segments) - 1):
            seg1, l1 = segments[i]
            seg2, l2 = segments[i + 1]

            distances_perp.append(self._perpendicular_distance(l1, l2))
            distances_theta.append(self._angular_distance(seg1, seg2))

        return distances_perp, distances_theta



    def _mdl_cost(self, trajectoire, start_index, end_index):
        """
        Calcule le coût MDL d'un segment allant du point à l'index start au point à l'index end.
        
        @param start_index: Indice de départ du segment.
        @param end_index: Indice de fin du segment.
        @return: Le coût MDL du segment.
        """
        segments = trajectoire.get_segments(start_index, end_index)
        distances_perp, distances_theta = self._calculer_distances(segments)
        l_h = 0
        for _, length in segments:
            if length > 0:
                l_h += np.log2(length)
        l_d_h = 0
        for d in distances_perp + distances_theta:
            if d > 0:
                l_d_h += np.log2(d)

        return l_h + l_d_h



    def traj_partitionning(self, trajectoire):
        """
        Effectue le découpage de la trajectoire en segments en utilisant l'algorithme de partitionnement MDL.
        
        @return: Une liste de points représentant les partitions de la trajectoire.
        """
        part = []

        if trajectoire.get_all_points() :
            part.append(trajectoire.get_point(0))
            start_index = 1
            length = 1

            #tdebut = time.time()

            while(start_index + length < len(trajectoire.get_all_points())):

                #tinter = time.time()
                #print(str(start_index + length) + "/" + str(len(trajectoire.points)), str(int(tinter - tdebut)) + "s")

                current_index = start_index + length
                cost_part = self._mdl_cost(trajectoire, start_index, current_index)
                cost_no_part = self._mdl_cost(trajectoire, start_index, current_index-1)    
                if start_index == current_index-1:
                    length += 1

                elif cost_part > cost_no_part :
                    part.append(trajectoire.get_point(current_index))
                    start_index = current_index
                    length = 1

                else:
                    length += 1

            part.append(trajectoire.get_point(-1))
            
        return part


    def __str__(self):
        return "Instance d'algo MDL"
