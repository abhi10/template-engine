import tokens
from tokens import Token
import re
import sys
#----------------------------------------------------------------------
#              constants refered in lexer class
WHITESPACE = ' \t\n'
OPEN_TAG = '<*'
CLOSE_TAG = '*>'

#----------------------------------------------------------------------
class Lexer(object):
    """ Lexer class in which lexical analysis of the input file name is
        done and the correspnding token list is computed
    """
    def __init__(self, file_name):
        self.input_string = self.getInputString(file_name)
        self.token_lst = self.tokenizeString(self.input_string)

    def getInputString(self, name):
        file_stream = open(name).read()
        return file_stream

    def tokenizeString(self, stream):
        return self.computeTokens(stream, "", [])

    def computeTokens(self, stream, seen, tokens):
        myToken = Token()
        for char in stream:
            if self.isValidTag(char, seen):
                continue #ignore white space characters
            seen += char
            if myToken.isTag(seen):
	        token = myToken.getToken(seen)
                tokens.append(token)
                seen = ""
        return tokens

    def isValidTag(self, tag, string_seen):
        return tag in WHITESPACE and OPEN_TAG not in string_seen

#----------------------------------------------------------------------


