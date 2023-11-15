from turtle import Turtle
import turtle
from enum import Enum
import copy

import sys
import argparse

sys.setrecursionlimit(10000) # Needed 

NUM_STEPS = 127 # For step num = 2n-1 for any n, the curve will form a square
SCALE_FACTOR = 11
COLORS = [
    (0, 0, 0),
    (255, 0, 0),
    (255, 0, 255),
    (0, 0, 255),
    (0, 255, 255),
    (0, 255, 0),
    (255, 255, 0),
    (255, 255, 255)
]

SCREEN_SIZE = 1300

t = Turtle()

class Orientation(Enum):
    VERTICAL = 1
    HORIZONTAL = 2

class StickNode:
    """
    A single line of the StickFractal graph. Nodes "point to" their parent
    creating an edge.
    """
    def __init__(self, pos, orientation, parent):
        super(StickNode, self).__init__()
        self.x = pos[0]
        self.y = pos[1]
        self.parent = parent
        self.children = [] # Every node will have 0 or 2 children.
                           # It will always have 2 children extending from it,
                           # however in the case two nodes are 1 space apart,
                           # both of them will "own" the common child.
                           # If a node shares a position with another node which has
                           # a different parent, then both nodes will have 0 children

        self.extendable = True
        self.orientation = orientation


    def add_child(self, node):
        self.children.append(node)
        return node

    def not_extendable(self):
        """
        A node is not extendable if it shares a position with another node, where
        the 2nd node has a different parent.
        """
        self.extendable = False

    def __repr__(self):
        return "{position:(" + str(self.x) + ", " + str(self.y) + "), orientation:" + self.orientation.name + ", extendable? " + str(self.extendable) + "}"


class StickFractal:
    """
    Data structure holding the full fractal object
    A collection of fractal nodes
    """
    def __init__(self):
        super(StickFractal, self).__init__()
        self.head_node = StickNode([0,0], Orientation.HORIZONTAL, None) # The first node is at the origin and has no length
        self.head_node.add_child(StickNode([0, 1], Orientation.VERTICAL, self.head_node))
        self.head_node.add_child(StickNode([0, -1], Orientation.VERTICAL, self.head_node))
        self.head_node.not_extendable()

        self.nodes = copy.deepcopy(self.head_node.children) # Simple list of all nodes in the graph
        self.nodes.append(self.head_node)
        self.end_nodes = copy.deepcopy(self.head_node.children) # List of nodes without children

    def next_step(self):
        """
        Take 1 step on the fractal generation. Add children to all end nodes
        """
        end_nodes = copy.deepcopy(self.end_nodes)
        self.end_nodes.clear() # Empty end_nodes so it can recieve all new nodes after this iteration
        #print(end_nodes)
        #print(self.end_nodes)
        for node in end_nodes:
            #print(node)
            if node.extendable:
                if node.orientation == Orientation.HORIZONTAL:
                    self.add_node(StickNode([node.x, node.y + 1], Orientation.VERTICAL, node), node)
                    self.add_node(StickNode([node.x, node.y - 1], Orientation.VERTICAL, node), node)
                if node.orientation == Orientation.VERTICAL:
                    self.add_node(StickNode([node.x - 1, node.y], Orientation.HORIZONTAL, node), node)
                    self.add_node(StickNode([node.x + 1, node.y], Orientation.HORIZONTAL, node), node)
            #print(node.children)
        #self.draw_graph(self.end_nodes)


    def init_graph(self):
        t.screen.screensize(SCREEN_SIZE, SCREEN_SIZE)
        t.screen.setworldcoordinates(SCREEN_SIZE / 2, -SCREEN_SIZE / 2, -SCREEN_SIZE / 2, SCREEN_SIZE / 2)
        t.pencolor(COLORS[0])
        t.speed(0)
        t.penup()
        t.hideturtle()
        turtle.tracer(False)

    def draw_graph(self, nodes):
        # Draw the lines for each node
        for node in nodes:
            if node.parent:
                t.setpos(node.parent.x * SCALE_FACTOR, node.parent.y * SCALE_FACTOR)
                t.pendown()
                t.setpos(node.x * SCALE_FACTOR, node.y * SCALE_FACTOR)
                t.penup()

        # Draw filled shapes for loops
        loop_shapes = self.find_loops()
        # TODO

    def add_node(self, node, parent):

        self.nodes.append(node)
        self.end_nodes.append(node)
        parent.add_child(node)

        for other in self.nodes:
            if other.x == node.x and other.y == node.y and other.parent != node.parent:
                node.not_extendable()
                other.not_extendable()


    def find_loops(self):
        pass
        


if __name__ == "__main__":
    fractal = StickFractal()
    fractal.init_graph()
    print("Generating shape...")
    for i in range(NUM_STEPS):
        fractal.next_step()
        #input() # Wait for user press `enter' to continue
    print("Drawing shape...")
    fractal.draw_graph(fractal.nodes)
    print("Done!")
    turtle.mainloop()