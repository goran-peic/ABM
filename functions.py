import actors
import random
import numpy as np
from actors import Grass, Sheep, Wolf

# grass_reproduction_rate = 0.5; sheep_reproduction_rate = 0.2; wolf_reproduction_rate = 0.1
# grass_life = 10; sheep_life = 10; wolf_life = 10


def assignToTiles(dataset, creature, tiles, grass_reproduction_rate, sheep_reproduction_rate, wolf_reproduction_rate,
                  grass_life, sheep_life, wolf_life):
  list_of_creatures = []
  for row, col in tiles:
    if creature == "grass":
      dataset.loc[row, col] = 1
      list_of_creatures.append(actors.Grass(life=grass_life, reproduction_rate=grass_reproduction_rate,
                                            position=[row, col]))
    elif creature == "sheep":
      dataset.loc[row, col] = 2
      list_of_creatures.append(actors.Sheep(life=sheep_life, reproduction_rate=sheep_reproduction_rate,
                                            position=[row, col]))
    elif creature == "wolf":
      dataset.loc[row, col] = 3
      list_of_creatures.append(actors.Wolf(life=wolf_life, reproduction_rate=wolf_reproduction_rate,
                                           position=[row, col]))
    else: print("Please enter a valid creature: grass, sheep, or wolf.")
  return(list_of_creatures)

def seedActors(dataset, terrain_size, grass, sheep, wolves, grass_reproduction_rate, sheep_reproduction_rate,
               wolf_reproduction_rate, grass_life, sheep_life, wolf_life):
  actors.terrain_size = terrain_size
  allTileCoord = [[x, y] for x in list(range(actors.terrain_size)) for y in list(range(actors.terrain_size))]

  grass_tiles = random.sample(allTileCoord, grass)
  list_of_grass = assignToTiles(dataset, creature="grass", tiles=grass_tiles, grass_reproduction_rate=grass_reproduction_rate,
                                sheep_reproduction_rate=sheep_reproduction_rate, wolf_reproduction_rate=wolf_reproduction_rate,
                                grass_life=grass_life, sheep_life=sheep_life, wolf_life=wolf_life)
  allTileCoord = [x for x in allTileCoord if x not in grass_tiles]

  sheep_tiles = random.sample(allTileCoord, sheep)
  list_of_sheep = assignToTiles(dataset, creature="sheep", tiles=sheep_tiles, grass_reproduction_rate=grass_reproduction_rate,
                                sheep_reproduction_rate=sheep_reproduction_rate, wolf_reproduction_rate=wolf_reproduction_rate,
                                grass_life=grass_life, sheep_life=sheep_life, wolf_life=wolf_life)
  allTileCoord = [x for x in allTileCoord if x not in sheep_tiles]

  wolf_tiles = random.sample(allTileCoord, wolves)
  list_of_wolves = assignToTiles(dataset, creature="wolf", tiles=wolf_tiles, grass_reproduction_rate=grass_reproduction_rate,
                                sheep_reproduction_rate=sheep_reproduction_rate, wolf_reproduction_rate=wolf_reproduction_rate,
                                grass_life=grass_life, sheep_life=sheep_life, wolf_life=wolf_life)
  return list(list_of_grass + list_of_sheep + list_of_wolves)

'''
def Live(poplist, terrain_size, grass_life, sheep_life, wolf_life):
  final_population = poplist[:]
  for creature in poplist:
    if creature.life <= 0 and creature in final_population:
      final_population.remove(creature)
    else:
      poplistWithoutMe = poplist[:]
      poplistWithoutMe.remove(creature)
      creature.life -= 1
      creature.move()
      if (isinstance(creature, Sheep) or isinstance(creature, Wolf)) and creature.eat(final_population):
        creatures_to_eat = creature.eat(final_population)
        for creature in creatures_to_eat:
          final_population.remove(creature)
      if isinstance(creature, Grass): creature_offspring = creature.reproduce(grass_life, poplist)
      elif isinstance(creature, Sheep): creature_offspring = creature.reproduce(sheep_life, poplistWithoutMe)
      elif isinstance(creature, Wolf): creature_offspring = creature.reproduce(wolf_life, poplistWithoutMe)
      else: creature_offspring = None
      if creature_offspring is not None:
        final_population.append(creature_offspring)
#        if isinstance(creature_offspring, Grass): print("Grass just reproduced!!!!")
#        elif isinstance(creature_offspring, Sheep): print("Sheep just REPRODUCED!!!!")
  return final_population
'''
def Live(poplist, grass_life, sheep_life, wolf_life):
  final_population = poplist[:]
  final_population = [creature for creature in poplist if creature.life > 0 and creature in final_population]
  for creature in poplist:
    poplistWithoutMe = [critter for critter in poplist if critter is not creature]
    creature.life -= 1
    creature.move()
    if (isinstance(creature, Sheep) or isinstance(creature, Wolf)) and creature.eat(final_population):
      creatures_to_eat = creature.eat(final_population)
      final_population = [critter for critter in final_population if critter not in creatures_to_eat]
    if isinstance(creature, Grass): creature_offspring = creature.reproduce(grass_life, poplist)
    elif isinstance(creature, Sheep): creature_offspring = creature.reproduce(sheep_life, poplistWithoutMe)
    elif isinstance(creature, Wolf): creature_offspring = creature.reproduce(wolf_life, poplistWithoutMe)
    else: creature_offspring = None
    if creature_offspring is not None:
      final_population.append(creature_offspring)
#      if isinstance(creature_offspring, Grass): print("Grass just reproduced!!!!")
#      elif isinstance(creature_offspring, Sheep): print("Sheep just REPRODUCED!!!!")
  return final_population

def extractInfo(dataset):
  number_of_grass = len([creature for creature in dataset if isinstance(creature, Grass)])
  number_of_sheep = len([creature for creature in dataset if isinstance(creature, Sheep)])
  number_of_wolves = len([creature for creature in dataset if isinstance(creature, Wolf)])
  current_composition = [number_of_grass, number_of_sheep, number_of_wolves]
  return current_composition

def RunSimulation(simulation_runs, dataset, initial_population, grass_life, sheep_life, wolf_life):
  run = 0
  initpop = initial_population[:]
  while run < simulation_runs and len(initpop) > 0:
    remaining_population = Live(initpop, grass_life, sheep_life, wolf_life)[:]
    current_info = extractInfo(remaining_population)
    dataset.loc[run, dataset.columns[0]] = run + 1
    dataset.loc[run, dataset.columns[1]] = current_info[0]
    dataset.loc[run, dataset.columns[2]] = current_info[1]
    dataset.loc[run, dataset.columns[3]] = current_info[2]
    run += 1
    initpop = remaining_population[:]
  return dataset

def stacked(df, categories):
  areas = dict()
  last = np.zeros(len(df[categories[0]]))
  for cat in categories:
    next = last + df[cat]
    areas[cat] = np.hstack((last[::-1], next))
    last = next
  return areas
