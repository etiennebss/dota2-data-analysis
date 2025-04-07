import os
from utils.data_manager import DataManager
from algorithms.PrefixSpanAnalyser import PrefixSpanAnalyser

def run_prefix_span(source_dir, result_dir, support):
    os.makedirs(result_dir, exist_ok=True)
    
    kmeans_files = [f for f in os.listdir(source_dir) if f.endswith('.json')]
    if not kmeans_files:
        print(f"[WARNING] Aucun fichier JSON trouvé dans {source_dir}. Passez cette étape.")
        return

    trajectoires_par_joueur = []
    for json_file_name in kmeans_files:
        json_file_path = os.path.join(source_dir, json_file_name)
        trajectoires = DataManager.load_trajs_from_json(json_file_path)
        for i, trajectoire in enumerate(trajectoires):
            if len(trajectoires_par_joueur) <= i:
                trajectoires_par_joueur.append([])
            trajectoires_par_joueur[i].append(trajectoire)

    equipe1, equipe2 = [], []
    for trajectoires_joueur in trajectoires_par_joueur:
        for trajectoire in trajectoires_joueur:
            points = [(p.get_coords()[0], p.get_coords()[1]) for p in trajectoire.get_all_points() if p.get_coords()[:2] != (None, None)]
            if trajectoire.player_id <= 4:
                equipe1.append(points)
            else:
                equipe2.append(points)
    
    if equipe1:
        export_prefix_span(equipe1, os.path.join(result_dir, "prefixSpanResultsEquipe1.json"), "Equipe 1", support)
    if equipe2:
        export_prefix_span(equipe2, os.path.join(result_dir, "prefixSpanResultsEquipe2.json"), "Equipe 2", support)

def export_prefix_span(trajectoires, result_file_path, equipe_name, support):
    psa = PrefixSpanAnalyser(support, trajectoires).export()
    DataManager.export_patterns_to_json(psa, result_file_path)
    print(f"Export réussi pour {equipe_name}: {result_file_path}")

def main():
    base_dir = os.path.dirname(__file__)
    processed_dir = os.path.join(base_dir, '..', 'data', 'results', 'kmeans')
    results_dir = os.path.join(base_dir, '..', 'data', 'results', 'prefixSpan')
    
    for stage in ["mid", "end"]:
        support = 12
        print(f"Traitement en cours pour {stage} avec un support de {support}...")
        run_prefix_span(os.path.join(processed_dir, stage), os.path.join(results_dir, stage, f"supp{support}"), support)

if __name__ == "__main__":
    main()
