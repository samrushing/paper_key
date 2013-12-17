paper key
=========

This is a standalone bitcoin paper key generator.  It has no dependencies other than Python and OpenSSL.

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

