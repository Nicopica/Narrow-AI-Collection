from SwarmSolver import SwarmSolver
from utils import get_locations
from EvolutionarySolver import EvolutionarySolver
from Visualizer import plot_results


def main():
    all_locations = get_locations()

    genetic_algorithm = EvolutionarySolver(
                    data = all_locations,
                    maps_per_generation = 400,
                    total_generations = 300,
                    mutation_probability = 35,
                    top_preserved = 4,
                    tournament_size = 3
    )

    genetic_algorithm.run()
    plot_results(genetic_algorithm.best_solution, genetic_algorithm.history, genetic_algorithm.calculated_fitness)


    ant_colony = SwarmSolver(
        data=all_locations,
        ants_per_generation=100,
        total_generations=40,
        alpha=1.0,
        beta=6.0,
        evaporation_rate=0.7,
        q=1000
    )

    ant_colony.run()
    plot_results(ant_colony.best_solution, ant_colony.history, ant_colony.calculated_fitness)


if __name__ == '__main__':
    main()