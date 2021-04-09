from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']

# Solution
traversal_path = []
traversal_graph = {}

class Queue():
    def __init__(self):
        self.queue = []

    def enqueue(self, value):
        self.queue.append(value)

    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return

    def size(self):
        return len(self.queue)

def path_traverser():
    global traversal_path

    while True:
        next_move = try_neighbors()

        while next_move:
            traversal_path.append(next_move)
            next_move = try_neighbors()

        nearest_empty_path = find_nearest_empty_path(player.current_room)

        if nearest_empty_path is None:
            break

        traversal_path += nearest_empty_path

        for direction in nearest_empty_path:
            player.travel(direction)


def try_neighbors():
    global traversal_graph
    directions = {"n", "s", "e", "w"}
    next_direction = None

    for direction in directions:
        traversal_graph.setdefault(player.current_room.id, {'n': '?', 's': '?', 'e': '?', 'w': '?'})
        if traversal_graph[player.current_room.id][direction] is not "?":
            continue

        last_room = player.current_room
        player.travel(direction)

        if update_rooms(direction, last_room, player.current_room):
            next_direction = direction
            player.travel(get_opposite_direction(direction))

    if next_direction:
        player.travel(next_direction)

    return next_direction


def update_rooms(direction, last_room, current_room):
    global traversal_graph

    if last_room is current_room:
        traversal_graph[current_room.id][direction] = None
        return False

    else:
        traversal_graph.setdefault(current_room.id, {'n': '?', 's': '?', 'e': '?', 'w': '?'})
        traversal_graph[last_room.id][direction] = current_room.id
        traversal_graph[current_room.id][get_opposite_direction(direction)] = last_room.id
        return True


def get_opposite_direction(direction):
    if direction is "s":
        return "n"
    elif direction is "n":
        return "s"
    elif direction is "e":
        return "w"
    elif direction is "w":
        return "e"
    else:
        return


def find_nearest_empty_path(current):
    global traversal_graph
    queue = Queue()
    queue.enqueue(current.id)
    visited = {}

    while queue.size() > 0:
        room = queue.dequeue()
        visited.setdefault(room, [])

        for (key, value) in traversal_graph[room].items():
            if value is None:
                continue

            if value is '?':
                return visited[room]
            else:
                if value not in visited:
                    visited.setdefault(value, visited[room].copy())
                    visited[value].append(key)
                    queue.enqueue(value)

    return

# bfs from yesterday, add weighted edges? fucking dijkstra
# though, I probably cannot edit the graph itself
# possibly A* and a heuristic like distance from an exit, I do have the coords,
# though they do not tell you where the exit is up front
# fuck me
# def path_traversal(graph, start, end):
#     visited = []
#     queue = collections.deque([[start]])

    # if start == end:
    #     return

    # while queue:
    #     path = queue.popleft()
    #     node = path[-1]

        # if node not in visited:
        #     neighbors = graph[node]

            # for neighbor in neighbors:
            #     new_path = list(path)
            #     new_path.append(neighbor)
            #     queue.append(new_path)

                # if neighbor == end:
                #     return new_path

            # visited.append(node)

    # return

# TRAVERSAL TEST
path_traverser()
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
