"""Summary
    Contains contains functions to generate directional graphs, traverse,
    and save them. Additionally tests if the graph is a directional circuit
    with no overlapping nodes traversed.
"""
import networkx as nx
import matplotlib.pyplot as plt

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
   
def generate_diGraph(edges):
    """Summary
        Generates a directional graph from a collection of edges.
    Args:
        edges (list of tuples): A list containing tuples indicating the path of each edge.
    
    Returns:
        DiGraph: A DiGraph object from the networkx library.
    """
    graph = nx.DiGraph()
    graph.add_edges_from(edges)

    return graph


#  todo 3 (general) +0: Nested folders for each filename
def save_graph(graph, nodes, alignment, sam_name):
    """Summary
        Saves a graph to disk. Requires a folder labeled "Output" (#  todo 4 (general) +0: Generate output folder <-).
        Stores with the name pattern: Output/fileName_alignmentName_MAPQUALITY.png
        Illegal characters in the filename are replaced with 2 '_'
    
    Args:
        graph (DiGraph): A directional graph from networkx
        nodes (list): A list of traversed nodes
        alignment (Alignment): An Alignment objected generated from a SAM entry
        sam_name (str): Name of the SAM file storing the alignment.
    """
    file_name = generate_output_path(sam_name, alignment)

    
    nodes = is_traversable(graph)[0]
    node_colors = ["blue" if n in nodes else "yellow" for n in graph.nodes()]
    node_colors[0] = "red"
    node_colors[-1] = "red"
    

    ## Saves the graph as an image
    plt.rcParams['figure.figsize'] = [100, 100]
    nx.draw_networkx(graph, arrows=True, with_labels=False, node_size=200, node_color=node_colors, **{"edgecolors": "tab:gray"})

    #Displays the graph, pauses running
    #plt.show()

    plt.savefig(file_name, format="PNG")
    plt.clf()

def loop_test(graph):
    """Summary
        Returns true when the graph is a 1-directional closed circuit. 

        Assumptions to return True:
            - No input edge exists more than once
            - No output edge exists more than once
            - The amount of edges must equal the amount of nodes
            - The graph is traversable by visiting every node once. (nodes traveled = total nodes)
    Args:
        graph (DiGraph): A directional graph from networkx
    
    Returns:
        (bool, list): Indicates that the graph is a 1-directional closed circuit. A list of nodes
                        that were traversed.
    """
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
    is_trav = is_traversable(graph)
    edge_chec = edge_check(graph)

    # print(edges_eq_nodes)
    # print(is_loop)
    # print(is_trav[1])
    # print(edge_chec)
    #  todo 15 (general) +0: way too high of a loop find rate
    return ((is_loop and edges_eq_nodes and is_trav[1] and edge_chec), is_trav[0])


# Utilize that sets cannot have duplicates to efficiently check for dupes
def check_dupes(input_list):
    """Summary
        Helper function for test_loop(). Checks if there are multiple edges entering each node.
        Does not find which node has multiple entries.
    Args:
        input_list (list): A list of edges (Typically a collection of input edges or output edges.
        But not both simultaneously)
    
    Returns:
        bool: Returns true when a node has multiple edges in input_list.
    """
    return len(input_list) != len(set(input_list))

# Tests if each node is visited in a traversal	(no disconnected seperate graphs)
def is_traversable(graph):
    """Summary
        Helper function for test_loop(). Checks if a graph contains multiple closed circuits
        that are disconnected from each other. A graph is traversable in this context when a 
        traverse passes each node sequentially. The total amount of nodes traversed should equal
        the total amount of nodes.
    Args:
        graph (DiGraph): A directional graph from networkx
    
    Returns:
        Tuple: Returns the nodes traveled through. Returns true if a graph is traversable as 
                defined above. The tuple is in the for of (nodes_traveled, bool)
    """
    root = list(graph.nodes())

    n = list(graph.neighbors(root[0]))
    nodes_traveled = []
    while len(n) == 1:
        n = n[0]
        if n in nodes_traveled:
            if n == nodes_traveled[0] and len(nodes_traveled) == len(root):
                #Back at starting node after travelling all nodes                
                return (nodes_traveled, True)
                
            else:
                return (nodes_traveled, False)

        nodes_traveled.append(n)
        
        new_neighbor = list(graph.neighbors(n))
        n = new_neighbor
    return (nodes_traveled, False)


def edge_check(graph):
    """Summary
        Checks if all nodes in a graph contain one input and one output edge.
    Args:
        graph (DiGraph): A networkx Directed Graph
    
    Returns:
        bool: Returns true when all graph nodes have 1 input and one output edge,
    """
    for node in graph.nodes():
        in_neighbors = nx.neighbors(graph, node)
        all_len = len(list(nx.all_neighbors(graph, node)))
        if (all_len - len(list(in_neighbors)) == 1) and all_len == 2:
            continue

        else:
            return False
    return True

