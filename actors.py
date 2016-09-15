import numpy as np


class Actor():

  def __init__(self, life, reproduction_rate, position):
    self.life = life
    self.reproduction_rate = reproduction_rate
    self.position = position
    self.consecutive_starve = 0

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

  def reproduce(self, life_amount, poplist):
    available_grass = [creature for creature in poplist if creature.position == self.position and isinstance(creature, Grass)]
    if len(available_grass) <= 3 and len(available_grass) > 0:
      if int(np.random.choice([0, 1], p=[1 - self.reproduction_rate, self.reproduction_rate])) == 1:
        offspring = Grass(life_amount, self.reproduction_rate, self.position)
        return offspring
      else: return None
    elif len(available_grass) > 3:
      reduced_reproduction_rate = (self.reproduction_rate/len(available_grass)**2)/\
                                  ((self.reproduction_rate/len(available_grass)**2) + (1 - self.reproduction_rate))
      if int(np.random.choice([0, 1], p=[1 - reduced_reproduction_rate, reduced_reproduction_rate])) == 1:
        offspring = Grass(life_amount, self.reproduction_rate, self.position)
        return offspring
      else: return None
    else: return None


class Sheep(Actor):

  def reproduce(self, life_amount, poplist):
    available_sheep = [creature for creature in poplist if creature.position == self.position and isinstance(creature, Sheep)]
    if len(available_sheep) <= 3 and len(available_sheep) > 0:
      # increased_reproduction_rate = self.reproduction_rate / (self.reproduction_rate + (1 - self.reproduction_rate) / len(available_sheep) ** 0.3)
      if int(np.random.choice([0, 1], p=[1-self.reproduction_rate, self.reproduction_rate])) == 1:
        offspring = Sheep(life_amount, self.reproduction_rate, self.position)
        return offspring
      else: return None
    elif len(available_sheep) > 3:
      reduced_reproduction_rate = (self.reproduction_rate/len(available_sheep)**2)/((self.reproduction_rate/len(available_sheep)**2) + (1 - self.reproduction_rate))
      if int(np.random.choice([0, 1], p=[1 - reduced_reproduction_rate, reduced_reproduction_rate])) == 1:
        offspring = Grass(life_amount, self.reproduction_rate, self.position)
        return offspring
      else: return None
    else: return None

  def eat(self, poplist):
    available_grass = [creature for creature in poplist if creature.position == self.position and isinstance(creature, Grass)]
    if available_grass:
      self.consecutive_starve = 0
      for grass in available_grass:
        self.life += grass.life
    else:
      self.consecutive_starve += 1
      self.life -= self.consecutive_starve
    return available_grass


class Wolf(Actor):

  def reproduce(self, life_amount, poplist):
    available_wolves = [creature for creature in poplist if creature.position == self.position and isinstance(creature, Wolf)]
    if len(available_wolves) <= 3 and len(available_wolves) > 0:
      # increased_reproduction_rate = self.reproduction_rate / (self.reproduction_rate + (1 - self.reproduction_rate) / len(available_wolves) ** 0.3)
      if int(np.random.choice([0, 1], p=[1 - self.reproduction_rate, self.reproduction_rate])) == 1:
        offspring = Wolf(life_amount, self.reproduction_rate, self.position)
        return offspring
      else: return None
    elif len(available_wolves) > 3:
      reduced_reproduction_rate = (self.reproduction_rate/len(available_wolves)**2)/((self.reproduction_rate/len(available_wolves)**2) + (1 - self.reproduction_rate))
      if int(np.random.choice([0, 1], p=[1 - reduced_reproduction_rate, reduced_reproduction_rate])) == 1:
        offspring = Grass(life_amount, self.reproduction_rate, self.position)
        return offspring
      else: return None
    else: return None

  def eat(self, poplist):
    available_sheep = [creature for creature in poplist if creature.position == self.position and isinstance(creature, Sheep)]
    if available_sheep:
      self.consecutive_starve = 0
      for sheep in available_sheep:
        self.life += sheep.life
    else:
      self.consecutive_starve += 1
      self.life -= self.consecutive_starve
      print('wolf just starved')
    return available_sheep