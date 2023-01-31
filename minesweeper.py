import itertools
import random
import copy



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
        if self.count==len( self.cells ):# if is true then do this part 
            return self.cells# return the paremter cells 

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count==0: # if is true then do this part
            return self.cells # return the premter cells 

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """

        if cell in self.cells: # if is true then do this part
            self.cells.remove( cell ) # delete cell
            self.count -=1# change the counter by minus 1
        else: # if the contion up is false do this part 
            pass# nothing change gust pass 


    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:# if contion true ( cell in set  )
            self.cells.remove(cell)# update and delete the cell
        else:# if not true do this part
            pass# nothiong change so just pass



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
        # mark  cell as it  moves  in game
        self.moves_made.add( cell ) # Keep track of which cells have been clicked on

        self.mark_safe( cell )# if its save you should marke it  and updat

        # add new sentence to AI knowledge base based on value of cell and count
        inti_cells=set() # add to AI
        counter=copy.deepcopy( count )
        nearest_Cells= self.return_close_cells(cell)  # returns colse cells  by calling method 
        for cell1 in nearest_Cells : # cell1 go over all close cells 
            if cell1 in self.mines : # if is true - the sell1 init
                counter-=1# minus the counter by 1
            if cell1 not in self.mines|self.safes: # if  its not init or not in safes then do this part 
                inti_cells.add( cell1 )# add cells tha unknown states

        new_sen=Sentence( inti_cells,counter ) # make the  new sentence
        if len( new_sen.cells )>0: #note : if its not empty 
            self.knowledge.append( new_sen )# add sentence
        #  print status
        # check sentences 
        self.check_knowledge()
        self.extra_inference()

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        for itme in self.safes-self.moves_made: # the idea is to find the first safe move "not taken before "
            # print status 
            return itme
        return None # if nothing 
        raise NotImplementedError

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """

        move=self.width*self.height # to use it in loop 

        while move>0:# while loop to go over all possibles in board  
            move-=1 # with each itration minus move by 1 
            Chosen_row=random.randrange( self.height ) # chose randomly 
            chosem_column=random.randrange( self.width ) # chose randomly and save it into column 
            if ( Chosen_row,chosem_column ) not in self.moves_made|self.mines: # look to the sets that has the made and safe   
                return ( Chosen_row,chosem_column ) # if its true that is not in these sets return psrametrs 

        return None # else return none  

        raise NotImplementedError
    def return_close_cells(self, cell):
        """
        return any cell that 1 cell from the cell we send in arf 
        """
        nearest_Cells=set() # to save all poissible next move 
        for i in range( self.height ) : # in this loop go over all rows 
            for j in range( self.width ) :# inner loop to go in each column
                if abs( cell[ 0]-i )<=1 and abs( cell[1 ]-j )<=1 and ( i, j )!= cell: # if the cell taken from set minus row or column are not eqaul to cell sneded" in parameter
                   nearest_Cells.add((i, j)) # add this cell to our set 
        return nearest_Cells # then return nearest possible cells
    def check_knowledge(self):
        """
        check our knowledge for new safe and  updates knowledge " if possible"

        """
        # take the knowledge 
        K_copy=copy.deepcopy(self.knowledge)# take a copy of knowledge to go over it and check 
        # note : i here refare to sentence
        for i in K_copy: # go over sentences by loop
            if len( i.cells )==0: # if there is no cells 
                # use try and except to handling
                try: # if it possible 
                    self.knowledge.remove(i) # remove 
                except ValueError: # or handle the Error by pass 
                    pass
            # look for all possibles 
            mines_copy =i.known_mines() # use the mines possbiles 
            copy_safes=i.known_safes()# or the possbiles we know its safe 
            # update knowledge if mine or safe was found
            if mines_copy:  # if its mine then
                for m in mines_copy:# go over all po 
                    self.mark_mine(m) # call the method up 
                    self.check_knowledge()# class our knowledge and check 
            if copy_safes:# if its safe then
                for safe in copy_safes:
                    # print(f"Marking {safe} as safe")
                    self.mark_safe(safe)
                    self.check_knowledge()
    def extra_inference(self):
        """
        update knowledge based on inference
        """
        #iteration
        for sent in self.knowledge: # sent refare to sentence
            for sent_2 in self.knowledge:# ent_2 refare to inner sentence 
                # in this part look if sentence  is subset of the inner sentence 
                if sent.cells.issubset( sent_2.cells ): # if its true then 
                    n_cells=sent_2.cells-sent.cells
                    n_count=sent_2.count-sent.count 
                    new_sent=Sentence(n_cells, n_count) #call a class and send new cells and counter to save them in new_sent
                    m=new_sent.known_mines() # m refare to mines 
                    s=new_sent.known_safes() # s refare to safes
                    if m:# if it true then 
                        for i in m :# go over all m " mines"
                            # print status 
                            self.mark_mine(i) # updated

                    if s:# if its true then
                        for j in s: # go over all s " safes"
                            # print status 
                            self.mark_safe(j)# updated 