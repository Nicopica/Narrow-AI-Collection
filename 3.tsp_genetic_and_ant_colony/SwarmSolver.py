import sys
from Assignment3.Pathfinder import Pathfinder
from Assignment3.Location import Location


class SwarmSolver:
    def __init__(self, data, ants_per_generation=50, total_generations=200, alpha=1.0, beta=4.0, evaporation_rate=0.5,
                 q=1000):
        self.ANTS_PER_GENERATION = ants_per_generation
        self.TARGET_GENERATIONS = total_generations
        self.ALPHA = alpha
        self.BETA = beta
        self.RHO = evaporation_rate
        self.Q = q

        self.locations = []
        self._add_locations(data)

        self.pheromones = {}
        self.distances = {}
        self._initialize_pheromones()

        self.generation = 0
        self.calculated_fitness = 0
        self.history = []
        self.best_solution = None

    def _add_locations(self, list_multiple_locations: list[list[int]]):
        for location in list_multiple_locations:
            if len(location) != 3:
                print("ERROR! List given to location has wrong number of elements")
                sys.exit(-1)
            id_node, x, y = location
            new_location = Location(id_node, x, y)
            self.locations.append(new_location)

    def _initialize_pheromones(self):
        for loc_a in self.locations:
            for loc_b in self.locations:
                if loc_a.id_loc != loc_b.id_loc:
                    self.pheromones[(loc_a.id_loc, loc_b.id_loc)] = 1.0

                    dist = loc_a.distance_to(loc_b)
                    self.distances[(loc_a.id_loc, loc_b.id_loc)] = dist

    def run(self):
        print(
            f"Started calculating {self.TARGET_GENERATIONS} generations. {self.ANTS_PER_GENERATION} ants per generation.")

        start_node = next((loc for loc in self.locations if loc.id_loc == 1), self.locations[0])

        while self.generation < self.TARGET_GENERATIONS:
            self.next_generation(start_node)
            self.generation += 1

    def next_generation(self, start_node):
        ants = []

        for _ in range(self.ANTS_PER_GENERATION):
            ant = Pathfinder(self.locations, start_location=start_node)
            ant.build_tour(self.pheromones, self.distances, self.ALPHA, self.BETA)
            self.calculated_fitness = ant.calculate_fitness(self.calculated_fitness)
            ants.append(ant)

        best_ant = max(ants, key=lambda x: x.fitness)

        if self.best_solution is None or best_ant.fitness > self.best_solution.fitness:
            self.best_solution = best_ant

        self._update_pheromones(ants)

        self.history.append((self.best_solution.fitness, self.best_solution.total_distance))

        # if (self.generation + 1) % 25 == 0:
        print(f"Processing Generation {self.generation + 1}/{self.TARGET_GENERATIONS} "
              f"| Current Best Distance: {best_ant.total_distance} | Fitness: {best_ant.fitness}")

    def _update_pheromones(self, ants):
        # evaporate pheromones
        for edge in self.pheromones:
            self.pheromones[edge] *= (1.0 - self.RHO)

        # add more pheromones
        for ant in ants:
            pheromone_drop = self.Q / ant.total_distance
            for i in range(len(ant.order_visited) - 1):
                u = ant.order_visited[i].id_loc
                v = ant.order_visited[i + 1].id_loc
                if (u, v) in self.pheromones:
                    self.pheromones[(u, v)] += pheromone_drop