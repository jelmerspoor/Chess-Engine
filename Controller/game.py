import sys

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
        self.castleRightsWhite = [True, True]  # [king side, queen side]
        self.castleRightsBlack = [True, True]  # [king side, queen side]
        self.enPassantTarget = None

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

        match start_piece:
            case 1:
                 if self.movePawnWhite(row, col):
                     return
            case 7:
                if self.movePawnBlack(row, col):
                    return
            case 2 | 8: 
                if self.moveBishop(row, col):
                    return
            case 3 | 9:
                if self.moveKnight(row, col):
                    return
            case 4 | 10:
                if self.moveRook(row, col):
                    return
                if self.turn == 0:
                    if self.firstClickCol == 0:
                        self.castleRightsWhite[1] = False
                    elif self.firstClickCol == 7:
                        self.castleRightsWhite[0] = False
                else:
                    if self.firstClickCol == 0:
                        self.castleRightsBlack[1] = False
                    elif self.firstClickCol == 7:
                        self.castleRightsBlack[0] = False
            case 5 | 11:
                if self.moveQueen(row, col):
                    return
            case 6 | 12:
                if self.moveKing(row, col):
                    return
                if self.turn == 0:
                    self.castleRightsWhite = [False, False]
                else:
                    self.castleRightsBlack = [False, False]

        old_piece = self.board.grid[row][col]
        self.board.grid[row][col] = start_piece
        self.board.grid[self.firstClickRow][self.firstClickCol] = 0

        if self.checkCheck():
            self.board.grid[self.firstClickRow][self.firstClickCol] = start_piece
            self.board.grid[row][col] = old_piece
            return
        
        self.board.grid[row][col] = self.checkPromotion(start_piece, row)

        if start_piece not in (1, 7):
            self.enPassantTarget = None

        self.turn = 1 - self.turn
        
        self.firstClick = False

        self.gui.clearHighlights()
        self.gui.updateBoard()


        if self.checkCheckmate():
            self.gui.showCheckmateScreen(self.turn)
            sys.exit()
        
        if self.checkStalemate():
            self.gui.showStalemateScreen()
            sys.exit()    

    def movePawnWhite(self, row, col):
    
        if self.firstClickRow - row == 1 and self.firstClickCol == col and self.board.grid[row][col] == 0:
            self.enPassantTarget = None
            return False

        if self.firstClickRow == 6 and self.firstClickRow - row == 2 and self.firstClickCol == col:
            if self.board.grid[5][col] == 0 and self.board.grid[row][col] == 0:
                self.enPassantTarget = (5, col)
                return False

        if self.firstClickRow - row == 1 and abs(self.firstClickCol - col) == 1:
            if self.board.grid[row][col] in self.BLACK_PIECES:
                self.enPassantTarget = None
                return False

            if self.enPassantTarget == (row, col):
                self.board.grid[row + 1][col] = 0 
                self.enPassantTarget = None
                return False

        return True

    def movePawnBlack(self, row, col):
        
        if self.firstClickRow - row == -1 and self.firstClickCol == col and self.board.grid[row][col] == 0:
            self.enPassantTarget = None
            return False

        if self.firstClickRow == 1 and self.firstClickRow - row == -2 and self.firstClickCol == col:
            if self.board.grid[2][col] == 0 and self.board.grid[row][col] == 0:
                self.enPassantTarget = (2, col)
                return False

        if self.firstClickRow - row == -1 and abs(self.firstClickCol - col) == 1:
            if self.board.grid[row][col] in self.WHITE_PIECES:
                self.enPassantTarget = None
                return False

            if self.enPassantTarget == (row, col):
                self.board.grid[row - 1][col] = 0
                self.enPassantTarget = None
                return False

        return True

    
    def moveBishop(self, row, col):
        if abs(self.firstClickRow - row) != abs(self.firstClickCol - col):
            return True
        step_row = 1 if row > self.firstClickRow else -1
        step_col = 1 if col > self.firstClickCol else -1
        r, c = self.firstClickRow + step_row, self.firstClickCol + step_col
        while r != row and c != col:
            if self.board.grid[r][c] != 0:
                return True
            r += step_row
            c += step_col
        return False
    
    def moveKnight(self, row, col):
        if (abs(self.firstClickRow - row) == 2 and abs(self.firstClickCol - col) == 1) or (abs(self.firstClickRow - row) == 1 and abs(self.firstClickCol - col) == 2):
            return False
        return True
    
    def moveRook(self, row, col):
        if self.firstClickRow != row and self.firstClickCol != col:
            return True
        if self.firstClickRow == row:
            step = 1 if col > self.firstClickCol else -1
            for c in range(self.firstClickCol + step, col, step):
                if self.board.grid[row][c] != 0:
                    return True
        else:
            step = 1 if row > self.firstClickRow else -1
            for r in range(self.firstClickRow + step, row, step):
                if self.board.grid[r][col] != 0:
                    return True
        return False
    
    def moveQueen(self, row, col):
        if self.firstClickRow == row or self.firstClickCol == col:
            return self.moveRook(row, col)
        elif abs(self.firstClickRow - row) == abs(self.firstClickCol - col):
            return self.moveBishop(row, col)
        return True
    
    def moveKing(self, row, col):
        if self.castle(row, col):
            return False
        if abs(self.firstClickRow - row) <= 1 and abs(self.firstClickCol - col) <= 1:
            return False
        return True
    
    def castle(self, row, col):
        if self.turn == 0:
            if row == 7 and col == 6 and self.castleRightsWhite[0]:
                if self.board.grid[7][5] == 0 and self.board.grid[7][6] == 0 and self.board.grid[7][7] == 4:
                    if not self.squareUnderAttack(7, 4) and not self.squareUnderAttack(7, 5) and not self.squareUnderAttack(7, 6):
                        self.board.grid[7][6] = 6
                        self.board.grid[7][5] = 4
                        self.board.grid[7][4] = 0
                        self.board.grid[7][7] = 0
                        return True
            elif row == 7 and col == 2 and self.castleRightsWhite[1]:
                if self.board.grid[7][3] == 0 and self.board.grid[7][2] == 0 and self.board.grid[7][1] == 0 and self.board.grid[7][0] == 4:
                    if not self.squareUnderAttack(7, 4) and not self.squareUnderAttack(7, 3) and not self.squareUnderAttack(7, 2):
                        self.board.grid[7][2] = 6
                        self.board.grid[7][3] = 4
                        self.board.grid[7][4] = 0
                        self.board.grid[7][0] = 0
                        return True
        else:
            if row == 0 and col == 6 and self.castleRightsBlack[0]:
                if self.board.grid[0][5] == 0 and self.board.grid[0][6] == 0 and self.board.grid[0][7] == 10:
                    if not self.squareUnderAttack(0, 4) and not self.squareUnderAttack(0, 5) and not self.squareUnderAttack(0, 6):
                        self.board.grid[0][6] = 12
                        self.board.grid[0][5] = 10
                        self.board.grid[0][4] = 0
                        self.board.grid[0][7] = 0
                        return True
            elif row == 0 and col == 2 and self.castleRightsBlack[1]:
                if self.board.grid[0][3] == 0 and self.board.grid[0][2] == 0 and self.board.grid[0][1] == 0 and self.board.grid[0][0] == 10:
                    if not self.squareUnderAttack(0, 4) and not self.squareUnderAttack(0, 3) and not self.squareUnderAttack(0, 2):
                        self.board.grid[0][2] = 12
                        self.board.grid[0][3] = 10
                        self.board.grid[0][4] = 0
                        self.board.grid[0][0] = 0
                        return True
        return False
    
    def checkPromotion(self, piece, row):
        if piece == 1 and row == 0:
            return self.gui.showPromotionScreen(self.turn)
        elif piece == 7 and row == 7:
            return self.gui.showPromotionScreen(self.turn)
        return piece

    def checkCheck(self):
        king_piece = 6 if self.turn == 0 else 12

        for r in range(8):
            for c in range(8):
                if self.board.grid[r][c] == king_piece:
                    return self.squareUnderAttack(r, c)
        return False
    
    def checkCheckmate(self):
        if not self.checkCheck():
            return False

        current_pieces = self.WHITE_PIECES if self.turn == 0 else self.BLACK_PIECES

        old_first_r = self.firstClickRow
        old_first_c = self.firstClickCol

        for r in range(8):
            for c in range(8):
                piece = self.board.grid[r][c]
                if piece not in current_pieces:
                    continue

                self.firstClickRow = r
                self.firstClickCol = c

                for new_r in range(8):
                    for new_c in range(8):

                        if r == new_r and c == new_c:
                            continue

                        if self.board.grid[new_r][new_c] in current_pieces:
                            continue

                        # Disable castling during search
                        if piece in (6, 12) and abs(new_c - c) > 1:
                            continue

                        captured = self.board.grid[new_r][new_c]
                        self.board.grid[new_r][new_c] = piece
                        self.board.grid[r][c] = 0

                        legal = True
                        oldEnPassant = self.enPassantTarget
                        match piece:
                            case 1:
                                legal = not self.movePawnWhite(new_r, new_c)
                            case 7:
                                legal = not self.movePawnBlack(new_r, new_c)
                            case 2 | 8:
                                legal = not self.moveBishop(new_r, new_c)
                            case 3 | 9:
                                legal = not self.moveKnight(new_r, new_c)
                            case 4 | 10:
                                legal = not self.moveRook(new_r, new_c)
                            case 5 | 11:
                                legal = not self.moveQueen(new_r, new_c)
                            case 6 | 12:
                                legal = not self.moveKing(new_r, new_c)

                        self.enPassantTarget = oldEnPassant
                        if legal and not self.checkCheck():
                            self.board.grid[r][c] = piece
                            self.board.grid[new_r][new_c] = captured
                            self.firstClickRow = old_first_r
                            self.firstClickCol = old_first_c
                            return False

                        self.board.grid[r][c] = piece
                        self.board.grid[new_r][new_c] = captured

        self.firstClickRow = old_first_r
        self.firstClickCol = old_first_c
        return True
    
    def checkStalemate(self):
        if self.chechInsufficientMaterial():
            return True

        if self.checkCheck():
            return False

        current_pieces = self.WHITE_PIECES if self.turn == 0 else self.BLACK_PIECES

        old_first_r = self.firstClickRow
        old_first_c = self.firstClickCol

        for r in range(8):
            for c in range(8):
                piece = self.board.grid[r][c]
                if piece not in current_pieces:
                    continue

                self.firstClickRow = r
                self.firstClickCol = c

                for new_r in range(8):
                    for new_c in range(8):

                        if r == new_r and c == new_c:
                            continue

                        if self.board.grid[new_r][new_c] in current_pieces:
                            continue

                        # Disable castling during search
                        if piece in (6, 12) and abs(new_c - c) > 1:
                            continue

                        captured = self.board.grid[new_r][new_c]
                        self.board.grid[new_r][new_c] = piece
                        self.board.grid[r][c] = 0

                        legal = True
                        oldEnPassant = self.enPassantTarget
                        match piece:
                            case 1:
                                legal = not self.movePawnWhite(new_r, new_c)
                            case 7:
                                legal = not self.movePawnBlack(new_r, new_c)
                            case 2 | 8:
                                legal = not self.moveBishop(new_r, new_c)
                            case 3 | 9:
                                legal = not self.moveKnight(new_r, new_c)
                            case 4 | 10:
                                legal = not self.moveRook(new_r, new_c)
                            case 5 | 11:
                                legal = not self.moveQueen(new_r, new_c)
                            case 6 | 12:
                                legal = not self.moveKing(new_r, new_c)

                        self.enPassantTarget = oldEnPassant
                        if legal and not self.checkCheck():
                            self.board.grid[r][c] = piece
                            self.board.grid[new_r][new_c] = captured
                            self.firstClickRow = old_first_r
                            self.firstClickCol = old_first_c
                            return False

                        self.board.grid[r][c] = piece
                        self.board.grid[new_r][new_c] = captured

        self.firstClickRow = old_first_r
        self.firstClickCol = old_first_c
        return True

    def chechInsufficientMaterial(self):
        pieces = []
        for r in range(8):
            for c in range(8):
                piece = self.board.grid[r][c]
                if piece != 0:
                    pieces.append(piece)

        if len(pieces) == 2:
            return True

        if len(pieces) == 3:
            if pieces.count(2) == 1 or pieces.count(8) == 1:
                return True
            if pieces.count(3) == 1 or pieces.count(9) == 1:
                return True

        if len(pieces) == 4:
            if (pieces.count(2) == 1 or pieces.count(3) == 1) and (pieces.count(8) == 1 or pieces.count(9) == 1):
                return True

        return False


    def squareUnderAttack(self, row, col):
        opponent_pieces = self.BLACK_PIECES if self.turn == 0 else self.WHITE_PIECES

        for r in range(8):
            for c in range(8):
                piece = self.board.grid[r][c]
                if piece not in opponent_pieces:
                    continue

                match piece:
                    case 1:
                        if self.attackByPawnWhite(r, c, row, col):
                            return True
                    case 7:
                        if self.attackByPawnBlack(r, c, row, col):
                            return True
                    case 2 | 8:
                        if self.attackByBishop(r, c, row, col):
                            return True
                    case 3 | 9:
                        if self.attackByKnight(r, c, row, col):
                            return True
                    case 4 | 10:
                        if self.attackByRook(r, c, row, col):
                            return True
                    case 5 | 11:
                        if self.attackByQueen(r, c, row, col):
                            return True
                    case 6 | 12:
                        if self.attackByKing(r, c, row, col):
                            return True

        return False

    def attackByPawnWhite(self, r, c, row, col):
        return (r == row + 1) and (c == col - 1 or c == col + 1)

    def attackByPawnBlack(self, r, c, row, col):
        return (r == row - 1) and (c == col - 1 or c == col + 1)

    def attackByKnight(self, r, c, row, col):
        return (abs(r - row) == 2 and abs(c - col) == 1) or (abs(r - row) == 1 and abs(c - col) == 2)

    def attackByBishop(self, r, c, row, col):
        if abs(r - row) != abs(c - col):
            return False
        step_row = 1 if row > r else -1
        step_col = 1 if col > c else -1
        r_curr, c_curr = r + step_row, c + step_col
        while r_curr != row and c_curr != col:
            if self.board.grid[r_curr][c_curr] != 0:
                return False
            r_curr += step_row
            c_curr += step_col
        return True

    def attackByRook(self, r, c, row, col):
        if r != row and c != col:
            return False
        if r == row:
            step = 1 if col > c else -1
            for c_curr in range(c + step, col, step):
                if self.board.grid[r][c_curr] != 0:
                    return False
        else:
            step = 1 if row > r else -1
            for r_curr in range(r + step, row, step):
                if self.board.grid[r_curr][c] != 0:
                    return False
        return True

    def attackByQueen(self, r, c, row, col):
        if r == row or c == col:
            return self.attackByRook(r, c, row, col)
        elif abs(r - row) == abs(c - col):
            return self.attackByBishop(r, c, row, col)
        return False
    
    def attackByKing(self, r, c, row, col):
        return abs(r - row) <= 1 and abs(c - col) <= 1