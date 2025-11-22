from View.chessGUI import ChessGUI

class Game:
    def __init__(self, board, gui):
        self.board = board
        self.gui = gui
        self.gui.run()

    def start(self):
        pass