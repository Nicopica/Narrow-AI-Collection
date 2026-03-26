DATA_PATH_SHORTEST_PATH = "Assignment1/data/spain_map.txt"
START = "Malaga"
END = "Valladolid"

def greedy_best_first(current_city, final_target, graph, straight_line):
    route = []
    distance_travelled = 0

    while current_city != final_target:

        # Sort based on the SLD to Valladolid
        ordered_neighbours = sorted(graph.edges[current_city], key=
                                lambda tup:
                                    straight_line[tup[0]])

        current_city = ordered_neighbours[0][0]

        if current_city in route: # Repeating city
            print("Entered a loop.")
            break

        distance_travelled += ordered_neighbours[0][1]
        route.append(current_city)

    return route, distance_travelled


def a_search(current_city, final_target, graph, straight_line):
    path = []
    total_distance = 0
    visited = set()

    # Frontier format: [Total Estimated Cost (f), Cost So Far (g), Current City, Path Taken]
    frontier = [[straight_line[current_city], 0, current_city, [current_city]]]

    while current_city != final_target:

        frontier.sort(key=lambda x: x[0])  # sort based on total_cost

        total_cost, total_distance, current_city, path = frontier.pop(0)

        if current_city in visited:
            continue

        visited.add(current_city)

        next_steps = [
            [total_distance + dist + straight_line[neighbor],  # Estimated Cost
             total_distance + dist,                            # Total Cost to that city
             neighbor,                                         # Current City
             path + [neighbor]]                                # Path Taken
            for neighbor, dist in graph.edges[current_city]
            if neighbor not in visited
        ]

        frontier.extend(next_steps)
    return path[1:], total_distance


def the_dumb_algorithm(current_city, graph, final_target):
    route = []
    last_city = ""

    while current_city != final_target:

        ordered_neighbours = sorted(graph.edges[current_city], key=lambda distance: distance[1])

        next_city = ordered_neighbours[0][0]

        if next_city == last_city and len(ordered_neighbours) > 2:  # Avoid going back and forth
            next_city = ordered_neighbours[1][0]

        last_city = current_city
        current_city = next_city


        if current_city in route: # Repeating city in bigger loop
            print("Entered a loop.")
            break

        route.append(current_city)

    return route
