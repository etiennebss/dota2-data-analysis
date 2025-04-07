import os
import time
import json

from utils.data_manager import DataManager
from algorithms.PrefixSpanAnalyser import PrefixSpanAnalyser
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

def main():
    dest_dir = os.path.join(os.path.dirname(__file__), '..', 'data', 'results', 'prefixSpan', 'early', 'supp20')
    os.makedirs(dest_dir, exist_ok=True)
    json_files = [f for f in os.listdir(dest_dir) if f.endswith('.json')]
    

    if not json_files:
        print("Pas de fichier a charger : faire tourner mainPrefixSpan.py")
        return

    patterns = DataManager.load_patterns_from_json(dest_dir + '/' +  json_files[0])
    patterns.append(DataManager.load_patterns_from_json(dest_dir + '/' +  json_files[0]))
    print("Fin de l'import des pattern")

    i=0
    for count, traj_a_afficher in patterns:
        i+=1
        print(f"Affichage Matplot du {i}ème pattern")
        x_coords = [point[0] for point in traj_a_afficher]
        y_coords = [point[1] for point in traj_a_afficher]
        
        map_image = mpimg.imread(os.path.join(os.path.dirname(__file__),"map.jpg"))

        plt.figure("Trajectoire Pattern", figsize=(10,6))

        plt.imshow(map_image, extent=[-50, 1090, -45, 1015])

        plt.plot(x_coords, y_coords, marker='o', label=f'Pattern numéro {i} avec {count} occurences', linestyle='-')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.title(f'Pattern')
        plt.legend()
        plt.grid(True)
        plt.show()

if __name__ == "__main__":
    main()
    