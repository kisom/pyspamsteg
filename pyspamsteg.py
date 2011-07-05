#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: kyle isom <coder@kyleisom.net>
# license: ISC / public domain dual license
#
# implementing spamsteg from
#     http://programmingpraxis.com/2011/06/10/steganography/

import math

def read(message):
    message.replace('\r', '')
    message = message.strip().split('\n\n')

    if len(message) < 2:
        return None
    
    message = [ token for token in message[1:] if token.strip() ]
    message = ' '.join(message)
    return decode(message)


def decode(body):
    """
    Read a body of an email message and return the message.
    """

    byte_position = 0 # current position in the current byte
    bit_position = 0  # current position in the bit stream

    tokens  = body.split( ' ' )
    bits    = len(tokens)
    bytes  = int(math.ceil( bits / 8.0 ))

    plaintext = '' # the eventual decrypted message

    for byte in range(bytes):

        current_byte = 0x00
        
        for byte_position in range(0, 8):

            # deal with partially-filled bytes
            bit_position = byte * 8 + byte_position
            if bit_position == bits:
                break

            if len(tokens[bit_position]) % 2:
                current_byte = current_byte | ( 1 << 7 - byte_position )

        current_byte = chr(current_byte)
        plaintext += current_byte

    return plaintext

def create(message):
    return encode(message)

def encode(message):
    return ''
