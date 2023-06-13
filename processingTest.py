from PIL import Image, ImageDraw
import math


def draw_square(app, pos, NODE_SIZE):
    x, y = pos
    img1 = ImageDraw.Draw(app)
    img1.rectangle((x, y, x + NODE_SIZE, y + NODE_SIZE),
                   fill=(0, 192, 192), outline=(255, 255, 255))


def draw_line_down(app, pos, LINE_SPACING):
    # line down
    app.stroke(0, 255, 0)
    app.line(pos[0], pos[1] - LINE_SPACING, pos[0], pos[1])


def store_pos(pos, node):
    name = node[0]
    x, y = pos

    return {name: pos}


nodes = {('ATA', 'TAT'), ('AAG', 'AGT'), ('GAA', 'AAT'), ('TGG', 'GGA'), ('GGA', 'GAC'), ('GTA', 'TAG'), ('AGT', 'GTA'), ('ATG', 'TGA'), ('TGA', 'GAA'), ('CAT', 'ATA'), ('CCG', 'CGG'), ('AGA', 'GAT'), ('ATA', 'ATA'),
         ('TAT', 'ATA'), ('GCC', 'CCA'), ('ATA', 'TAA'), ('CCA', 'CAT'), ('CGG', 'GGC'), ('AAT', 'ATG'), ('GGC', 'GCC'), ('GAC', 'ACC'), ('ATG', 'TGG'), ('ATG', 'ATG'), ('GAT', 'ATG'), ('TAA', 'AAG'), ('TAG', 'AGA'), ('ACC', 'CCG')}

known_nodes = {}
total_nodes = 5

WIDTH = 1800
HEIGHT = 1800

NODE_SIZE = 6
LINE_SPACING = 10

R = WIDTH * 0.45
HALF_NODE = int(NODE_SIZE / 2)

PI = math.pi

theta = 0
pos = (WIDTH / 2, HEIGHT / 2)

image = Image.new('RGB', (WIDTH, HEIGHT), (255, 255, 255))
image.save("image.png", "PNG")


draw_square(image, pos, NODE_SIZE)

while theta < (PI * 2):

    draw_square(image, ((R * math.cos(theta)+pos[0]), R * math.sin(theta)+pos[1]), NODE_SIZE)
    theta += 2 * PI / total_nodes
    print(theta)

image.show()
#known_nodes.update(store_pos(pos, [node]))
