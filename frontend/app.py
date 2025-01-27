from flask import Flask, render_template, request, jsonify, send_file
from backend.api.aco_api import solve_tsp, visualize

# App instance
app = Flask(__name__, template_folder="templates", static_folder="static")


@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/solve", methods=["POST"])
def solve():
    try:
        result = solve_tsp()
        return result
    except Exception as e:
        print("Error in solve:", str(e))
        return jsonify({"error": str(e)}), 500

@app.route("/visualize", methods=["POST"])
def visualize_route():
    if request.is_json:
        return visualize()
    return jsonify({"error": "Invalid request"}), 400

if __name__ == "__main__":
    app.run(debug=True, threaded=False)