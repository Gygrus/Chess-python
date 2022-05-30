from backend.Vector import Vector


def to_column(x):
    return {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7, }[x]


def to_row(x):
    return {'8': 0, '7': 1, '6': 2, '5': 3, '4': 4, '3': 5, '2': 6, '1': 7, }[x]


def from_column(x):
    return {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h', }[x]


def from_row(x):
    return {0: 8, 1: 7, 2: 6, 3: 5, 4: 4, 5: 3, 6: 2, 7: 1, }[x]


def string_to_vector(string):
    return Vector(to_row(string[1]), to_column(string[0]))
