# implementation of the playfair cipher

import struct

DEF_KEYSPACE8  = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
DEF_KEYSPACE8 += 'abcdefghijklmnopqrstuvwxyz'
DEF_KEYSPACE8 += '1234567890. '

DEF_KEYSPACE5 = 'ABCDEFGHIKLMNOPQRSTUVWXYZ'
LCMAP = ''.join( [ chr(i) for i in range( ord('a'), ord('k')) ] )

class Char:
    """
    Class representation of a character in the grid. The character is stored as its
    (x, y) position in the grid with a get() method to return an tuple of the 
    character's (x, y) position.
    """
    x = None
    y = None

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get(self):
        """
        Return the (x, y) position of the character
        """
        return (self.x, self.y)

class PlayFair:
    """
    Class representation of the PlayFair cipher. For more information, see 
        https://secure.wikimedia.org/wikipedia/en/wiki/Playfair_cipher
        (wikipedia article)

        http://programmingpraxis.com/2009/07/03/the-playfair-cipher/
        (Programming Praxis introduciton with test vectors).

        In the code, the grid is stored as a single-dimension array of characters.
        The class includes helper functions to translate the index in this array
        to (x, y) grid coordinates and vice versa.
    """
    pad_char = None                                         # the padding character
                                                            #     for repeating chars
    GRID_X   = None                                         # number of columns
    GRID_Y   = None                                         # number of rows
    keyspace = None                                         # the sequence of valid
                                                            #     characters in the
                                                            #     grid.

    # pair of functions to return the row and column of an index position
    get_row = lambda self, i : i / self.GRID_Y
    get_col = lambda self, i : i % self.GRID_X

    # given a character and the key, find the character's position in the key
    get_idx = lambda self, char, key : key.find( char )

    # maps lowercase to digits for the 8x8 grid
    map_lc  = lambda self, char: (LCMAP.find(char) + 1) % 10

    # map encrypt and decrypt methods to the appropriate call to the cipher method
    encrypt = lambda self, message, key : self.cipher( message, key )
    decrypt = lambda self, message, key : self.cipher( message, key, encrypt = False )

    def get_char(self, char, key):
        """
        Builds a Char() instance based for a character. It searches the given key
        for the character, and the resulting Char() instance is initialised with that
        character's (x, y) coordinates.
        """
        idx = self.get_idx(char, key)
        x = self.get_col(idx)
        y = self.get_row(idx)

        return Char(x, y)
        
    def get_pos(self, *args):
        """
        Translates an (x, y) pair into an index position. Takes two forms of
        arguments:
            1. a tuple in the form (x, y) - ex. get_pos( (x, y) )
            2. a pair of arguments corresponding to x, y - ex. get_pos( x, y )
        """
        if 1 == len(args):
            x = args[0][0]
            y = args[0][1]
        elif 2 == len(args):
            x = args[0]
            y = args[1]
        else:
            raise Exception('invalid number of args: %d' % len(args))

        return x + (y * self.GRID_Y)
        
    def __init__(self, rows = 8, cols = 8, keyspace = DEF_KEYSPACE8, pad_char = 'X'):
        """
        The PlayFair instance should be initialised with the keyspace and number of
        rows and columns. By default, uses the 8x8 grid. The padding character may
        also be specified but defaults to 'X'.
        """
        self.GRID_X = cols
        self.GRID_Y = rows
        self.pad_char = pad_char
        self.keyspace = keyspace
        
    def get_digrams(self, message):
        """
        Breaks a message into pairs of characters, inserting the padding character
        as required.
        """
        digrams = [ ]

        # build digrams as long as we can pull a pair of characters out of the
        # message
        while len(message) > 1:
            first, second = message[0], message[1]

            # if the first character isn't in the keyspace, remove it and continue
            # on with building the digrams
            if not first in self.keyspace:
                message = message[1:]
                continue
            
            # same for the second character
            elif not second in self.keyspace:
                message = message[0] + message[2:]
                continue
            # if the two characters are the same, add the padding character in
            # between
            elif first == second:
                second = self.pad_char
                message = message[1:]

            # if both characters are in the keyspace and are not the same, the digram
            # is the first characters in the message.
            else:
                message = message[2:]

            digrams.append( first + second )

        # pad the message as necessary with an extra padding character
        if 1 == len( message ):
            digrams.append( message + self.pad_char )

        return digrams


    def make_key(self, passphrase):
        """
        Basic description of a PlayFair key from Programming Praxis:
        The pass-phrase is first filled in to the 5-square block, then the remaining
        letters of the alphabet complete the 5-square block, with duplicates removed.
        For instance, the pass-phrase PLAYFAIR leads to this 5-square block:

            P L A Y F
            I R B C D
            E G H K M
            N O Q S T
            U V W X Z

        The PlayFair instance doesn't necessarily use the 5x5 grid (or even by
        default), but the same basic principle applies to any size grid.
        """
        key = ''

        # build the first part of the key based on the passphrase: for every character
        # not already in the key, append it to the key
        for char in passphrase:
            if char in self.keyspace and not char in key:
                if char in LCMAP:
                    # the 8x8 grid appends numbers after the first ten lowercase
                    # characters (i.e. a...j inclusive).
                    char += str( self.map_lc(char) )
                key += char

        # the second part of the key generation is to append all the unused characters
        for char in self.keyspace:
            if not char in key:
                if char in LCMAP:
                    char += str( self.map_lc(char) )
                key += char
                
        return key

    def print_key(self, new_key = False, passphrase = None, key = None):
        """
        Pretty print the key in a grid format, i.e. for displaying / using by end
        users.
        """
        if passphrase and new_key:
            key = self.make_key(passphrase)
        elif not key:
            return

        for y in range(self.GRID_Y):
            row = ''
            for x in range(self.GRID_X):
                row += key [ self.get_char(x, y) ] + ' '
            print row

    def cipher( self, message, key, encrypt = True ):
        """
        Method to perform the PlayFair cipher functions. The documentation describes
        the process of encryption; decryption is simple the application of the rules
        in reverse. This should not be called directly but should be called using the
        encrypt() and decrypt() methods, which take a pair of arguments corresponding
        to the message and key, ex.:
            self.encrypt( message, key )
            self.decrypt( message, key )
        """

        # start by getting a list of digrams in the message
        digrams = self.get_digrams(message)

        # this is the resulting output; ciphertext if encrypt, plaintext if not encrypt
        result = ''

        # set the operation: +1 if encrypting, -1 if decrypting. documented further
        # in the actual cipher section below.

        # determine the maximum size of the grid for wrapping purposes.
        grid = self.GRID_X * self.GRID_Y

        # this is the actual cipher section, which operates over each digram
        for digram in digrams:

            # get the (x, y) coordinates of each character in the digram. this
            # makes the code clearer later on.
            # a and b are the original characters
            # c and d are the output characters (i.e. post-transformation)
            a, b = self.get_char(digram[0], key), self.get_char(digram[1], key)
            c, d = a, b

            # rule 1:
            #  If the two letters of the digram are in the same row, they are replaced
            #  pairwise by the letters to their immediate right, wrapping around to the
            #  left of the row if needed.
            if a.y == b.y:
                c.x += 1
                d.x += 1

            # rule 2:
            #  If the two letters of the digram are in the same column, they are
            #  replaced pairwise by the letters immediately below, wrapping around to
            #  the top of the column if needed.
            elif a.x == b.x:
                c.y += 1
                d.y += 1

            # rule 3:
            #  Otherwise, the first letter of the digram is replaced by the letter in
            #  the same row as the first letter of the digram and the same column as
            #  the second letter of the digram, and the second letter of the digram is
            #  replaced by the letter in the same row as the second letter of the
            #  digram and the same column as the first letter of the digram.
            else:
                c = Char( b.x, a.y )
                d = Char( a.x, b.y )

            # append the transformed characters to the result, ensuring characters
            # are wrapped as necessary (e.g. the % grid component)
            result += key[ self.get_pos( c.get() ) % grid ]
            result += key[ self.get_pos( d.get() ) % grid ]

        return result
