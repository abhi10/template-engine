"""

This file defines the grammar rules for the given template input
and provides accessor function to retrieve the rules from grammar 
in a convenient manner
"""
import sys
from tokens import token_map
#-------------------------------------------------------------------------------
# grammar table which contains a dictionary of key, value pairs where keys
# are terminals and values are the rules associated with it.
#-------------------------------------------------------------------------------
grammar_table = {
'html': ['HTML-START', 'html-content','HTML-END'],
'html-content' : ['html-head','html-body'],
'html-head': ['HEAD-START', 'head-content', 'HEAD-END'],
'head-content': ['TITLE-START', 'object', 'TITLE-END'],
'html-body': ['BODY-START','body-content','BODY-END'],
'body-content':[['h1', 'body-content'],
	            ['para','body-content'],
	            ['object', 'body-content'],
	            []],
'h1': ['H1-START', 'object', 'H1-END'],
'para': ['PARA-START', 'object', 'PARA-END'],
'object': [['ITEM-TOKEN'],
	   ['ITEM-TOKEN', 'object'],
	   ['LOOP-START', 'para','LOOP-END'],
	   ['LOOP-START', 'object', 'LOOP-END']]
}
#---------  useful constants ---------------------------------------
other_tokens =  ['LOOP-START','ITEM-TOKEN']# removed EMPTY tag
loop_tag = 'LOOP-START'
item_tag = 'ITEM-TOKEN'
h1_tag = 'H1-START'
para_tag = 'PARA-START'

#-------------------------------------------------------------------
# Create a Grammar Class
#----------------------------------------------------------------------
class GrammarEngine(object):
    """GrammarEngine class keeps track of the grammar table, the token hash map,
       and variables to access the grammar and taken values.
       The GrammarEngine class is used to determine if an input symbol is terminal 
       or token and also determine the corresponding grammar rule based on type of
       argument (object, Item Token , Para, Body etc.) """
    def __init__(self):
        self.rule_map = grammar_table
        self.token_map = token_map
        self.rule_keys = self.rule_map.keys()
        self.terminal_keys = self.token_map.values()

    def rules(self):
        """Returns the hash map of Rules."""
        return self.rule_map

    def tokenMap(self):
        """Returs the hash map of Token."""
        return self.token_map

    def terminalKeys(self):
        """Returns a list of terminal keys."""
        terminal_keys = self.terminal_keys
        terminal_keys = terminal_keys + other_tokens
        return terminal_keys
        
    def nonTerminalKeys(self):
        """Returns a list of Grammar Keys."""
        return self.rule_keys

    def isTerminal(self, symbol):
        """Returns True if input symbol is Terminal."""
        return symbol in self.terminalKeys()

    def isNonTerminal(self, symbol):
        """Returns True if input symbol is a Non Terminal."""
        return symbol in self.rule_keys

    
    #--------------------------------------------------------------------
    # Compute the next grammar rule required by looking into future tokens
    #-------------------------------------------------------------------
    def grammarRule(self, rule_tag, token, token_lst):
        """Returns the rule associated with the rule tag
           by looking up rule_map dictionary.
        """
        if rule_tag == 'object':
            return self.objectRule(token, token_lst)
        elif rule_tag == 'body-content':
            return self.bodyRule(token, token_lst)
        else:
            return self.rule_map[rule_tag] #Simple Rule
    
    #-------------------------------------------------------------------
    # compute grammar rule for token type  'object' 
    #-------------------------------------------------------------------         
    def objectRule(self, token, token_lst):
        """Returns the object rule list , else throws exception."""
        object_rules = self.rule_map['object']
        if self.isLoopToken(token):
            return self.loopStartRule(object_rules, token_lst)
        elif self.isItemToken(token): #, token_lst[0]):
           return self.itemRule(object_rules, token, token_lst)
        else:
            sys.exit("Rule Not Found")
    
    #--------------------------------------------------------------------
    # compute grammar rule for ITEM-TOKEN within Object Type
    # two cases :
    # current token is ITEM-TOKEN or Loop-TOKEN
    #--------------------------------------------------------------------
    def isItemToken(self, token):
        return (item_tag in token)

    def itemRule(self, rules, current_token, rest_tokens):
        if self.isItemToken(current_token) and self.isLoopToken(rest_tokens[0]):
            return rules[1]
        else:
            return rules[0]
            
    #---------------------------------------------------------------
    # compute grammar rule for LOOP-START token in Object Type
    # two cases ::
    # token type is 'para'
    # token type is  'object'
    #---------------------------------------------------------------
    def isLoopToken(self, token):
        return loop_tag in token

    def loopStartRule(self, rules, token_lst):
        current_token = token_lst[0]
        next_token = token_lst[0][0]
        if self.isTokenPara(token_lst[0]):
            return rules[2] #loop para rule
        elif self.isTokenObject(current_token):
            return rules[3] #loop object rule
        elif self.isTokenObject(next_token):
            return rules[3] #loop object rule
        else:
            sys.exit("rule not found")

    
    #---------------------------------------------------------------
    # compute grammar rule for token type 'body-content'
    #---------------------------------------------------------------
    def bodyRule(self, token, token_lst):
        """Returns the object rule list for type body-content."""
        body_rules = self.rule_map['body-content']
        if self.isTokenHead(token):
            return body_rules[0] # head rule
        elif self.isTokenPara(token):
            return body_rules[1] # para rule
        elif self.isTokenObject(token):
            return body_rules[2] # body-object rule
        else:
            return body_rules[3] # return []

    def isTokenHead(self, token):
        head_rule = self.rule_map['h1']
        return token in head_rule

    def getTerminalToken(self, symbol, data_token):
        if self.isTokenObject(symbol):
            return self.convert_to_tuple(data_token)
        else:
            return symbol
        
    def convert_to_tuple(self, data_token):
        return (data_token[0], data_token[1])

    #-------------------------------------------------------------
    # common functions
    #--------------------------------------------------------------

    # given a token , outputs boolean value if token is Object type -ITEM or LOOP
    def isTokenObject(self, token):
        """Returns True if input token is of type ITEM or LOOP."""
        return  self.isItemToken(token) or self.isLoopToken(token)

    def isTokenPara(self, token):
        para_rule = self.rule_map['para']
        return token in para_rule
        
    #--------------------------------------------------------------
    
    
    
    
        
 


    
