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

'''

### square_supplies

def answer(n):
  bought = 0
  remaining = n
  while remaining > 0:
    spent = 0
    current_factor = 1
    while spent <= remaining:
      spent = current_factor**2
      current_factor += 1
    spent = (current_factor - 2)**2
    remaining = remaining - spent
    bought += 1
  return bought

correct_results = [answer(n) for n in range(10000)]

###

from math import sqrt, floor

def answer(n):
  counter = 0
  still_have_coins = True
  remainder = n
#  print('i have ', remainder, 'coins')
  while still_have_coins:
    if remainder > 3 and remainder != 8:
      counter += 1
#      print('bought pad size ', floor(sqrt(remainder)), 'x', floor(sqrt(remainder)))
#      print('count = ', counter)
      remainder = remainder % floor(sqrt(remainder))**2
#      print('i have', remainder, 'coins remaining')
    elif remainder == 8:
      counter += 2
#      print('bought two 2x2s')
#      print('count = ', counter)
#      print('i have 0 coin(s) remaining')
      still_have_coins = False
    else:
      if remainder > 0:
        counter += remainder
#        print('bought ', remainder, ' 1x1s')
#        print('count = ', counter)
#        print('i have 0 coins remaining')
        still_have_coins = False
      still_have_coins = False
  return counter

my_results = [answer(n) for n in range(10000)]

# print('the smallest number of square pads you can buy is ', answer(0))
# diff = [idx for idx in my_results if my_results != correct_results]
# print(diff)

print(my_results == correct_results)
'''
'''

### level 3, challenge 2: string_cleaning

from collections import deque

def find_all(string, sub):
    start = 0
    while True:
        start = string.find(sub, start)
        if start > -1:
            yield (start, start+len(sub),)
            start += 1
        else:
            break

def answer(chunk, word):
    final_result = chunk
    queue = deque([chunk])
    seen = set()

    while len(queue):
        value = queue.popleft()
        matches = find_all(value, word)
        for s, e in matches:
            result = value[:s] + value[e:]
            if result in seen:
                continue
            elif len(result) == len(final_result):
                final_result = min(result, final_result)
            elif len(result) < len(final_result):
                final_result = result
            seen.add(result)
            queue.append(result)
    return final_result

'''
'''

import time

def random_number(low, high):
  return int(low + int(time.time()*1000) % (high - low))

def answer(chunk, word):
  tempList = []
  if chunk is None:
    return chunk
  else:
    iter = 0
    while iter < 4000:
      chunkTemp = chunk[:]
      while word in chunkTemp:
        word_positions = [chunkTemp.find(word, i) for i in range(len(chunkTemp))]
        word_positions = [pos for pos in word_positions if pos is not -1]
        word_positions = list(set(word_positions))
        removal_starting_position = word_positions[random_number(0, len(word_positions))]
        removal_ending_position = removal_starting_position + len(word)
        chunkTemp = chunkTemp[: removal_starting_position] + chunkTemp[removal_ending_position: ]
      tempList.append(chunkTemp)
      iter += 1
    sorted_list = list(set(tempList))
    sorted_list_lengths = [len(chunky) for chunky in sorted_list]
    sorted_list = [chunky for chunky in sorted_list if len(chunky) == min(sorted_list_lengths)]
    sorted_list = sorted(sorted_list)
    return sorted_list[0]

chunk = 'lololololo'
word = 'lol'

chunk = 'govgovnonogovno'
word = 'g'

# chunk = 'goodgooogoogfogoood'
# word = 'goo'

print(answer(chunk=chunk, word=word))
'''

'''
import random

def answer(chunk, word):
  tempList = []
  if chunk is None:
    return chunk
  else:
    iter = 0
    while iter < 1000:
      chunkTemp = chunk[:]
      while word in chunkTemp:
        word_positions = [chunkTemp.find(word, i) for i in range(len(chunkTemp))]
        word_positions = [pos for pos in word_positions if pos is not -1]
        word_positions = list(set(word_positions))
        removal_starting_position = random.choice(word_positions)
        removal_ending_position = removal_starting_position + len(word)
        chunkTemp = chunkTemp[: removal_starting_position] + chunkTemp[removal_ending_position: ]
      tempList.append(chunkTemp)
      iter += 1
    sorted_list = list(set(tempList))
    sorted_list_lengths = [len(chunky) for chunky in sorted_list]
    sorted_list = [chunky for chunky in sorted_list if len(chunky) == min(sorted_list_lengths)]
    sorted_list = sorted(sorted_list)
    return sorted_list[0]

chunk = 'lololololo'
word = 'lol'

chunk = 'goodgooogoogfogoood'
word = 'goo'

print(answer(chunk=chunk, word=word))

'''
'''

def scramble(mylist):
  tempList = mylist[:]
  scrambled_word_positions = {str(pos): str(idx) for idx, pos in enumerate(tempList)}
  scrambled_word_positions = list(scrambled_word_positions.keys())
  scrambled_word_positions = [int(pos) for pos in scrambled_word_positions]
  return scrambled_word_positions[0]

def getOneChunk(word, chunk):
  chunkTemp = chunk[:]
  while word in chunkTemp:
    word_positions = [chunkTemp.find(word, i) for i in range(len(chunkTemp))]
    word_positions = [pos for pos in word_positions if pos is not -1]
    word_positions = list(set(word_positions))
    word_positions = scramble(word_positions)
    print(word_positions)
    removal_starting_position = word_positions
    removal_ending_position = removal_starting_position + len(word)
    chunkTemp = chunkTemp[: removal_starting_position] + chunkTemp[removal_ending_position:]
  return(chunkTemp)


def answer(chunk, word):
  tempList = []
  iter = 0
  while iter < 10:
    chunkTemp = chunk[:]
    tempList.append(getOneChunk(word=word, chunk=chunkTemp))
    iter += 1
  print(tempList)
  sorted_list = list(set(tempList))
  sorted_list_lengths = [len(chunky) for chunky in sorted_list]
  sorted_list = [chunky for chunky in sorted_list if len(chunky) == min(sorted_list_lengths)]
  sorted_list = sorted(sorted_list)
  return sorted_list[0]

chunk = 'lololololo'
word = 'lol'

# chunk = 'goodgooogoogfogoood'
# word = 'goo'

print(answer(chunk=chunk, word=word))
'''

'''

### hash_it_out challenge

def hashFunction(message):
  messageTemp = message[:]
  messageTemp.append(0)
  digest = [(((129 * messageTemp[i]) ^ messageTemp[i-1]) % 256) for i in range(len(messageTemp))]
  return digest[:-1]

digest = [0, 0]
digest = [0, 129, 3, 129, 7, 129, 3, 129, 15, 129, 3, 129, 7, 129, 3, 129]
digest = [0, 129, 5, 141, 25, 137, 61, 149, 113, 145, 53, 157, 233, 185, 109, 165]
#(int list) [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

print("###########"); print()

def msgFunction(digest):
  message = []
  message.append(129*(digest[0] ^ 0) % 256)
  for idx, dig in enumerate(digest[1:]):
    message.append(129*(dig ^ message[idx]) % 256)
  return message


x = msgFunction(digest=digest)
print('digest input: ', digest)
print('message output: ', x)

'''

'''

## challenge: save beta rabbit
import numpy as np


initial_food = 7
grid = [[0, 2, 5, 3, 4, 6, 0, 1, 2], [1, 1, 3, 4, 3, 6, 3, 6, 4], [2, 1, 1, 3, 7, 4, 9, 5, 2], [0, 2, 5, 3, 4, 6, 0, 1, 2], [1, 1, 3, 4, 3, 6, 3, 6, 4], [2, 1, 1, 3, 7, 4, 9, 5, 2], [0, 2, 5, 3, 4, 6, 0, 1, 2], [1, 1, 3, 4, 3, 6, 3, 6, 4], [2, 1, 1, 3, 7, 4, 9, 5, 2]]
# grid = [[0, 2, 5], [1, 1, 3], [2, 1, 1]]

class Rabbit():

  def __init__(self, initial_food):
    self.x = 0
    self.y = 0
    self.food = initial_food

  def move(self, grid):
    bunnyMoves = True
    while bunnyMoves:
      print('x = ', self.x, 'y = ', self.y)
      self.food -= grid[self.x][self.y]
      print('now i have ', self.food, 'food.')
      if self.x == len(grid) - 1 and self.y == len(grid) - 1:
        bunnyMoves = False
      elif self.x == len(grid) - 1 and self.y < len(grid) - 1:
        self.y += 1
      elif self.x < len(grid) - 1 and self.y == len(grid) - 1:
        self.x += 1
      else:
        if int(np.random.choice([0, 1], p=[0.5, 0.5])) == 1:
          self.x += 1
        else:
          self.y += 1


def RunBunny(iterations, grid, food):
  dataset = []
  iter = 0
  while iter < iterations:
    bunny = Rabbit(initial_food=food)
    bunny.move(grid=grid)
    dataset.append(bunny.food)
    iter += 1
  return(dataset)

dataset = RunBunny(iterations=1000, grid=grid, food=initial_food)
if all(run < 0 for run in dataset):
  result = -1
else:
  dataset = [run for run in dataset if run >= 0]
  result = min(dataset)
print(dataset)
print('result is: ', result)
'''

'''
# name_that_rabbit challenge
import string


def answer(names):

  # (1) map each letter to a corresponding integer via hash table.
  alphabet_dictionary = {}
  for idx, letter in enumerate(string.ascii_lowercase):
    alphabet_dictionary[letter] = idx + 1

  # (2) compute sum of letters for each name in list
  totals = []
  for name in names:
    name_list = list(name)
    name_values = [alphabet_dictionary[letter] for letter in name_list]
    name_sum = sum(name_values)
    totals.append(name_sum)
  sorted_names = [name for (total, name) in sorted(zip(totals, names), reverse=True)]
  return sorted_names

names = ["abcdefg", "goran", "a", "vi", "lambda", "king", "sranje", "cj", "al"]


if __name__ == "__main__":
  print(answer(names))
'''

'''
# maximum_equality challenge

x = [0, 0, 0, 1, 1]

if sum(x) < len(x):
  max_same_size_wagons = sum(x)
elif sum(x) > len(x):
  max_same_size_wagons = len(x) - (sum(x) % len(x))
else:
  max_same_size_wagons = len(x)

print(max_same_size_wagons)

'''