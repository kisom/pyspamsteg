#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: kyle isom <coder@kyleisom.net>
# license: ISC / public domain dual license
#
# implementing spamsteg from
#     http://programmingpraxis.com/2011/06/10/steganography/

import math
import playfair

debug = False
charsize = 7
cryptf = playfair.PlayFair

def TRACE(*messages):
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
    message.replace('\r', '')
    message = message.strip().split('\n\n')

    if len(message) < 2:
        TRACE( '[!] invalid message length' )
        return None
    
    message = [ token.strip() for token in message[1:] if token.strip('\n') ]
    message = ' '.join(message).replace( '\n', ' ' )

    message = decode( message )

    if not None == passphrase:
        TRACE( '[+] decrypting with PlayFair' )
        P   = cryptf()
        key = P.make_key( passphrase )
        message = P.decrypt( message, key )
    else:
        TRACE( '[!] *not* encrypting' )
    
    return message


def decode(body):
    """
    Read a body of an email message and return the message.
    """

    byte_position = 0 # current position in the current byte
    bit_position = 0  # current position in the bit stream

    tokens  = body.split()
    bits    = len(tokens) 
    bytes  = int(math.ceil( 1.0 * bits / charsize ))
    TRACE( bytes )

    plaintext = '' # the eventual decrypted message

    for byte in range(bytes):

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
