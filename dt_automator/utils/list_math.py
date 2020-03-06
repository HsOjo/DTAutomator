from typing import List


def operate(p1: List[float], p2: List[float], func):
    r = []
    for i in range(len(p1)):
        r.append(func(p1[i], p2[i]))
    return r


def add(p1, p2):
    return operate(p1, p2, func=lambda a, b: a + b)


def reduce(p1, p2):
    return operate(p1, p2, func=lambda a, b: a - b)


def multiply(p1, p2):
    return operate(p1, p2, func=lambda a, b: a * b)


def divide(p1, p2):
    return operate(p1, p2, func=lambda a, b: a / b)


def abs_(p):
    return [abs(i) for i in p]
