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
    #Either knight or a knave, not both
    And(Or(AKnight,AKnave), Not(And(AKnight, AKnave))),
    
    #Knight always tells the truth, Knave always lies

    #If knight, the sentence spoken must be true.
    Implication(AKnight, And(AKnight, AKnave)),
    #If knave, the sentence spoken is false. Not needed
    #Implication(AKnave, Not(And(AKnight, AKnave)))
    # TODO
)

# Puzzle 1
# A says "We are both knaves.""
# B says nothing.
knowledge1 = And(
    #Rules
    And(Or(AKnight,AKnave), Not(And(AKnight, AKnave))),
    And(Or(BKnight,BKnave), Not(And(BKnight, BKnave))),
    
    #If A is a knight, what he says is true and vice versa
    Biconditional(AKnight, And(AKnave, BKnave)),
    #What B says

    # TODO
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(

    #Rules
    And(Or(AKnight,AKnave), Not(And(AKnight, AKnave))),
    And(Or(BKnight,BKnave), Not(And(BKnight, BKnave))),
    
    #If what A says is true, hes a knight, and vice versa
    Biconditional(AKnight, Or(And(AKnight, BKnight), And(AKnave, BKnave))),
    #If what B says is true, He's a knight and vice versa
    Biconditional(BKnight, Or(And(AKnight, BKnave), And(AKnave, BKnight))),
    # TODO
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    #Rules
    And(Or(AKnight,AKnave), Not(And(AKnight, AKnave))),
    And(Or(BKnight,BKnave), Not(And(BKnight, BKnave))),
    And(Or(CKnight,CKnave), Not(And(CKnight, CKnave))),

    #If A is a knight, what he says is true and vice versa
    #Not really needed 
    #Or(Biconditional(AKnight, AKnight), Biconditional(AKnight, AKnave)), 
    
    #If B is a knight, what he says is true and vice versa
    Biconditional(BKnight, Biconditional(AKnight, AKnave)),
    Biconditional(BKnight, CKnave),
    #If C is a knight, what he says is true and vice versa
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
