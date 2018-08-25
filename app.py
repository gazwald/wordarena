#!/usr/bin/env python3
import random
import sys
import numpy as np


class Player:
    def __init__(self, name):
        self.name = name
        self.rack = []

    def __str__(self):
        return self.name

    def append_rack(self, tile):
        self.rack.append(tile)

    def show_rack(self):
        return self.rack

    def remove_from_rack(self, letters):
        for tile in self.rack:
            if tile.letter in letters:
                self.rack.remove(tile)


class Tile:
    def __init__(self, letter, points):
        self.letter = letter
        self.points = points
        self.x = None
        self.y = None
        self.z = None

    def __str__(self):
        return self.letter

    def __repr__(self):
        return self.__str__()


class Bonus:
    def __init__(self, name, multiplier, x, y, z=None):
        self.x = x
        self.y = y
        self.z = z
        self.name = name
        self.multiplier = multiplier


class WordBonus(Bonus):
    def __init__(self):
        pass


class LetterBonus(Bonus):
    def __init__(self):
        pass


class Board:
    def __init__(self, width, height, depth=None):
        self.width = width
        self.height = height
        self.depth = depth
        self.board = [[None for x in range(self.width)] for y in range(self.height)]

    def show_geometry(self):
        return dict(width=self.width,
                    height=self.height,
                    depth=self.depth)

    def add_entry(self, entry):
        if entry.alignment == 'v':
            for _, tile in enumerate(entry.entry):
                self.board[_][entry.y] = tile
        elif entry.alignment == 'h':
            for _, tile in enumerate(entry.entry):
                self.board[entry.x][_] = tile


class Bag:
    tiles = dict(blank={'count': 2, 'points': 0},
                 e={'count': 12, 'points': 1},
                 a={'count': 9, 'points': 1},
                 i={'count': 9, 'points': 1},
                 o={'count': 8, 'points': 1},
                 n={'count': 6, 'points': 1},
                 r={'count': 6, 'points': 1},
                 t={'count': 6, 'points': 1},
                 l={'count': 4, 'points': 1},
                 s={'count': 4, 'points': 1},
                 u={'count': 4, 'points': 1},
                 d={'count': 4, 'points': 2},
                 g={'count': 3, 'points': 2},
                 b={'count': 2, 'points': 3},
                 c={'count': 2, 'points': 3},
                 m={'count': 2, 'points': 3},
                 p={'count': 2, 'points': 3},
                 f={'count': 2, 'points': 4},
                 h={'count': 2, 'points': 4},
                 v={'count': 2, 'points': 4},
                 w={'count': 2, 'points': 4},
                 y={'count': 2, 'points': 4},
                 k={'count': 1, 'points': 5},
                 j={'count': 1, 'points': 8},
                 x={'count': 1, 'points': 8},
                 q={'count': 1, 'points': 10},
                 z={'count': 1, 'points': 10})

    def __init__(self):
        self.playable_tiles = []
        self.generate_tiles()

    def generate_tiles(self):
        for tile, value in self.tiles.items():
            _ = 0
            while _ != value.get('count'):
                self.playable_tiles.append(Tile(letter=tile,
                                                points=value.get('points')))
                _ += 1

    def assign_tile(self):
        return self.playable_tiles.pop(self.playable_tiles.index(random.choice(self.playable_tiles)))

    def remaining_tiles(self):
        return len(self.playable_tiles)


class Entry:
    def __init__(self, geometry, player, turn, entry, alignment, x, y, z=0):
        self.geometry = geometry
        self.entry = entry
        self.alignment = alignment
        self.turn = turn
        self.player = player
        self.x = int(x)
        self.y = int(y)
        self.z = int(z)
        self.length = len(entry)
        self.validation_functions = [self.validate_letters,
                                     self.validate_turn,
                                     self.validate_word]
        self.isvalid = True
        self.invalid_reason = None
        self.validate()

    def validate(self):
        for function in self.validation_functions:
            if not function():
                self.isvalid = False
                break

    def validate_letters(self):
        for letter in self.entry:
            if letter not in str(self.player.show_rack()):
                self.invalid_reason = '{} used tile they do not possess: letter'.format(self.player, letter)
                return False

        return True

    def validate_turn(self):
        start_x = int(self.geometry.get('width', 0) / 2)
        start_y = int(self.geometry.get('height', 0) / 2)
        if self.turn == 0:
            if self.alignment == 'h':
                if (self.x + self.length) >= start_x:
                    self.invalid_reason = '{} did not start ({}, {}) within the starting position: {} {}'.format(self.player,
                                                                                                                 self.x,
                                                                                                                 self.y,
                                                                                                                 start_x,
                                                                                                                 start_y)
                    return False
            elif self.alignment == 'v':
                if (self.y + self.length) >= start_y:
                    self.invalid_reason = '{} did not start ({}, {}) within the starting position: {} {}'.format(self.player,
                                                                                                                 self.x,
                                                                                                                 self.y,
                                                                                                                 start_x,
                                                                                                                 start_y)
                    return False
        else:
            if self.alignment == 'h':
                if self.length >= (self.geometry.get('width' - self.x)):
                    self.invalid_reason = 'Too long'
                    return False
            elif self.alignment == 'v':
                if self.length >= (self.geometry.get('depth' - self.y)):
                    self.invalid_reason = 'Too long'
                    return False

        return True

    def validate_word(self):
        return True


class Game:
    def __init__(self):
        self.board = Board(8, 8)
        self.bag = Bag()
        self.player1 = Player('Player 1')
        self.player2 = Player('Player 2')
        self.current_player = None
        self.starting_tiles = 7
        self.turn = 0
        _ = 0
        while _ != self.starting_tiles:
            self.player1.append_rack(self.bag.assign_tile())
            self.player2.append_rack(self.bag.assign_tile())
            _ += 1

        print(self.player1.show_rack())
        print(self.player2.show_rack())

        self.state_manager()

    def take_turn(self):
        try:
            entry = input('{}, enter a word:'.format(self.current_player))
            alignment = input('{}, enter a direction (h/v):'.format(self.current_player))
            x = input('{}, enter a x position:'.format(self.current_player))
            y = input('{}, enter a y position:'.format(self.current_player))
        except:
            raise

        new_entry = Entry(self.board.show_geometry(), self.current_player, self.turn, entry, alignment, x, y)

        if new_entry.isvalid:
            print("Success!")
            self.current_player.remove_from_rack(entry)
            self.replenish_tiles(new_entry.length)
            self.update_board(new_entry)
            return True
        else:
            print("Fail!")
            print(new_entry.invalid_reason)
            return False

    def replenish_tiles(self, count):
        _ = 0
        while _ != count:
            if self.bag.remaining_tiles() != 0:
                self.current_player.append_rack(self.bag.assign_tile())
                _ += 1
            else:
                break

    def update_board(self, entry):
        self.board.add_entry(entry)

    def switch_player(self):
        if self.current_player is self.player2:
            self.current_player = self.player1
        else:
            self.current_player = self.player2

    def state_manager(self):
        while True:
            print(np.matrix(self.board.board))
            print("Turn: {}".format(self.turn))
            self.switch_player()
            while True:
                try:
                    if self.take_turn():
                        break
                except KeyboardInterrupt:
                    self.quit()

            self.turn += 1
            print("{} turn end.".format(self.current_player))
            print("{} rack is: {}".format(self.current_player, self.current_player.show_rack()))

    def quit(self):
        print()
        print("Exiting...")
        sys.exit(0)


if __name__ == '__main__':
    new_game = Game()
