#!/usr/bin/env python3
import random
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
    def __init__(self, x, y):
        self.x = x
        self.y = y


class LetterBonus(Bonus):
    def __init__(self, multiplier):
        self.multiplier = multiplier


class WordBonus(Bonus):
    def __init__(self, multiplier):
        self.multiplier = multiplier


class Board:
    def __init__(self):
        self.width = 7
        self.height = 7
        self.board = [[None for x in range(self.width)] for y in range(self.height)]
        print(np.matrix(self.board))


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
            count = 0
            while count != value.get('count'):
                self.playable_tiles.append(Tile(letter=tile,
                                                points=value.get('points')))
                count += 1

    def assign_tile(self):
        return self.playable_tiles.pop(self.playable_tiles.index(random.choice(self.playable_tiles)))


class Game:
    def __init__(self):
        self.bag = Bag()
        self.player1 = Player('Player 1')
        self.player2 = Player('Player 2')
        self.current_player = None
        count = 0
        while count != 7:
            self.player1.append_rack(self.bag.assign_tile())
            self.player2.append_rack(self.bag.assign_tile())
            count += 1

        print(self.player1.show_rack())
        print(self.player2.show_rack())

        self.state_manager()

    def take_turn(self):
        entry = input('{}, enter a word:'.format(self.current_player))
        return self.validate_entry(entry)

    def validate_entry(self, entry):
        print("Validating ,", entry)
        for letter in entry:
            if letter not in str(self.current_player.show_rack()):
                return False

        return True

    def switch_player(self):
        if self.current_player is self.player2:
            self.current_player = self.player1
        else:
            self.current_player = self.player2

    def state_manager(self):
        while True:
            self.switch_player()
            while True:
                if self.take_turn():
                    break


if __name__ == '__main__':
    new_board = Board()
    new_game = Game()
