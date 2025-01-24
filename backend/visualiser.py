import matplotlib.pyplot as plt

from backend.aco import ACO
from backend.data_loader import DataLoader


class Visualizer:
    def __init__(self, coordinates):
        self.coordinates = coordinates

    def plot_route(self, path):
        coords = [(self.coordinates[i + 1]) for i in path]
        coords.append(coords[0])

        x_coords, y_coords = zip(*coords)

        plt.figure(figsize=(10, 10))
        plt.plot(x_coords, y_coords, "b-", linewidth=0.7)
        plt.plot(x_coords, y_coords, "ro")

        for i, (x, y) in enumerate(zip(x_coords[:-1], y_coords[:-1])):
            plt.annotate(
                f"City {path[i] + 1}",
                (x, y),
                xytext=(5, 5),
                textcoords="offset points",
            )

        plt.title("TSP Route")
        plt.xlabel("X Coordinate")
        plt.ylabel("Y Coordinate")
        plt.grid(True)
        plt.show()


if __name__ == "__main__":
    handler = DataLoader()
    handler.read_tsp_file("att48.tsp.gz")

    aco = ACO(handler.get_distance_matrix())
    best_path, best_distance = aco.solve()

    visualizer = Visualizer(handler.get_coordinates())
    visualizer.plot_route(best_path)
