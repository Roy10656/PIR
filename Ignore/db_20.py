import random

n = 25
chunk_size = 16384 // 2

database = [0] * (2**n)

def create_database_chunks():
    random.seed(42)
    for i in range(len(database)):
        database[i] = i * random.randint(1, 100)

    # Create chunks after filling the database
    chunks = []
    for i in range(0, len(database), chunk_size):
        chunk = database[i:i + chunk_size]
        chunks.append(chunk)

    
    return chunks