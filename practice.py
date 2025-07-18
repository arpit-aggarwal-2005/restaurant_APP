from itertools import permutations

def calculate_cost(path, distances, start):

    total_cost = 0
    current_city = start
    for next_city in path:
        total_cost += distances[current_city][next_city]
        current_city = next_city
    total_cost += distances[current_city][start]  # Return to the starting city
    return total_cost

def tsp_minimum_cost(distances, start):

    all_neighbours = [i for i in range(len(distances)) if i != start]
    all_paths = permutations(all_neighbours)

    min_cost = float('inf')

    for path in all_paths:
        path_cost = calculate_cost(path, distances, start)
        if path_cost < min_cost:
            min_cost = path_cost

    return min_cost

def main():
    distances = [[0,10,15,20],[10,0,35,25],[15,35,0,30],[20,25,30,0]]
    start_city = 0
    print("Minimum cost for TSP:", tsp_minimum_cost(distances, start_city))

if __name__ == "__main__":
    main()
