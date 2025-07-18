import heapq
import copy

q = []
visited = set()
min_mismatch_count = float('inf')


def compare(s, g):
    for i in range(len(s)):
        for j in range(len(s[0])):
            if s[i][j] != g[i][j]:
                return 0
    return 1


def huerestic(s, g):
    mismatch_count = 0
    for i in range(len(s)):
        for j in range(len(s[0])):
            if s[i][j] != g[i][j]:
                mismatch_count += 1
    return mismatch_count


def find_pos(s):
    for i in range(len(s)):
        for j in range(len(s[0])):
            if s[i][j] == 0:
                return [i, j]


def up(s):
    pos = find_pos(s)
    row = pos[0]
    col = pos[1]
    new_state = copy.deepcopy(s)
    if row > 0:
        new_state[row][col] = new_state[row - 1][col]
        new_state[row - 1][col] = 0
    return new_state


def down(s):
    pos = find_pos(s)
    row = pos[0]
    col = pos[1]
    new_state = copy.deepcopy(s)
    if row < 2:
        new_state[row][col] = new_state[row + 1][col]
        new_state[row + 1][col] = 0
    return new_state


def left(s):
    pos = find_pos(s)
    row = pos[0]
    col = pos[1]
    new_state = copy.deepcopy(s)
    if col > 0:
        new_state[row][col] = new_state[row][col - 1]
        new_state[row][col - 1] = 0
    return new_state


def right(s):
    pos = find_pos(s)
    row = pos[0]
    col = pos[1]
    new_state = copy.deepcopy(s)
    if col < 2:
        new_state[row][col] = new_state[row][col + 1]
        new_state[row][col + 1] = 0
    return new_state


def generate_children(s, g):
    global q
    global visited
    global min_mismatch_count

    def add_to_queue(new_state):
        mismatch_count = huerestic(new_state, g)
        new_state_tuple = tuple(map(tuple, new_state))  # Convert list to tuple
        if new_state_tuple not in visited and mismatch_count <= min_mismatch_count:
            heapq.heappush(q, (mismatch_count, new_state))

    new_state = up(s)
    add_to_queue(new_state)

    new_state = down(s)
    add_to_queue(new_state)

    new_state = left(s)
    add_to_queue(new_state)

    new_state = right(s)
    add_to_queue(new_state)


def search(g):
    c = 0
    global q
    global visited
    global min_mismatch_count
    while q:
        c += 1
        _, curr_state = heapq.heappop(q)
        if compare(curr_state, g) == 1:
            print("found")
            exit()
        else:
            generate_children(curr_state, g)
            visited.add(tuple(map(tuple, curr_state)))
        print(c)

    if not q:
        print("Not found")


def main():
    global q
    global min_mismatch_count
    s = [[1, 2, 3],
         [8, 0, 4],
         [7, 6, 5]]

    g = [[2, 8, 1],
         [0, 4, 3],
         [7, 6, 5]]

    q.append((huerestic(s, g), s))
    search(g)


if __name__ == "__main__":
    main()
