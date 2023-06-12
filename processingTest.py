from processing_py import *


known_nodes = {}
pos = (2, 2)
total_nodes = 1000

WIDTH = 1800
HEIGHT = 1000
NODE_SIZE = 4
LINE_SPACING = 10

app = App(WIDTH, HEIGHT)
app.background(255, 255, 255)


HALF_NODE = int(NODE_SIZE/2)
MAX_COL_SIZE = 300
n = 0
app.rectMode(CENTER)
TOTAL_ROWS = 35
i = 0

while i < TOTAL_ROWS:
    print(i)
    #Left to right
    while n < MAX_COL_SIZE:
        inc = (WIDTH / MAX_COL_SIZE) #spacing

        if n != 0 :
            pos = pos[0] + inc, pos[1]
        app.noStroke()
        app.fill(255, 0, 0)
        app.rect(pos[0], pos[1], NODE_SIZE, NODE_SIZE) #node size: 4x4 (x0, y0, x1, y1)

        #Line between nodes
        app.stroke(0, 0, 0)
        app.line(pos[0]+HALF_NODE, pos[1], pos[0]-inc-HALF_NODE, pos[1])

        n += 1
    app.redraw()
    pos = pos[0], pos[1] + NODE_SIZE + LINE_SPACING
    n = 0
    #line down
    app.stroke(0, 255, 0)
    app.line(pos[0], pos[1] - LINE_SPACING, pos[0], pos[1])
    #Right to left
    while n < MAX_COL_SIZE:
        inc = (WIDTH / MAX_COL_SIZE) #spacing
        if n != 0 :
            pos = pos[0] - inc, pos[1]

        app.noStroke()
        app.fill(255, 0, 0)
        app.rect(pos[0], pos[1], NODE_SIZE, NODE_SIZE) #node size: 4x4 (x0, y0, x1, y1)

        #Line between nodes
        app.stroke(0, 0, 0)
        app.line(pos[0]+HALF_NODE, pos[1], pos[0]-inc-HALF_NODE, pos[1])

        n += 1

    pos = pos[0], pos[1] + NODE_SIZE + LINE_SPACING
    n = 0
    #line down
    app.stroke(0, 255, 0)
    app.line(pos[0], pos[1] - LINE_SPACING, pos[0], pos[1])
    i += 1
    app.redraw()
app.redraw()

# app.translate(WIDTH/2, HEIGHT/2) # center the circle
# while theta < 2 * PI:
#     x = R * math.cos(theta)
#     y = R * math.sin(theta)
#     app.fill(255, 0, 0)
#     app.rect(x, y, NODE_SIZE, NODE_SIZE) #node size: 4x4 (x0, y0, x1, y1)
#     theta += 2 * PI / total_nodes 
# app.redraw()

# for pair in edges:1
#     for edge in pair:
#         if edge in known_nodes:

#             print(edge)
