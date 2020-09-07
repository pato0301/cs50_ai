import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        print()
        for variable, word in assignment.items():
            print(word)
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        # Iterate through the domain of each variable 
        # and make them node consistent
        for var in self.domains:
            temp_set_words = self.domains[var].copy()
            for word in temp_set_words:
                if len(word) != var.length:
                    self.domains[var].remove(word)
        # raise NotImplementedError

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """

        var_x = x
        var_y = y
        is_arc_cons = False
        if self.crossword.overlaps[(var_x,var_y)] != None:
            temp_words_x = self.domains[var_x].copy()
            temp_words_y = self.domains[var_y].copy()
            binary_cons = self.crossword.overlaps[(var_x,var_y)]
            for word_x in temp_words_x:
                for word_y in temp_words_y:
                    if word_x[binary_cons[0]] == word_y[binary_cons[1]]:
                        is_arc_cons = True
                if not is_arc_cons:
                    self.domains[var_x].remove(word_x)
        
        return not is_arc_cons
        # raise NotImplementedError

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        if arcs == None:
            queue = list(self.crossword.overlaps.keys())
        else:
            queue = arcs
        # Dequeue
        while len(queue) != 0:
            for arc in queue:
                queue.remove(arc)
                if self.revise(arc[0],arc[1]):
                    if self.domains[arc[0]] == 0:
                        return False
                    for z in (self.crossword.neighbors(arc[0])-{arc[1]}):
                        queue.append((z,arc[0]))

        return True
        # raise NotImplementedError

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        # for every variable in assigment check if any 
        # has more than one solution, if so return False
        assign = assignment
        completed = False

        for var in self.crossword.variables:
            if var not in assign:
                completed = False
                return completed 

        completed = True  

        return completed
        # raise NotImplementedError

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """

        assign = assignment
        is_consisten = False
        # print(assign)
        for var in assign:
            # value = list(assign[var])[0]
            value = assign[var]

            if var.length != len(value): 
                return is_consisten

            if value not in self.domains[var]:
                return is_consisten
            for other_var in assign:
                if var != other_var:
                    value_other = assign[other_var]
                    if value == value_other: 
                        return is_consisten
            # Neighbors
            neigh_x = self.crossword.neighbors(var)
            for each_n in neigh_x:
                if each_n in assign:
                    value_neigh = assign[each_n]
                    overlap_cell = self.crossword.overlaps[(var,each_n)]
                    if value[overlap_cell[0]] != value_neigh[overlap_cell[1]]:
                        return is_consisten
        is_consisten = True 
        return is_consisten
        # raise NotImplementedError

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        order_domain = []
        assign = assignment.copy()
        neigh_x = self.crossword.neighbors(var)
        counter_dict = {}
        for word in self.domains[var]:
            counter = 0
            for each_n in neigh_x:
                if each_n not in assign:
                    for word_n in self.domains[each_n]:
                        # value_neigh = assign[each_n]
                        overlap_cell = self.crossword.overlaps[(var,each_n)]
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


        return order_domain
        # raise NotImplementedError

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """

        unassigned = set(self.domains.keys())-set(assignment.keys())

        min_rem = dict()
        degree_heu_dict = dict()
        poss_values = len(self.crossword.words)
        for x in range(poss_values):
            for var in unassigned:
                length_dom = len(self.domains[var])
                if length_dom == x:
                    if x not in min_rem:
                        min_rem[x] = {var}
                    else:
                        min_rem[x].add(var)
        min_num_rem = min(list(min_rem.keys()))
        if len(min_rem[min_num_rem]) == 1:
            return min_rem[min_num_rem].pop()
        else:
            for var in min_rem[min_num_rem]:
                length_neigh = len(self.crossword.neighbors(var))
                if length_neigh not in degree_heu_dict:
                    degree_heu_dict[length_neigh] = {var}
                else:
                    degree_heu_dict[length_neigh].add(var)
            max_degree = max(list(degree_heu_dict.keys()))
            if len(degree_heu_dict[max_degree]) == 1:
                return degree_heu_dict[max_degree].pop()
            else:
                list_choose = list(degree_heu_dict[max_degree])
                return list_choose[0]
        # raise NotImplementedError

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """

        assign = assignment.copy()

        if self.assignment_complete(assign): 
            return assign
        var = self.select_unassigned_variable(assign) 

        for value in self.order_domain_values(var, assign):
            assign[var] = value

            if self.consistent(assign): 
                assignment[var] = value 
                # inference 
                inferences = self.inference(assignment)
                if inferences:
                    list_inferred = self.enforce_inference(assignment)
                # fin inference 
                result = self.backtrack(assignment) 

                if result != None: 
                    return result 
                del assignment[var]
                list_inferred = self.enforce_inference(assignment,list_inferred=list_inferred,fail=True) 
            del assign[var] 
        return None
        # raise NotImplementedError

    def inference(self,assignment):
        assign = assignment.copy()
        arcs = []
        for var in assign:
            neigh_x = self.crossword.neighbors(var) 
            for each_n in neigh_x: 
                if each_n not in assign:
                    overlap_cell = self.crossword.overlaps[(var,each_n)]
                    if overlap_cell != None:
                        arcs.append((var,each_n))

        consistent = self.ac3(arcs=arcs)
        return consistent

    
    def enforce_inference(self,assignment,list_inferred=[],fail=False):
        assign = assignment.copy()

        if not fail: 
            for var in assign:
                if len(self.domains[var]) == 1:
                    value = list(self.domains[var])[0]
                    assignment[var] = value
                    list_inferred.append(var)
        else:
            list_inferred_loop = list_inferred.copy()
            for var in list_inferred_loop:
                del assignment[var]
                list_inferred.remove(var) 
        
        return list_inferred

def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)

    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
