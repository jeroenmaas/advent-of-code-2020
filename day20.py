import json
import math

import numpy as np

with open('day20.txt') as f:
    tiles_input = list(map(lambda a: a.split('\n'), f.read().strip().split('\n\n')))

# Because i don't know the amount of unique positions i'll just rotate
def generate_options(tile_parts):
    options = []

    tile_parts_np = np.array(list(map(lambda a: list(a), tile_parts)))
    for i in range(4):
        tile_parts_np = np.rot90(tile_parts_np)
        options.append(tile_parts_np)

        r = np.array(list(reversed(list(tile_parts_np))))
        options.append(r)

    return options

def generate_borders(tile_parts):
    borders = []
    borders.append(tile_parts[0])
    right = []
    for i in tile_parts:
        right.append(i[-1])
    borders.append(right)
    borders.append(tile_parts[-1])
    left = []
    for i in tile_parts:
        left.append(i[0])
    borders.append(left)
    return borders

def convert_border_to_value(border):

    value = 0
    for i, b in enumerate(reversed(border)):
        if b == True:
            value += pow(2, i)
    return value

def print_option(option):
    for line in option:
        print(''.join(map(lambda a: '#' if a else '.', line)))

def check_neighbours(map, x, y, border_option):
    inverse_direction = [2, 3, 0, 1]

    # check top, right, bottom, left
    for i, (xoffset, yoffset) in enumerate([[-1, 0], [0, 1], [1, 0], [0, -1]]):
        xcheck = x + xoffset
        ycheck = y + yoffset
        try:
            border = map[ycheck][xcheck]
            if border is not None and border[inverse_direction[i]] != border_option[i]:
                if i == 2:
                    print('x1: ' + str(xcheck))
                    print('y1: ' + str(ycheck))
                return False
        except:
            pass
    return True

tiles = {}
for i in tiles_input:
    id = int(i[0].replace('Tile ', '').replace(':', ''))
    tile_parts = list(map(lambda a: list(map(lambda b: b == '#', a)), i[1:]))
    options = generate_options(tile_parts)

    # print('id: ' + str(id))
    # for o in options:
    #     print_option(o)
    #     print('---------')
    #
    # exit()

    borders_options = list(map(lambda a: list(map(lambda b: convert_border_to_value(b), generate_borders(a))), options))
    tiles[id] = {
        'options': options,
        'borders_options': borders_options
    }
# flip
# invert

size = int(math.sqrt(len(tiles)))

a = np.zeros((size,size))

map = a.tolist()
for x in range(size):
    for y in range(size):
        map[y][x] = None

options = []
for x in range(size):
    for y in range(size):
        print('x: ' + str(x))
        print('y: ' + str(y))
        print(len(options))
        if len(options) == 24:
            print(options)

        if x == 0 and y == 0:
            for id, t in tiles.items():
                for bo in t['borders_options']:
                    new_map = json.loads(json.dumps(map))
                    new_map[0][0] = bo

                    options.append({'map': new_map, 'ids': [id]})
        else:
            previous_options = options
            options = []
            for p in previous_options:
                for id, t in tiles.items():
                    if id in p['ids']:
                        continue

                    for bo in t['borders_options']:
                        if check_neighbours(p['map'], x, y, bo):
                            new_map = json.loads(json.dumps(p['map']))
                            new_map[y][x] = bo
                            ids = json.loads(json.dumps(p['ids']))
                            ids.append(id)
                            options.append({'map': new_map, 'ids': ids})

ids = options[0]['ids']
print(ids)

corners = []
corners.append(ids[0])
corners.append(ids[-1])
corners.append(ids[size-1])
corners.append(ids[size*size-size])

output = 1
for c in corners:
    output *= c

print('part1: ' + str(output))
