import math

class City:
    def __init__(self, name, coordinates):
        self.name = name
        self.coordinates = coordinates


def calculate_distance(city1, city2):
    lon1, lat1 = city1.coordinates
    lon2, lat2 = city2.coordinates
    # Using Haversine formula to calculate distance between two coordinates
    radius = 6371  # Radius of the Earth in kilometers
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) * math.sin(dlat / 2) + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(
        dlon / 2) * math.sin(dlon / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = radius * c
    return distance


def depth_first_search(city_list, start_index, goal_index):
    stack = [(start_index, [start_index])]  # Stack to keep track of visited cities and paths
    visited = set()  # Set to keep track of visited cities

    while stack:
        current_city, path = stack.pop()
        visited.add(current_city)

        if current_city == goal_index:
            return path

        for neighbor in range(len(city_list)):
            if neighbor not in visited:
                stack.append((neighbor, path + [neighbor]))

    return None


# Example usage:
cities = [
    City("City A", [0.0, 0.0]),
    City("City B", [1.0, 1.0]),
    City("City C", [2.0, 2.0]),
    City("City D", [3.0, 3.0]),
    City("City E", [4.0, 4.0])
]

start_index = 0  # Index of the starting city
goal_index = 3   # Index of the goal city

shortest_path = depth_first_search(cities, start_index, goal_index)

if shortest_path:
    path_names = [cities[index].name for index in shortest_path]
    print("Shortest path:", path_names)
else:
    print("No path found!")
