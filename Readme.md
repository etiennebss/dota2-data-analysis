# 🧠 Analyse de données de trajectoires dans Dota 2

Projet réalisé dans le cadre de la Licence 3 Informatique à l’Université de Caen.

**Auteurs :**  
@etiennebss , @Lebonvieuxjack, @DoguetThomas et Romain Moalic

---

## 🎯 Objectif

Ce projet a pour but d’analyser les trajectoires des héros dans une partie de **Dota 2**. À partir de données brutes issues de plusieurs parties, nous appliquons une série d’étapes de traitement, d’extraction de patterns et de clustering pour mieux comprendre les comportements des joueurs.

---

## 🧰 Technologies & Librairies

- Python 3
- `numpy`
- `pandas`
- `matplotlib`
- `prefixSpan`

---

## 🛠️ Sur les machines de l'université

Avant de lancer le projet sur les machines de l’université:

pip install pandas==1.5.3  
pip install prefixSpan

⚠️ Attention : Il est important de préciser la version de `pandas` pour éviter tout problème de compatibilité avec `numpy` ou `matplotlib`

---

## 🚀 Lancement du projet

Tous les fichiers exécutables se trouvent dans le dossier `src`, lancez les depuis la *racine du projet*.

### Lancer l’interface principale :

python3 src/main.py

### Exécuter un fichier spécifique :

python3 src/nom_du_fichier.py

---

## 📁 Structure du projet

### `data/`
- `raw/` :  
  Contient les fichiers CSV d’origine. Chaque fichier représente les coordonnées (`xi`, `vec_xi`, `yi`, `vec_yi`) des joueurs, indexées par tick.
  
- `processed/` :  
  Données transformées au format JSON avec trajectoires normalisées.

- `results/` :  
  Résultats des algorithmes (MDL, KMeans, PrefixSpan).

### `src/`
- `algorithms/` :  
  Implémentations des différents algorithmes :
  - MDL (Minimum Description Length)
  - KMeans / KMedoids
  - PrefixSpan

- `model/` :  
  Définition des structures de données utilisées (trajectoires, points, etc.).

- `results/data_manager.py` :  
  Classe utilitaire pour la gestion des fichiers (chargement, sauvegarde, etc.).

- Fichiers exécutables :
  - `main*.py` : Traitement global sur l’ensemble des données.
  - `display*.py` : Affichage des résultats des algorithmes.
  - `compare*.py` : Comparaison des algorithmes selon différents paramètres.

---

## 🔍 Fonctionnalités principales

- **Normalisation** des trajectoires à partir des coordonnées brutes.
- **Segmentation** des trajectoires via l'approche **MDL**.
- **Clustering** des segments avec **KMeans**
- **Détection de motifs** comportementaux avec **PrefixSpan**.

---

## 📊 Visualisations

Des outils de visualisation avec **Matplotlib** sont inclus dans les scripts `display*.py` pour observer :
- Les trajectoires originales vs. segmentées
- Les clusters générés
- Les motifs extraits par PrefixSpan


