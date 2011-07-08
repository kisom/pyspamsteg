# implementation of the playfair cipher

import struct

DEF_KEYSPACE8  = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
DEF_KEYSPACE8 += 'abcdefghijklmnopqrstuvwxyz'
DEF_KEYSPACE8 += '1234567890. '

DEF_KEYSPACE5 = 'ABCDEFGHIKLMNOPQRSTUVWXYZ'
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

    get_row = lambda self, i : i / self.GRID_Y
    get_col = lambda self, i : i % self.GRID_X
    get_idx = lambda self, char, key : key.find( char )
    map_lc  = lambda self, char: (LCMAP.find(char) + 1) % 10

    def get_char(self, char, key):
        idx = self.get_idx(char, key)
        x = self.get_col(idx)
        y = self.get_row(idx)

        return Char(x, y)
        
    def get_pos(self, *args):
        if 1 == len(args):
            x = args[0][0]
            y = args[0][1]
        elif 2 == len(args):
            x = args[0]
            y = args[1]
        else:
            raise Exception('invalid number of args: %d' % len(args))

        return x + (y * self.GRID_Y)
        
    def __init__(self, keyspace = DEF_KEYSPACE8, rows = 8, cols = 8):
        self.GRID_X = cols
        self.GRID_Y = rows
        
        self.keyspace = keyspace
        
    def get_digrams(self, message):
        digrams = [ ]

        while len(message) > 1:
            first, second = message[0], message[1]
            if not first in self.keyspace:
                message = message[1:]
                continue
            elif not second in self.keyspace:
                message = message[0] + message[2:]
                continue
            elif first == second:
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

    def encrypt( self, message, key ):
        digrams = self.get_digrams(message)
        ciphertext = ''

        grid = self.GRID_X * self.GRID_Y
        for digram in digrams:
            a, b = self.get_char(digram[0], key), self.get_char(digram[1], key)
            c, d = a, b

            if a.y == b.y:
                c.x += 1
                d.x += 1
            elif a.x == b.x:
                c.y += 1
                d.y += 1
            else:
                c = Char( b.x, a.y )
                d = Char( a.x, b.y )
                    
            ciphertext += key[ self.get_pos( c.get() ) % grid ]
            ciphertext += key[ self.get_pos( d.get() ) % grid ]

        return ciphertext

    def decrypt( self, ciphertext, key ):
        digrams = self.get_digrams(ciphertext)
        plaintext = ''

        grid = self.GRID_X * self.GRID_Y
        for digram in digrams:
            a, b = self.get_char(digram[0], key), self.get_char(digram[1], key)
            c, d = a, b

            if a.y == b.y:
                c.x -= 1
                d.x -= 1
            elif a.x == b.x:
                c.y -= 1
                d.y -= 1
            else:
                c = Char( b.x, a.y )
                d = Char( a.x, b.y )
                    
            plaintext += key[ self.get_pos( c.get() ) % grid ]
            plaintext += key[ self.get_pos( d.get() ) % grid ]

        return plaintext
        
