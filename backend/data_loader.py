import gzip
import re
import numpy as np


class DataLoader:
    def __init__(self):
        self.dimension = 0
        self.coordinates = {}
        self.distances = None

    def read_tsp_file(self, file_path):
        with gzip.open(file_path, "rt") as f:
            content = f.read()

        self.parse_dimension(content)

        coord_section = content.split("NODE_COORD_SECTION")[1].strip()
        lines = coord_section.split("\n")

        for line in lines:
            line = line.strip()
            if line == "EOF":
                break
            self.parse_line(line)

        self._calculate_distance_matrix()

    def parse_line(self, line):
        parts = line.split()
        if len(parts) == 3:
            city_id = int(parts[0])
            x, y = float(parts[1]), float(parts[2])
            self.coordinates[city_id] = (x, y)

    def parse_dimension(self, content):
        dimension_match = re.search(r"DIMENSION\s*:\s*(\d+)", content)
        if dimension_match:
            self.dimension = int(dimension_match.group(1))

    def _calculate_distance_matrix(self):
        self.distances = np.zeros((self.dimension, self.dimension))

        for i in range(1, self.dimension + 1):
            for j in range(1, self.dimension + 1):
                if i != j:
                    x1, y1 = self.coordinates[i]
                    x2, y2 = self.coordinates[j]
                    distance = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
                    self.distances[i - 1][j - 1] = round(distance)

    def get_coordinates(self):
        return self.coordinates

    def get_distance_matrix(self):
        return self.distances

    def get_distance(self, city1, city2):
        return self.distances[city1 - 1][city2 - 1]


if __name__ == "__main__":
    handler = DataLoader()
    handler.read_tsp_file("att48.tsp.gz")
    print(handler.distances)
