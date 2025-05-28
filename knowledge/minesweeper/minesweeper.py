import itertools
import random
from typing import List


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
        #all cells in the sentence are mines if the number of cells is equal to the count
        if len(self.cells) == self.count:
            return self.cells
        

        #should i return an empty set if im not certain that the cells are mines?
        empty_set = set()
        return None
        raise NotImplementedError

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            return self.cells
        
        empty_set = set()
        return empty_set
        raise NotImplementedError

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



    def cell_index_out_of_bounds(self, row_index, col_index) -> bool:
        if row_index < 0 or row_index > self.width - 1 or col_index < 0 or col_index > self.height - 1:
            return True
        return False
    


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
        #1 The function should mark the cell as one of the moves made in the game.
        self.moves_made.add(cell)

        #2 The function should mark the cell as a safe cell, updating any sentences that contain the cell as well.
        self.mark_safe(cell)

        #3 The function should add a new sentence to the AI’s knowledge base, based on the value of cell and count,
        # to indicate that count of the cell’s neighbors are mines. Be sure to only include cells whose state is 
        # still undetermined in the sentence.
        new_sentence_cells = set() #Set where the neighboring cells will be added
        #iterate over the eight neighboring cells, ignoring them if they are out of bounds, or known mines/safes
        for row in range(-1, 2):
          for col in range(-1, 2):
                if not (self.cell_index_out_of_bounds(cell[0] + row, cell[1] + col)) and not (row == cell[0] and col == cell[1]): #checks out of bounds and that its not the cell itself
                    new_cell = (cell[0] + row, cell[1] + col)
                    if new_cell not in (self.mines or self.safes): #add the cell if its state is not already known
                        new_sentence_cells.add(new_cell)

        #add new sentence with the cells to the KB
        self.knowledge.append(Sentence(new_sentence_cells, count))

        #If, based on any of the sentences in self.knowledge, new cells can be marked as safe or as mines, 
        #then the function should do so.
        new_safe_cells = set()
        new_mines = set()
        for sentence in self.knowledge:
            if sentence.known_safes():
                for c in sentence.cells:
                    new_safe_cells.add(c)
            if sentence.known_mines():
                for c in sentence.cells:
                    new_mines.add(c)
        self.safes = self.safes.union(new_safe_cells)
        self.mines = self.safes.union(new_mines)

        #If, based on any of the sentences in self.knowledge, new sentences can be inferred 
        # (using the subset method described in the Background),
        # then those sentences should be added to the knowledge base as well.

        def add_possible_inferences(self):
    
            new_sentence_list: List[Sentence] = [] 
            for i, sentence in enumerate(self.knowledge): #loop over each sentence, comparing it to other sentences, no pair-comparisons
                for other_sentence in self.knowledge[i + 1:]:
                    
                    if sentence.cells <= other_sentence.cells: #Check for true subsets and make new sentences if possible
                        cells = other_sentence.cells.difference(sentence.cells)
                        count = other_sentence.count - sentence.count 
                        new_sentence_list.append(Sentence(cells= cells, count= count))

            self.knowledge.append(new_sentence_list) #add new sentences to KB
            if len(new_sentence_list) != 0: #compares the sentences again if there is new info in KB
                add_possible_inferences()

        #4
        #Iterate over the sentences and compare to all other sentences, if there are subsets, create new sentences:
        # change_in_KB = True
        # while change_in_KB:
        #     for sentence in self.knowledge:
        #         for other_sentence in self.knowledge:

        #             if sentence.cells <= other_sentence.cells: #if true subset, create new set which is intersection of sets
        #                 new_cell_set = other_sentence.cells.difference(sentence.cells)
        #                 new_cell_set_count = other_sentence.count - sentence.count
        #                 new_sentence = Sentence(new_cell_set, new_cell_set_count)
        #                 self.knowledge.append(new_sentence)

        #                 if new_sentence.known_safes(): #if the new sentence turns out to be all safe, add that
        #                     for cell in new_sentence.cells:
        #                         self.safes.add(cell)
        #                         self.mark_safe(cell)
                        
        #                 if new_sentence.known_mines(): #if the new sentence turns out to ne all mines, add that
        #                     for cell in new_sentence.cells:
        #                         self.mines.add(cell)
        #                         self.mark_safe(cell)
                        
        #                 change_in_KB = True            
        #             else:
        #                 change_in_KB = False
                            
        

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        safe_moves_not_made_set = self.safes.difference(self.moves_made)
        if len(safe_moves_not_made_set) != 0:
            safe_moves_not_made_list = list(safe_moves_not_made_set) #must make to sequence, like list, to use random
            return random.choice(safe_moves_not_made_list) 
        else:
            return None
        #raise NotImplementedError

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        possible_choices = []
        for r in range(self.height):
            for c in range(self.width):
                if (r, c) not in (self.moves_made or self.mines):
                    possible_choices.append((r, c))

        return random.choice(possible_choices) 

        raise NotImplementedError
