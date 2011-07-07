# implementation of the playfair cipher

import struct

DEF_KEYSPACE  = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
DEF_KEYSPACE += 'abcdefghijklmnopqrstuvwxyz'
DEF_KEYSPACE += '1234567890. '
LCMAP = ''.join( [ chr(i) for i in range( ord('a'), ord('k')) ] )

class Char:
    x = None
    y = None

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get(self):
        return (self.x, self.y)

class PlayFair:
    GRID_X = None                                           # number of columns
    GRID_Y = None                                           # number of rows
    passphrase = None
    keyspace = None

    get_row = lambda self, i : i / 8
    get_col = lambda self, i : i % 8
    get_idx = lambda self, char : self.keymap.find( char )
    map_lc  = lambda self, char: (LCMAP.find(char) + 1) % 10

    def get_char(self, char):
        idx = self.get_idx(char)
        x = self.get_col(idx)
        y = self.get_row(idx)

        return Char(x, y)
        
    def get_pos(self, *args):
        if 2 == len(args):
            x = args[0][0]
            y = args[0][1]
        if 3 == len(args):
            x = args[1]
            y = args[2]
        
    def __init__(self, keyspace = DEF_KEYSPACE, rows = 8, cols = 8):
        self.GRID_X = cols
        self.GRID_Y = rows
        self.keyspace = keyspace
        
    def get_digrams(self, message):
        digrams = [ ]

        while len(message) > 1:
            first, second = message[0], message[1]
            if first == second:
                second = 'X'
                message = message[1:]
            else:
                message = message[2:]

            digrams.append( first + second )

        if 1 == len( message ):
            digrams.append( message + 'X' )

        return digrams


    def make_key(self, passphrase):
        key = ''
        
        for char in passphrase:
            if char in self.keyspace and not char in key:
                if char in LCMAP:
                    char += str( self.map_lc(char) )
                key += char

        for char in self.keyspace:
            if not char in key:
                if char in LCMAP:
                    char += str( self.map_lc(char) )
                key += char
                
        return key

    def print_key(self, new_key = False, passphrase = None, key = None):
        if passphrase and new_key:
            key = self.make_key(passphrase)
        elif not key:
            return

        for y in range(self.GRID_Y):
            row = ''
            for x in range(self.GRID_X):
                row += key [ self.get_char(x, y) ] + ' '
            print row

    def encrypt( message, key ):
        digrams = get_digrams(message)
        ciphertext = ''

        for digram in digrams:
            a, b = get_char(digram[0]), get_char(digram[1])

            if a.y == b.y:
                a.y += 1
                b.y += 1
                ciphertext += key[ get_pos( a.get() ) ]
                ciphertext += key[ get_pos( b.get() ) ]
