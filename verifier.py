from graph import Graph
from math import floor

'''
An instance of TwoColorQuarterNodeCover has the syntax:
Graph;NodeColorings;Color1;Color2

Graph is an undirected, unweighted graph defined as a white-space
delimited sequence of edges (for example: 'a,b a,c d,e d,f')

NodeColorings is a white-space delimited list of node colors (for
example: 'a:beige b:umber c:umber d:gray e:taupe f:cerulean')

Color1 and Color2 are both colors (for example: beige; gray)

NodeCoverSize is an integer > 1  

'a,b a,c d,e d,f;a:beige b:umber c:umber d:crimson e:umber
f:umber;beige;crimson' is an instance of TwoColorQuarterNodeCover.

A node cover subset is a subset of the nodes of a graph, such that every
edge in the graph has at least one end point in a node in the subset.

A ATwoColorQuarterNodeCover instance is a positive instance if it has a
node cover subset with at most 1/4 the nodes in the graph, and every
node in that subset is colored either Color1 or Color2.

'a,b a,c d,e d,f a,g d,h;a:beige b:umber c:taupe d:crimson e:umber
f:beige g:puce h:ecru ; beige; crimson' is a POSITIVE INSTANCE of
TwoColorQuarterNodeCover because nodes a and d cover the graph; they are
colored beige (Color1) and crimson (Color2) respectively; and |{a,d}| =
2 = floor(# nodes in Graph/4). 

'a,b a,c d,e d,f a,g ;a:beige b:umber c:taupe d:crimson e:umber f:beige
g:puce ; beige; crimson' is a NEGATIVE INSTANCE of
TwoColorQuarterNodeCover because |{a,d}| = 2 > 1 = floor(# nodes in
Graph/4)

'a,b a,c d,e d,f a,g b,h;a:beige b:umber c:taupe d:crimson e:umber
f:beige g:puce h:ecru ; beige; crimson' is a NEGATIVE INSTANCE of
TwoColorQuarterNodeCover because there no set of two nodes that cover the graph.

'a,b a,c d,e d,f a,g d,h;a:incarnadine b:umber c:taupe d:crimson e:umber
f:beige g:puce h:ecru ; beige; crimson' is a NEGATIVE INSTANCE of
TwoColorQuarterNodeCover because while nodes a and d cover the graph, node a is not colored beige (Color1) or crimson (Color2).

'''

V2CNCv = 'VERBOSE: VfyTwoColorQuarterNodeCover() '
VERBOSE = True
def printV(text):
    if VERBOSE: print(f'{V2CNCv}{text}')

V2CNCd = 'DEV: VfyTwoColorQuarterNodeCover() '
DEV = False
def printD(text):
    if DEV: print(f'{V2CNCv}{text}')
    
def VfyTwoColorQuarterNodeCover(I,S,H):
    S_len = len(S)
    H_len = len(H)

    ### ** HW #1: CHANGE TO 'REASONABLE' S & H MAX LENGTH TEST
    # reasonable test for H is very broad here b/c the quarter limit is checked later
    if S_len > 3 | H_len > len(I): ### ** HW #1 -- CHANGE ME 
        s = f'Solution length {S_len} or hint length {H_len}'
        printV(f'{s} is unreasonable')
        return 'unsure'
    
    if S != 'yes':
        printV(f'The solution "{S}" is not verifying a positive instance')
        return 'unsure'

    (graph_str, node_colorings, color1, color2) = I.split(';')
    # squeeze out white space
    color1 = color1.strip()
    color2 = color2.strip()
    
    g = Graph(graph_str, directed=False, weighted=False)
    nodes = list(g.nodes.keys()) # create list of graph's node names

    ### ** HW #1: CHANGE TO ACTUAL MAX NODE COVER SIZE FOR TwoColorQuarterNodeCover
    max_node_cover_size = floor(len(nodes) / 4) ### ** HW #1 -- CHANGE ME 
    
    node_cover = H.split() # H is a white-spaced delimited list of nodes

    ### ** HW #1: CHANGE TO TEST FOR NODES IN HINT > MAX ALLOWED
    if len(node_cover) > max_node_cover_size: ### ** HW #1 -- CHANGE ME 
        tmp = ' hint nodes but the maximum allowed is'
        s = f'{len(node_cover)}{tmp} {max_node_cover_size}.'
        printV(f'{s}')
        return 'unsure'

    node_color_kv = {} # node->color key/value pairs
    colorings_list = node_colorings.split()
    for node_color in colorings_list:
        node, color = node_color.split(':')
        node_color_kv[node] = color

    ### ** HW #1: Insert code to return 'unsure' if node in hint but not in graph,
    ### ** HW #1: and for nodes in the hint that are not color1 or color2.
    ### ** HW #1: In the former case write the verbose message:
    ### ** HW #1: printV(f'{node} in hint but not in graph')
    ### ** HW #1: In the latter write:
    ### ** HW #1: printV(f'{node} colored "{color}", but must be {color1} or {color2}')
    for node in node_cover:
        if node not in nodes:
            printV(f'{node} in hint but not in graph')
            return 'unsure'
        color = node_color_kv.get(node)
        if color != color1 and color != color2:
            printV(f'{node} colored "{color}", but must be {color1} or {color2}')
            return 'unsure'
        
    ### ** HW #1: Insert code to return unsure if the nodes in the hint do not
    ### ** HW #1: cover the graph. Before returning, write the verbose message:
    ### ** HW #1: printV(f'Edge "{edge}" does not have end point in "{H}".')
    edges = graph_str.split()
    for edge in edges:
        node1, node2 = edge.split(',')
        if node1 not in node_cover and node2 not in node_cover:
            printV(f'Edge "{edge}" does not have end point in "{H}".')
            return 'unsure'

    printV(f'"{I}" is a positive instance, all verifications succeeded')
    return 'correct'

if __name__ == '__main__':

    def test_case(func, I, S, H, expected, num, comment=''):
        err = '** '
        result = func(I, S, H)
        func_name = str(func).split()[1]
        func_call = f'''{func_name}("{I}","{S}","{H}")'''
        if result == expected: err = ''
        e = expected
        print (f'{err}test #{num} {func_call}: expected "{e}", received "{result}"')
        print (f'test #{num} Explanation: {comment}\n')
        return num + 1
    
    F = VfyTwoColorQuarterNodeCover
    num = 1

    I ='a,b;a:c b:d;c;d'
    H = 'weird hint '*int(2**(len(I))/4096)
    exp = 'Size of hint is kinda unreasonable'
    num = test_case(F, I, 'yes', H, 'unsure', num, exp)

    I ='a,b a,c d,e d,f a,g ;' +\
        'a:beige b:umber c:taupe d:crimson e:umber f:beige g:puce ;' +\
        'beige; crimson'
    exp = '{a,d}| = 2 > 1 = floor(# nodes in Graph/4)'
    num = test_case(F, I, 'yes', 'a d', 'unsure', num, exp)

    I = 'a,b a,c d,e d,f a,g b,h; ' +\
        'a:beige b:umber c:taupe d:crimson e:umber f:beige g:puce h:ecru;' +\
        'beige; crimson'
    exp = 'no set of two nodes cover graph'
    num = test_case(F, I, 'yes', 'a d', 'unsure', num, exp)

    I = 'a,b a,c d,e d,f a,g b,h; ' +\
        'a:incarnadine b:umber c:taupe d:crimson e:umber f:beige g:puce h:ecru;' +\
        'beige; crimson'
    exp = 'node a not colored beige or crimson'
    num = test_case(F, I, 'yes', 'a d', 'unsure', num, exp)

    I = 'a,b a,c d,e d,f a,g d,h;' +\
        'a:beige b:umber c:taupe d:crimson e:umber f:beige g:puce h:ecru' +\
        '; beige; crimson'
    exp = 'a & d, beige & crimson, cover graph'
    num = test_case(F, I, 'yes', 'a d', 'correct', num, exp)

    # additional test cases

    I = 'a,b a,c d,e d,f a,g d,h;' +\
        'a:alizarin b:bistre c:catawba d:daintree e:eminence f:flax g:gamboge h:harlequin' +\
        '; bistre; flax'
    exp = 'not verifying positive instance'
    num = test_case(F, I, 'no', 'a d', 'unsure', num, exp)

    I = 'a,b a,c d,e d,f a,g d,h;' +\
        'a:razzmatazz b:feldgrau c:australien d:fulvous e:zaffre f:xanadu g:smaragdine h:eau-de-nil' +\
        '; eau-de-nil; feldgrau'
    exp = 'node z is not in the graph'
    num = test_case(F, I, 'yes', 'z a', 'unsure', num, exp)
