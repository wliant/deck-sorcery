from DataProvider import *
import random
from deap import base
from deap import creator
from deap import tools

# initialSelection is a list of cards id preselected by the user. can by empty
# this method return the result after the genetic algorithm run.
def generateDeck(heroClass, initialSelection):
    cardPool = getAvailableCardIdsForConstruction(heroClass)

    creator.create("FitnessMax", base.Fitness, weights=(1.0,-0.7))
    creator.create("Individual", list, fitness=creator.FitnessMax)

    toolbox = base.Toolbox()

    toolbox.register("attr_gen", random.randint, 0, len(cardPool) - 1)
    toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_gen, 30 - len(initialSelection))
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    def evalFct(individual):
        deck = set()
        for i in initialSelection:
            deck.add(i)
        for index in individual:
            deck.add(cardPool[index])
        return random.randint(0, 15), len(deck)

    def feasible(individual):
        deck = {}
        for i in initialSelection:
            if i in deck:
                deck[i] += 1
            else:
                deck[i] = 1

        for index in individual:
            card = cardPool[index]
            if card in deck:
                deck[card] += 1
            else:
                deck[card] = 1
        
        for card in deck.keys():
            cardRarity = getRarity(card)

            if cardRarity == "LEGENDARY" and deck[card] > 1 or deck[card] > 2:
                return False
        return True
    #----------
    # Operator registration
    #----------
    # register the goal / fitness function
    toolbox.register("evaluate", evalFct)
    toolbox.decorate("evaluate", tools.DeltaPenalty(feasible, -100))

    # register the crossover operator
    toolbox.register("mate", tools.cxTwoPoint)

    # register a mutation operator with a probability to
    # flip each attribute/gene of 0.05
    toolbox.register("mutate", tools.mutUniformInt, low=0, up=len(cardPool) - 1, indpb=0.05)

    # operator for selecting individuals for breeding the next
    # generation: each individual of the current generation
    # is replaced by the 'fittest' (best) of three individuals
    # drawn randomly from the current generation.
    toolbox.register("select", tools.selTournament, tournsize=3)

    random.seed(64)
    pop = toolbox.population(n=300)
    CXPB,MUTPB = 0.5,0.2

    print("Start of evolution")

    fitnesses = list(map(toolbox.evaluate, pop))
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit

    print("  Evaluated %i individuals" % len(pop))  
    # Extracting all the fitnesses of 
    fits = [ind.fitness.values[0] for ind in pop]

    # Variable keeping track of the number of generations
    g = 0
    
    # Begin the evolution
    while max(fits) < 100 and g < 1000:
        # A new generation
        g = g + 1
        print("-- Generation %i --" % g)
        
        # Select the next generation individuals
        offspring = toolbox.select(pop, len(pop))
        # Clone the selected individuals
        offspring = list(map(toolbox.clone, offspring))
        print("offspring length: {0}".format(len(offspring)))
    
        # Apply crossover and mutation on the offspring
        for child1, child2 in zip(offspring[::2], offspring[1::2]):

            # cross two individuals with probability CXPB
            if random.random() < CXPB:
                toolbox.mate(child1, child2)

                # fitness values of the children
                # must be recalculated later
                del child1.fitness.values
                del child2.fitness.values

        for mutant in offspring:

            # mutate an individual with probability MUTPB
            if random.random() < MUTPB:
                toolbox.mutate(mutant)
                del mutant.fitness.values
    
        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit
        
        print("  Evaluated %i individuals" % len(invalid_ind))
        
        # The population is entirely replaced by the offspring
        pop[:] = offspring
        
        # Gather all the fitnesses in one list and print the stats
        fits = [ind.fitness.values[1] for ind in pop]
        
        length = len(pop)
        mean = sum(fits) / length
        sum2 = sum(x*x for x in fits)
        std = abs(sum2 / length - mean**2)**0.5
        
        print("  Min %s" % min(fits))
        print("  Max %s" % max(fits))
        print("  Avg %s" % mean)
        print("  Std %s" % std)
    
    print("-- End of (successful) evolution --")
    
    best_ind = tools.selBest(pop, 1)[0]
    print("Best individual is %s, %s" % (best_ind, best_ind.fitness.values))

    al = sorted(best_ind)
    for index in al:
        print(getCardName(cardPool[index]))
    return []