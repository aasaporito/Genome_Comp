from PIL import Image, ImageDraw
import math


def draw_square(image, pos, NODE_SIZE, color=""):
    x, y = pos
    img1 = ImageDraw.Draw(image)
    c = (0, 192, 192)
    if color == "red":
        c = (255, 0, 0)
    elif color == "green":
        c = (0, 255, 0)
    elif color == "blue":
        c = c
    img1.rectangle((x, y, x + NODE_SIZE, y + NODE_SIZE),
                   fill=c, outline=(255, 255, 255))
    return (x,y)


def store_pos(pos, node):
    name = node
    x, y = pos
    weight = 0
    connections = []
    return {name: [pos, weight, connections]}

def update_weights(known_nodes, node, edge_type, image, NODE_SIZE):
    if edge_type == "input":
        known_nodes[node][1] += 2
    elif edge_type == "output": #output edge
        known_nodes[node][1] += 4
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
            #print("Node has 1 input and 1 output edge: " + node) # perfect
            draw_square(image, known_nodes[node][0], NODE_SIZE, color="green")
        case _:
            #print("Node has >2 edges: " + node) #problem area
            draw_square(image, known_nodes[node][0], NODE_SIZE, color="red")

def generate_plot(nodes):
    nodes = list({('ATA', 'TAT'), ('AAG', 'AGT'), ('GAA', 'AAT'), ('TGG', 'GGA'), ('GGA', 'GAC'), ('GTA', 'TAG'), ('AGT', 'GTA'), ('ATG', 'TGA'), ('TGA', 'GAA'), ('CAT', 'ATA'), ('CCG', 'CGG'), ('AGA', 'GAT'), ('ATA', 'ATA'), ('TAT', 'ATA'), ('GCC', 'CCA'), ('ATA', 'TAA'), ('CCA', 'CAT'), ('CGG', 'GGC'), ('AAT', 'ATG'), ('GGC', 'GCC'), ('GAC', 'ACC'), ('ATG', 'TGG'), ('ATG', 'ATG'), ('GAT', 'ATG'), ('TAA', 'AAG'), ('TAG', 'AGA'), ('ACC', 'CCG')})

    known_nodes = {}
    total_nodes = len(nodes)
    WIDTH, HEIGHT = 1500, 1500

    #Increases canvas size as needed
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
    image.save("image.png", "PNG")

    #Construct the nodes and stores their coordinates
    for pair in nodes:
        for node in pair:
            if node not in known_nodes:
                current_pos = draw_square(image, (round(R * math.cos(theta)+pos[0]), round(R * math.sin(theta)+pos[1])), NODE_SIZE)
                known_nodes.update(store_pos(current_pos, node))
                theta += 2 * PI / (total_nodes+1)


    for pair in nodes:
        node1 = pair[0]
        node2 = pair[1]
        
        #todo are weights truly needed beyond coloring? or even needed for coloring?
        #todo seems to plot graphs fully green even if they shouldnt be
        update_weights(known_nodes, node1, "input", image, NODE_SIZE) #<- is the problem that the first node iterated technically isn't an input?, most likely yes
        update_weights(known_nodes, node2, "output", image, NODE_SIZE)

        known_nodes[node1][2].append(node2)
        known_nodes[node2][2].append(node1)
        if len(known_nodes[node1][2]) > 2 :
            update_weights(known_nodes, node1, "failed", image, NODE_SIZE)
        if len(known_nodes[node2][2]) > 2:
            update_weights(known_nodes, node2, "failed", image, NODE_SIZE)

        img1 = ImageDraw.Draw(image)
        img1.line([known_nodes[node1][0], known_nodes[node2][0]], fill=(0,0,0))
    #print(known_nodes)

    image.show()