#!/usr/bin/python
import re
import itertools
import sys

"""
First, some protocols:

    the deck is represented in a text file with one card per line, each line w/
    4 characters in sequence according to above vector layout, and with some
    combination of the following abbreviations:

    1  r(ed)     b(lank)       d(iamond)
    2  g(reen)   c(rosshatch)  s(quiggle)
    3  p(urple)  f(ill)        o(val)

    e.g., a card with 2 red-filled squiggles is 2rfs.

    each card is represented as a 4-d matrix, with the dimensions representing

            <count, color, content, shape>

    with each dimension having a value in {0,1,2}.
"""

TRANS_TABLE = [["1","2","3"], ["r","g","p"], ["b","c","f"], ["d","s","o"]]
def readCard(card):
    card = card.strip()
    
    return "".join(map(lambda i: str(TRANS_TABLE[i].index(str(card[i]))), range(0, 4)))

def readDeck(f_name):
    return map(lambda l: readCard(l), open(f_name, "r").readlines())

def findSets(deck_f_name):
    deck = readDeck(deck_f_name)
    print "deck: %s" % (deck,)
    sets = []
    for card in deck:
        print "testing %s" % (card,)
        card = vectorFromRepr(card)
        for dim_limit in range(1,len(card)+1):
            for dims in dimensionCombinations(dim_limit):
                test_card = list(card)
                for dim in dims:
                    print "dimension %d" % dim
                    test_card[dim] = list(set(range(3)).difference(card[dim]))
                ##res = filter(lambda d: len(d) == len(card)-1 and False not in d, findSetTree(test_card, deck))
                res = filter(lambda d: False not in d, findSetTree(test_card, deck))
                if len(res) > 0:
                    map(lambda d: d.append(card), res)
                    map(lambda d: sets.append(d), res)
    sets = map(lambda s: map(reprFromVector, s), sets)
    map(lambda s: s.sort(), sets)
    ret = []
    for s in sets:
        if s not in ret:
            ret.append(s)
    return ret

def findSetTree(card_vars_vector, deck):
    permutations = findPermutations(card_vars_vector)
    print "permutations: %s" % (permutations,)

    if len(permutations) == 1:
        if cardExists(permutations[0], deck):
            print "KAZAA"
            return card_vars_vector
        else:
            return False
    
    ret_perms = []
    for permutation in permutations:
        if cardExists(permutation, deck):
            ret_perms.append([permutation, findSetTree(cardVectorComplement(card_vars_vector, permutation), deck)])
    return ret_perms

def cardExists(card_vector, deck):
    return reprFromVector(card_vector) in deck

def findPermutations(card_vars_vector):
    """accepts a multi-dim card w/ 0 or more vector elements"""
    dims = cardVectorVariantDims(card_vars_vector)
    if len(dims) < 1:
        ## just one card
        return [card_vars_vector,]

    ##print "finding permutations for %d dimensions" % (len(dims))
    ## tricky bit here; need to keep dims coordinated with variant values
    variants = [card_vars_vector[i] for i in dims]
    perms = []
    for prod in list(itertools.product(*variants)):
        card_perm = list(card_vars_vector)
        for d_idx in range(len(dims)):  ## <-- argh!!!
            card_perm[dims[d_idx]] = [prod[d_idx],]
        perms.append(card_perm)
    ##print "%d permutations found" % (len(perms))
    return perms

def cardVectorComplement(card_vector, card_comp):
    if len(card_vector) != len(card_comp):
        raise Exception("error -- card-vector and card-comp not of same arity")
    ret_vector = []
    for i in range(0,len(card_vector)):
        if len(card_vector[i]) > 1:
            ret_vector.append(list(set(card_vector[i]).difference(card_comp[i])))
        else:
            ret_vector.append(card_vector[i])
    return ret_vector

def cardVectorVariantDims(card_vector):
    ## possibly:
    ## [i if len(card_vector[i]) > 1 for i in range(0,4)]
    dims = []
    for i in range(0, len(card_vector)):
        if len(card_vector[i]) > 1:
            dims.append(i)
    return dims

def reprFromVector(card_vector):
    return "".join(map(lambda e: str(e[0]), card_vector))
def vectorFromRepr(card):
    return [[int(card[i]),] for i in range(0,4)]

def dimensionCombinations(cnt):
    return list(itertools.combinations(range(4), cnt))


def main():
    if len(sys.argv) > 1:
        sets_res = findSets(sys.argv[1])
    else:
        print "please specify a file to read the deck from."
        sys.exit(0)
    print sets_res
