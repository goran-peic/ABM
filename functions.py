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
      dataset.ix[row, col] = 1
      list_of_creatures.append(actors.Grass(life=grass_life, reproduction_rate=grass_reproduction_rate,
                                            position=[row, col]))
    elif creature == "sheep":
      dataset.ix[row, col] = 2
      list_of_creatures.append(actors.Sheep(life=sheep_life, reproduction_rate=sheep_reproduction_rate,
                                            position=[row, col]))
    elif creature == "wolf":
      dataset.ix[row, col] = 3
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
  allTileCoord = [x for x in allTileCoord if x not in wolf_tiles]
  return list(list_of_grass + list_of_sheep + list_of_wolves)

def Live(poplist, grass_life, sheep_life, wolf_life):
  final_population = poplist[:]
  offspring = []
  actually_deleted = 0
  for creature in poplist:
    if isinstance(creature, Grass): creature_offspring = creature.reproduce(grass_life)
    elif isinstance(creature, Sheep): creature_offspring = creature.reproduce(sheep_life)
    else: creature_offspring = creature.reproduce(wolf_life)
    if creature_offspring is not None:
      final_population.append(creature_offspring)
      offspring.append(creature_offspring)
    creature.life -= 1
    creature.move()
    if creature.life <= 0: final_population.remove(creature)
    if (isinstance(creature, Sheep) or isinstance(creature, Wolf)) and creature.eat(final_population):
      creatures_to_eat = creature.eat(final_population)
      for creature in creatures_to_eat:
        actually_deleted += 1
        final_population.remove(creature)
  return final_population

def extractInfo(dataset):
  number_of_grass = 0; number_of_sheep = 0; number_of_wolves = 0
  for creature in dataset:
    if isinstance(creature, Grass): number_of_grass += 1
    elif isinstance(creature, Sheep): number_of_sheep += 1
    elif isinstance(creature, Wolf): number_of_wolves += 1
  current_composition = [number_of_grass, number_of_sheep, number_of_wolves]
  return current_composition

def RunSimulation(simulation_runs, dataset, initial_population, grass_life, sheep_life, wolf_life):
  run = 0
  while run < simulation_runs - 1:
    run += 1
    remaining_population = Live(initial_population, grass_life, sheep_life, wolf_life)
    current_info = extractInfo(remaining_population)
    dataset.ix[run, dataset.columns[0]] = run + 1
    dataset.ix[run, dataset.columns[1]] = current_info[0]
    dataset.ix[run, dataset.columns[2]] = current_info[1]
    dataset.ix[run, dataset.columns[3]] = current_info[2]
  return dataset

def stacked(df, categories):
  areas = dict()
  last = np.zeros(len(df[categories[0]]))
  for cat in categories:
    next = last + df[cat]
    areas[cat] = np.hstack((last[::-1], next))
    last = next
  return areas