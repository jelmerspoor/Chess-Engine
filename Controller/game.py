class Game:
    WHITE_PIECES = {1, 2, 3, 4, 5, 6}
    BLACK_PIECES = {7, 8, 9, 10, 11, 12}

    def __init__(self, board, gui):
        self.board = board
        self.gui = gui
        self.turn = 0                      # 0 = white, 1 = black
        self.firstClick = False
        self.firstClickRow = None
        self.firstClickCol = None

    def start(self):
        self.gui.updateBoard()

    def handleClick(self, x, y):
        row = y // self.gui.cellSize
        col = x // self.gui.cellSize

        if not self.firstClick:
            self.selectSquare(row, col)
        else:
            self.move(row, col)

    def selectSquare(self, row, col):
        piece = self.board.grid[row][col]

        if piece == 0:
            return
        if self.turn == 0 and piece not in self.WHITE_PIECES:
            return
        if self.turn == 1 and piece not in self.BLACK_PIECES:
            return 

        self.firstClick = True
        self.firstClickRow = row
        self.firstClickCol = col
        self.gui.highlight(row, col)

    def move(self, row, col):
        start_piece = self.board.grid[self.firstClickRow][self.firstClickCol]

        if self.turn == 0 and self.board.grid[row][col] in self.WHITE_PIECES:
            self.selectSquare(row, col)
            return

        if self.turn == 1 and self.board.grid[row][col] in self.BLACK_PIECES:
            self.selectSquare(row, col)
            return

        self.board.grid[row][col] = start_piece
        self.board.grid[self.firstClickRow][self.firstClickCol] = 0

        self.turn = 1 - self.turn

        self.firstClick = False

        self.gui.clearHighlights()
        self.gui.updateBoard()
