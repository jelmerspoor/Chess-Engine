class Game:
    def __init__(self, board):
        self.board = board

    def start(self):
        while True:
            self.board.print_board()
            self.move()

    def move(self):
        x1, y1, x2, y2 = map(int, input("Enter x1 y1 x2 y2: ").split())
        temp = self.board.grid[x2][y2]
        self.board.grid[x2][y2] = self.board.grid[x1][y1]
        self.board.grid[x1][y1] = temp
