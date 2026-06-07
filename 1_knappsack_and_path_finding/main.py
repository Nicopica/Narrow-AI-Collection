from Graph import Graph
from knapsack import *
from shortest_path import *
from utils import *


def main():
    print_knapsack_results()
    print_shortest_path_results()


def print_shortest_path_results():
    # Read and clean data
    data = readData(DATA_PATH_SHORTEST_PATH)
    data = [list(line.strip().split()) for line in data[1:] if line.strip()]

    # Split into real distances and SLR
    connections = filter_by_size(data, 3)
    straight_line = dict(map(lambda e: (e[0], int(e[1])), filter_by_size(data, 2)))

    graph = Graph()

    alphabetically_sorted = sorted(connections, key=lambda name: name[0])

    # Add to graph
    [graph.add_connection(route[0], route[1], int(route[2])) for route in alphabetically_sorted]

    # MALAGA(Start Node) to VALLADOLID (Goal Node).
    final_route_greedy, distance_travelled_greedy= greedy_best_first(START, END, graph, straight_line)

    print(f"Greedy best first result\n"
          f"Route taken from {START} to {END}: {final_route_greedy}\n"
          f"Total distance travelled: {distance_travelled_greedy}km\n")

    final_route_a_search, distance_travelled_a_search = a_search(START, END, graph, straight_line)

    print(f"A search result\n"
          f"Route taken from {START} to {END}: {final_route_a_search}\n"
          f"Total distance travelled: {distance_travelled_a_search}km")


def print_knapsack_results():
    data = readData(DATA_PATH_KNAPSACK)
    data = [list(map(int, line.strip().split())) for line in data[1:] if line.strip()]

    tree = Node(0, 0, 0)
    tree = build_binary_tree(tree, data)

    best_value_dfs, last_dfs = dfs(tree, MAX_CAPACITY)
    path_to_parent_dfs = get_path_to_root(last_dfs)
    print(f"DFS Output:\n"
          f" Best value: {best_value_dfs}\n"
          f" Weight taken: {weight_accumulated(path_to_parent_dfs)}/{MAX_CAPACITY}\n"
          f" Path taken:\n"
          f"{formatted_string(path_to_parent_dfs)}\n")

    best_value_bfs, last_bfs = bfs(tree, MAX_CAPACITY)
    path_to_parent_bfs = get_path_to_root(last_bfs)
    print(f"\nBFS Output:\n"
          f" Best value: {best_value_bfs}\n"
          f" Weight taken: {weight_accumulated(path_to_parent_bfs)}/{MAX_CAPACITY}\n"
          f" Path taken: \n"
          f"{formatted_string(path_to_parent_bfs)}\n")

    # Extra solution

    tree_only_with_solutions = Node(0, 0, 0)
    tree_only_with_solutions = build_binary_tree_only_possible_solutions(tree_only_with_solutions, data)

    result = get_all_leaves(tree_only_with_solutions)
    sorted_result = sorted(result, key=lambda node: node.benefit, reverse=True)
    result_to_string = list(map(str, sorted_result))
    first_option = formatted_string_accumulative_left(get_path_to_root(sorted_result[0]))
    second_option = formatted_string_accumulative_left(get_path_to_root(sorted_result[1]))
    print(f"\nOnly with possible solutions output:\n"
          f" All possibilities: {result_to_string[0:50]}\n"
          f" Best possibility:\n"
          f"{first_option}\n\n"
          f" Second best possibility:\n"
          f"{second_option}")


if __name__ == '__main__':
    main()
