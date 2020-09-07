import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if len(self.cells) == self.count:
            return self.cells
        #raise NotImplementedError

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            return self.cells
            
        #raise NotImplementedError

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

        #raise NotImplementedError

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)
        #raise NotImplementedError


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []
    
    def neighbor(self,cell):
        neigh = set()
        # Get Neighbors
        for i in range(max(0,cell[0]-1),min(self.height,cell[0]+2)):
            for j in range(max(0,cell[1]-1),min(self.width,cell[1]+2)):
                if (i,j) != cell and (i,j) not in self.safes:
                    neigh.add((i,j))
        return neigh

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """

        # Mark cell a a move made
        self.moves_made.add(cell)

        # Mark cell as a safe one
        if cell not in self.safes:
            self.mark_safe(cell)
        
        # Add new sentence to knowledge
        neighbors = self.neighbor(cell)

        self.knowledge.append(Sentence(neighbors,count))

        # Mark new cells as safe or mine if can be infered
        safe_cell_known = set()
        mine_cell_known = set()
        new_inferences = []

        for sentence in self.knowledge:
            if len(sentence.cells) == 0:
                self.knowledge.remove(sentence)
            elif sentence.count == 0:
                safe_cell_known = sentence.cells.copy()
                for cell in safe_cell_known:
                    self.mark_safe(cell)
                self.knowledge.remove(sentence)
                safe_cell_known.clear()
        
        for sentence in self.knowledge:
            if len(sentence.cells) == sentence.count:
                mine_cell_known = sentence.cells.copy()
                for cell in mine_cell_known:
                    self.mark_mine(cell)
                self.knowledge.remove(sentence)
                mine_cell_known.clear()

        temp_knowledge = self.knowledge.copy()
        knowledge_view = []

        for sentence in self.knowledge:
            for sentence2 in self.knowledge:
                if (sentence,sentence2) in knowledge_view:
                    break
                if sentence.cells == sentence2.cells:
                    break
                elif len(sentence.cells) >= len(sentence2.cells):
                    break
                elif sentence.cells.issubset(sentence2.cells):
                    knowledge_view.append((sentence2,sentence))
                    new_count = sentence2.count - sentence.count
                    new_set = sentence2.cells - sentence.cells
                    new_sentence = Sentence(new_set,new_count) 
                    if sentence2 in temp_knowledge:
                        temp_knowledge.remove(sentence2)

                    if new_count == 0:
                        safe_cell_known = new_sentence.cells.copy()
                        for cell in safe_cell_known:
                            self.mark_safe(cell)
                        safe_cell_known.clear()
                    elif len(new_set) == new_count: 
                        mine_cell_known = new_sentence.cells.copy()
                        for cell in mine_cell_known:
                            self.mark_mine(cell)
                        mine_cell_known.clear()
                    else:
                        temp_knowledge.append(new_sentence)

        self.knowledge += new_inferences

        #raise NotImplementedError

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        for cell in self.safes:
            if cell not in self.mines and cell not in self.moves_made:
                return cell
        return None
        #raise NotImplementedError

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        if self.make_safe_move() is None:
            poss_moves = self.height * self.width
            for x in range(poss_moves):
                rand_i = random.randint(0, self.height-1)
                rand_j = random.randint(0, self.width-1)
                cell = (rand_i,rand_j)
                if cell not in self.mines and cell not in self.moves_made:
                    return cell
            return None

        #raise NotImplementedError
