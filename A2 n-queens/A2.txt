import random

# Fitness function to evaluate fitness value of one chromosome in the population by the number of violations
def fitness(chrom, maxFit):
    # no need to determine vertical violations as there would not be any
    # determine horizontal violations (chromosomes)
    horizontal = sum([chrom.count(value)-1 for value in chrom])/2
    # determine diagonal violations
    diagonal = 0
    size = len(chrom)
    diagonal_right = [0]*(2*size)
    diagonal_left = [0]*(2*size)

    for i in range(size):
        diagonal_right[len(chrom) - i + chrom[i] - 2] += 1
        diagonal_left[i + chrom[i] - 1] += 1
    for i in range(2*size - 1):
        count = 0
        if diagonal_right[i] > 1:
            count += diagonal_right[i] - 1
        if diagonal_left[i] > 1:
            count += diagonal_left[i] - 1
        diagonal += count
    
    # subtract horizontal and diagonal clashes from maximum fitness
    return int(maxFit - (horizontal + diagonal))

# Randomly select chromosome
def random_select(population, prob):
    popWithProb = zip(population, prob)
    total = sum(num for _, num in popWithProb)
    rand = random.uniform(0, total)
    top = 0
    for pop, prob in zip(population, prob):
        if top + prob >= rand:
            return pop
        top += prob

# Randomly change the value of a random index in a chromosome
def mutate(chromosome):
    size = len(chromosome)
    chromosome[random.randint(0, size - 1)] = random.randint(0, size - 1)
    return chromosome

# Crossover between two chromosomes
def crossover(chrom1, chrom2):
    size = len(chrom1)
    offspring = [0] * size
    for i in range(size):
        num = random.randint(0, 1)
        if num < 0.5:
            offspring[i] = chrom1[i]
        else:
            offspring[i] = chrom2[i]
    return offspring

# Genetic algorithm steps to be repeated until maximum fitness value found
def genetic(population, mutation_probability, maxFitness):
    new_pop = []
    probabilities = [fitness(chrom, maxFitness) / maxFitness for chrom in population]

    for i in range(len(population)):
        # randomly select best 2 chromosomes
        chrom1 = random_select(population, probabilities)
        chrom2 = random_select(population, probabilities)
        # reproduce (crossover) new offspring from best 2 randomly selected
        offspring = crossover(chrom1, chrom2)
        # mutate offspring based on given probability
        if random.random() < mutation_probability:
            offspring = mutate(offspring)
        # add offspring to population
        new_pop.append(offspring)
        # if the an arrangement with a maximum fitness value is found, stop
        if fitness(offspring, maxFitness) == maxFitness:
            break
    return new_pop

# Main
# Set number of queens for problem
NUM_OF_QUEENS = 8
# Set mutation probability
MUTATION_PROBABILITY = 0.1
# Calculate and set max fitness value
MAX_FITNESS = NUM_OF_QUEENS * (NUM_OF_QUEENS-1) /2

# Add chromosomes to population array
population = []
for _ in range(NUM_OF_QUEENS-1):
    # Making random chromosomes for population - index represents column and value is the row
    population.append([random.randint(1, NUM_OF_QUEENS - 1) for _ in range(NUM_OF_QUEENS)])

# Track generation
gen = 1

# Genetic algorithm repeating steps until arrangement with maximimum fitness value found
while not (MAX_FITNESS in [fitness(chromosome, MAX_FITNESS) for chromosome in population]):
    population = genetic(population, MUTATION_PROBABILITY, MAX_FITNESS)
    print("Generation {}, Max Fitness in Generation = {}".format(gen, max([fitness(n, MAX_FITNESS) for n in population])))
    gen += 1

# Print solution and board
solution_chrom = []
print()
print("Solution found in Generation {}!".format(gen-1))
for chrom in population:
    if fitness(chrom, MAX_FITNESS) == MAX_FITNESS:
        solution_chrom = chrom
        print("Solution Chromosome = {}, Solution Fitness = {}, Max Fitness = {}".format(str(chrom), fitness(chrom, MAX_FITNESS), MAX_FITNESS))        

board = []
for _ in range(NUM_OF_QUEENS):
    board.append(["x"] * NUM_OF_QUEENS)

for i in range(NUM_OF_QUEENS):
    board[solution_chrom[i]][i]="Q"

for row in board:
    print (" ".join(row))