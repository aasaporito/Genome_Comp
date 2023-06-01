import networkx as nx
import matplotlib.pyplot as plt
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

# TODO: Add name as file name parameter
def save_graph(graph):
    ## Saves the graph as an image
    plt.tight_layout()
    nx.draw_networkx(graph, arrows=True)
    plt.savefig("graph.png", format="PNG")
    plt.clf()

# TODO: https://networkx.org/documentation/stable/reference/functions.html#nodes
# Returns true when the graph is a loop
# Assumption: a graph is a loop when no input or output edge exists more than once
# TODO: Do I need to test if each node has 2 connections?
def loop_test(graph):
    all_inputs = []
    all_outputs = []

    for node in graph.nodes(): 
        in_edges = list(nx.neighbors(graph, node))
        all_edges = list(nx.all_neighbors(graph, node)) #Becomes only output edges

        for edge in all_edges:
            if edge in in_edges:
                all_edges.remove(edge)
        all_inputs.extend(in_edges)
        all_outputs.extend(all_edges)


    return not(check_dupes(all_inputs) and check_dupes(all_outputs))


# Utilize that sets cannot have duplicates to efficiently check for dupes
# True indicates that there are duplicates
def check_dupes(input_list):
    return len(input_list) != len(set(input_list))
	