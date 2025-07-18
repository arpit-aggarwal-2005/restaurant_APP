import heapq
import copy

priority_queue = []
visited_states = set()
min_mismatch_count = float('inf')


def compare_states(current_state, goal_state):
    for i in range(len(current_state)):
        for j in range(len(current_state[0])):
            if current_state[i][j] != goal_state[i][j]:
                return 0
    return 1


def heuristic_function(current_state, goal_state):
    mismatch_count = 0
    for i in range(len(current_state)):
        for j in range(len(current_state[0])):
            if current_state[i][j] != goal_state[i][j]:
                mismatch_count += 1
    return mismatch_count


def find_position(state):
    for i in range(len(state)):
        for j in range(len(state[0])):
            if state[i][j] == 0:
                return [i, j]


def move_up(state):
    position = find_position(state)
    row = position[0]
    col = position[1]
    new_state = copy.deepcopy(state)
    if row > 0:
        new_state[row][col] = new_state[row - 1][col]
        new_state[row - 1][col] = 0
    return new_state


def move_down(state):
    position = find_position(state)
    row = position[0]
    col = position[1]
    new_state = copy.deepcopy(state)
    if row < 2:
        new_state[row][col] = new_state[row + 1][col]
        new_state[row + 1][col] = 0
    return new_state


def move_left(state):
    position = find_position(state)
    row = position[0]
    col = position[1]
    new_state = copy.deepcopy(state)
    if col > 0:
        new_state[row][col] = new_state[row][col - 1]
        new_state[row][col - 1] = 0
    return new_state


def move_right(state):
    position = find_position(state)
    row = position[0]
    col = position[1]
    new_state = copy.deepcopy(state)
    if col < 2:
        new_state[row][col] = new_state[row][col + 1]
        new_state[row][col + 1] = 0
    return new_state


def generate_child_states(state, goal_state):
    global priority_queue
    global visited_states
    global min_mismatch_count

    def add_to_queue(new_state):
        mismatch_count = heuristic_function(new_state, goal_state)
        new_state_tuple = tuple(map(tuple, new_state))  # Convert list to tuple
        if new_state_tuple not in visited_states and mismatch_count <= min_mismatch_count:
            heapq.heappush(priority_queue, (mismatch_count, new_state))

    new_state = move_up(state)
    add_to_queue(new_state)

    new_state = move_down(state)
    add_to_queue(new_state)

    new_state = move_left(state)
    add_to_queue(new_state)

    new_state = move_right(state)
    add_to_queue(new_state)


def search(goal_state):
    c = 0
    global priority_queue
    global visited_states
    global min_mismatch_count
    while priority_queue:
        c += 1
        _, current_state = heapq.heappop(priority_queue)
        if compare_states(current_state, goal_state) == 1:
            print("Found")
            exit()
        else:
            generate_child_states(current_state, goal_state)
            visited_states.add(tuple(map(tuple, current_state)))
        print(c)

    if not priority_queue:
        print("Not found")


def main():
    global priority_queue
    global min_mismatch_count
    initial_state = [[1, 2, 3],
                     [8, 0, 4],
                     [7, 6, 5]]

    goal_state = [[2, 8, 1],
                  [0, 4, 3],
                  [7, 6, 5]]

    priority_queue.append((heuristic_function(initial_state, goal_state), initial_state))
    search(goal_state)


if __name__ == "__main__":
    main()
