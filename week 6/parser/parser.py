import nltk
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to" | "until"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP | NP VP PP | NP VP Adv | NP | NP VP NP | NP VP NP PP | NP VP Conj VP
VP -> V | V NP | V NP PP | Adv V | V Adv
NP -> N | Det N | Det N N | Det N N PP | AP N | Det AP N | Det AP N | Det N PP
NP -> N Adv | Det N Adv | Det AP | N PP | AP N PP
PP -> P NP VP | P NP | P NP Conj NP VP | P NP VP PP | P Det Adj N
AP -> Adj | Adj Adj | Adj Adj Adj | Adj N Adv
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """

    s_token = nltk.word_tokenize(sentence)
    sentence_token = []

    for word in range(len(s_token)):
        s_token[word] = s_token[word].lower()
        if speller(s_token[word]):
            sentence_token.append(s_token[word])

    return sentence_token
    # raise NotImplementedError


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """

    np_list = []
    sub_trees(tree, np_list)

    return np_list

def sub_trees(tree,tree_list):

    tmp_list = []
    for sub_tree in tree.subtrees(filter=lambda t: t.label() == 'NP'):
        tmp_list.append(sub_tree)
    
    if len(tmp_list) == 1:
        value_tree = tmp_list[0]
        if value_tree not in tree_list:
            tree_list.append(value_tree)
    elif len(tmp_list) > 1:
        for sub_tree in tree.subtrees():
            if sub_tree != tree:
                sub_trees(sub_tree,tree_list)
    
    # raise NotImplementedError

def speller(word):
    is_word = False
    for c in word:
        if c.isalpha():
            is_word = True
            break
    
    return is_word


if __name__ == "__main__":
    main()
