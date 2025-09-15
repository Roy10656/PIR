import random
import pickle
import os

n = 32
total_size = 2**n          # Total database size (very large)
chunk_size = 8192           # Fixed chunk size matching ciphertext capacity
folder = 'db_chunks'
os.makedirs(folder, exist_ok=True)

def generate_and_save_chunks():
    random.seed(42)
    num_chunks = total_size // chunk_size
    for chunk_idx in range(num_chunks):
        chunk = []
        start = chunk_idx * chunk_size
        end = start + chunk_size
        for i in range(start, end):
            chunk.append(i * random.randint(1, 100))
        filename = os.path.join(folder, f"chunk_{chunk_idx}.pkl")
        with open(filename, 'wb') as f:
            pickle.dump(chunk, f, protocol=pickle.HIGHEST_PROTOCOL)
        print(f"Saved chunk {chunk_idx}")

def load_chunk(chunk_idx):
    filename = os.path.join(folder, f"chunk_{chunk_idx}.pkl")
    with open(filename, 'rb') as f:
        chunk = pickle.load(f)
    return chunk

def chunk_generator(folder='db_chunks'):
    chunk_files = sorted(os.listdir(folder))
    for filename in chunk_files:
        with open(os.path.join(folder, filename), 'rb') as f:
            yield pickle.load(f)


if __name__ == "__main__":
    generate_and_save_chunks()

    # Example: load and print first 5 elements of chunk 0
    first_chunk = load_chunk(0)
    print("First 5 elements of chunk 0:", first_chunk[:5])
