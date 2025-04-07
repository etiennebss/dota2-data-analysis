import numpy as np
from model.Point import Point

class KMeans:
    def __init__(self, k=3, time_weight=0.2, max_iters=100, tol=1e-4):
        """
        Implémente le clustering K-Means pour les trajectoires en prenant en compte la dimension temporelle.

        :param k: Nombre de clusters.
        :param max_iters: Nombre maximal d'itérations.
        :param time_weight: Poids du temps dans la distance (plus grand = plus d'importance pour le temps).
        :param tol: Seuil d'arrêt basé sur le déplacement moyen des centroids.
        """
        self.k = k
        self.max_iters = max_iters
        self.time_weight = time_weight
        self.tol = tol
        self.centroids = None
        self.clusters = []

    def _weighted_distance(self, p1, p2):
        """
        Calcule la distance pondérée entre deux points en prenant en compte l'espace et le temps.
        
        :param p1: Tuple (x, y, tick) ou objet avec x, y, tick.
        :param p2: Tuple (x, y, tick) ou objet avec x, y, tick.
        :return: Distance pondérée.
        """
        # Vérifier si p1 et p2 sont des objets avec des attributs
        if hasattr(p1, 'x') and hasattr(p1, 'y') and hasattr(p1, 'tick'):
            x1, y1, t1 = p1.x, p1.y, p1.tick
        else:
            x1, y1, t1 = p1  # Tuple (x, y, tick)

        if hasattr(p2, 'x') and hasattr(p2, 'y') and hasattr(p2, 'tick'):
            x2, y2, t2 = p2.x, p2.y, p2.tick
        else:
            x2, y2, t2 = p2  # Tuple (x, y, tick)
        spatial_dist = np.linalg.norm(np.array([x1, y1]) - np.array([x2, y2]))  
        temporal_dist = abs(t1 - t2)  

        #return (spatial_dist + self.time_weight * temporal_dist)
        # donner un time_weight entre 0 et 1, correspond à un pourcentage
        return 1-((1-self.time_weight)*spatial_dist + self.time_weight * temporal_dist)

    def fit(self, data):

        data = np.array(data)
        if data.ndim != 2 or data.shape[1] != 3:
            raise ValueError("Les données doivent être sous forme de tableau 2D avec 3 colonnes (x, y, tick).")
        
        # Initialisation des centroids à partir de k points aléatoires dans les données
        indices = np.random.choice(len(data), self.k)
        self.centroids = data[indices]

        for iteration in range(self.max_iters):
            # Créer une liste pour les clusters
            clusters = [[] for _ in range(self.k)]
            
            # Attribution des points aux centroids les plus proches
            for point in data:
                distances = np.linalg.norm(self.centroids - point, axis=1)
                closest_centroid = np.argmin(distances)
                clusters[closest_centroid].append(point)

            # Mise à jour des centroids
            new_centroids = []
            for cluster in clusters:
                if cluster:  # Éviter la division par zéro si un cluster est vide
                    new_centroids.append(np.mean(cluster, axis=0))
                else:
                    new_centroids.append(np.zeros(3))  # Si le cluster est vide, remettre les centroids à zéro

            #Conversion en tableau 2D
            new_centroids = np.array(new_centroids)
            new_centroids = new_centroids.reshape(self.k, 3)

            # Calcul de la distance entre les centroids
            centroid_shift = np.linalg.norm(self.centroids - new_centroids, axis=1).mean()
            
            # Si le déplacement des centroids est inférieur à la tolérance, on arrête
            if centroid_shift < self.tol:
                break
            
            # Mise à jour des centroids pour la prochaine itération
            self.centroids = new_centroids

        self.clusters = clusters
        return clusters



    def predict(self, points):
        """
        Retourne l'index du cluster pour chaque point donné.

        :param points: Liste de tuples (x, y, tick).
        :return: Liste d'indices de clusters.
        """
        return [np.argmin([self._weighted_distance(p, c) for c in self.centroids]) for p in points]
    
    def prepare_data_for_prefixspan(self):
        """
        Prépare les clusters pour l'algorithme PrefixSpan

        :return: Liste de séquences ordonnées par tick, chaque séquence étant une liste de points.
        """
        prepared_data = []

        # Parcours de chaque cluster
        count = 0
        for centroid in self.centroids:
            if centroid[0] == 0 and centroid[1] == 0:
                continue
            point = Point(int(round(centroid[0]/100)*100), int(round(centroid[1]/100)*100), count)
            prepared_data.append(point)
            count +=1

        return prepared_data

    def comparatorHelper(self, data):
        self.fit(data)
        #ici créer la donnée pertiante pour coparer les poids