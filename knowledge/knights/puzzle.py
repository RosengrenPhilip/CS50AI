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

    #rules
    And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))),

    #If a knight, what he says is true and vice versa
    Biconditional(AKnight, And(AKnight, AKnave))
    # TODO
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(

    #rules
    And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))),
    And(Or(BKnight, BKnave), Not(And(BKnight, BKnave))),

    #if a is a knight, what he says is true, and vice versa
    Biconditional(AKnight, And(AKnave, BKnave)),
    #what b says


    # TODO
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(

    #rules
    And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))),
    And(Or(BKnight, BKnave), Not(And(BKnight, BKnave))),

    # A says "We are the same kind."
    Biconditional(AKnight, Or(And(AKnight, BKnight), And(AKnave, BKnave))),
    # B says "We are of different kinds."
    Biconditional(BKnight, Or(And(AKnight, BKnave), And(AKnave, BKnight))),
    # TODO
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))),
    And(Or(BKnight, BKnave), Not(And(BKnight, BKnave))),
    And(Or(CKnight, CKnave), Not(And(CKnight, CKnave))),

    Biconditional(BKnight, Biconditional(AKnight, AKnave)),

    Biconditional(BKnight, CKnave),

    Biconditional(CKnight, AKnight),

    # TODO
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