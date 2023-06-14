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
        known_nodes[node][1] += 1
    else: #output edge
        known_nodes[node][1] += 9
        
    weight = known_nodes[node][1]

    match (weight):
        case 0:
            print("Node not traveled: " + node)
            draw_square(image, known_nodes[node][0], NODE_SIZE, color="red")
        case 1:
            print("Node has 1 input edge: " + node) #
            draw_square(image, known_nodes[node][0], NODE_SIZE, color="red")
        case 10:
            print("Node has 1 input and 1 output edge: " + node) # perfect
            draw_square(image, known_nodes[node][0], NODE_SIZE, color="green")
        case _:
            print("Node has >2 edges: " + node) #problem area
            draw_square(image, known_nodes[node][0], NODE_SIZE, color="red")


nodes = list({('TGGAC', 'GGACC'), ('GGACC', 'GACCG'), ('AGTAG', 'GTAGA'), ('GCCAT', 'CCATA'), ('TATAA', 'ATAAG'), ('CCGGC', 'CGGCC'), ('GACCG', 'ACCGG'), ('CCATA', 'CATAT'), ('TAGAT', 'AGATG'), ('GATGA', 'ATGAA'), ('TAAGT', 'AAGTA'), ('AGATG', 'GATGA'), ('CATAT', 'ATATA'), ('AAGTA', 'AGTAG'), ('TGAAT', 'GAATG'), ('ATGGA', 'TGGAC'), ('AATGG', 'ATGGA'), ('ACCGG', 'CCGGC'), ('GGCCA', 'GCCAT'), ('ATATA', 'TATAA'), ('ATAAG', 'TAAGT'), ('CGGCC', 'GGCCA'), ('GAATG', 'AATGG'), ('ATGAA', 'TGAAT'), ('GTAGA', 'TAGAT')})

known_nodes = {}
total_nodes = len(nodes)
WIDTH, HEIGHT = 1200, 1200

#Increases canvas size as needed
if total_nodes > 500:
    multiplier = int(total_nodes / 500) + 1
    WIDTH *= multiplier
    HEIGHT *= multiplier

NODE_SIZE = 6
LINE_SPACING = 10

R = WIDTH * 0.49
HALF_NODE = int(NODE_SIZE / 2)

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
    update_weights(known_nodes, node1, "input", image, NODE_SIZE)
    update_weights(known_nodes, node2, "output", image, NODE_SIZE)

    known_nodes[node1][2].append(node2)
    known_nodes[node2][2].append(node1)
    if len(known_nodes[node1][2]) > 2:
        update_weights(known_nodes, node1, "output", image, NODE_SIZE)
    if len(known_nodes[node2][2]) > 2:
        update_weights(known_nodes, node2, "output", image, NODE_SIZE)

    img1 = ImageDraw.Draw(image)
    img1.line([known_nodes[node1][0], known_nodes[node2][0]], fill=(0,0,0))
print(known_nodes)

image.show()