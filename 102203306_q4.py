def calculate_cost(nodes_data, condition, weight=1):
    cost = {}
    if 'AND' in condition:
        and_nodes = condition['AND']
        path_a = ' AND '.join(and_nodes)
        pathA = sum(nodes_data.get(node, 0) + weight for node in and_nodes)
        cost[path_a] = pathA

    if 'OR' in condition:
        or_nodes = condition['OR']
        path_b = ' OR '.join(or_nodes)
        pathB = min(nodes_data.get(node, 0) + weight for node in or_nodes)
        cost[path_b] = pathB
    return cost

def update_cost(nodes_data, conditions, weight=1):
    main_nodes = list(conditions.keys())
    main_nodes.reverse()
    least_cost = {}
    for key in main_nodes:
        condition = conditions[key]
        print(key, ':', conditions[key], '>>>', calculate_cost(nodes_data, condition, weight))
        c = calculate_cost(nodes_data, condition, weight)
        nodes_data[key] = min(c.values())
        least_cost[key] = c
    return least_cost

def shortest_path(start, updated_cost, nodes_data):
    path = start
    if start in updated_cost.keys():
        min_cost = min(updated_cost[start].values())
        key = list(updated_cost[start].keys())
        values = list(updated_cost[start].values())
        index = values.index(min_cost)

        next_nodes = key[index].split()
        if len(next_nodes) == 1:
            start = next_nodes[0]
            path += '<--' + shortest_path(start, updated_cost, nodes_data)

        else:
            path += '<--(' + key[index] + ') '

            start = next_nodes[0]
            path += '[' + shortest_path(start, updated_cost, nodes_data) + ' + '

            start = next_nodes[-1]
            path += shortest_path(start, updated_cost, nodes_data) + ']'

    return path

nodes_data = {'A': -1, 'B': 6, 'C': 12, 'D': 10, 'E': 4, 'F': 4}

conditions = {
    'A': {'AND': ['B', 'C'], 'OR': ['D']},
    'B': {'OR': ['G', 'H']},
    'D': {'AND': ['E', 'F']}
}

weight = 1

print('Updated Cost:')
updated_cost = update_cost(nodes_data, conditions, weight=1)
print('*' * 75)
print('Shortest Path:\n', shortest_path('A', updated_cost, nodes_data))
