from graph import Graph
from VfyQuarterClique import VfyQuarterClique 
from math import ceil, floor # why

name = 'PolyReduceQuarterNodeCoverToQuarterClique()'
VERBOSE = True
def printV(text):
    if VERBOSE: print(f'VERBOSE: {name} - {text}')

DEV = True
def printD(text):
    if DEV: print(f'DEV: {name} - {text}')

def make_new_node(nodes, new_nodes):
    '''
    Arguments:
      nodes -- list of nodes in the quarterNodeCover instance
      new_nodes -- new nodes

    Returns a node name consisting of Z's, which is not in either
    nodes or new_nodes
    '''
    
    new_node = 'Z1'
    names = nodes + new_nodes
    idx = 2
    for n in names:
        if n == new_node:
            new_node = f'Z{idx}'
            idx += 1
        
    return new_node

def graph_complement(graph_str, directed_=False):
    '''
    Given an unweighted graph defined as a white-space delimited sequence of
    edges, return a *list* of the edges in the graph complement.

    If there are no edges connecting a node in the graph complement, then a
    loopback edge for that node is included in the return list.

    For example, if the input was an undirected, unweighted graph
    'a,b b,c c,a b,d', the return list would be some permutation of:
    [a,d b,b c,d] 

    '''
    g = Graph(graph_str, directed=directed_, weighted=False)
    nodes = list(g.nodes.keys())
    edges =  graph_str.split()
    g_complement_edges = []
    for n1_idx in range(len(nodes)-1):
        for n2_idx in range(n1_idx+1,len(nodes)):
            n1 = nodes[n1_idx]
            n2 = nodes[n2_idx]
            if f'{n1},{n2}' not in edges and f'{n2},{n1}' not in edges:
                g_complement_edges.append(f'{n1},{n2}')
    
    g_complement_str = ' '.join(g_complement_edges)
    g_complement = Graph(g_complement_str, directed=False, weighted=False)
    g_complement_nodes = list(g_complement.nodes.keys())
    loopback_edges =\
        [f'{n},{n}' for n in nodes if n not in g_complement_nodes]

    g_complement_edges.extend(loopback_edges)
    
    return g_complement_edges #returns list of edges

 
def PolyReduceQuarterNodeCoverToQuarterClique(QNC_instance):
    g = Graph(QNC_instance, weighted=False, directed=False)
    nodes = list(g.nodes.keys())

    new_nodes = []

    #** HW #2 -- calculate number of new nodes required
    #** for the QuarterClique instance
    # CHANGE THIS
    num_new_nodes = 2 * len(nodes) # nodes - cover_size = (nodes + new) / 4
                                   # since no danger of positive -> negative (lower cover size only makes it easier for quarter clique)
                                   # we can just use the upper bound for cover_size:
                                   # nodes - (nodes / 4) = (nodes + new) / 4 => 4 * nodes - nodes = nodes + new
                                   # => new = 2 * nodes
    
    for node in range(num_new_nodes):
        new_nodes.append(make_new_node(nodes, new_nodes))

    #** HW #2 Apply the correct transformation when converting
    #** node cover instances to clique instances.
    QClique_edges = graph_complement(QNC_instance) # CHANGE THIS

    #** HW #2 Configure the new nodes correctly for the QuarterClique
    #** instance, and add them to QClique_instance 
    if new_nodes:
        for new in new_nodes:
            QClique_edges.append(f'{new},{new}')    # config to be island

    QClique_instance = ' '.join(QClique_edges)
    
    printV(f'Quarter clique instance = "{QClique_instance}"')
    return QClique_instance

C = PolyReduceQuarterNodeCoverToQuarterClique
                                                   

def vfyQuarterNodeCovervViaVfyQuarterClique(QNC_instance,S,H):
    # Please do not modify this routine
    QClique_instance = C(QNC_instance)
    
    g = Graph(QNC_instance, weighted=False, directed=False)
    nodes = list(g.nodes.keys()) #Convert to list
    
    H_QuarterClique = ','.join([node for node in nodes if node not in H.split()])
    

    printV('Hint for QuarterClique  verifier to use on converted' + \
           f' instance: "{H_QuarterClique}": ' + \
           f'  (nodes in QNC instance, but not in H = "{H}")')
    result = \
        VfyQuarterClique(QClique_instance,S, H_QuarterClique)
                                                   
    return result


if __name__ == '__main__':

    def test_case(F,I,S,H,expected,num,comment=''):
        err = '** '
        result = F(I,S,H)
        func_name = str(F).split()[1]
        func_call = f'''{func_name}("{I}","{S}","{H}")'''
        if result == expected: err = ''
        e = expected
        print (f'{err}test #{num} {func_call}: expected "{e}", received "{result}"')
        print (f'test #{num} Explanation: {comment}\n')
        return num + 1

    F =  vfyQuarterNodeCovervViaVfyQuarterClique
    num = 1

    I = 'a,b a,c a,d b,e'                    
    exp = 'a does not cover 5 node graph'
    num = test_case(F,I,'yes','a','unsure',num,exp)    

    I = 'a,b a,c a,d b,e'                    
    exp = 'a b is more than 1/4 nodes'
    num = test_case(F,I,'yes','a b','unsure',num,exp)    

    I = 'a,b a,c'                    
    exp = 'a is more than 1/4 nodes'
    num = test_case(F,I,'yes','a','unsure',num,exp)    

    I = 'a,b a,c a,d'                    
    exp = 'a covers 4 node graph'
    num = test_case(F,I,'yes','a','correct',num,exp)

    I = 'a,b a,c a,d a,e'                    
    exp = 'a covers 5 node graph'
    num = test_case(F,I,'yes','a','correct',num,exp)

    I ='a,b a,c d,e d,f a,g'
    exp = '{a,d}| = 2 > 1 = floor(# nodes in Graph/4)'
    num = test_case(F,I,'yes','a d','unsure',num,exp)

    I = 'a,b a,c d,e d,f a,g b,h'
    exp = 'no set of two nodes cover graph'
    num = test_case(F,I,'yes','a d','unsure',num,exp)

    I = 'a,b a,c d,e d,f a,g d,h' 
    exp = 'a & d  cover graph' 
    num = test_case(F,I,'yes','a d', 'correct',num,exp)

    # additional test cases

    # upper bound for cover is 3/12, actual is 2. lower bound for clique is 9/36, actual is 10. +/+
    I = 'a,b a,c a,d a,e a,f a,g h,i h,j h,k h,l'
    exp = '{a, h} cover 12 nodes, {b, c, d, e, f, g, i, j, k, l} form 10 clique out of 36 nodes'
    num = test_case(F, I, 'yes', 'a h', 'correct', num, exp)

    # upper bound for cover is 3/12, actual is 3. lower bound for clique is 9/36, actual is 9. +/+
    I = 'a,b a,c a,d e,f e,g h,i h,j h,k h,l'
    exp = '{a, e, h} cover 12 nodes, {b, c, d, f, g, i, j, k, l} form 9 clique out of 36 nodes'
    num = test_case(F, I, 'yes', 'a e h', 'correct', num, exp)

    # upper bound for cover is 3/12, actual is 4. lower bound for clique is 9/36, actual is 8. -/- (DANGER CASE)
    I = 'a,b a,c e,f e,g h,i h,j k,l k,d'
    exp = 'no set of <= 3/12 nodes covers graph, no set of >= 9/36 nodes form a clique (danger here is mapping negative to positive)'
    num = test_case(F, I, 'yes', 'a e h', 'unsure', num, exp)
