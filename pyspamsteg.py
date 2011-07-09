#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: kyle isom <coder@kyleisom.net>
# license: ISC / public domain dual license
#
# implementing spamsteg from
#     http://programmingpraxis.com/2011/06/10/steganography/

import math
import playfair

debug = False                                                # enable debug messages
charsize = 7                                                 # set character size:
                                                             #    7 bits for ASCII
                                                             #    8 bits for UTF-8
cryptf = playfair.PlayFair                                   # class providing
                                                             #   encrpyion

def TRACE(*messages):
    """
    Wrapper for print: prints all of its arguments on one line if debug is enabled.
    """
    if debug:
        for message in messages:
            print message,
        print
    else:
        return

def set_charsize(new_size):
    global charsize

    charsize = new_size

def read( message, passphrase = None ):
    """
    Function to read a properly-formatted message body, strip out the header,
    and decode the binary-encoded words (with decryption if a passphrase is provided).
    """

    # fix any windows line endings
    message.replace('\r', '')

    # split the message based on a blank line
    message = message.strip().split('\n\n')

    # should just be a message containing a header, the body, and possibly a footer.
    if len(message) < 2:
        TRACE( '[!] invalid message length' )
        return None

    # pull out the binary-encoded words. strips newlines and any trailing or leading
    # whitespace
    message = [ token.strip() for token in message[1] if token.strip('\n') ]
    message = ' '.join(message).replace( '\n', ' ' )

    # decode the message from binary-encoded words to the proper character sequence
    message = decode( message )

    if not None == passphrase:
        # if a passphrase was provided, decrypt
        TRACE( '[+] decrypting with PlayFair' )
        P   = cryptf()
        key = P.make_key( passphrase )
        message = P.decrypt( message, key )
    else:
        # otherwise TRACE a message alerting to the fact we are not decrypting
        TRACE( '[!] *not* encrypting' )

    # return the resulting decoded and potentially decrypted message
    return message


def decode(body):
    """
    Read a body of an email message containing binary-encoded words and return the
    message.
    """

    byte_position = 0 # current position in the current byte
    bit_position = 0  # current position in the bit stream

    # set up the token list and loop values:
    #     we separate out the tokens into a list for indexing
    tokens  = body.split()
    #     the number of tokens is the number of bits in the message
    bits    = len(tokens)
    #     the number of bytes is the number of bits divided by the character size
    bytes  = int(math.ceil( 1.0 * bits / charsize ))
    TRACE( bytes )

    message = '' # the eventual decoded message

    # build the plaintext one byte at a time
    for byte in range(bytes):
        # zero out the current byte
        current_byte = 0x00
        
        for byte_position in range(0, charsize):

            # deal with partially-filled bytes
            bit_position = byte * charsize + byte_position
            if bit_position == bits:
                break

            if len(tokens[bit_position]) % 2:
                TRACE( tokens[bit_position], '->', '1' )
                current_byte = current_byte | ( 1 << (charsize - 1) - byte_position )
            else:
                TRACE( tokens[bit_position], '->', '0' )

        current_byte = chr(current_byte)
        TRACE( '%d: %s' % (byte, current_byte) )
        plaintext += current_byte

    return plaintext

def create( message, passphrase = None ):
    return encode(message)

def encode(message):
    return ''
