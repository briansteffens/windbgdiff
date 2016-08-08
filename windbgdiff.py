#!/usr/bin/env python3

import sys
import re
import shutil


if len(sys.argv) != 3:
    print("Usage: python3 windbgdiff file1 file2")
    sys.exit(1)


class Instruction(object):

    def __init__(self):
        self.offset = 0
        self.code = None

    def to_string(self, max_len=None):
        ret = '{}  {}'.format(hex(self.offset), self.code)

        if max_len:
            ret = ret[:max_len]

        return ret


def load(fn):
    with open(fn) as f:
        lines = f.readlines()

    instructions = []
    instruction = None

    for line in lines:
        line = line.strip()

        if re.match('^[0-9a-f]{8} ', line):
            if instruction:
                instructions.append(instruction)

            instruction = Instruction()

            parts = [p for p in line.split(' ') if p]
            instruction.offset = int(parts[0], 16)
            instruction.code = ' '.join(parts[2:])

    if instruction:
        instructions.append(instruction)

    return instructions


def how_far(insts, index, target_offset):
    for i in range(0, len(insts) - index):
        if insts[index + i].offset == target_offset:
            return i

    return None


def next_join(left, li, right, ri):
    for i in range(li, len(left)):
        dist = how_far(right, ri, left[i].offset)

        if dist is not None:
            return dist

    return None


left = load(sys.argv[1])
right = load(sys.argv[2])

width = int(shutil.get_terminal_size((80, 20)).columns / 2 - 1)
empty_str = ''.join(' ' for i in range(width))

li = 0
ri = 0

differences = None

while True:
    lefti = None
    righti = None

    show_left = False
    show_right = False

    if li < len(left):
        lefti = left[li]
        show_left = True

    if ri < len(right):
        righti = right[ri]
        show_right = True

    if not lefti and not righti:
        break

    # Are there left and right instructions?
    if lefti and righti:

        # Instructions match
        if lefti.offset == righti.offset:
            default_direction = None

        # Instructions don't match
        else:
            if not differences:
                left_join = next_join(right, ri, left, li)
                right_join = next_join(left, li, right, ri)

                differences = [
                    {
                        'direction': 'left',
                        'remaining': left_join
                    },
                    {
                        'direction': 'right',
                        'remaining': right_join
                    }
                ]

                if right_join < left_join:
                    differences.reverse()

                if differences[0]['remaining'] == 0:
                    del differences[0]

            if differences[0]['direction'] == 'left':
                show_right = False
            else:
                show_left = False

            differences[0]['remaining'] -= 1

            if differences[0]['remaining'] <= 0:
                del differences[0]
                if not len(differences):
                    differences = None

    left_str = empty_str
    right_str = empty_str

    if show_left:
        left_str = lefti.to_string(max_len=width)

    if show_right:
        right_str = righti.to_string(max_len=width)

    while len(left_str) < width:
        left_str += ' '

    print("{} {}".format(left_str, right_str))

    if show_left:
        li += 1

    if show_right:
        ri += 1
