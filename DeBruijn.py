"""Summary
    Contains contains functions to generate directional graphs, traverse,
    and save them. Additionally tests if the graph is a directional circuit
    with no overlapping nodes traversed.
"""
from file_tools import *


def get_counts_from_seq(seq, k=50, circular=True):
    """Summary
        Split a sequence into k-mers of length k and return them with their 
        respect counts.
    Args:
        seq (str): Data to process, i.e. a portion of DNA.
        k (int, optional): k-mer size. 50 by default.
        circular (bool, optional): Indicates whether wrap around should be included in k-mers. True by default.
    
    Returns:
        dict: A collection of k-mers
    """
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


def get_edges(collection):
    """Summary
        Generates all edges between a given collection of k-mers.
    Args:
        collection (dict): A collection of k-mers
    
    Returns:
        set: A set of all edges between the given collection's overlap between items.
    """
    edges = set()

    for j in collection:
        for k in collection:
            if j != k:
                if j[1:] == k[:-1]:
                    edges.add((j[:-1], k[:-1]))  # Add overlap from j to k
                if j[:-1] == k[:-1]:
                    edges.add((k[:-1], j[:-1]))  # Add overlap from k to j

    return edges
   
#todo Rewrite these for processing_plot
# def loop_test(graph):
#     """Summary
#         Returns true when the graph is a 1-directional closed circuit. 

#         Assumptions to return True:
#             - No input edge exists more than once
#             - No output edge exists more than once
#             - The amount of edges must equal the amount of nodes
#             - The graph is traversable by visiting every node once. (nodes traveled = total nodes)
#     Args:
#         graph (DiGraph): A directional graph from networkx
    
#     Returns:
#         (bool, list): Indicates that the graph is a 1-directional closed circuit. A list of nodes
#                         that were traversed.
#     """
#     all_inputs = []
#     all_outputs = []
#     total_edges = 0

#     for node in graph.nodes(): 
#         in_edges = list(nx.neighbors(graph, node))
#         all_edges = list(nx.all_neighbors(graph, node)) #Becomes only output edges

#         for edge in all_edges:
#             if edge in in_edges:
#                 all_edges.remove(edge)

#         all_inputs.extend(in_edges)
#         all_outputs.extend(all_edges)

#     total_edges = len(all_inputs) + len(all_outputs)

#     #Implies graph loops on itself (edges/2 because total_edges counts in and out)
#     edges_eq_nodes = (total_edges/2 == len(graph.nodes()))

#     #Checks that no input or output edge exists twice
#     is_loop = not(check_dupes(all_inputs) and check_dupes(all_outputs))
#     is_trav = is_traversable(graph)
#     edge_chec = edge_check(graph)

#     # print(edges_eq_nodes)
#     # print(is_loop)
#     # print(is_trav[1])
#     # print(edge_chec)
#     #  todo 15 (general) +0: way too high of a loop find rate
#     return ((is_loop and edges_eq_nodes and is_trav[1] and edge_chec), is_trav[0])