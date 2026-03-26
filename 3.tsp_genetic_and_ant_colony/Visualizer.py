import matplotlib.pyplot as plt


def plot_results(best_map, progress_history, calculated_fitness):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    x = [loc.x for loc in best_map.order_visited]
    y = [loc.y for loc in best_map.order_visited]

    ax1.plot(x, y, 'o-r', markersize=4, linewidth=1, label='Route')

    ax1.plot(x[0], y[0], 'go', markersize=10, label='Start')

    ax1.set_title(f"Best Route Found (Distance: {best_map.total_distance:.2f})")
    ax1.set_xlabel("X Coordinate")
    ax1.set_ylabel("Y Coordinate")
    ax1.legend()
    ax1.grid(True)



    fitness_values = [item[0] for item in progress_history]
    distance_values = [item[1] for item in progress_history]

    ax2.plot(distance_values, label='Distance')
    ax2.plot(fitness_values, label='Fitness')
    ax2.legend()

    ax2.set_title(f"Genetic Algorithm Progress | Fitness calculations: {calculated_fitness:,}")
    ax2.set_xlabel("Generation")
    ax2.set_ylabel("Fitness improvement & Distance reduction")
    ax2.grid(True)

    plt.tight_layout()
    plt.show()