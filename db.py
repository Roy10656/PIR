import random

n = 14
database = [0]*(2**n)


def create_database(database):
    random.seed(42)

    for i in range(2**n):
        database[i] = i * random.randint(1, 100)
    return database
