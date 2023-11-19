import heapq

class Node:
    def __init__(self, position, cost, parent=None):
        self.position = position
        self.cost = cost
        self.parent = parent

    def __lt__(self, other):
        return self.cost < other.cost

def calc_total_cost(path, lmap):
    total_cost = 0
    for position in path:
        cost = lmap[position[0]][position[1]]

        if(position != start_pos):
            if(cost == 0):
                total_cost += 1
            else:
                total_cost += cost
            
    return total_cost

def astar(lmap, start, goal):
    rows, cols = len(lmap), len(lmap[0])
    directions = [(-1, 0), (0, -1), (1, 0), (0, 1)]

    start_node = Node(start, 0)
    goal_node = Node(goal, 0)

    open_set = [start_node]
    visited = set()

    while open_set:
        current_node = heapq.heappop(open_set)

        if current_node.position == goal_node.position:
            path = []
            while current_node:
                path.append(current_node.position)
                current_node = current_node.parent
            path.reverse()
            total_cost = calc_total_cost(path, lmap)
            return path, total_cost

        visited.add(current_node.position)

        for direction in directions:
            new_position = (current_node.position[0] + direction[0], current_node.position[1] + direction[1])

            if 0 <= new_position[0] < rows and 0 <= new_position[1] < cols and lmap[new_position[0]][new_position[1]] != -1:
                if new_position not in visited:
                    new_cost = current_node.cost + lmap[new_position[0]][new_position[1]]
                    new_node = Node(new_position, new_cost, current_node)
                    heapq.heappush(open_set, new_node)

    return None, None

def read_txt(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
        return lines
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None
    except Exception as e:
        print(f"Error reading the file: {e}")
        return None

def start_vars():

    map_size = []
    start_pos = []
    goal_pos = []
    lmap = None

    lines = read_txt('data.txt')

    if lines is not None:
        map_size = list(map(int,lines[0].split()))
        start_pos = list(map(int,lines[1].split()))
        lmap = [[None] * map_size[0] for _ in range(map_size[1])]

        for c in range(2,len(lines)):
            x = c-2
            items = list(map(int,lines[c].split()))
            
            for i in range(0,len(items)):
                lmap[x][i] = items[i]

    while not goal_pos:
        goal_input = input(f"Map size is {map_size}\nInsert final coords (example: '6 4'): ")
        goal_pos = list(map(int,goal_input.split()))

        if len(goal_pos) != 2:
            print("\nERROR: Invalid entry\n")
            goal_pos = []
        elif goal_pos[0] > map_size[0] or goal_pos[1] > map_size[1]:
            print("\nERROR: At least one given coord is bigger than map size\n")
            goal_pos = []
        elif goal_pos[0] < 0 or goal_pos[1] < 0:
            print("\nERROR: Coords should be greater or equal than 0\n")
            goal_pos = []

    return lmap, tuple(start_pos), tuple(goal_pos)

lmap, start_pos, goal_pos = start_vars()
final_path, final_total_cost = astar(lmap, start_pos, goal_pos)

if final_path is not None and final_total_cost is not None:
    print("\nResult:", final_total_cost, " ".join(f"{c}" for c in final_path))
else:
    print('\nImpossible.')