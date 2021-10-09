import random
import copy
from optparse import OptionParser
import util
import numpy as np

class SolveEightQueens:
    def __init__(self, numberOfRuns, verbose, lectureExample):
        """
        Value 1 indicates the position of queen
        """
        self.numberOfRuns = numberOfRuns
        self.verbose = verbose
        self.lectureCase = [[]]
        if lectureExample:
            self.lectureCase = [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 0],
            [1, 0, 0, 0, 1, 0, 0, 0],
            [0, 1, 0, 0, 0, 1, 0, 1],
            [0, 0, 1, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            ]
    def solve(self):
        solutionCounter = 0
        for i in range(self.numberOfRuns):
            if self.search(Board(self.lectureCase), self.verbose).getNumberOfAttacks() == 0:
                solutionCounter += 1
        print("Solved: %d/%d" % (solutionCounter, self.numberOfRuns))

    def search(self, board, verbose):
        """
        Hint: Modify the stop criterion in this function
        """
        newBoard = board
        i = 0 
        while True:
            if verbose:
                print("iteration %d" % i)
                print(newBoard.toString())
                print("# attacks: %s" % str(newBoard.getNumberOfAttacks()))
                print(newBoard.getCostBoard().toString(True))
            currentNumberOfAttacks = newBoard.getNumberOfAttacks()
            (newBoard, newNumberOfAttacks, newRow, newCol) = newBoard.getBetterBoard()
            i += 1
            if currentNumberOfAttacks < newNumberOfAttacks:
                break
            if i == 100:
                break

        return newBoard

class Board:
    def __init__(self, squareArray = [[]]):
        if squareArray == [[]]:
            self.squareArray = self.initBoardWithRandomQueens()
        else:
            self.squareArray = squareArray

    @staticmethod
    def initBoardWithRandomQueens():
        tmpSquareArray = [[ 0 for i in range(8)] for j in range(8)]
        for i in range(8):
            tmpSquareArray[random.randint(0,7)][i] = 1
        return tmpSquareArray
          
    def toString(self, isCostBoard=False):
        """
        Transform the Array in Board or cost Board to printable string
        """
        s = ""
        for i in range(8):
            for j in range(8):
                if isCostBoard: # Cost board
                    cost = self.squareArray[i][j]
                    s = (s + "%3d" % cost) if cost < 9999 else (s + "  q")
                else: # Board
                    s = (s + ". ") if self.squareArray[i][j] == 0 else (s + "q ")
            s += "\n"
        return s 

    def getCostBoard(self):
        """
        First Initalize all the cost as 9999. 
        After filling, the position with 9999 cost indicating the position of queen.
        """
        costBoard = Board([[ 9999 for i in range(8)] for j in range(8)])
        for r in range(8):
            for c in range(8):
                if self.squareArray[r][c] == 1:
                    for rr in range(8):
                        if rr != r:
                            testboard = copy.deepcopy(self)
                            testboard.squareArray[r][c] = 0
                            testboard.squareArray[rr][c] = 1
                            costBoard.squareArray[rr][c] = testboard.getNumberOfAttacks()
        return costBoard

    def getBetterBoard(self):
        """
        "*** YOUR CODE HERE ***"
        This function should return a tuple containing containing four values
        the new Board object, the new number of attacks, 
        the Column and Row of the new queen  
        For exmaple: 
            return (betterBoard, minNumOfAttack, newRow, newCol)
        The datatype of minNumOfAttack, newRow and newCol should be int
        """
        import random

        curr_attack = self.getNumberOfAttacks()
        if curr_attack == 0:
            return(Board(self.squareArray), self.getNumberOfAttacks(), -1, -1)

        new_board = copy.deepcopy(self)
        cost_board = self.getCostBoard()

        min_attack = min([cost_board.squareArray[r][c] for r in range(len(self.squareArray)) for c in range(len(self.squareArray[r]))])
        min_loc_index = [(r,c) for r in range(len(self.squareArray)) for c in range(len(self.squareArray[r])) if cost_board.squareArray[r][c]==min_attack]

        if min_attack <= curr_attack:
            new_row, new_col = random.choice(min_loc_index)
            old_row = [r for r in range(len(self.squareArray)) if cost_board.squareArray[r][new_col]==9999][0]

            new_board.squareArray[old_row][new_col] = 0
            new_board.squareArray[new_row][new_col] = 1

            return (new_board, new_board.getNumberOfAttacks(), new_row, new_col)

        else:
            return (self, self.getNumberOfAttacks(), -1, -1)

        util.raiseNotDefined()


    def getNumberOfAttacks(self):
        """
        "*** YOUR CODE HERE ***"
        This function should return the number of attacks of the current board
        The datatype of the return value should be int
        """
        attacking = 0

        for row in range(len(self.squareArray)):
            for column in range(len(self.squareArray[row])):
                if self.squareArray[row][column] == 1:
                    # top
                    for i in range(0, row):
                        if self.squareArray[i][column] == 1:
                            attacking += 1
                    # bottom
                    for i in range(row+1, len(self.squareArray[row])):
                        if self.squareArray[i][column] == 1:
                            attacking += 1
                    # left
                    for i in range(0, column):
                        if self.squareArray[row][i] == 1:
                            attacking += 1
                    # right
                    for i in range(column+1, len(self.squareArray)):
                        if self.squareArray[row][i] == 1:
                            attacking += 1
                    # top left
                    tmp_row, tmp_col = row, column
                    while tmp_row != 0 and tmp_col:
                        tmp_row -= 1
                        tmp_col -= 1
                        if self.squareArray[tmp_row][tmp_col] == 1:
                            attacking += 1
                    # top right
                    tmp_row, tmp_col = row, column
                    while tmp_row != 0 and tmp_col != len(self.squareArray)-1:
                        tmp_row -= 1
                        tmp_col += 1
                        if self.squareArray[tmp_row][tmp_col] == 1:
                            attacking += 1
                    # bottom left
                    tmp_row, tmp_col = row, column
                    while tmp_row != len(self.squareArray)-1 and tmp_col != 0:
                        tmp_row += 1
                        tmp_col -= 1
                        if self.squareArray[tmp_row][tmp_col] == 1:
                            attacking += 1
                    # bottom right
                    tmp_row, tmp_col = row, column
                    while tmp_row != len(self.squareArray[row])-1 and tmp_col != len(self.squareArray)-1:
                        tmp_row += 1
                        tmp_col += 1
                        if self.squareArray[tmp_row][tmp_col] == 1:
                            attacking += 1

        return int(attacking/2)

        util.raiseNotDefined()


if __name__ == "__main__":
    #Enable the following line to generate the same random numbers (useful for debugging)
    random.seed(1)
    parser = OptionParser()
    parser.add_option("-q", dest="verbose", action="store_false", default=True)
    parser.add_option("-l", dest="lectureExample", action="store_true", default=False)
    parser.add_option("-n", dest="numberOfRuns", default=1, type="int")
    (options, args) = parser.parse_args()
    EightQueensAgent = SolveEightQueens(verbose=options.verbose, numberOfRuns=options.numberOfRuns, lectureExample=options.lectureExample)
    EightQueensAgent.solve()
