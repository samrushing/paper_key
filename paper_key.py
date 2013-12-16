# -*- Mode: Python -*-

# standalone, self-contained paper wallet generator
import ctypes
import ctypes.util
import sys
import hashlib
from hashlib import sha256

ssl = ctypes.cdll.LoadLibrary (ctypes.util.find_library ('ssl'))

# this specifies the curve used with ECDSA.
NID_secp256k1 = 714 # from openssl/obj_mac.h

# thx to WyseNynja and https://github.com/jgarzik/python-bitcoinlib
# http://crypto.stackexchange.com/questions/8914/ecdsa-compressed-public-key-point-back-to-uncompressed-public-key-point
POINT_CONVERSION_COMPRESSED = 2

# Thx to Sam Devlin for the ctypes magic 64-bit fix.
def check_result (val, func, args):
    if val == 0:
        raise ValueError
    else:
        return ctypes.c_void_p (val)

ssl.EC_KEY_new_by_curve_name.restype = ctypes.c_void_p
ssl.EC_KEY_new_by_curve_name.errcheck = check_result
ssl.EC_KEY_get0_private_key.restype = ctypes.c_void_p
ssl.EC_KEY_get0_private_key.errcheck = check_result
ssl.BN_bn2hex.restype = ctypes.c_char_p

class KEY:

    def __init__ (self):
        self.k = ssl.EC_KEY_new_by_curve_name (NID_secp256k1)

    def __del__ (self):
        ssl.EC_KEY_free (self.k)
        self.k = None

    def generate (self):
        ssl.EC_KEY_generate_key (self.k)
        ssl.EC_KEY_set_conv_form (self.k, POINT_CONVERSION_COMPRESSED)

    def get_privkey_bignum (self):
        pk = ssl.EC_KEY_get0_private_key (self.k)
        return ssl.BN_bn2hex (pk).decode ('hex')

    def get_pubkey_bignum (self):
        size = ssl.i2o_ECPublicKey (self.k, 0)
        if size == 0:
            raise SystemError
        else:
            mb = ctypes.create_string_buffer (size)
            ssl.i2o_ECPublicKey (self.k, ctypes.byref (ctypes.pointer (mb)))
            return mb.raw

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

def key_to_address (s):
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

def pkey_to_address (s):
    kind = '\x80'
    # zero pad to 32 bytes
    padding = '\x00' * (32 - len (s))
    # flag the associated public key as a 'compressed' key.
    compressed_flag = '\x01'
    s0 = kind + padding + s + compressed_flag
    checksum = dhash (s0)[:4]
    return base58_encode (
        int ((s0 + checksum).encode ('hex'), 16)
        )

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        nkeys = int (sys.argv[1])
    else:
        nkeys = 1
    for i in range (nkeys):
        k = KEY()
        k.generate()
        pri = k.get_privkey_bignum()
        pub = k.get_pubkey_bignum()
        print pub.encode ('hex')
        print 'private:', pkey_to_address (pri)
        print 'public:', key_to_address (rhash (pub))
        k = None
