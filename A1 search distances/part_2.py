import math
import csv

# Function to read city data from a CSV file
def read_data(file_name):
    city_data = []
    with open(file_name, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            city_data.append(row)
    return city_data

# Function to calculate the distance matrix
def calc_distance_matrix(city_data):
    dist_matrix = []
    # Iterate over each city in the city_data list
    for i in range(len(city_data)):
        distances = []
        # Get the latitude and longitude of the current city
        lat = float(city_data[i]['latitude'])
        lon = float(city_data[i]['longitude'])
        # Iterate over each city again to calculate distances
        for j in range(len(city_data)):
            lat2 = float(city_data[j]['latitude'])
            lon2 = float(city_data[j]['longitude'])
            # Calculate the Euclidean distance between the two cities
            dist = math.sqrt((lat2 - lat) ** 2 + (lon2 - lon) ** 2)
            # Appending the distance to the list
            distances.append(dist)
        # Further Appending the list to the matrix
        dist_matrix.append(distances)
    return dist_matrix

# DFS
def depth_first_search(city_data, distan_matrix, current_city, visiting, distance, path):
    # If all cities have been visited, return the current distance and path
    if len(visiting) == len(city_data):
        return distance, path

    min_dist = float('inf')
    min_path = None

    for i in range(len(city_data)):
        if i not in visiting:
            next_city = city_data[i]['name']
            new_distance = distance + distan_matrix[current_city][i]
            visiting.add(i)
            new_path = path + [next_city]
            result = depth_first_search(
                city_data, distan_matrix, i, visiting.copy(), new_distance, new_path)
            if result[0] < min_dist:
                # Update the minimum distance and corresponding path
                min_dist = result[0]
                min_path = result[1]
            visiting.remove(i)

    return min_dist, min_path

# BFS
def breadth_first_search(city_data, distan_matrix):
    # Initialize the queue with starting cities and paths
    queue = [(i, [city_data[i]['name']]) for i in range(len(city_data))]
    # Initialize the minimum distance with infinity and path as None
    min_distance = float('inf')
    min_path = None

    while queue:
        current_city, path = queue.pop(0)
        # If all cities have been visited, calculate the distance of the path
        if len(path) == len(city_data):
            distance = calculate_path_distance(
                path, distan_matrix, city_data)
            # Update the minimum distance and corresponding path if a shorter path is found
            if distance < min_distance:
                min_distance = distance
                min_path = path
        else:
            # Explore neighboring cities
            for i in range(len(city_data)):
                if city_data[i]['name'] not in path:
                    next_city = city_data[i]['name']
                    new_path = path + [next_city]
                    queue.append((i, new_path))

    return min_distance, min_path

# To calculate the total distance of path (It is a helper function)
def calculate_path_distance(path, distan_matrix, city_data):
    distance = 0
    # Iterate over each consecutive pair of cities in the path
    for i in range(len(path) - 1):
        # Get the name of the first & second city
        city1 = path[i]
        city2 = path[i + 1]
        # Find the indices of the cities in the city_data list
        ind1 = next((index for index, city in enumerate(
            city_data) if city['name'] == city1), None)
        ind2 = next((index for index, city in enumerate(
            city_data) if city['name'] == city2), None)
        # If both indices are valid, add the distance between the cities to the total distance
        if ind1 is not None and ind2 is not None:
            distance += distan_matrix[ind1][ind2]
    return distance


# Main
# Set city data and distance matrix
city_data = read_data('city_data_50.csv')
distan_matrix = calc_distance_matrix(city_data)

# Call Depth-first search
starting_city = city_data[0]['name']
visiting = set([0])
distance, path = depth_first_search(
    city_data, distan_matrix, 0, visiting, 0, [starting_city])
print("\nDepth-first search:")
print("Shortest distance is -", distance)
print("Shortest path is:", ' --> '.join(path))

# Call Breadth-first search
distance, path = breadth_first_search(city_data, distan_matrix)
print("\nBreadth-first search:")
print("Shortest distance is -", distance)
print("Shortest path is:", ' --> '.join(path))
print("\n")
