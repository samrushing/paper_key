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
    private: 5JhMXWnS1cneH8bghyPg1rB1A16P9bkNd8wg83owWVWDT9L7LKr
    public: 194Lh7bXfDh48CHyHESPGPsruP1t3bvCqJ
    private: 5K6odT3abhMZYzTejoYCnLaZH1NgjTzqZq3bPVZjsMY37aQpzQi
    public: 1M325fFAZXGGadEw7d44tgVm9Qbvbuhx7Z
    private: 5JRVAr7PfDZFR4EMaWo5HG4QPLrKEdKLaddCGJqCMTjN8Cmxg4X
    public: 14cnNH6bUCXGJHmyUcfd6fzyjnss8J3NaU

Send them to your printer:

    $ python paper_key.py 5 | lpr

