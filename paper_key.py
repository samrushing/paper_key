# -*- Mode: Python -*-

# Generate Bitcoin keys in WIF (wallet import format).

#
# https://github.com/warner/python-ecdsa
# $ easy_install ecdsa
#

# 20170221, still waiting for SEC format from python-ecdsa.
# until then, we can only use uncompressed public keys.

import ecdsa
import hashlib
from hashlib import sha256

class KEY:

    def __init__ (self, key=None):
        if key == None:
            self.generate()
        else:
            self.set_privkey (key)

    def generate (self):
        self.prikey = ecdsa.SigningKey.generate (curve=ecdsa.SECP256k1)
        self.pubkey = self.prikey.get_verifying_key()
        return self.prikey.to_der()

    def set_privkey (self, key):
        self.prikey = ecdsa.SigningKey.from_string (key, ecdsa.SECP256k1)
        self.pubkey = self.prikey.get_verifying_key()

    def set_pubkey (self, key):
        key = key[1:]
        self.pubkey = ecdsa.VerifyingKey.from_string (key, curve=secp256k1)

    def get_privkey (self):
        return self.prikey.to_string()

    def get_pubkey (self):
        return '\x04' + self.pubkey.to_string()

    def sign (self, msg):
        return self.prikey.sign_digest (msg)

    def verify (self, hash, sig):
        return self.pubkey.verify_digest (sig[:-1], hash, sigdecode=ecdsa.util.sigdecode_der)


b58_digits = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'

def base58_encode (n):
    l = []
    while n > 0:
        n, r = divmod (n, 58)
        l.insert (0, (b58_digits[r]))
    return ''.join (l)

def dhash (s):
    return sha256(sha256(s).digest()).digest()

def rhash (s):
    h1 = hashlib.new ('ripemd160')
    h1.update (sha256(s).digest())
    return h1.digest()

def pub_key_to_address (s):
    s = '\x00' + s
    checksum = dhash (s)[:4]
    encoded = base58_encode (
        int ((s + checksum).encode ('hex'), 16)
    )
    pad = 0
    for c in s:
        if c == '\x00':
            pad += 1
        else:
            break
    return ('1' * pad) + encoded

def pri_key_to_address (s, version=0x80, compressed=False):
    # zero pad to 32 bytes
    padding = '\x00' * (32 - len (s))
    if compressed:
        # flag the associated public key as a 'compressed' key.
        compressed_flag = '\x01'
    else:
        compressed_flag = ''
    s0 = chr(version) + padding + s + compressed_flag
    checksum = dhash (s0)[:4]
    return base58_encode (
        int ((s0 + checksum).encode ('hex'), 16)
        )

def gen_one (compressed=False):
    if compressed:
        raise NotImplementedError ("no support [yet] for compressed public keys")
    k = KEY()
    pri = k.get_privkey()
    pub = k.get_pubkey()
    return pri, pub

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        nkeys = int (sys.argv[1])
    else:
        nkeys = 1
    for i in range (nkeys):
        pri, pub = gen_one()
        if pub[0] in '\x02\x03':
            compressed = True
        elif pub[0] == '\x04':
            compressed = False
        else:
            raise ValueError ("unexpected public key SEC tag", pub)
        print 'wif:', pri_key_to_address (pri, compressed=compressed)
        print 'pub:', pub_key_to_address (rhash (pub))
        print
    
