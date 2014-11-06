## Intro
 Learning more about Python Classes and LL grammar concepts this code is a simple mini-templating engine.

## About Templating Engine

* I have implemented a template language and the corresponding template engine.
* The Template engine is a software component that combines one or more templates with a data model to output a result document.
* The language that the templates are written in is known as template language.
Result documents can be any formatted output like web page or source code(in source code generator). 

## High Level Design

* The Mini Template Engine is broken into 5 main parts.
* Tokens
* Lexer
* Parser
* Grammar
* Template Engine

### LL Grammar for the Template Engine:

    html          = [ HTML-START ] [ html-content] [ HTML-END ]	
    html-content  = [ html-head ] [ html-body] 
    html-head     = [ HEAD-START ] [ head-content ] [ HEAD-END ]
    head-content  = [ TITLE-START ] [ object ] [ TITLE-END ]
    html-body     = [ BODY-START ] [ body-content ] [ BODY-END ]

    body-content  = [ h1 ] [ body-content ]|
    		    [ para ] [ body-content ]|
                    [ object ] [ body-content ]|
                    []
    h1            = [ H1-START ] [ object ] [ H1-END ]
    para          = [ PARA-START ] [ object ] [ PARA-END ]

    object        = [ ITEM-TOKEN ]|
                    [ ITEM-TOKEN ] [ object ]|
                    [ LOOP-START ] [ para ] [ LOOP-END ]|
                    [ LOOP-START ] [ object ] [ LOOP-END]


## Run Instructions:
```Shell
    $ python -B template_engine.py template.sample data.json render.html
    $ cat render.html
    $ <browser> render.html
```
