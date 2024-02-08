# CP468 Assignment 1 Part 2
# By Tara and Eesha

import csv
import math

# creating distance matrix of Euclidian distances between cities
distance_matrix = []
city_matrix = []

class City:
    def __init__ (self, name, desc, coordinate):
        self.name = name
        self.desc = desc
        self.coordinate = coordinate
    
    def distance_between(self, goal):
        y1 = self.coordinate[0]
        x1 = self.coordinate[1]
        y2 = goal.coordinate[0]
        x2 = goal.coordinate[1]
        euclidean = math.sqrt(pow((x2-x1), 2) + pow((y2-y1), 2))
        return euclidean

# read from the provided city data file
csv_file = open('city_data_50.csv')
csv_reader = csv.reader(csv_file, delimiter=',')

csv_file2 = open('city_data_50.csv')
csv_reader2 = list(csv.reader(csv_file2, delimiter=','))

line_count = 0
for row in csv_reader:
    if line_count == 0:
        # print(f'Column names are {", ".join(row)}')
        line_count += 1
    else:
        # print(f'\t{row[0]} has the description {row[1]} with a latitude of {row[2]} and a longitude of {row[3]}.')
        line_count += 1
        second_line_count = 0
        city_matrix.append(City(row[0], row[1], [float(row[2]), float(row[3])]))

        # distance_matrix[0].append(row[0])
        matrix_row = []
        for second in csv_reader2:
            if second_line_count == 0: #or second_line_count == line_count:
                second_line_count += 1
            else:
                # print('first:', row[0])
                # print('second:', second[0])
                # print(math.dist([float(row[2]), float(row[3])], [float(second[2]), float(second[3])]))

                # calculate Euclidian distance between the current city and all of the rest and add to array
                matrix_row.append(math.dist([float(row[2]), float(row[3])], [float(second[2]), float(second[3])]))
                second_line_count += 1
        # print(f'Second Processed {second_line_count} lines.')
        distance_matrix.append(matrix_row)

# for line in distance_matrix:
#     temp = []
#     for num in line:
#         if (num != 0.0):
#             temp.append('N')
#         else:
#             temp.append(num)
#     # print(len(temp))
#     print(temp)

# for line in distance_matrix:
#     print(line)

# print(distance_matrix)
print(f'Processed {line_count} lines.')
for city in city_matrix:
    print('[' + city.name + ', ' + city.desc + ']')
print(len(city_matrix))
print(city_matrix[0].name)
print(city_matrix[23].name)
print(city_matrix[0].distance_between(city_matrix[23]))
# print(city_matrix[6].distance_between(city_matrix[36]))
# print(city_matrix)

# Depth-first search
def dfs (distances):
    num = len(distances)
    # stack = [(i, [i], 0) for i in range(num)]
    stack = city_matrix
    min_path = None
    min_dist = math.inf

    while stack:
        v, path, distance = stack.pop()
        if len(path) == num:
            if distance + distances[v][0] < min_dist:
                min_path = path + [0]
                min_dist = distance + distances[v][0]
            
            else:
                for u in range(num):
                    if u not in path:
                        stack.append((u, path + [u], distance + distances[v][u]))
            
    return min_dist, min_path #[df.iloc[i]['name'] for i in min_path]

print('*' * 10)
# test_dist, test_path = dfs(distance_matrix)
# print(test_dist)
# print(test_path)
print('*' * 10)

def dfs_paths(graph, start, goal):
    stack = [(start, [start])]
    while stack:
        (vertex, path) = stack.pop()
        for next in graph[vertex] - set(path):
            if next == goal:
                yield path + [next]
            else:
                stack.append((next, path + [next]))
