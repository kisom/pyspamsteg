#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: kyle isom <coder@kyleisom.net>
# license: ISC / public domain dual-licensed
#
# unit tests for the playfair implementation

import playfair
import unittest

class PlayFairTests(unittest.TestCase):

    def test_playfair5(self):
        P = playfair.PlayFair(playfair.DEF_KEYSPACE5, cols = 5, rows = 5)
        message = 'PROGRAMMING PRAXIS' 
        key = P.make_key( 'PLAYFAIR ')
        ct  = P.encrypt( 'PROGRAMMING PRAXIS', key )
        expected_ct = 'LIVOBLKZEDOELIYWCN'
        pt  = P.decrypt(ct, key)
        expected_pt = 'PROGRAMXMINGPRAXIS'

        self.assertEquals( len(ct), len(expected_ct) )
        self.assertEquals( ct, expected_ct )
        self.assertEquals( pt, expected_pt )

    def test_playfair(self):
        passphrase  = "President Obama's visit to a Chrysler plant in Toledo, "
        passphrase += "Ohio, on Friday was the culmination of a campaign to "
        passphrase += "portray the auto bailouts as a brilliant success with "
        passphrase += "no unpleasant side effects."

        key = "Pre5si9d4nt Ob2a1mvoCh8ylpTFwc3uf6g7.ABDEGHIJKLMNQRSUVWXYZj0kqxz"
        
        crypter = playfair.PlayFair()

        self.assertEquals(crypter.make_key(passphrase), key)

    
    
if __name__ == '__main__':
    suite   = unittest.TestSuite()
    loader  = unittest.TestLoader()
    suite.addTests(loader.loadTestsFromTestCase(PlayFairTests))
    unittest.TextTestRunner(verbosity = 2).run(suite)
