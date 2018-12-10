# func to initialize an empty board of nw0m
# func to place a gate with top left corner at (w0, y) in the board

import numpy as np


##########################################
### FUNCTIONS FOR ASSEMBLING THE BOARD ###
##########################################

def board(n, m):
# construct a board w n = vertical dimension, m = horizontal dimension
    row = ['z']*m
    return np.asarray([row, ]*n, dtype = object)

def add_gate(g, row, col, b):
    # given a gate g (a 2D np.array), a row, col coordinate
    # on the board b, place g with its upper left corner at (w0, y);
    # return the modified board

    # get dimensions of the gate
    (n, m) = g.shape

    # set the subset of the board to the gate
    b[row:row+n, col:col+m] = g
    return b

def add_wire(start_row, start_col, end_row, end_col, b):
    # add a horizontal or a vertical wire to a board b (including wires at end
    # points)

    # determine whether the wire is horizontal or vertical
    v = (start_row - end_row != 0)

    if v:
        if start_row < end_row:
            for i in range(start_row, end_row + 1):
                b[i, start_col] = 'w'
        else:
            for i in range(end_row, start_row + 1):
                b[i, start_col] = 'w'
    else:
        if start_col < end_col:
            for i in range(start_col, end_col + 1):
                b[start_row, i] = 'w'
        else:
            for i in range(end_col, start_col + 1):
                b[start_row, i] = 'w'

    return b

def add_piecewise_wire(pts, b):
    # add a wire that starts at pts[0] and has either a vertical or a horizontal
    # segment between pts[i] and pts[i+1]

    for i, p in enumerate(pts):
        if i > 0:
            b = add_wire(p[0], p[1], pts[i-1][0], pts[i-1][1], b)

    return b

#############
### GATES ###
#############

# reset w0 to w0 and w1 to Y

OR = np.asarray([['I', 'w0', 'w', 'w1', 'I'],
                ['z', 'J', 'z', 'J', 'z'],
                ['w', 'J', 'w', 'J', '1']], dtype = object)

AND = np.asarray([['I', 'w0', 'w', 'w1', 'I'],
                ['z', 'J', 'z', 'J', 'z'],
                ['0', 'J', 'w', 'J', 'w']], dtype = object)

NOT = np.asarray([['I', 'w0', 'w', 'w1', 'I'],
                ['z', 'J', 'z', 'J', 'z'],
                ['1', 'J', 'w', 'J', '0']], dtype = object)

FAN_OUT = np.asarray([['I1', 'w', 'J', '1'],
                     ['w1', 'w0', 'w1', 'z'],
                     ['I', 'w0', 'K', '0'],
                     ['w', 'z', 'w', 'z']], dtype = object)

WIREx = np.asarray([['z', 'w0', 'w', 'w1', 'z'],
                    ['I0', 'z', 'P', 'z', '0'],
                    ['w', 'J', 'J', 'w0', 'J'],
                    ['I1', 'z', 'P', 'z', '1'],
                    ['z', '0', 'P', '1', 'z']], dtype = object)

##########################
### ASSEMBLE THE BOARD ###
##########################

b = board(26, 37)

# add FAN_OUT

fo_loc = [(0, 1), (0, 10), (6, 20)]
for (row, col) in fo_loc:
    b = add_gate(FAN_OUT, row, col, b)

# add wire w0

b = add_gate(WIREx, 7, 8, b)

# add OR

or_loc = [(13, 8), (20, 23), (0, 31)]
for (row, col) in or_loc:
    b = add_gate(OR, row, col, b)

# add AND

and_loc = [(11, 14), (16, 23)]
for (row, col) in and_loc:
    b = add_gate(AND, row, col, b)

# add NOT

b = add_gate(NOT, 12, 23, b)

# add wires

wire_loc = [[(4, 0), (15, 0), (15, 4)],
            [(4, 3), (9, 3), (9, 7)],
            [(4, 10), (6, 10)],
            [(16, 10), (18, 10)],
            [(4, 11), (4, 21), (5, 21)],
            [(9, 12), (9, 15), (10, 15)],
            [(10, 20), (13, 20), (13, 19)],
            [(14, 15), (22, 15), (22, 23)],
            [(0, 29), (2, 29), (2, 30)],
            [(3, 33), (18, 33), (18, 30)],
            [(10, 21), (10, 24), (11, 24)],
            [(15, 24), (15, 24)],
            [(19, 24), (19, 24)],
            [(23, 24), (24, 24)],
            [(12, 10), (12, 10)]]

for pts in wire_loc:
    b = add_piecewise_wire(pts, b)

board_file = open("circuits/sqrt_layout.txt", "w")
for row in b:
    board_file.write("%s\n" % ' '.join(row))

board_file.close()
