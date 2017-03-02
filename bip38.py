# -*- Mode: Python; coding: utf-8 -*-

# see the BIP38 spec:
#   https://github.com/bitcoin/bips/blob/master/bip-0038.mediawiki
#
# This implements only the simple non-ec-multiply version,
#   with uncompressed keys.

import getpass
import pyaes
import scrypt
#import pyscrypt as scrypt

from paper_key import *

b58_map = {}
for i, dig in enumerate (b58_digits):
    b58_map[dig] = i

def base58_decode (s):
    n = 0
    for ch in s:
        n *= 58
        digit = b58_map[ch]
        n += digit
    return n

class BadAddress (Exception):
    pass

def address_to_key (s, version=0, width=50):
    hex_format = '%%0%dx' % (width,)
    s = (hex_format % base58_decode (s)).decode ('hex')
    key, check0 = s[:-4], s[-4:]
    check1 = dhash (key)[:4]
    if key[0] != chr(version) or check0 != check1:
        raise BadAddress (s)
    return key[1:]

def xor16 (s0, s1):
    r = [0] * 16
    for i in range (16):
        r[i] = ord(s0[i]) ^ ord(s1[i])
    return ''.join (chr(x) for x in r)

def make_flagbyte (compressed=False):
    # 76543210
    # 76       == 11 - non-ec-multiplied key
    #   5      == pubkey compression
    #    4     == 0 reserved
    #     3    == 0 reserved
    #      2   == 0 lot/seq (0 for non-ec-mult key)
    #       10 == 0 reserved
    #     76543210
    r = 0b11000000
    r |= compressed << 5
    return chr(r)

def bip38_to_base58 (s0):
    checksum = dhash (s0)[:4]
    return base58_encode (
        int ((s0 + checksum).encode ('hex'), 16)
        )

def bip38_encrypt (wif, phrase=None):
    key0 = address_to_key (wif, 0x80)
    if len(key0) == 33 and key0[-1] == '\x01':
        raise NotImplementedError ("compressed keys not [yet] supported")
    elif len(key0) == 32:
        key1 = KEY (key0)
        pri, pub = key1.get_privkey(), key1.get_pubkey()
        address = pub_key_to_address (rhash (pub))
        # begin bip38
        address_hash = dhash (address)[:4]
        if phrase is None:
            phrase = getpass.getpass ("passphrase: ")
        derived = scrypt.hash (phrase, address_hash, 16384, 8, 8, 64)
        dhalf0, dhalf1 = derived[:32], derived[32:]
        aes = pyaes.AESModeOfOperationECB (dhalf1)
        ehalf0 = aes.encrypt (xor16 (dhalf0[:16], pri[:16]))
        ehalf1 = aes.encrypt (xor16 (dhalf0[16:32], pri[16:]))
        return bip38_to_base58 (
            '\x01\x42' + make_flagbyte() + address_hash + ehalf0 + ehalf1
        )
    else:
        raise ValueError ("strange/unknown wif format", wif)

def bip38_decrypt (enc0, phrase=None):
    enc1 = address_to_key (enc0, 0x01, width=86)
    if enc1[0] != '\x42':
        raise ValueError ("bad encrypted key", enc0)
    else:
        if phrase is None:
            phrase = getpass.getpass ("passphrase: ")
        flagbyte = enc1[1]
        address_hash = enc1[2:2+4]
        enc2 = enc1[6:]
        derived = scrypt.hash (phrase, address_hash, 16384, 8, 8, 64)
        dhalf0, dhalf1 = derived[:32], derived[32:]
        aes = pyaes.AESModeOfOperationECB (dhalf1)
        if flagbyte != '\xc0':
            raise ValueError ("unsupported flag byte", flagbyte)
        else:
            aes = pyaes.AESModeOfOperationECB (dhalf1)
            pri0 = xor16 (dhalf0[:16], aes.decrypt (enc2[:16]))
            pri1 = xor16 (dhalf0[16:], aes.decrypt (enc2[16:]))
            pri = pri0 + pri1
            key = KEY (pri)
            return key

def test():
    enc = '6PRVWUbkzzsbcVac2qwfssoUJAN1Xhrg6bNk8J7Nzm5H7kxEbn2Nh2ZoGg'
    wif = '5KN7MzqK5wt2TP1fQCYyHBtDrXdJuXbUzm4A9rKAteGu3Qi5CVR'
    key = 'TestingOneTwoThree'
    assert (enc == bip38_encrypt (wif, key))
    key = 'Satoshi'
    enc = '6PRNFFkZc2NZ6dJqFfhRoFNMR9Lnyj7dYGrzdgXXVMXcxoKTePPX1dWByq'
    wif = '5HtasZ6ofTHP6HCwTqTkLDuLQisYPah7aUnSKfC7h4hMUVw2gi5'
    assert (enc == bip38_encrypt (wif, key))    
    # using the NFC-normalized version.
    key = 'cf9300f0909080f09f92a9'.decode ('hex')
    wif = '5Jajm8eQ22H3pGWLEVCXyvND8dQZhiQhoLJNKjYXk9roUFTMSZ4'
    enc = '6PRW5o9FLp4gJDDVqJQKJFTpMvdsSGJxMYHtHaQBF3ooa8mwD69bapcDQn'
    assert (enc == bip38_encrypt (wif, key))

if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser (description='BIP38 key encoder/generator.')
    p.add_argument ('-n', '--numkeys', type=int, help="number of keys to generate")
    p.add_argument ('-t', '--test', help='run [some] BIP38 test vectors', action='store_true')
    p.add_argument ('keys', help="WIF keys to wrap with BIP38, or BIP38 keys to decrypt to WIF", nargs='*')

    args = p.parse_args()

    if args.test:
        test()

    for key in args.keys:
        if key.startswith ('5'):
            print bip38_encrypt (key)
        elif key.startswith ('6P'):
            k = bip38_decrypt (key)
            pri = k.get_privkey()
            pub = k.get_pubkey()
            print 'wif:', pri_key_to_address (pri, compressed=False)
            print 'pub:', pub_key_to_address (rhash (pub))
        else:
            raise ValueError ("unknown key type", key)
    
    if args.numkeys > 0:
        phrase0 = getpass.getpass ("passphrase: ")
        phrase1 = getpass.getpass ("again     : ")
        if phrase0 != phrase1:
            raise ValueError ("passphrase mismatch")
        else:
            for i in range (args.numkeys):
                pri, pub = gen_one()
                wif = pri_key_to_address (pri)
                print pub_key_to_address (rhash (pub))
                print bip38_encrypt (wif, phrase0)
                
    if not args.keys and not args.numkeys and not args.test:
        p.print_help()
