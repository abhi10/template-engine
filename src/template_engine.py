'''
Main Driver Engine

'''
import sys
import string
from grammar import GrammarEngine
from lexer import Lexer
from tokens import Token
from parser import Parser
from json_parser import JsonParser

# read command line arguments 
file_name = sys.argv[1]
json_file = sys.argv[2]
output_file = sys.argv[3]

#global hash map for key-value mapping of JSON data
json = JsonParser(json_file)
json_map = json.object_map
# grammar object
grammar = GrammarEngine() 
#-------------------------------------------------------------------------------
def main():
    """ Initializes the pre-requisites to build the abstract syntax tree(ast)
        This ast is then processed to replace Item object names 
        with their respective scope binded keys specific to a loop.
        Remaining values like page.title and teacher.name are substituted in subst_Tree
        The ast built at this point has all the values substituted ,
         now the final html tags need to be replaced by recurring over the ast tree.
        The final html string is written into the html file.
    """
    ast = set_up_ast()
    subst_ast = process_ast(ast)
    html_string = final_html(subst_ast)
    write_to_output(html_string, output_file) # output the html tree to output.html file
    
def set_up_ast():
    """ This function initializes the lexer and parser and 
        returns the ast(Abstract Syntax Tree)
    """
    lexer = Lexer(file_name) # Init Lexer
    token_lst = lexer.token_lst # Get Sequence of Tokens for given template
    parser = Parser(token_lst) # Init Parser
    return parser.ast  # Get ast of given token list

def process_ast(ast):
    full_ast = unroll_loops(ast, json_map) #unwind the ast
    subst_ast = subst_Tree(full_ast, json) # make final substitution
    return subst_ast

def final_html(subst_ast):
    """ Final html string is computed by lookin up the
        token,terminal reverse hash map.
    """
    token  = Token() #Init Token
    html_map = token.inverseMap() # Get Inverse mapping of tokens and html terminals
    html_final = html_Tree(subst_ast, html_map) # Compute Final html tree in a string type
    return html_final

#-------------------------------------------------------------------------------------
    
def pop_top_name1(key,ast):
    if type(ast) is not list:
        return ast
    elif isItemObject(ast):
        item_string = ast[1][1]
        str_lst = item_string.split('.')
        return pop_name_from_object(str_lst,
                                    key,
                                    (ast[1][0], dotify_lst(str_lst[1:])),
                                    ast)
    elif isLoopObject(ast):
        ltag, (each, xs, x)  = ast[1]
        str_lst = xs.split('.')
        return pop_name_from_object(str_lst,
                                    key,
                                    (ltag, (each,dotify_lst(str_lst[1:]),x)),
                                    ast)
    else:
        return [ast[0]] + pop_top_name(key, ast[1:])

def pop_name_from_object(str_lst, key, second, ast):
    """ TO ensure scope binding of for loop the first item of
        item value like "student.name" is replace with name
    """
    if str_lst[0] == key:
        return ['object', second] + pop_top_name(key, ast[2:])
    else:
        return ast
       
def pop_top_name(name, asts):
    """pop top name from all item/loop objects in asts"""
    ans = []
    for ast in asts:
        ans = ans + [pop_top_name1(name, ast)]
    return ans

def dotify_lst (lst):
    if len(lst) == 1:
        return lst[0]
    elif len(lst) == 0:
        return []
    else:
        return [lst[0]] + ['.'] + dotify_lst(lst[1:])


def is_list_of_dict (xs):
    """ Function returns a boolean value if the given argument
        is a list of dictionaries
    """
    if len(xs) == 0:
        return True
    else:
        return type(xs[0]) is dict and is_list_of_dict(xs[1:])
        
def createDicts(key, vals):
    """for each val, create a dict which has  key->val"""
    lod = [] # list of dictionary
    for val in vals:
        d = {} # dictionary
        d[key] = val
        lod = lod + [d]
    return lod

#---------------------------------------------------------    
def unroll_loops (ast, D):
    """ unroll all loop objects in Tree ast for dictionary D
    """
    if type(ast) is not list:
        if ast[1] in D.keys():
            return D[ast[1]]
        else:
            return ast
    elif isLoopObject(ast):
       _, (each, xs, x)  = ast[1]
       if is_list_of_dict(D[xs]):
           Ds = D[xs]
           loop_objects = pop_top_name(x, ast[2:-1])
       else:
           Ds= createDicts(x,D[xs])
           loop_objects = ast[2:-1]
       return ['object'] + unroll_one_loop(loop_objects, Ds)
    else:
       return [ast[0]] + unroll_loops_lst(ast[1:],D)
    
def unroll_one_loop (asts, Ds):
    """ Unrolling one instance of for loop
    """
    if len(Ds) == 0:
       return []
    else:
       return unroll_loops_lst(asts, Ds[0]) + unroll_one_loop(asts, Ds[1:])
   
def unroll_loops_lst (asts, D):
    """ Recursively iterate over asts """
    if len(asts) == 0:
       return []
    else:
       return [unroll_loops(asts[0],D)] + unroll_loops_lst(asts[1:],D) #TEST here
       

#-----------------------------------------------------------------
# SUBSTITUTE JSON values into AST
def subst_Tree(ast, D):
    """ Substitute in Tree ast, the key-value mapping of D
    """
    if type(ast) is not list:
        val = getJSONValue(ast, D)
        return val
    else:
        return [ast[0]] + subst_Trees(ast[1:], D)

def subst_Trees (asts, D):
    """ Recurse over asts trees
    """
    if len(asts) == 0:
       return []
    else:
       return [subst_Tree(asts[0], D)] + subst_Trees(asts[1:], D)
   
#-----------------------------------------------------------------
#Helper Functions
def isLoopObject(ast):
    """ Function returns boolean value if given ast is
        an 'object' type and start of a Loop
    """
    return ast[0] == 'object' and isLoopStart(ast[1])

def isLoopStart(ast):
    return ast[0] == 'LOOP-START'


def isItemObject(ast):
    return ast[0] == 'object' and isItemToken(ast[1])
 
def isItemToken(ast):
    return ast[0] == 'ITEM-TOKEN'

def getJSONValue(o, D):
    if type(o) is tuple:
       lst =  o[1].split('.')
       if len(lst) == 2:
           key , field = lst[0], lst[1]
           value = D.objectValue(key)
           return str(value[field])
    else:
       return o
   
#----------------------------------------------------------------------
# FINAL HTML TAG SUBSTITUTION
def html_Tree(ast, D):
    """ Substitute in Tree ast, html tags ,
        the terminals like 'HTML-START' are replaced
        with their html tags, whereas non terminals like 'html'
        are repalced with empty string
    """
    if type(ast) is not list:
        if grammar.isTerminal(ast):
            return D[ast]
        else:
            return ast
    elif grammar.isNonTerminal(ast[0]):
        return html_Trees(ast[1:],D)
    else:
        return ast[0] + html_Trees(ast[1:], D)

def html_Trees (asts, D):
    """ Recurse over asts
    """
    if len(asts) == 0:
       return ''
    else:
       return html_Tree(asts[0], D) + html_Trees(asts[1:], D)
   
#---------------------------------------------------------------------
def write_to_output(html_string, output_html):
    """ The html string list is written to the html file
    """
    text_file = open(output_html, "w")
    text_file.write(html_string)
    text_file.close()
#--------------------------------------------------------------------    
main()
