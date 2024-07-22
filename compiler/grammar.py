# Constants

TT_NEXT_SEG = "NEXT_SEG"
TT_OX = "OPEN_EXPRESSION"
TT_CE = "CLOSE_EXPRESSION"
TT_NUMBER = "NUMBER"
TT_QUESTION_MARK = "QUESTION_MARK"

DIGITS = "0123456789"

#classes

class Token:
    def __init__(self,name,value=None):
        self.name= name
        self.value = value
    def __repr__(self) -> str:
        return f"[{self.name}: {self.value}]"

class Lexer:
    def __init__(self,grammar):
        self.char = ""
        self.idx = -1
        self.grammar = grammar
        self.advance()
    def advance(self):
        self.idx += 1
        self.char = self.grammar[self.idx] if len(self.grammar) > self.idx else None
    def unadvance(self):
        self.idx -= 1
        self.char = self.grammar[self.idx] if len(self.grammar) > self.idx else None
    def tokenize(self):
        tokens = []
        while self.char != None:
            if self.char == " ":pass
            elif self.char == ",":
                tokens.append(Token(TT_NEXT_SEG))
            elif self.char == "[":
                tokens.append(Token(TT_OX))
            elif self.char == "]":
                tokens.append(Token(TT_CE))
            elif self.char == "?":
                tokens.append(Token(TT_QUESTION_MARK))
            elif self.char == ".":
                tokens.append(self.make_number())
            self.advance()
        return tokens
    def make_number(self):
        num_str = ""

        self.advance()
        while self.char != None and self.char in DIGITS:
            num_str += self.char
            self.advance()
        self.unadvance()
        return Token(TT_NUMBER, int(num_str))

# Nodes

class WeightNode:
    def __init__(self,tok) -> None:
        self.tok = tok
    def __repr__(self) -> str:
        return f"weight:{self.tok.value}"

class AtomicNode:
    def __init__(self) -> None:
        self.atomic_symbol = "?"
    def __repr__(self) -> str:
        return f"?"

'''
{
    weight: int
    atomic: bool
}
'''

class SegmentNode:
    def __init__(self,node,atomic) -> None:
        self.node= node
        self.atomic = atomic
    def __repr__(self) -> str:
        return f"[{self.node}]{self.atomic if self.atomic else ""}"
# Parser

class Parser:
    def __init__(self,tokens: list[Token]) -> None:
        self.tokens = tokens
        self.idx = -1
        self.current_token = None
        self.advance()
    def advance(self):
        self.idx += 1
        self.current_token = self.tokens[self.idx] if len(self.tokens) > self.idx else None
    def parse(self):
        nodes = []
        while self.current_token != None:
            if self.current_token.name == TT_NEXT_SEG:
                pass
            elif self.current_token.name == TT_OX: # > [
                nodes.append(self.expr())
            self.advance()
        return nodes
    def expr(self):
        self.advance()
        if self.current_token.name == TT_NUMBER: # > DIGITS
            number_node = WeightNode(self.current_token)
            result = None
            self.advance()
            if self.current_token.name == TT_CE:
                result = SegmentNode(number_node,None)
                self.advance()
                if self.current_token != None:
                    if self.current_token.name == TT_QUESTION_MARK:
                        result.atomic = AtomicNode()
                return result
            else:
                print("not closed segment")
                exit(1)
        else:
            print("Invalid Syntax")
            exit(1)

def NewGrammar(file):
    with open(file) as file:
        data = file.readlines()
    
    trees: list[list[dict]] = []
    for line in data:
        List: list[dict] = []
        temp: list[SegmentNode] = Parser(Lexer(line).tokenize()).parse()
        for seg in temp:
            List.append(
                {
                    "weight":seg.node.tok.value,
                    "atomic": (True if seg.atomic != None else False)
                }
            )
        trees.append(List)
    return trees

