from random import random


def pinGen():
    pin = int(random() * 10000)
    while pin < 1000:
        pin = int(random() * 10000)
    return pin