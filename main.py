from Model.board import Board
from Controller.game import Game
from View.chessGUI import ChessGUI

def main():
    board = Board()
    gui = ChessGUI(board)
    game = Game(board, gui)
    game.start()

if __name__ == "__main__":
    main()