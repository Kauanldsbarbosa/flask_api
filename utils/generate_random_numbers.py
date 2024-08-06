from random import Random
from string import digits


def generate_random_numbers(size=4):
    list = []
    numbers = [int(digito) for digito in digits]
    for number in range(size):
        index_aleatorio = Random().choice(numbers)
        list.append(index_aleatorio)

    return ''.join(str(digito) for digito in list)
