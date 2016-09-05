import numpy as np


class Actor():

  def __init__(self, life, reproduction_rate, position):
    self.life = life
    self.reproduction_rate = reproduction_rate
    self.position = position

  def move(self):
    illegal_move = True
    while illegal_move:
      moveAmount = [int(i) for i in np.random.choice([-1, 0, 1], size=2, replace=True)]
      tempPosition = [sum(x) for x in zip(self.position, moveAmount)]
      if tempPosition[0] < 0 or tempPosition[0] > terrain_size - 1 or tempPosition[1] < 0 or tempPosition[
        1] > terrain_size - 1:
        illegal_move = True
      else:
        illegal_move = False
        self.position = tempPosition

class Grass(Actor):

  def reproduce(self, life_amount):
    if int(np.random.choice([0, 1], p=[1 - self.reproduction_rate, self.reproduction_rate])) == 1:
      offspring = Grass(life_amount, self.reproduction_rate, self.position)
      return offspring
    else: return None


class Sheep(Actor):

  def reproduce(self, life_amount):
    if int(np.random.choice([0, 1], p=[1-self.reproduction_rate, self.reproduction_rate])) == 1:
      offspring = Sheep(life_amount, self.reproduction_rate, self.position)
      return offspring
    else: return None

  def eat(self, poplist):
    available_grass = []
    for creature in poplist:
      if creature.position == self.position and isinstance(creature, Grass):
        available_grass.append(creature)
    if available_grass:
      for sheep in available_grass:
        self.life += sheep.life
    return available_grass


class Wolf(Actor):

  def reproduce(self, life_amount):
    if int(np.random.choice([0, 1], p=[1-self.reproduction_rate, self.reproduction_rate])) == 1:
      offspring = Wolf(life_amount, self.reproduction_rate, self.position)
      return offspring
    else: return None

  def eat(self, poplist):
    available_sheep = []
    for creature in poplist:
      if creature.position == self.position and isinstance(creature, Sheep): available_sheep.append(creature)
    if available_sheep:
      for sheep in available_sheep:
        self.life += sheep.life
    return available_sheep