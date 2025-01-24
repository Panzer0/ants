from flask import Flask, request, jsonify, send_file
from matplotlib import pyplot as plt

from backend.aco import ACO
from backend.data_loader import DataLoader
from backend.visualiser import Visualizer
import io

app = Flask(__name__)


@app.route("/solve", methods=["POST"])
def solve_tsp():
    data = request.json

    n_ants = data.get("n_ants", 20)
    n_iterations = data.get("n_iterations", 100)
    decay = data.get("decay", 0.1)
    alpha = data.get("alpha", 1.0)
    beta = data.get("beta", 2.0)
    tsp_file = data.get("tsp_file", "att48.tsp.gz")

    loader = DataLoader()
    loader.read_tsp_file(tsp_file)
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

    visualizer = Visualizer(loader.get_coordinates())
    img = io.BytesIO()
    visualizer.plot_route(best_path)
    plt.savefig(img, format='png')
    img.seek(0)

    response = {
        "best_path": best_path,
        "best_distance": best_distance,
        "parameters": {
            "n_ants": n_ants,
            "n_iterations": n_iterations,
            "decay": decay,
            "alpha": alpha,
            "beta": beta,
        },
    }

    return jsonify(response)


@app.route("/visualize", methods=["POST"])
def visualize():
    data = request.json
    tsp_file = data.get("tsp_file", "att48.tsp.gz")
    best_path = data.get("best_path")

    loader = DataLoader()
    loader.read_tsp_file(tsp_file)

    visualizer = Visualizer(loader.get_coordinates())
    img = io.BytesIO()
    visualizer.plot_route(best_path)
    plt.savefig(img, format="png")
    img.seek(0)

    return send_file(img, mimetype="image/png")


if __name__ == "__main__":
    app.run(debug=True)
