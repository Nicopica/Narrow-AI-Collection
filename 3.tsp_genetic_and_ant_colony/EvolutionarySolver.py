from random import randint, sample
from Assignment3.Population import Population


class EvolutionarySolver:
    def __init__(self, data, maps_per_generation, total_generations, mutation_probability, top_preserved, tournament_size):
        self.MAPS_PER_GENERATION = maps_per_generation
        self.MUTATION_PROBABILITY = mutation_probability
        self.TARGET_GENERATIONS = total_generations
        self.TOP_PRESERVED = top_preserved
        self.TOURNAMENT_SIZE = tournament_size
        self.maps_with_location: list[Population] = []
        self.generation = 0
        self.calculated_fitness = 0
        self.history = []
        self.best_solution = None
        self._generate_maps(data)

    def _generate_maps(self, data):
        for i in range(self.MAPS_PER_GENERATION):
            map_locations = Population()
            map_locations.add_multiple_locations(data)
            map_locations.get_random_solution()
            self.calculated_fitness = map_locations.calculate_fitness(self.calculated_fitness)
            self.maps_with_location.append(map_locations)

    def run(self):
        print(f"Started calculating {self.TARGET_GENERATIONS} generations. {self.MAPS_PER_GENERATION} maps per generations "
              f"and top {self.TOP_PRESERVED} preserved.")

        while self.generation < self.TARGET_GENERATIONS:

            self.next_generation()

            best_map = max(self.maps_with_location, key= lambda x: x.fitness)

            self.history.append((best_map.fitness, best_map.total_distance))

            if (self.generation + 1) % 25 == 0:
                # ids_in_order = [loc.id_loc for loc in best_map.visited_locations]
                print(f"Processing Generation {self.generation + 1}/{self.TARGET_GENERATIONS} "
                      f"| Current Best Distance: {best_map.total_distance} | Fitness: {best_map.fitness}")
                      # f"Order for solution: {ids_in_order}\n")

            self.generation += 1
        self.best_solution = self.give_best_solution()

    def give_best_solution(self):
        return max(self.maps_with_location, key= lambda x: x.fitness)

    def next_generation(self):
        top_selection = sorted(self.maps_with_location, key=lambda x: x.fitness, reverse=True)[:self.TOP_PRESERVED]

        new_population = []

        for elite in top_selection:
            new_population.append(elite.clone())

        while len(new_population) < self.MAPS_PER_GENERATION:
            parent_a = self.tournament_selection()
            parent_b = self.tournament_selection()

            child = parent_a.breed(parent_b)

            # could add a check for stagnation to make mutation probability higher
            if randint(0, 100) < self.MUTATION_PROBABILITY:
                child.mutate()

            self.calculated_fitness = child.calculate_fitness(self.calculated_fitness)

            new_population.append(child)

        self.maps_with_location = new_population

    def tournament_selection(self):
        competitors = sample(self.maps_with_location, self.TOURNAMENT_SIZE)
        return max(competitors, key= lambda x: x.fitness)

    def __str__(self):
        output = ""
        for map_location in self.maps_with_location:
            output += str(map_location)
            output += "\n----\n"
        return output



