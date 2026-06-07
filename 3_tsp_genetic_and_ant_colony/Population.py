from random import randint, sample
import sys
from Location import Location


class Population:
    def __init__(self, starting_position: Location = None):
        self.position: Location = starting_position
        self.locations_available: list[Location] = []
        self.order_visited: list[Location] = []
        self.STARTING_POSITION = starting_position
        self.MAX_POSSIBLE_MUTATIONS = 1
        self.total_distance = 0
        self.fitness = 0

        if starting_position:
            self.order_visited.append(starting_position)

    def add_multiple_locations(self, list_multiple_locations: list[list[Location]]):
        for list_with_data in list_multiple_locations:
            if len(list_with_data) != 3:
                print("ERROR! List given to location has wrong number of elements")
                sys.exit(-1)

            id_node, x, y = list_with_data
            location = Location(id_node, x, y)
            self.locations_available.append(location)

            if self.position is None:
                self.position = location
                self.STARTING_POSITION = location
                self.order_visited.append(location)
                self.locations_available.remove(location)


    def _move(self, destination):
        if (destination != self.STARTING_POSITION and
            destination in self.order_visited):
            print("ERROR! Location already visited")
            sys.exit(-1)

        self.total_distance += self.position.distance_to(destination)
        self.order_visited.append(destination)
        self.position = destination

    def get_random_solution(self):

        while self.locations_available:
            len_locations = len(self.locations_available) - 1
            random_index = randint(0, len_locations)
            destination: Location = self.locations_available[random_index]

            self._move(destination)
            self.locations_available.remove(destination)

        self._move(self.STARTING_POSITION)

    def mutate(self):
        path_length = len(self.order_visited)

        random_index_1, random_index_2 = sample(range(1, path_length - 1), 2)

        start_cut = min(random_index_1, random_index_2)
        end_cut = max(random_index_1, random_index_2)

        node_a = self.order_visited[start_cut - 1]
        node_b = self.order_visited[start_cut]
        node_c = self.order_visited[end_cut]
        node_d = self.order_visited[end_cut + 1]

        # reverses a part of it
        self.order_visited[start_cut:end_cut + 1] = self.order_visited[start_cut:end_cut + 1][::-1]

        # Calculate distances
        removed_dist = node_a.distance_to(node_b) + node_c.distance_to(node_d)
        added_dist = node_a.distance_to(node_c) + node_b.distance_to(node_d)

        self.total_distance = self.total_distance - removed_dist + added_dist

        # self.calculate_total_distance()

        return

    def breed(self, partner) -> 'Population':
        start_node = self.order_visited[0]
        child = Population(start_node)

        parent1_genes = self.order_visited[1:-1]
        parent2_genes = partner.order_visited[1:-1]

        size_genome = len(parent1_genes)

        random_index_1, random_index_2 = sample(range(0, size_genome - 1), 2)

        start_pos = min(random_index_1, random_index_2)
        end_pos = max(random_index_1, random_index_2)

        child_genes = [None] * size_genome
        p1_subset_set = set()

        # parts from p1
        for i in range(start_pos, end_pos + 1):
            gene = parent1_genes[i]
            child_genes[i] = gene
            p1_subset_set.add(gene)

        # parts from p2
        remaining_genes = (gene for gene in parent2_genes if gene not in p1_subset_set)

        # fill empty spaces
        for i in range(size_genome):
            if child_genes[i] is None:
                child_genes[i] = next(remaining_genes)

        child.order_visited = [start_node] + child_genes + [start_node]
        child.locations_available = []
        child.calculate_total_distance()

        return child

    def calculate_total_distance(self):
        self.total_distance = 0
        for i in range(len(self.order_visited) - 1):
            self.total_distance += (
                self.order_visited[i].distance_to(self.order_visited[i + 1])
            )

    def clone(self):
        new_map = Population()
        new_map.position = self.position
        new_map.order_visited = self.order_visited[:]
        new_map.total_distance = self.total_distance
        new_map.fitness = self.fitness
        return new_map


    def calculate_fitness(self, calculated_fitness):
        if self.total_distance == 0:
            print("ERROR! Distance is 0")
            sys.exit(-1)

        calculated_fitness += 1
        if calculated_fitness == 250000:
            print("WARNING: THRESHOLD OF CALCULATIONS PASSED\n")

        self.fitness = round((1 / self.total_distance) * 100000000, 2) # Scale it so it's representative with total distance

        return calculated_fitness

    def __str__(self):
        # locations_str = [str(loc) for loc in self.locations_available]
        # visited_locations_str = [str(loc) for loc in self.visited_locations]
        return (
                # f"Map: {locations_str} \n\n"
                # f"Visited locations: {visited_locations_str}\n\n"
                # f"Current position: {self.position}\n"
                f"Total distance: {self.total_distance}")
