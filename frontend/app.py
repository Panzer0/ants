from flask import Flask, render_template, request, jsonify, send_file
from backend.api.aco_api import solve_tsp, visualize

# App instance
app = Flask(__name__, template_folder="templates", static_folder="static")

# Default values
default_values = {
    "ants": 20,
    "iterations": 100,
    "decay": 0.1,
    "alpha": 1.0,
    "beta": 2.0
}

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html", default_values=default_values)

@app.route("/solve", methods=["POST"])
def solve():
    return solve_tsp()

@app.route("/visualize", methods=["POST"])
def visualize_route():
    return visualize()

if __name__ == "__main__":
    app.run(debug=True)
