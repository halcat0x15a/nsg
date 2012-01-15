def contains(bounds, pos):
    return pos[1] > bounds[1] and \
        pos[1] < bounds[1] + bounds[3] and \
        pos[0] < bounds[0] + bounds[2] and \
        pos[0] > bounds[0]
