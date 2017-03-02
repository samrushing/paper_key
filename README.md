paper key
=========

This is a standalone bitcoin key generator for making paper wallets.
The goal: as much as possible, use pure python.  Keep the code short enough to be audited easily.

Dependencies for paper_key:

  * https://pypi.python.org/pypi/ecdsa

Dependcies for bip38:

  * https://pypi.python.org/pypi/pyaes/
  * https://pypi.python.org/pypi/scrypt/ -or-
  * https://pypi.python.org/pypi/pyscrypt

If you choose pyscrypt, then all dependencies are in python, and auditable.
Note however, pyscrypt takes about 3-5 minutes to encrypt/decrypt a key, on a fast machine.

It will generate a set of fresh keys and send them to stdout with the private keys in 'wallet import format'.

Depending on your level of paranoia, you could run this on a fresh VM, or simply redirect the output directly to a printer.

usage
-----

    $ python paper_key.py <number-of-keys>

Example:

    ampulex:paper_key rushing$ python paper_key.py 3
    private: L3rx4SDmX3kY4P8B1KngkzdS9qmWZbNoRS8u34dNkhZqeJsUPkE1
    public: 1GvzcndBngkUo35GjQs5MVysVEVtP2t2X
    private: L4KVi876oJCefon7G87Eu5wex4wgvGDgYdK6AmW1rNcM1TMTJGdC
    public: 16LaFUQmzXe77RCY7UGi7pgvFgx6ZG35eQ
    private: KzBHWT4iY7gfn69ojHnrTDbfjJYMKSRX5kQuGYVYSy5n3GBNQgh3
    public: 1JeW2uxWhGm7vhtFAtjZbkTPMQdZsYkZmp

Send them to your printer:

    $ python paper_key.py 5 | lpr


Encrypted BIP38 keys:

    usage: bip38.py [-h] [-n NUMKEYS] [-t] [keys [keys ...]]
    
    BIP38 key encoder/generator.
    
    positional arguments:
      keys                  WIF keys to wrap with BIP38, or BIP38 keys to decrypt
                            to WIF
    
    optional arguments:
      -h, --help            show this help message and exit
      -n NUMKEYS, --numkeys NUMKEYS
                            number of keys to generate
      -t, --test            run [some] BIP38 test vectors

    $ python bip38.py -n 3
    passphrase:
    again     :
    1CpYc1i3DUHFskk8uywT68t8FeBjUkYrzk
    6PRNCwpmVNhQx8MVhZRh4Sm8GGUiiwq7MGAZ8DGPpuruerd8kkFsdeb6x9
    19VQWDwnvNUiMAnA9dM1P7eKm3jncGYGtB
    6PRQWcV2yF1Pfo6PXHWpXNMGFet6dSWTwxjhuNxD2UKUGEocxUfpUguxEM
    1F6KCYKSL7GVD2qVYhuostHsRgEJSwkMRt
    6PRLvtN3KmvpKy3k5ZVR6EoJVoBgnkzXHP4YDYMPX3tgabUWDRGSBDkntN

Send encrypted keys to your printer:

    $ python bip38.py -n 3 | lpr

Decrypt an existing key:

    $ python bip38.py 6PRNCwpmVNhQx8MVhZRh4Sm8GGUiiwq7MGAZ8DGPpuruerd8kkFsdeb6x9
    passphrase:
    wif: 5JopRbTAnoBnd3WWt5UFDLkw2JYftAbs8rYBiZj9fz62H4Kkd9j
    pub: 1CpYc1i3DUHFskk8uywT68t8FeBjUkYrzk

Encrypt an existing key:

    $ python bip38.py 5JopRbTAnoBnd3WWt5UFDLkw2JYftAbs8rYBiZj9fz62H4Kkd9j
    passphrase:
    6PRNCwpmVNhQx8MVhZRh4Sm8GGUiiwq7MGAZ8DGPpuruerd8kkFsdeb6x9

