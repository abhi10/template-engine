"""
templater.tokens

define symbols , tokens and other keywords
"""

import string
import re
#----------------------------------------------------------------------
# Key value pair of html tag,Terminals
token_map = {
    '<html>': 'HTML-START',
    '</html>':'HTML-END',
    '<head>':'HEAD-START',
    '</head>':'HEAD-END',
    '<title>':'TITLE-START',
    '</title>':'TITLE-END',
    '<body>':'BODY-START',
    '</body>':'BODY-END',
    '<h1>':'H1-START',
    '</h1>':'H1-END',
    '<p>':'PARA-START',
    '</p>':'PARA-END',
    'ENDEACH':'LOOP-END'
}
#-----------------------------------------------------------------------
token_keys = token_map.keys()
#----------------------------------------------------------------------
# EXCEPTION : regex expression to match tokens which are not part of token_map
# this is extensible as you can add new regex and just update the matchPattern 
# function
pattern_map = {
    'end_loop': '\<\*\s*([\.ENDEACH]+)\s*\*\>',
    'item_token': '\<\*\s*([\.a-zA-Z0-9_]+)\s*\*\>',
    'start_loop': '\<\*\s*([\.A-Z]+)\s*([\.a-zA-Z0-9_]+) ([\.a-zA-Z0-9_]+)\s*\*\>'
}
#----------------------------------------------------------------------

class Token(object):
    def __init__(self):
        """Constructor for Token class, matches different token types
           and validates them
        """
        self.token_map = token_map
        self.pattern_map = pattern_map
         
    def isTag(self, input_str):
        if self.inputInTokenKeys(input_str):
            return True
        else:
            return self.isValidPattern(input_str)

    def inputInTokenKeys(self, input_str):
        return input_str in self.token_map.keys()


    def isValidPattern(self, input_str):
        for key in self.pattern_map:
            if self.isPattern(key, input_str):
                return True
        return False
        
    def isPattern(self, key, input_str):
        pattern = self.pattern_map[key]
        return bool(re.match(pattern, input_str))
 
    def getToken(self, input_str):
        if self.inputInTokenKeys(input_str):
            return self.token_map[input_str]
        else:
            return self.matchPattern(input_str)

    def matchPattern(self,input_str):
        token = []
        if self.isPattern('end_loop', input_str):
            token_loop = self.getRegexValue('end_loop', input_str)
            token = self.token_map[token_loop]
        elif self.isPattern('item_token', input_str):
            token_string = self.getRegexValue('item_token', input_str)
            token = ['ITEM-TOKEN', token_string]
        else:
            token_tuple = self.getRegexValue('start_loop', input_str)
            token = ['LOOP-START', token_tuple]
        return token
    
    def getRegexValue(self, key, input_str):
        pattern = self.pattern_map[key]
        if key is "start_loop":
            return re.compile(pattern).search(input_str).groups()
        else:
            return re.compile(pattern).search(input_str).group(1)

    def inverseMap(self):
        """Returns a reverse hash map of the Token map """
        inv_map = {v: k for k,v in self.token_map.items()}
        return inv_map

#----------------------------------------------------------------------




























