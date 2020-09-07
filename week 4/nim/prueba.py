# lista = [1,2,3,4,4,5,6,9,1,4,3,9,9,9,5,6]
# tupla = tuple(lista)
# print(tupla)

# get_q_value
# if (state, action) in self.q:
#     return self.q[(state, action)]
# else:
#     return 0

import random

# best_future_reward(self, state):

piles = [2, 1, 0, 0]
best_reward = -2
q = dict()
# q['a'] = 0
actions = set()
for i, pile in enumerate(piles):
    for j in range(1, piles[i] + 1):
        actions.add((i, j))

for action in actions:
    # self.q[(state, action)]
    move = (tuple(piles), action)
    if move in q:
        if q[(piles, action)] > best_reward:
            best_reward = q[(piles, action)]
            best_move = (piles, action)
    else:
        best_reward = 0
        best_move = (piles, action)

# print(best_reward)

#===============================================================================================================
# #choose_action
# epsilon
# best_action = 0
# for x in range(10):
#     is_random = random.choices([False,True],weights = [0.9,0.1],k=1)
#     print(type(is_random[0]))

actions = {(3, 4), (3, 1), (3, 7), (1, 1), (3, 3), (3, 6), (3, 2), (3, 5)}

choice = random.choice(list(actions))
print(choice)