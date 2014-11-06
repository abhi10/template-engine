import sys
import string
from grammar import GrammarEngine

class Parser(object):
    """ Parser class in which the list of tokens is parsed 
        to compute the corresponding Abstract Syntax Tree
        by matching the grammar rules for symbols and tokens.
    """
    def __init__(self, token_lst):
        self.ast = self.startParser(token_lst)

    def startParser(self, token_lst):
        ast, rest_tokens = self.parse1('html', token_lst)
        return ast
        
    def parse1(self, symbol, tokens):
        """ Return an ast corresponding to symbol
        """
        match, type = self.matchSymbol(symbol, tokens)
        if type is 'rule':
            asts, rest_tokens = self.parse(match, tokens)
            ast = [symbol] + asts # create the AST
            return ast, rest_tokens
        elif type is 'token':
            return match, tokens[1:]
        else:
            sys.exit("no match found")

    def parse(self, symbols, tokens):
        """return a list of asts corresponding to symbols
        """
        if not symbols:
           return [], tokens #base case
        elif not tokens:
           sys.exit("bad parse: tokens empty, but symbols not")
        else:
           top = symbols[0]
           ast, rest_tokens = self.parse1(top, tokens)
           rest_asts, rest_tokens = self.parse(symbols[1:], rest_tokens)
           return [ast] + rest_asts, rest_tokens

    def matchSymbol(self, sym, rest_tokens):
        """return tuple of rule_type and rule """
        grammar = GrammarEngine()
        if grammar.isNonTerminal(sym):
            rule = grammar.grammarRule(sym, rest_tokens[0], rest_tokens[1:])
            return (rule, 'rule')
        elif grammar.isTerminal(sym):
            return (grammar.getTerminalToken(sym, rest_tokens[0]), 'token')
        else:
            return (None, 'error')


