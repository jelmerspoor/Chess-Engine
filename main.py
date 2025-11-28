from Model.board import Board
from View.chessGUI import ChessGUI
from Controller.game import Game

def main():
    board = Board()
    gui = ChessGUI(board)
    game = Game(board, gui)

    gui.game = game
    game.start()
    gui.run()

if __name__ == "__main__":
    main()
