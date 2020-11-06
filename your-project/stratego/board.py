import pygame
from .menu import *
import stratego
from .piece import Piece

class GameBoard:
    # TODO: calcular BOARD_SIDE_X, BOARD_SIDE_X & add to class variables
    def __init__(self, game):
        self.game = game
        self.board_color = GAME_BOARD_BACKGROUND
        self.board_x = 50
        self.board_y = 50
        self.board_h = GAME_BOARD_H
        self.board_w = GAME_BOARD_W
        self.side_bar_x = self.board_w + 100
        self.side_bar_h = SIDE_BAR_H
        self.side_bar_w = SIDE_BAR_W
        self.side_bar_color = SIDE_BAR_COLOR
        self.square_h = BLOCK_H
        self.square_w = BLOCK_W
        self.reg = []
        self.populate_board()

    ##########################
    #### functions ###########
    ##########################
    def check_input(self):
        if self.game.START_KEY:
            self.game.playing = False
        if self.game.MOUSE_POS != ():
            row, col = self.get_row_col_from_mouse()
            piece = self.get_piece(row, col)
            self.move(piece, 4,3)

    def blit_screen(self):
        self.game.window.blit(self.game.display, (0,0))
        pygame.display.update() # "send to monitor"
        self.game.reset_keys()

    def display_board(self):
        """Checks for input, blits board image to game surface & draws pieces possition acording to self.reg"""
        while self.game.playing == True:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            # side_bar
            self.draw_side_bar()
            # board
            self.draw_squares()
            # Checks for pieces pos in self.reg & calls piece method draw self
            # TODO: It may need to be a func on its own
            for row in range(ROWS):
                for col in range(COLS):
                    piece = self.reg[row][col]
                    if piece != 0:
                        piece.draw_piece()
            # send to display
            self.blit_screen()
            self.game.clock.tick(FPS)

    def draw_squares(self):
        """Draws the squares that make the board image"""
        pygame.draw.rect(self.game.display, self.board_color, (self.board_x, self.board_y,self.board_w, self.board_h), 0)
        # draws de colored squares to make the board image
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                pygame.draw.rect(self.game.display, SQ_COLOR, ((row*self.square_h)+self.board_y, (col *self.square_w)+self.board_x,self.square_h,self.square_h),0)

    def draw_side_bar(self):
        # font = pygame.font.Font(self.font_name, size)
        # text_surface = font.render('text', True, self.WHITE) # font.render(text, antialiasing, color)
        # text_rect = text_surface.get_rect() # rect obj(x,y, heigth, width)
        # text_rect.center = ((self.side_bar_w // 2, self.side_bar_h + 100) # coordinates
        # self.game.display.blit(text_surface,text_rect)
        pygame.draw.rect(self.game.display, self.side_bar_color, (self.side_bar_x, 0,self.side_bar_w, self.side_bar_h), 0)
        self.draw_text('STRATEGOpyHack',30,self.side_bar_x+self.side_bar_w//2,50)

    def draw_text(self, text, size, x,y):
        font = pygame.font.Font(self.game.font_name, size)
        text_surface = font.render(text, True, self.game.WHITE) # font.render(text, antialiasing, color)
        text_rect = text_surface.get_rect() # rect obj(x,y, heigth, width)
        text_rect.center = (x,y) # coordinates
        self.game.display.blit(text_surface,text_rect)

    def populate_board(self):
        """Draws the pieces at their initial possition"""
        for row in range(ROWS):
            # appends an empty list to the registry self.reg that represents rows
            self.reg.append([])
            for col in range(COLS):
                if row < BLUE_POS:
                    # appends the blue piece of to the corresponding initial row poss
                    self.reg[row].append(Piece(self.game, row, col, BLUE))
                elif row > RED_POS:
                    # appends the red piece obj to the corresponding initial row poss
                    self.reg[row].append(Piece(self.game, row, col, RED))
                else:
                    # appends zero to the empty pos
                    self.reg[row].append(0)

    def move(self, piece, row, col):
        """gets the piece player whants to move and where to move"""
        # piece.last_poss = (piece.x, piece.y)
        self.reg[piece.row][piece.col], self.reg[row][col] = self.reg[row][col], self.reg[piece.row][piece.col]
        piece.move(row, col)
        # Evaluate if fight, same team, etc.

    def get_piece(self, row, col):
        return self.reg[row][col]

    def get_row_col_from_mouse(self):
        x, y = self.game.MOUSE_POS
        row = int((y - self.board_y)/self.square_h)
        col = int((x - self.board_x)/self.square_w)
        return row, col
