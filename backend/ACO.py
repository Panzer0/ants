import numpy as np
from typing import List, Tuple
import random


class ACO:
    def __init__(
        self,
        distances: np.ndarray,
        n_ants: int = 20,
        n_iterations: int = 10000,
        decay: float = 0.1,
        alpha: float = 1.0,  # pheromone importance
        beta: float = 2.0,  # distance importance
    ):
        self.distances = distances
        self.n_cities = len(distances)
        self.n_ants = n_ants
        self.n_iterations = n_iterations
        self.decay = decay
        self.alpha = alpha
        self.beta = beta

        self.pheromone = np.ones((self.n_cities, self.n_cities))
        self.best_path = None
        self.best_distance = float("inf")

    def solve(self) -> Tuple[List[int], float]:
        """Run the ACO algorithm and return the best path and its length"""
        for iteration in range(self.n_iterations):
            ant_paths = self._generate_all_paths()

            self._update_pheromone(ant_paths)

            iteration_best_path = min(
                ant_paths, key=lambda x: self._calculate_path_distance(x)
            )
            iteration_best_dist = self._calculate_path_distance(
                iteration_best_path
            )

            if iteration_best_dist < self.best_distance:
                self.best_distance = iteration_best_dist
                self.best_path = iteration_best_path

        return self.best_path, self.best_distance

    def _generate_all_paths(self) -> List[List[int]]:
        all_paths = []
        for _ in range(self.n_ants):
            path = self._generate_path()
            all_paths.append(path)
        return all_paths

    def _generate_path(self) -> List[int]:
        path = [random.randint(0, self.n_cities - 1)]
        while len(path) < self.n_cities:
            next_city = self._select_next_city(path)
            path.append(next_city)
        return path

    def _select_next_city(self, path: List[int]) -> int:
        current = path[-1]
        unvisited = list(set(range(self.n_cities)) - set(path))

        if not unvisited:
            return path[0]

        pheromone = np.array([self.pheromone[current][j] for j in unvisited])
        distance = np.array([self.distances[current][j] for j in unvisited])

        distance = np.where(distance == 0, 1e-10, distance)

        probability = (pheromone**self.alpha) * (
            (1.0 / distance) ** self.beta
        )
        probability = probability / probability.sum()

        next_city = np.random.choice(unvisited, p=probability)
        return next_city

    def _calculate_path_distance(self, path: List[int]) -> float:
        distance = 0
        for i in range(len(path)):
            from_city = path[i]
            to_city = path[(i + 1) % self.n_cities]
            distance += self.distances[from_city][to_city]
        return distance

    def _update_pheromone(self, ant_paths: List[List[int]]):
        self.pheromone *= 1.0 - self.decay

        for path in ant_paths:
            distance = self._calculate_path_distance(path)
            for i in range(len(path)):
                from_city = path[i]
                to_city = path[(i + 1) % self.n_cities]
                self.pheromone[from_city][to_city] += 1.0 / distance
                self.pheromone[to_city][from_city] += 1.0 / distance


if __name__ == "__main__":
    from data_loader import DataLoader

    loader = DataLoader()
    loader.read_tsp_file("att48.tsp.gz")
    distances = loader.get_distance_matrix()

    aco = ACO(
        distances=distances,
        n_ants=20,
        n_iterations=100,
        decay=0.1,
        alpha=1.0,
        beta=2.0,
    )

    best_path, best_distance = aco.solve()
    print(f"Best path found: {best_path}")
    print(f"Best distance: {best_distance}")
