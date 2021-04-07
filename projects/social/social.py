from random import randint
from collections import deque

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
            for _ in range(randint(avg_friendships - 1, avg_friendships + 1)):
                self.add_friendship(i + 1, randint(1, len(self.users.items())))

    def dfs(graph, visited, node):
        if node not in visited:
            print(node)
            visited.add(node)
            for neighbor in graph[node]:
                dfs(visited, graph, neighbor)

    def get_all_social_paths(self, user_id):
        """
        Takes a user's user_id as an argument

        Returns a dictionary containing every user in that user's
        extended network with the shortest friendship path between them.

        The key is the friend's ID and the value is the path.
        """

        def dfs(graph, visited, node):
            if node not in visited:
                print(node)
                visited.add(node)
                for neighbor in graph[node]:
                    dfs(visited, graph, neighbor)

        visited = set()  # Note that this is a dictionary, not a set
        queue = deque()
        # !!!! IMPLEMENT ME
        dfs(self.friendships, visited, self.friendships[user_id])

        return visited


if __name__ == '__main__':
    sg = SocialGraph()
    sg.populate_graph(10, 2)
    print(sg.friendships)
    connections = sg.get_all_social_paths(1)
    print(connections)
