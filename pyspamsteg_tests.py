#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: kyle isom <coder@kyleisom.net>
# license: ISC / public domain dual license
#
# tests for python spam steganography

import pyspamsteg
import unittest

test_ct00  = 'zero one one zero one zero zero zero '
test_ct00 += 'zero one one zero one zero zero one'
test_pt00  = 'hi'

test_ct01  = 'message header\nsecondary message\n\n' + test_ct00
test_pt01  = 'hi'

test_ct02  = 'this is not a valid hidden message'


class PySpamStegTests(unittest.TestCase):
    
    def test_valid_decode(self):
        """
        Test to ensure the decoding of messages works. Decoding is the process of
        taking the binary-encoded words and transforming them into a character
        sequence. No encryption is used here.
        """
        self.assertEqual(pyspamsteg.decode(test_ct00), test_pt00)

    def test_valid_read(self):
        """
        Test case to ensure that a message can be read properly. This implicitly
        tests the decode function as well. This tests just the read and decode
        functions without testing the cipher suite.
        """
        self.assertEqual(pyspamsteg.read(test_ct01), test_pt01)

    def test_invalid_read(self):
        """
        Test case to ensure proper handling of improperly-formatted messages. Does not
        use the cipher suite.
        """
        self.assertEqual(pyspamsteg.read(test_ct02), None)

    def test_valid_encode(self):
        """
        Test case to verify the proper encoding of messages: taking a character
        sequence and converting that to binary-encoded words. Does not use encryption.
        """
        message = pyspamsteg.encode(test_pt00)
        self.assertEqual(pyspamsteg.decode(message), test_pt00)

    def test_valid_message_build(self):
        """
        Test case for the build function. Build is the opposite of read, and the output
        is a properly-formatted message body. Does not use encryption.
        """
        message = pyspamsteg.create(test_pt00)
        self.assertEqual(pyspamsteg.read(message), test_pt00)

    def test_build(self):
        """
        Test case to verify proper build and read of a steganograpic message with
        PlayFair encryption.
        """
        message = 'testing pyspamsteg'
        passphrase = 'pyspamsteg'
        
        ct = pyspamsteg.create( message, passphrase )
        pt = pyspamsteg.read( ct, passphrase )

        self.assertEquals( pt, message )

    def test_steg_vector(self):
        """
        Test case validating the test vector from the site. Uses PlayFair encryption.
        """
        expected_pt = 'Programming Praxis'
        passphrase  = "President Obama's visit to a Chrysler plant in Toledo, "
        passphrase += "Ohio, on Friday was the culmination of a campaign to "
        passphrase += "portray the auto bailouts as a brilliant success with "
        passphrase += "no unpleasant side effects."
        
        vector = open('tests/spam_example_vector').read()
        pyspamsteg.set_charsize( 7 )
        pt = pyspamsteg.read( vector, passphrase )

        self.assertEquals( pt, expected_pt )

if __name__ == '__main__':
    suite   = unittest.TestSuite()
    loader  = unittest.TestLoader()
    suite.addTests(loader.loadTestsFromTestCase(PySpamStegTests))
    unittest.TextTestRunner(verbosity = 2).run(suite)

