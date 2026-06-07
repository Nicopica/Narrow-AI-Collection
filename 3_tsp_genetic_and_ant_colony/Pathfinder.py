import random
import sys
from Location import Location


class Pathfinder:
    def __init__(self, locations, start_location: Location):
        self.locations_available = locations.copy()
        self.STARTING_POSITION = start_location
        self.order_visited = [start_location]
        self.visited_ids = {start_location.id_loc}
        self.total_distance = 0
        self.fitness = 0
        self.current_location = start_location

    def build_tour(self, pheromones, distances, alpha, beta):
        self.locations_available = [loc for loc in self.locations_available if
                                    loc.id_loc != self.STARTING_POSITION.id_loc]

        while self.locations_available:
            self._visit_next_location(pheromones, distances, alpha, beta)

        self._move(self.STARTING_POSITION)

    def _visit_next_location(self, pheromones, distances, alpha, beta):
        neighbors = []
        weights = []

        for neighbor in self.locations_available:
            edge = (self.current_location.id_loc, neighbor.id_loc)

            phero = pheromones.get(edge, 1.0)
            dist = distances.get(edge, 1.0)
            eta = 1.0 / dist if dist > 0 else 1.0

            prob_value = (phero ** alpha) * (eta ** beta)

            neighbors.append(neighbor)
            weights.append(prob_value)

        next_node = random.choices(neighbors, weights=weights, k=1)[0]
        """Return a k sized list of population elements chosen with replacement.
        """

        self._move(next_node)

    def _move(self, destination):

        dist_to_next = self.current_location.distance_to(destination)

        self.total_distance += dist_to_next
        self.current_location = destination
        self.order_visited.append(destination)
        self.visited_ids.add(destination.id_loc)

        if destination in self.locations_available:
            self.locations_available.remove(destination)

    def calculate_fitness(self, calculated_fitness):
        if self.total_distance == 0:
            print("ERROR! Distance is 0")
            sys.exit(-1)

        calculated_fitness += 1
        # if calculated_fitness == 250000:
        #     print("WARNING: THRESHOLD OF CALCULATIONS PASSED\n")

        self.fitness = round((1 / self.total_distance) * 100000000, 2)
        return calculated_fitness