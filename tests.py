def test_plot(sequence, k):
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