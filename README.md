# setsolver

---

##overview

This is a script to find solutions for the card game Set. It works by creating permuations on each card and then recursively testing 3-card sequences. This script is somewhat specialized to Set (3 choices along 4 dimensions), but could be extended to any m-by-n dimensional pattern matcher.

##rundown

The deck is represented in a text file with one card per line, each line w/ 4 characters in sequence according to above vector layout, and with some combination of the following abbreviations:

    1  r(ed)     b(lank)       d(iamond)
    2  g(reen)   c(rosshatch)  s(quiggle)
    3  p(urple)  f(ill)        o(val)

e.g., a card with 2 solid red squiggles is `2rfs`.

Each card is represented internally as a 4D matrix, with the dimensions representing (in order)

    <count, color, content, shape>

with each dimension having a value in `{0,1,2}`.

## usage

To use the script, make a file with your deck in it, one card per line, e.g.:

    1gcd
    3pfo
    ..

Then run it on the command line via

    >> python ./setsolve.py deck.txt

The parser is none too smart, but this should do it.

