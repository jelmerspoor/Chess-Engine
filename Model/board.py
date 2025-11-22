    # Pawn: White = 1, Black = 7
    # Bishop: White = 2, Black = 8
    # Knight: White = 3, Black = 9
    # Rook: White = 4, Black = 10
    # Queen: White = 5, Black = 11
    # King: White = 6, Black = 12

class Board:
    def __init__(self):
        self.grid = [[0 for _ in range(8)] for _ in range(8)]
        self.setupPieces()

    def setupPieces(self):
        for i in range(8):
            self.grid[1][i] = 7
            self.grid[6][i] = 1

        self.grid[0][2], self.grid[0][5], self.grid[7][2], self.grid[7][5] = 8, 8, 2, 2
        self.grid[0][1], self.grid[0][6], self.grid[7][1], self.grid[7][6] = 9, 9, 3, 3
        self.grid[0][0], self.grid[0][7], self.grid[7][0], self.grid[7][7] = 10, 10, 4, 4
        self.grid[0][3], self.grid[7][3] = 11, 5
        self.grid[0][4], self.grid[7][4] = 12, 6

    def printBoard(self):
        for row in self.grid:
            print(row)
        print()

