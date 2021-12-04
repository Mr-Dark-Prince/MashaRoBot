from random import choice


async def random_line(fname):
    with open(fname) as f:
        data = f.read().splitlines()
    return choice(data)
