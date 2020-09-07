import sys  #python3 prueba.py data/structure0.txt data/words0.txt
import itertools

from crossword import *
from generate import *

if len(sys.argv) not in [3, 4]:
    sys.exit("Usage: python generate.py structure words [output]")

# Parse command-line arguments
structure = sys.argv[1]
words = sys.argv[2]
output = sys.argv[3] if len(sys.argv) == 4 else None

# Generate crossword
crossword = Crossword(structure, words)
creator = CrosswordCreator(crossword)
# print(creator.domains)
# print("===========================================================")
# print(creator.crossword.overlaps)
# print("===========================================================")
# for var_x,var_y in zip(creator.domains,creator.domains):
#     print(f"x: {var_x}, y: {var_y}")
# for x in itertools.product(creator.domains, creator.domains):
#     print(x)
# print("===========================================================")
        # print(f"x: {var_x}, y: {var_y}")
# print(creator.crossword.neighbors)
# for x in creator.crossword.variables:
#     print(x.length)
# print(list(creator.crossword.overlaps.keys()))
# print("===========================================================")
for var in creator.domains:
    temp_set_words = creator.domains[var].copy()
    for word in temp_set_words:
        if len(word) != var.length:
            creator.domains[var].remove(word)
# print("UNICIDAD")
# print(creator.domains)
# print("===========================================================")
for var_x in creator.domains:
    for var_y in creator.domains:
        if var_x != var_y:
            if creator.crossword.overlaps[(var_x,var_y)] != None:
                temp_words_x = creator.domains[var_x].copy()
                temp_words_y = creator.domains[var_y].copy()
                binary_cons = creator.crossword.overlaps[(var_x,var_y)]
                for word_x in temp_words_x:
                    is_arc_cons = False
                    # print(word_x)
                    for word_y in temp_words_y:
                        # print(f"word y: {word_y}")
                        if word_x[binary_cons[0]] == word_y[binary_cons[1]]:
                            is_arc_cons = True
                            # print(f"var  x: {creator.domains[var_x]}")
                            # print(f"var  y: {creator.domains[var_y]}")
                            # creator.domains[var_x].remove(word_x)
                    if not is_arc_cons:
                        creator.domains[var_x].remove(word_x)
                # print(creator.crossword.overlaps[(var_x,var_y)])
                # print(f"i {arc_cons[0]}, j {arc_cons[1]}")
                # print(creator.domains[var_x])
                # print(creator.domains[var_y])
# print(creator.crossword.overlaps[(Variable(1, 4, 'down', 4),Variable(4, 1, 'across', 4))])
# print("BI-CONSTRAINS")
# print(creator.crossword.neighbors((Variable(1, 4, 'down', 4))))
# var_y = Variable(4, 1, 'across', 4)#creator.crossword.neighbors((Variable(1, 4, 'down', 4)))
# print(creator.crossword.overlaps[(Variable(1, 4, 'down', 4),var_y)])
# print(creator.domains)
# print(is_arc_cons)
# print(not is_arc_cons)

#order domain
order_domain = []
var = Variable(4, 1, 'across', 4)
# assign = assignment.copy()
assign = {Variable(0, 1, 'down', 5): 'SEVEN'}
neigh_x = creator.crossword.neighbors(var)
counter_dict = {}
for word in creator.domains[var]:
    counter = 0
    for each_n in neigh_x:
        if each_n not in assign:
            for word_n in creator.domains[each_n]:
                # value_neigh = assign[each_n]
                overlap_cell = creator.crossword.overlaps[(var,each_n)]
                if word[overlap_cell[0]] != word_n[overlap_cell[1]]:
                    counter += 1
                if word == word_n:
                    counter += 1
    if counter not in counter_dict:
        counter_dict[counter] = {word}
    else:
        counter_dict[counter].add(word)

max_elim = max(counter_dict.keys()) + 1
for x in range(max_elim):
    if x in counter_dict:
        all_values = list(counter_dict[x])
        for val in range(len(all_values)):
            order_domain.append(all_values[val])
            print(all_values[val])
# print(order_domain)
# print(counter_dict)
# print("max: ",max(counter_dict.keys()))

# print(creator.crossword.overlaps.keys())
print(creator.crossword.neighbors((Variable(1, 4, 'down', 4))))

#inference
# assign = assignment.copy()
assign = {Variable(0, 1, 'down', 5): 'SEVEN', Variable(0, 1, 'across', 3): 'SIX'}
arcs = []
for var in assign:
    neigh_x = creator.crossword.neighbors(var) 
    for each_n in neigh_x: 
        if each_n not in assign:
            overlap_cell = creator.crossword.overlaps[(var,each_n)]
            if overlap_cell != None:
                arcs.append((var,each_n))
                # print("lista overlaps: ",creator.crossword.overlaps)
print("lista overlaps keys: ",list(creator.crossword.overlaps.keys()))
print(arcs)
            # print("cell overlap: ",overlap_cell)
            # value_neigh = assign[each_n] 
            # ac3(self, arcs=None)
            # overlap_cell = self.crossword.overlaps[(var,each_n)]

#ARC-3
# queue = list(creator.crossword.overlaps.keys())
# print(queue)
# print(len(queue))
# Dequeue
# count = 0
# while len(queue) != 0:
#     for arc in queue:
#         queue.remove(arc)
    # if revise(arc[0],arc[1]):
        # if self.domains[arc[0]] == 0:
            #return False
        # for z in (creator.crossword.neighbors(arc[0])-{arc[1]}):
            # print((z,arc[0])) 
            # queue.append((z,arc[0]))
# return True
    # print("vecinos: ",creator.crossword.neighbors(arc[0]))
    # print("Y is: ",arc[1])
    # print("Z is: ",creator.crossword.neighbors(arc[0])-{arc[1]})
    # print(arc[0])
    # print(creator.domains[arc[0]])
    # print(type(creator.domains[arc[0]]))
    # print("vecinos: ",creator.crossword.neighbors(arc[0]))
    # print(f"x: {arc[0]}, y: {arc[1]}")

# prueba = set()
# print(len(prueba))


# prueba = (dict())
# print(prueba)

# Domain var
# order_domain = []
# for word in creator.domains[Variable(1, 4, 'down', 4)]:
#     order_domain.append(word)
# order_domain.append(creator.domains[Variable(1, 4, 'down', 4)])
# print(order_domain)
# print(creator.domains)
# print(creator.crossword.overlaps)

# assignment = dict()
# assignment[Variable(0, 1, 'down', 5)]='ONE'
# # unselected var
# unassigned = set(creator.domains.keys())-set(assignment.keys())
# min_rem = dict()
# degree_heu_dict = dict()
# # print(len(creator.crossword.neighbors(Variable(0, 1, 'down', 5))))
# pos_values = len(creator.crossword.words)
# for x in range(pos_values):
#     for var in unassigned:
#         length_dom = len(creator.domains[var])
#         if length_dom == x:
#             if x not in min_rem:
#                 min_rem[x] = {var}
#             else:
#                 min_rem[x].add(var)
# min_num_rem = min(list(min_rem.keys()))
# print(len(min_rem[min_num_rem]))
# # print(min_rem[min_num_rem])
# if len(min_rem[min_num_rem]) == 1:
#     print(min_rem[min_num_rem].pop())
# else:
#     for var in min_rem[min_num_rem]:
#         length_neigh = len(creator.crossword.neighbors(var))
#         if length_neigh not in degree_heu_dict:
#             degree_heu_dict[length_neigh] = {var}
#         else:
#             degree_heu_dict[length_neigh].add(var)
#     max_degree = max(list(degree_heu_dict.keys()))
#     if len(degree_heu_dict[max_degree]) == 1:
#         print(degree_heu_dict[max_degree].pop())
#     else:
#         list_choose = list(degree_heu_dict[max_degree])
#         print(list_choose[0])
    # for x in range(len(min_rem[min_num_rem])):
    #     for var in min_rem[min_num_rem]:
    #         # list_rem = list(min_rem[min_num_rem])
    #         # var = list_rem[x]
    #         length_neigh = len(creator.crossword.neighbors(var))
    #         if length_neigh == x:
    #             if x not in degree_heu_dict:
    #                 degree_heu_dict[x] = {var}
    #             else:
    #                 degree_heu_dict[x].add(var)
    #         # degree_heu_dict[var] = length_neigh
    #     # print(list_rem[var])
# print(degree_heu_dict)
# for var in unassigned:
#     length_neigh = len(creator.crossword.neighbors(var))
#     length_dom = len(creator.domains[var])
#     min_rem[var] = (length_dom)
# if 0 not in min_rem:
#     print(min_rem[0])

# print(creator.domains)
# print(min(list(min_rem.keys())))
# print(creator.crossword.words)
# print(set(creator.domains.keys()))
# print(set(assignment.keys()))
# print(set(creator.domains.keys())-set(assignment.keys()))

# assignment = dict()
# # Backtracking
# assign = assignment
# if assignment_complete(assign): 
    # return assign
# var = select_unassigned_variable(assign) 
# for value order_domain_values(var, assign) 
    # assign[var] = value 
    # if consistent(assign): 
        # assignment[var] = value 
        # inference 
        # result = backtrack(assignment) 
        # if result != None: 
            # result 
        # del my_dict['key'] 
# return None

# # Assigment
# print(creator.domains)
# assign = assignment
# completed = False
# for var in creator.crossword.variables: 
    # if var in assign:
        # if len(assign[var]) == 1:
            # completed == True 
        # else:
            # completed == False 
#         print(creator.domains[var])

# consisten
# assign = assignment
# is_consisten = False
# for var in assign: 
    # if var.length != len(assign[var]) 
        # return is_consisten 
    # if assign[var] not in self.domain[var]:
        # return is_consisten
    # for other_var in assign:
        # if var != other_var:
            # if assign[var] == assign[other_val]: 
                # return is_consisten
# is_consisten = True 
# return is_consisten

# order_domain_values
# assigned = set(self.domains.keys())-set(assignment.keys()) NO VA
# for value in creator.domains[var]:
    # unassign_neigh = creator.crossword.neighbors(var) - set(assignment.keys())
    # for var_neigh in unassign_neigh:
        # if self.crossword.overlaps[(var,var_neigh)] != None:
            # binary_cons = self.crossword.overlaps[(var,var_neigh)]
            # count = 0

# print(creator.crossword.neighbors(Variable(4, 1, 'across', 4)))
# print(creator.crossword.variables)
# print(creator.domains)
# for var in creator.domains:
#     print(var.length)

# order_domain = []
# for word in creator.domains[Variable(4, 1, 'across', 4)]:
#     order_domain.append(word)

# var = {Variable(4, 1, 'across', 4)}

# print(order_domain)

# ass = {Variable(0, 1, 'down', 5): 'SEVEN', Variable(0, 1, 'across', 3): 'SIX', Variable(4, 1, 'across', 4): 'NINE', Variable(1, 4, 'down', 4): 'FIVE'}

# def assignment_complete(assignment):
#         """
#         Return True if `assignment` is complete (i.e., assigns a value to each
#         crossword variable); return False otherwise.
#         """
#         # for every variable in assigment check if any 
#         # has more than one solution, if so return False
#         assign = assignment
#         completed = False
#         for var in creator.crossword.variables: 
#             if var in assign:
#                 print(assign[var])
#                 if len(assign[var]) == 1:
#                     completed == True 
#                 else:
#                     completed == False 

#         return completed

# print(assignment_complete(ass))
# # print(creator.crossword.variables)