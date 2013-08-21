
paper key
=========

This is a standalone bitcoin paper key generator.  It has no dependencies other than Python and OpenSSL.

It will generate a set of fresh keys and send them to stdout with the private keys in 'wallet import format'.

Depending on your level of paranoia, you could run this on a fresh VM, or simply redirect the output directly to a printer:

  $ python paper_keys.py 5 | lpr

