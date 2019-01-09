# maximise 0.2x1 + 0.3x2 + 0.5x3 + 0.1x4

import random

MUTATION_PROB = 0.2
CROSSOVER_PROB = 0.7
GENERATION_COUNT = 5
INPUTS = [0.2, 0.3, 0.5, 0.1]
WEIGHTS_COUNT = 4
POPULATION_SIZE = 5


def generate_random_population(size=POPULATION_SIZE):
	population = []
	for i in range(size):
		chromosome = []
		for j in range(len(INPUTS)):
			chromosome.append(random.randrange(0,2))
		population.append(chromosome)		
	return population

def fitness_func(inputs, chromosome, print_fitness = False):
	fitness = sum([i * inputs[index] for index, i in enumerate(chromosome)])
	if print_fitness:
		print("fitness value for chromosome - " + "".join(str(i) for i in chromosome) + " is: " + str(fitness))
	return fitness

def discarding_population(inputs, population, value):
	new_population = []
	for chromosome in population:
		fitness = fitness_func(inputs, chromosome)
		if fitness <= value:
			new_population.append(chromosome)
	return new_population

def discarding_duplicates(population):
	new_population = []
	for chromosome in population:
		if not chromosome in new_population:
			new_population.append(chromosome)
	return new_population


def select_parent(population):
	fitnesses = []
  
	for chromosome in population:
		fitnesses.append(fitness_func(INPUTS, chromosome))
  
	rand = random.uniform(0, sum(fitnesses))

	for index, fitness in enumerate(fitnesses):
		if rand <= 0:
			break
		rand -= fitness

	return population[index]


def crossover(parent1, parent2):
	if(random.uniform(0,1) <= CROSSOVER_PROB):
		print("===================== Selected parents for crossover: ", parent1, parent2)
		crossover_point = len(INPUTS)//2
		offspring1 = parent1[0:crossover_point] + parent2[crossover_point:]
		offspring2 = parent2[0:crossover_point] + parent1[crossover_point:]
		print("===================== After crossover: ", offspring1, offspring2)
		return [offspring1, offspring2]
	else:
		return [parent1, parent2]

def mutation(chromosome):
	if(random.uniform(0, 1) < MUTATION_PROB):
		print("===================== Selected for mutation, before mutation: ", chromosome)
		idx = random.randrange(0,len(chromosome))
		if chromosome[idx] == 0:
			chromosome[idx] = 1
		else:
			chromosome[idx] = 0
		print("===================== After mutation: ", chromosome)
	return chromosome



def evolve():
	print("*************************==================================********************************")
	print("Hyper parameters used are: ")
	print("MUTATION PROB", MUTATION_PROB)
	print("CROSSOVER PROB", CROSSOVER_PROB)
	print("NUMBER OF GENERATION", GENERATION_COUNT)
	print("INPUTS TO MAXIMISE", INPUTS)
	print("POPULATION SIZE", POPULATION_SIZE)
	print("*************************==================================********************************")
	print("")


	new_population = generate_random_population()

	new_population = discarding_population([0.5, 1.0, 1.5, 0.1], new_population, 3.1)
	new_population = discarding_population([0.3, 0.8, 1.5, 0.4], new_population, 2.5)
	new_population = discarding_population([0.2, 0.2, 0.3, 0.1], new_population, 0.4)
	# new_population = discarding_duplicates(new_population)

	while len(new_population) < POPULATION_SIZE:
		for chromosome in generate_random_population(POPULATION_SIZE - len(new_population)):
			new_population.append(chromosome)
		new_population = discarding_population([0.5, 1.0, 1.5, 0.1], new_population, 3.1)
		new_population = discarding_population([0.3, 0.8, 1.5, 0.4], new_population, 2.5)
		new_population = discarding_population([0.2, 0.2, 0.3, 0.1], new_population, 0.4)
		# new_population = discarding_duplicates(new_population)


	max_fitnesses = []
	max_fitnesses_values = []

	for generation in range(GENERATION_COUNT):
		print("===================== GENERATION : ", generation + 1)
		print("Population : ", new_population)

		generation_max_fitness = []
		generation_max_fitness_values = []

		
		new_population_temp = []

		for i in range(POPULATION_SIZE//2):
			parent1 = select_parent(new_population)
			parent2 = select_parent(new_population)
			offspring1, offspring2 = crossover(parent1, parent2)
			offspring1 = mutation(offspring1)
			offspring2 = mutation(offspring2)
			new_population_temp.append(offspring1)
			new_population_temp.append(offspring2)

		new_population_temp = discarding_population([0.5, 1.0, 1.5, 0.1], new_population_temp, 3.1)
		new_population_temp = discarding_population([0.3, 0.8, 1.5, 0.4], new_population_temp, 2.5)
		new_population_temp = discarding_population([0.2, 0.2, 0.3, 0.1], new_population_temp, 0.4)
		# new_population = discarding_duplicates(new_population_temp)

		while len(new_population_temp) < POPULATION_SIZE:
			for i in range(POPULATION_SIZE - len(new_population_temp)):
				new_population_temp.append(random.choice(new_population))
			new_population_temp = discarding_population([0.5, 1.0, 1.5, 0.1], new_population_temp, 3.1)
			new_population_temp = discarding_population([0.3, 0.8, 1.5, 0.4], new_population_temp, 2.5)
			new_population_temp = discarding_population([0.2, 0.2, 0.3, 0.1], new_population_temp, 0.4)
			# new_population = discarding_duplicates(new_population_temp)

		print("===================== Generated children : ", new_population_temp)

		# if generation == GENERATION_COUNT:
		for index, chromosome in enumerate(new_population_temp):
			fitness = fitness_func(INPUTS, chromosome, True)
			if not generation_max_fitness_values:
				generation_max_fitness_values = chromosome
			elif(fitness >= max(generation_max_fitness)):
				generation_max_fitness_values = chromosome
			generation_max_fitness.append(fitness)

		print("====================================================================================")
		print("maximum fitness in generation - " + str(generation + 1) + " is : " + str(max(generation_max_fitness)) + " for chromosome : " + 
			str(generation_max_fitness_values[0]) + str(generation_max_fitness_values[1]) + str(generation_max_fitness_values[2]) + 
			str(generation_max_fitness_values[3])
		)
		print("====================================================================================")
		max_fitnesses.append(max(generation_max_fitness))
		max_fitnesses_values.append(generation_max_fitness_values)

		new_population = new_population_temp
		print("")

	print("************************************* Overall *************************************")
	print("maximum fitness for all generation - is : " + str(max(max_fitnesses)) + " for chromosome : ", 
			max_fitnesses_values[max_fitnesses.index(max(max_fitnesses))]
		)
	print("***********************************************************************************")

evolve()