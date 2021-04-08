from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# my imports
import collections

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
map_file = "maps/test_loop_fork.txt"
# map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

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
