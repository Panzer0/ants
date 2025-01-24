from flask import Flask, request, jsonify
from backend.ACO import ACO
from backend.data_loader import DataLoader

app = Flask(__name__)

@app.route("/solve", methods=["POST"])
def solve_tsp():
    data = request.json

    # Oczekiwane parametry
    n_ants = data.get("n_ants", 20)
    n_iterations = data.get("n_iterations", 100)
    decay = data.get("decay", 0.1)
    alpha = data.get("alpha", 1.0)
    beta = data.get("beta", 2.0)
    tsp_file = data.get("tsp_file", "att48.tsp.gz")

    # Wczytanie danych
    loader = DataLoader()
    loader.read_tsp_file(tsp_file)
    distances = loader.get_distance_matrix()

    # Algorytm mrówkowy
    aco = ACO(
        distances=distances,
        n_ants=n_ants,
        n_iterations=n_iterations,
        decay=decay,
        alpha=alpha,
        beta=beta,
    )
    best_path, best_distance = aco.solve()

    # Wynik zwrócony jako JSON
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

if __name__ == "__main__":
    app.run(debug=True)
