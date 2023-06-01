from DeBruijn import *
#  todo 1 (general) +0: Rework/erase file
def test_plot(sequence, k):
    """Summary
        Non-functional method for testing hand-input data.
    Args:
        sequence (str): Description
        k (int): Description
    
    Returns:
        DiGraph: Description
    """
    #Circular Sequence example: test_plot("ACTGAGTACCATGGAC",4)
    sequences = get_counts_from_seq(sequence, k)
    edges = get_edges(sequences)
    
    #print(sequences)
    #print(edges)

    g1 = generate_diGraph(edges)
    if loop_test(g1):
        print("Loop found")
        save_graph(g1)
        return
    else:
        print("No loop found\n\n")
    return g1