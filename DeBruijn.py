import networkx as nx
import matplotlib.pyplot as plt

from file_tools import *
''' 
Split a sequence into parts of length k and return them with their 
respect counts.

Parameters: 
	- seq: an input string
	- k: chunk sizes to test for overlap
Returns a dictionary.
'''


def get_counts_from_seq(seq, k=50, circular=True):
    collection = {}  # dict

    for i in range(0, len(seq)):
        chunk = seq[i:i + k]  # Gets the next sequence chunk between i and k

        chunk_length = len(chunk)

        # For sequences that ideally wrap around
        if circular:
            if chunk_length != k:
                chunk += seq[:(k - chunk_length)]

        # Linear sequences
        else:
            if chunk_length != k:
                continue

        if chunk in collection:
            collection[chunk] += 1  # Already exists in collection
        else:
            collection[chunk] = 1  # New entry to the collection

    return collection


'''
'''
def get_edges(collection):

    edges = set()

    for j in collection:
        for k in collection:
            if j != k:
                if j[1:] == k[:-1]:
                    edges.add((j[:-1], k[:-1]))  # Add overlap from j to k
                if j[:-1] == k[:-1]:
                    edges.add((k[:-1], j[:-1]))  # Add overlap from k to j

    return edges

#edges should be a list of tuples    
def generate_diGraph(edges):
    graph = nx.DiGraph()
    graph.add_edges_from(edges)

    return graph

# Stores with the name pattern: Output/fileName_alignmentName_MAPQUALITY.png
# Illegal characters in the filename are replaced with 2 '_'
# TODO: Nested folders for each fileName
def save_graph(graph, alignment, sam_name):
    file_name = generate_output_path(sam_name, alignment)
    
    ## Saves the graph as an image
    plt.rcParams['figure.figsize'] = [100, 100]
    nx.draw_networkx(graph, arrows=True, with_labels=False, node_size=100)
    #plt.show()
    plt.savefig(file_name, format="PNG")
    plt.clf()

# Returns true when the graph is a loop with no deadends
# Assumption: a graph is a loop when no input or output edge exists more than once, nodes = edges
# A: Graph is traversable, where nodes traveled = total nodes
def loop_test(graph):
    all_inputs = []
    all_outputs = []
    total_edges = 0

    for node in graph.nodes(): 
        in_edges = list(nx.neighbors(graph, node))
        all_edges = list(nx.all_neighbors(graph, node)) #Becomes only output edges

        for edge in all_edges:
            if edge in in_edges:
                all_edges.remove(edge)

        all_inputs.extend(in_edges)
        all_outputs.extend(all_edges)

    total_edges = len(all_inputs) + len(all_outputs)

    #Implies graph loops on itself (edges/2 because total_edges counts in and out)
    edges_eq_nodes = (total_edges/2 == len(graph.nodes()))

    #Checks that no input or output edge exists twice
    is_loop = not(check_dupes(all_inputs) and check_dupes(all_outputs))

    return is_loop and edges_eq_nodes and is_traversable(graph)


# Utilize that sets cannot have duplicates to efficiently check for dupes
# True indicates that there are duplicates
def check_dupes(input_list):
    return len(input_list) != len(set(input_list))

# Tests if each node is visited in a traversal	(no disconnected seperate graphs)
def is_traversable(graph):
    nodes = graph.nodes()
    traveled_nodes = list(nx.dfs_preorder_nodes(graph))

    return len(traveled_nodes) == len(nodes)

