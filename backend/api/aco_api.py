from flask import Flask, request, jsonify, send_file
from matplotlib import pyplot as plt
import matplotlib
from backend.ACO import ACO
from backend.data_loader import DataLoader
from backend.visualiser import TSPVisualizer
import io
import os

matplotlib.use('Agg')
plt.ioff()

def solve_tsp():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400

        n_ants = int(data.get("n_ants", 20))
        n_iterations = int(data.get("n_iterations", 100))
        decay = float(data.get("decay", 0.1))
        alpha = float(data.get("alpha", 1.0))
        beta = float(data.get("beta", 2.0))
        tsp_file = data.get("tsp_file", "att48.tsp.gz")

        current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        tsp_file_path = os.path.join(current_dir, tsp_file)

        if not os.path.exists(tsp_file_path):
            return jsonify({"error": f"File not found: {tsp_file_path}"}), 404

        loader = DataLoader()
        loader.read_tsp_file(tsp_file_path)
        distances = loader.get_distance_matrix()

        aco = ACO(
            distances=distances,
            n_ants=n_ants,
            n_iterations=n_iterations,
            decay=decay,
            alpha=alpha,
            beta=beta,
        )
        best_path, best_distance = aco.solve()

        response_data = {
            "best_path": [int(x) for x in best_path],
            "best_distance": int(best_distance),
            "parameters": {
                "n_ants": n_ants,
                "n_iterations": n_iterations,
                "decay": decay,
                "alpha": alpha,
                "beta": beta,
            },
        }
        return jsonify(response_data)

    except Exception as e:
        print(f"Error in solve_tsp: {str(e)}")
        return jsonify({"error": str(e)}), 500


def visualize():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400

        tsp_file = data.get("tsp_file", "att48.tsp.gz")
        best_path = data.get("best_path")

        if not best_path:
            return jsonify({"error": "No best_path provided"}), 400

        current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        tsp_file_path = os.path.join(current_dir, tsp_file)

        loader = DataLoader()
        loader.read_tsp_file(tsp_file_path)

        visualizer = TSPVisualizer(loader.get_coordinates())
        img = io.BytesIO()
        visualizer.plot_route(best_path)
        plt.savefig(img, format='png', bbox_inches='tight')
        plt.close()
        img.seek(0)

        return send_file(
            img,
            mimetype='image/png',
            as_attachment=False
        )

    except Exception as e:
        print(f"Error in visualize: {str(e)}")
        return jsonify({"error": str(e)}), 500