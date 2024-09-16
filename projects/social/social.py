from random import randint
from collections import deque
import timeit

class User:
    def __init__(self, name):
        self.name = name

class SocialGraph:
    def __init__(self):
        self.last_id = 0
        self.users = {}
        self.friendships = {}

    def add_friendship(self, user_id, friend_id):
        """
        Creates a bi-directional friendship
        """
        if user_id == friend_id:
            print("WARNING: You cannot be friends with yourself")
        elif friend_id in self.friendships[user_id] or user_id in self.friendships[friend_id]:
            print("WARNING: Friendship already exists")
        else:
            self.friendships[user_id].add(friend_id)
            self.friendships[friend_id].add(user_id)

    def add_user(self, name):
        """
        Create a new user with a sequential integer ID
        """
        self.last_id += 1  # automatically increment the ID to assign the new user
        self.users[self.last_id] = User(name)
        self.friendships[self.last_id] = set()

    def populate_graph(self, num_users, avg_friendships):
        """
        Takes a number of users and an average number of friendships
        as arguments

        Creates that number of users and a randomly distributed friendships
        between those users.

        The number of users must be greater than the average number of friendships.
        """
        # Reset graph
        self.last_id = 0
        self.users = {}
        self.friendships = {}
        # !!!! IMPLEMENT ME
        if num_users < avg_friendships:
            raise ValueError("Invalid arguments! Number of Users must be greater than Avg number of friendships.")

        # Add users
        for i in range(num_users):
            self.add_user(f"Test User {i+1}")

        # Create friendships
        for i in range(len(self.users.items())):
            # for _ in range(randint(avg_friendships - 1, avg_friendships + 1)):
            for _ in range(avg_friendships):
                self.add_friendship(i + 1, randint(1, len(self.users.items())))

    def get_all_social_paths(self, user_id):
        """
        Takes a user's user_id as an argument

        Returns a dictionary containing every user in that user's
        extended network with the shortest friendship path between them.

        The key is the friend's ID and the value is the path.
        """
        beg = timeit.default_timer()

        out = []  # Note that this is a dictionary, not a set
        # !!!! IMPLEMENT ME
        for node in self.friendships.keys():
            if node != user_id:
                # needed for first pass solutions
                # out.append(self.get_all_social_paths_util_dfs(user_id, node))
                shortest_path = self.get_paths_util_bfs(user_id, node)
                if shortest_path is not None:
                    out.append(shortest_path)

        # needed for first pass solutions
        # filtered_out = []
        # for paths in visited:
        #     if len(paths) != 0:
        #         filtered_out.append(min(paths, key=len))
        end = timeit.default_timer()
        print(f"timeit = {end - beg}")
        # needed for first pass solutions
        # return filtered_out
        return out

    # Best version so far
    def get_paths_util_bfs(self, start, end):
        visited = []
        queue = deque([[start]])

        if start == end:
            return

        while queue:
            path = queue.popleft()
            node = path[-1]

            if node not in visited:
                neighbors = self.friendships[node]

                for neighbor in neighbors:
                    new_path = list(path)
                    new_path.append(neighbor)
                    queue.append(new_path)

                    if neighbor == end:
                        return new_path

                visited.append(node)

        return

    # first pass solution
    def get_all_social_paths_util_dfs(self, start, end, path = []):
        path = path + [start]
        if start == end:
            return [path]

        if not self.friendships[start]:
            return []

        paths = []
        for node in self.friendships[start]:
            if node not in path:
                new_paths = self.get_all_social_paths_util_dfs(node, end, path)
                for new_path in new_paths:
                    paths.append(new_path)

        return paths

    # first pass solution
    def get_all_social_paths_util_bfs(self, start, end):
        nodes = deque()
        nodes.append([start])
        all_possible_paths = []
        while nodes:
            prev = nodes.popleft()
            last = prev[-1]
            if last == end:
                all_possible_paths.append(prev)

            for node in self.friendships[last]:
                if node not in prev:
                    new_path = prev + [node]
                    nodes.append(new_path)

        return all_possible_paths

if __name__ == '__main__':
    sg = SocialGraph()
    sg.populate_graph(10, 2)
    # for testing scalability (hangs at 10,000) I might do a 3rd pass but this seems efficient enough to turn in
    # sg.populate_graph(4000, 100)
    print(sg.friendships)
    connections = sg.get_all_social_paths(1)
    print(connections)
