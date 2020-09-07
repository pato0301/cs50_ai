from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    Or(AKnight, AKnave),
    Implication(AKnight,And(AKnight,AKnave))
    # TODO
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    Or(And(AKnave,BKnight),And(AKnave,BKnave)),
    Or(AKnave,AKnight), Or(BKnave,BKnight),
    Implication(AKnave,And(AKnave,BKnight))
    # TODO
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    Or(AKnave,AKnight), Or(BKnave,BKnight),
    Or(And(AKnight,BKnight),And(AKnave,BKnight)),
    Implication(BKnight,And(AKnave,BKnight)),
    Implication(AKnave,And(AKnave,BKnight)),
    # Or(And(AKnight,BKnight),And(AKnave,BKnight)),
    # Or(And(BKnight,AKnave))
    #Biconditional(AKnight,BKnight),
    # Implication(AKnight,And(AKnight,BKnight)),
    # Implication(BKnave,And(AKnight,BKnave))
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    Or(AKnave,AKnight), Or(BKnave,BKnight), Or(CKnight,CKnave),
    Or(And(BKnight,AKnave,CKnave),And(BKnave,CKnight,AKnight)),
    Implication(AKnight,Not(AKnave)),
    Implication(AKnight,And(BKnave,CKnight)),
    
    # If B says the truth then A said he is a knave because Knave sentences are fault, 
    # that would mean that he is a knight, but knight dont lie.
    # that would mean that B is telling a lie
    Implication(AKnave,And(BKnave,CKnave)),
    #Implication(BKnight,And(CKnave,AKnight)), 
    Implication(CKnight,And(AKnight,BKnave)),
    Biconditional(CKnight,AKnight),
    Biconditional(BKnight,And(CKnave,AKnight)),
    Implication(AKnight,And(CKnight,BKnave))
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
