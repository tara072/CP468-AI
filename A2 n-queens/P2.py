import random

# Making random chromosomes for population - index represents column and value is the row
def random_chromosome(size):
    return [random.randint(1, size - 1) for _ in range(size)]

# Fitness function to evaluate fitness value of one chromosome in the population by the number of violations
def fitness(chrom, maxFit):
    # no need to determine vertical violations as there would not be any
    # determine horizontal violations (chromosomes)
    horizontal = sum([chrom.count(queen)-1 for queen in chrom])/2
    # determine diagonal violations
    diagonal = 0
    size = len(chrom)
    left_daigonal = [0]*(2*size)
    right_daigonal = [0]*(2*size)

    for i in range(size):
        left_daigonal[i + chrom[i] - 1] += 1
        right_daigonal[len(chrom) - i + chrom[i] - 2] += 1
    for i in range(2*size - 1):
        count = 0
        if left_daigonal[i] > 1:
            count += left_daigonal[i] - 1
        if right_daigonal[i] > 1:
            count += right_daigonal[i] - 1
        diagonal += count
    
    # subtract horizontal and diagonal clashes from maximum fitness
    return int(maxFit - (horizontal + diagonal))

# Calculate probability
def probability(chromosome, maxFit):
    return fitness(chromosome, maxFit) / maxFit

# Randomly select chromosome
def random_select(population, prob):
    populationWithProb = zip(population, prob)
    total = sum(n for _, n in populationWithProb)
    rand = random.uniform(0, total)
    upto = 0
    for c, w in zip(population, prob):
        if upto + w >= rand:
            return c
        upto += w

# Randomly change the value of a random index in a chromosome
def mutate(chromosome):
    size = len(chromosome)
    chromosome[random.randint(0, size - 1)] = random.randint(0, size - 1)
    return chromosome

# Crossover between two chromosomes
def crossover(chrom1, chrom2):
    size = len(chrom1)
    child = [0] * size
    for i in range(size):
        c = random.randint(0, 1)
        if c < 0.5:
            child[i] = chrom1[i]
        else:
            child[i] = chrom2[i]
    return child

# Genetic algorithm steps to be repeated until maximum fitness value found
def genetic(population, mutation_probability, maxFitness):
    new_pop = []
    probabilities = [probability(chromosome, maxFitness) for chromosome in population]

    for i in range(len(population)):
        # randomly select best 2 chromosomes
        chrom1 = random_select(population, probabilities)
        chrom2 = random_select(population, probabilities)
        # reproduce (crossover) new offspring from best 2 randomly selected
        child = crossover(chrom1, chrom2)
        # mutate offspring based on given probability
        if random.random() < mutation_probability:
            child = mutate(child)
        # add offspring to population
        new_pop.append(child)
        # if the an arrangement with a maximum fitness value is found, stop
        if fitness(child, maxFitness) == maxFitness: break
    return new_pop

# Main
# Set number of queens for problem
NUM_OF_QUEENS = 8
# Set mutation probability
MUTATION_PROBABILITY = 0.1
# Calculate and set max fitness value
MAX_FITNESS = NUM_OF_QUEENS * 7 /2

# Add chromosomes to population array
population = []
for _ in range(8-1):
    population.append(random_chromosome(NUM_OF_QUEENS))

for chromosome in population:
    print(chromosome)

# Track generation
generation = 1

# Genetic algorithm repeating steps until arrangement with maximimum fitness value found
while not (MAX_FITNESS in [fitness(chromosome, MAX_FITNESS) for chromosome in population]):
    print("=== Generation {} ===".format(generation))
    population = genetic(population, MUTATION_PROBABILITY, MAX_FITNESS)
    print("Maximum Fitness in Generation = {}".format(max([fitness(n, MAX_FITNESS) for n in population])))
    generation += 1

# Print solution and board
solution_chrom = []
print()
print("Solution found in Generation {}!".format(generation-1))
for chrom in population:
    if fitness(chrom, MAX_FITNESS) == MAX_FITNESS:
        solution_chrom = chrom
        print("Solution: ")
        print("Chromosome = {}, Fitness = {}, Max Fitness = {}".format(str(chrom), fitness(chrom, MAX_FITNESS), MAX_FITNESS))        

board = []
for x in range(NUM_OF_QUEENS):
    board.append(["x"] * NUM_OF_QUEENS)
for i in range(NUM_OF_QUEENS):
    board[solution_chrom[i]][i]="Q"
for row in board:
    print (" ".join(row))