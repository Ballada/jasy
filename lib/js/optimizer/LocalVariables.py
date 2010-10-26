#
# JavaScript Tools - Optimizer for local variable names
# Copyright 2010 Sebastian Werner
#

from js.tokenizer.Tokenizer import keywords
from copy import copy
import string, logging

__all__ = ["optimize"]



#
# Public API
#

def optimize(node):
    __patch(node)



#
# Implementation
#

def __baseEncode(num, alphabet=string.ascii_letters):
    if (num == 0):
        return alphabet[0]
    arr = []
    base = len(alphabet)
    while num:
        rem = num % base
        num = num // base
        arr.append(alphabet[rem])
    arr.reverse()
    return "".join(arr)


def __patch(node, enable=False, translate=None):
    # Start with first level scopes (global scope should not be affected)
    if node.type == "script" and hasattr(node, "parent"):
        enable = True
    
    
    #
    # GENERATE TRANSLATION TABLE
    #
    if enable and hasattr(node, "__defines"):
        usedRepl = set()
        
        if not translate:
            translate = {}
        else:
            # copy only the interesting ones from the __inherits set
            newTranslate = {}
            
            for name in node.__inherits:
                if name in translate:
                    newTranslate[name] = translate[name]
                    usedRepl.add(translate[name])
            translate = newTranslate
            
        # Merge in usage data into declaration map to have
        # the possibilities to sort translation priority to
        # the usage number. Pretty cool.
        
        defined = {}
        for name in node.__defines:
            if name in node.__uses:
                defined[name] = node.__uses[name]
            else:
                defined[name] = 0
                
        definedSorted = list(reversed(sorted(defined, key=lambda x: defined[x])))

        # Extend translation map by new replacements for locally 
        # defined variables. Automatically ignores keywords. Only
        # blocks usage of replacements where the original variable from
        # outer scope is used. This way variable names may be re-used more
        # often than in the original code.
        pos = 0
        for name in definedSorted:
            while True:
                repl = __baseEncode(pos)
                pos += 1
                if not repl in usedRepl and not repl in keywords:
                    break
                
            # print("Translate: %s => %s" % (name, repl))
            translate[name] = repl


    #
    # APPLY TRANSLATION
    #
    if translate:
        # Update param names in outer function block
        if node.type == "script" and hasattr(node, "parent"):
            function = node.parent
            if function.type == "function" and hasattr(function, "params"):
                for identifier in function.params:
                    if identifier.value in translate:
                        identifier.value = translate[identifier.value]
            
        # Update names of exception objects
        elif node.type == "exception" and node.value in translate:
            node.value = translate[node.value]

        # Update function name
        elif node.type == "function" and hasattr(node, "name") and node.name in translate:
            node.name = translate[node.name]
    
        # Update identifiers
        elif node.type == "identifier":
            # Ignore param blocks from inner functions
            if node.parent.type == "list" and getattr(node.parent, "rel", None) == "params":
                pass
                
            # Ignore keyword in property initialization names
            elif node.parent.type == "property_init" and node.parent[0] == node:
                pass
            
            # Update all identifiers which are 
            # a) not part of a dot operator
            # b) first in a dot operator
            elif node.parent.type != "dot" or node.parent.index(node) == 0:
                if node.value in translate:
                    node.value = translate[node.value]
                
        # Update declarations (as part of a var statement)
        elif node.type == "declaration":
            varName = getattr(node, "name", None)
            if varName != None:
                if varName in translate:
                    node.name = varName = translate[varName]
            else:
                # JS 1.7 Destructing Expression
                for identifier in node.names:
                    if identifier.value in translate:
                        identifier.value = translate[identifier.value]


    #
    # PROCESS CHILDREN
    #
    for child in node:
        # None children are allowed sometimes e.g. during array_init like [1,2,,,7,8]
        if child != None:
            __patch(child, enable, translate)


