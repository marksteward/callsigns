Callsigns
=========

Generates a list of available amateur radio callsigns from Ofcom's
website. In order to reduce the number of hits, this will check a
previous list of callsigns and filter it down to the available ones.

How to use
==========

1. Copy `config.py.sample` to `config.py` and edit to fill in the details.
2. Run `./callsigns.py ./foundation.txt | tee ./foundation_new.txt`,
   where `foundation.txt` is the list of existing callsigns.
3. If your run is successful, copy `foundation_new.txt` to
   `foundation.txt`, and submit a pull request.

If you're creating a list for a new prefix, or want to check for callsigns
that have been returned to the pool, you can use the following
command to generate all possible three-letter callsigns for a prefix:
    ./generate_callsigns.py M7 > ./callsigns.txt

Then filter them using `callsigns.py`.

Requires
========

* python2.6
* lxml

