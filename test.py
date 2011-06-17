#!/usr/bin/python

import setsolve

CARDS = [("3rfs", "2021"),
         ("1gbd", "0100"),
         ("2pfo", "1222")]

CARD_VECTORS = [("2012", [[2,],[0,],[1,],[2,]]),
                ("1001", [[1,],[0,],[0,],[1,]])]

TEST_DECK = "fixtures/good_deck_sets.txt"
TEST_DECK_SETS = "fixtures/good_deck_sets_answers.txt"

def test_readCard():
    for card_in,card_out in CARDS:
        assert setsolve.readCard(card_in) == card_out

def test_readDeck():
    deck_len = len(open(TEST_DECK, "r").readlines())
    out_deck = setsolve.readDeck(TEST_DECK)
    assert len(out_deck) == deck_len
    for card in out_deck:
        for c in card:
            assert c in ["0","1","2"]

def test_reprVectorConversions():
    for rep,vec in CARD_VECTORS:
        assert setsolve.reprFromVector(vec) == rep
        assert setsolve.vectorFromRepr(rep) == vec

def test_checkExists():
    VECTOR = [[1,],[2,],[4,]]
    DECK_YES = ["425", "264", "124"]
    DECK_NO = ["542", "274", "241"]
    assert setsolve.cardExists(VECTOR, DECK_YES) == True
    assert setsolve.cardExists(VECTOR, DECK_NO) == False

def test_findCardPermutations():
    VECTOR = [[1,2],[3,],[4,]]
    PERMS = [[[1,],[3,],[4,]],
             [[2,],[3,],[4,]]]
    for p in setsolve.findPermutations(VECTOR):
        assert p in PERMS

def test_findCardVectorComplement():
    VECTOR = [[1,2,5],[3,],[4,]]
    CARD = [[2,],[3,],[4,]]
    assert setsolve.cardVectorComplement(VECTOR, CARD) == [[1,5],[3,],[4,]]

def test_cardVariantDims():
    VECTORS = [
            ([[1,2,3],[3,],[4,]], [0,]),
            ([[2,3], [4,5], [6,]], [0,1]),
            ([[2,],[3,],[4,]], [])]
    for v_in, dims in VECTORS:
        assert setsolve.cardVectorVariantDims(v_in) == dims

def test_findSets():
    res = setsolve.findSets(TEST_DECK)
    ##sets = setsolve.readDeck(TEST_DECK_SETS)
    sets = [['0102', '1102', '2102'], ['1011', '1111', '1211']]
    print "SETS:%s" % (res,)
    assert len(res) == len(sets)
    for res_set in res:
        assert res_set in sets
    for ans_set in sets:
        assert ans_set in res

