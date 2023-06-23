from PIL import Image, ImageDraw
import math
import os
from Dictlist import Dictlist


def draw_square(image, pos, NODE_SIZE, color=""):
    x, y = pos
    img1 = ImageDraw.Draw(image)
    c = (0, 0, 192)
    if color == "red":
        c = (255, 0, 0)
    elif color == "green":
        c = (0, 255, 0)
    elif color == "blue":
        c = c
    img1.rectangle((x, y, x + NODE_SIZE, y + NODE_SIZE),
                   fill=c, outline=(255, 255, 255))
    return (x, y)


def store_pos(pos, node):
    name = node
    x, y = pos
    weight = 0
    connections = [[],[]] #first inputs, 2nd outputs
    return {name: [pos, weight, connections]}


def update_weights(known_nodes, node, edge_type, image, NODE_SIZE):
    if edge_type == "input":
        known_nodes[node][1] += 2
    elif edge_type == "output":  # output edge
        known_nodes[node][1] += 19
    else:
        known_nodes[node][1] += 99

    weight = known_nodes[node][1]

    match (weight):
        case 0:
            #print("Node not traveled: " + node)
            draw_square(image, known_nodes[node][0], NODE_SIZE, color="red")
        case 2:
            #print("Node has 1 input edge: " + node) #
            draw_square(image, known_nodes[node][0], NODE_SIZE, color="red")
        case 6:
            # print("Node has 1 input and 1 output edge: " + node) # perfect
            draw_square(image, known_nodes[node][0], NODE_SIZE, color="green")
        case _:
            # print("Node has >2 edges: " + node) #problem area
            draw_square(image, known_nodes[node][0], NODE_SIZE, color="red")


def generateOutput(fname, seq, image):
    fname = fname.replace("/", "_")
    path = 'Output/' + fname + "/"
    print(path)
    if not os.path.exists(path):  # path exists, create new sub file name
        os.makedirs(path)

    with open(path + "sequence" + '.txt', 'w') as file:
        file.write(seq)

    image.save(path + "plot" + '.png')


def generate_plot(nodes, fname):

    nodes = list(nodes)
    key1 = nodes[0][0]

    nodes_dict = dict(nodes)

    known_nodes = {}
    total_nodes = len(nodes)
    WIDTH, HEIGHT = 1500, 1500

    # Increases canvas size as needed
    if total_nodes > 500:
        multiplier = int(total_nodes / 500) + 1
        WIDTH *= multiplier
        HEIGHT *= multiplier

    NODE_SIZE = 6

    R = WIDTH * 0.49
    PI = math.pi

    theta = 0
    pos = (WIDTH / 2, HEIGHT / 2)

    image = Image.new('RGB', (WIDTH, HEIGHT), (255, 255, 255))

    current_pos = draw_square(image, (round(
        R * math.cos(theta) + pos[0]), round(R * math.sin(theta) + pos[1])), NODE_SIZE)
    known_nodes.update(store_pos(current_pos, key1))
    node1 = key1
    seq = node1

    print("Assembling genome")
    for i in range(len(nodes)):
        node2 = nodes_dict[node1]

        current_pos = draw_square(image, (round(
            R * math.cos(theta) + pos[0]), round(R * math.sin(theta) + pos[1])), NODE_SIZE)
        known_nodes.update(store_pos(current_pos, node2))
        theta += 2 * PI / (total_nodes + 1)
        seq = node1 + node2
        node1 = node2

    for pair in nodes:
        node1 = pair[0]
        node2 = pair[1]

        # todo are weights truly needed beyond coloring? or even needed for coloring?
        # todo seems to plot graphs fully green even if they shouldnt be

        # <- is the problem that the first node iterated technically isn't an input?, most likely yes
        update_weights(known_nodes, node1, "output", image, NODE_SIZE)
        update_weights(known_nodes, node2, "input", image, NODE_SIZE)

        known_nodes[node1][2][1].append(node2) #outputs
        known_nodes[node2][2][0].append(node1) #inputs

        if len(known_nodes[node1][2]) > 2:
            update_weights(known_nodes, node1, "failed", image, NODE_SIZE)
        if len(known_nodes[node2][2]) > 2:
            update_weights(known_nodes, node2, "failed", image, NODE_SIZE)

        img1 = ImageDraw.Draw(image)
        img1.line([known_nodes[node1][0], known_nodes[node2][0]], fill=(0, 0, 0))

    # image.show()

    # if looptest == true
    print("Checking circularity")
    print(is_traversable(known_nodes))
    for key in known_nodes:
        if not edge_check(known_nodes[key]):
            print("Edges are not balanced for a traverable graph")
            break

    print("Generating plot")
    generateOutput(fname, seq, image)
    return seq

def is_traversable(known_nodes):
    """Summary
        Helper function for test_loop(). Checks if a graph contains multiple closed circuits
        that are disconnected from each other. A graph is traversable in this context when a 
        traverse passes each node sequentially. The total amount of nodes traversed should equal
        the total amount of nodes.
    Args:
        known_nodes (dict): A complex dict list structure, do not manually create.
    
    Returns:
        bool: True if the amount of nodes traveresed - 1 is equal to the total amount of known nodes.
    """
    startKey = None
    traversed = [] 
    for key in known_nodes:
        startKey = key
        break

    traversed.append(startKey)
    currentKey = startKey

    print("Traversing graph")
    while (startKey != currentKey or len(traversed) <= 1):
        currentKeys = known_nodes[currentKey][2][1]

        if len(currentKeys) == 1:
            currentKey = known_nodes[currentKey][2][1][0]
            #print("Traversing ->", currentKey)
        elif len(currentKeys) == 0:
            print("Node has no outputs")
            break
        elif len(currentKeys) > 1:
            print("Node has multiple output nodes")
            break
        else:
            print("Negative node count, this shouldn't be possible")
            break

        traversed.append(currentKey)                # Does not account for revisting nodes, but that is covered in node_check?
    return len(traversed) - 1 == len(known_nodes) #Shows that the total amount of nodes has been visited

def edge_check(node):
    """Summary
         Checks if a node in a graph contain one input and one output edge.
         Covers the prior check_dupes function
     Args:
         graph (DiGraph): A networkx Directed Graph

     Returns:
         bool: Returns true when the node have 1 input and one output edge,
     """
    return node[1] == 21  # The correct weight is established as 21 for 1 input and 1 output
