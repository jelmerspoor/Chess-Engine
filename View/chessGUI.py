import tkinter as tk

PIECE_SYMBOLS = {
    1: "♙", 2: "♗", 3: "♘", 4: "♖", 5: "♕", 6: "♔",
    7: "♟", 8: "♝", 9: "♞", 10: "♜", 11: "♛", 12: "♚",
}

class ChessGUI:
    def __init__(self, board):
        self.board = board
        self.game = None
        self.cellSize = 80
        self.root = tk.Tk()
        self.canvas = tk.Canvas(self.root, width=8*self.cellSize, height=8*self.cellSize, bg='white')
        self.setupRoot()
        self.setupCanvas()
        
    def setupRoot(self):
        self.root.title("Chess-Engine")
        self.root.resizable(False, False)

    def setupCanvas(self):
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.click_handler)
        self.drawBoard()
        self.drawPieces()

    def drawBoard(self):
        self.canvas.delete("square")
        for row in range(8):
            for col in range(8):
                if (row + col) % 2 == 0:
                    color = "#F0D9B5"
                else:
                    color = "#B58863"
                x1 = col * self.cellSize
                y1 = row * self.cellSize
                x2 = x1 + self.cellSize
                y2 = y1 + self.cellSize
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, tags="square")
        
    def drawPieces(self):
        self.canvas.delete("piece")
        for row in range(8):
            for col in range(8):
                piece = self.board.grid[row][col]
                if piece != 0:
                    x = col * self.cellSize + self.cellSize // 2
                    y = row * self.cellSize + self.cellSize // 2
                    self.canvas.create_text(x, y, text=PIECE_SYMBOLS[piece], font=("Arial", 48), tags="piece")
    
    def clearHighlights(self):
        self.canvas.delete("highlight")

    def highlight(self, row, col):
        self.clearHighlights()

        x1 = col * self.cellSize
        y1 = row * self.cellSize
        x2 = x1 + self.cellSize
        y2 = y1 + self.cellSize

        self.canvas.create_rectangle(
            x1, y1, x2, y2,
            outline="#FFD700",
            width=2,
            tags="highlight"
        )

    def click_handler(self, event):
        if event.num == 1:
            self.game.handleClick(event.x, event.y)

    def updateBoard(self):
        self.drawBoard()
        self.drawPieces()
    
    def run(self):
        self.root.mainloop()
