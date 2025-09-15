import tenseal as ts
import socket
import Utils.comm as cm
from db_pkl import chunk_generator

def get_chunk_at_index(gen, index):
    for i, chunk in enumerate(gen):
        if i == index:
            return chunk
    return None  # index out of range

# Parameters must match server/db settings
n = 32
chunk_size = 16384 // 2
num_chunks = 2**n // chunk_size
desired_index = 1023  # Example target index

context = ts.context(
    ts.SCHEME_TYPE.CKKS,
    poly_modulus_degree=32768 // 2,
    coeff_mod_bit_sizes=[60, 40, 40, 60]
)
context.global_scale = 2**40
context.generate_galois_keys()

# Connect to server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('localhost', 9901))

# Send context once
cm.send_msg(s, context.serialize())
print("Client: Context sent")

responses = []

# Send query and receive response chunk-wise
for chunk_idx in range(num_chunks):
    query_chunk = [0] * chunk_size
    start_idx = chunk_idx * chunk_size
    if start_idx <= desired_index < start_idx + chunk_size:
        query_chunk[desired_index - start_idx] = 1

    query_enc_chunk = ts.ckks_vector(context, query_chunk)
    print(f"Client: Sending chunk {chunk_idx + 1}/{num_chunks}")
    cm.send_msg(s, query_enc_chunk.serialize())

    response_bytes = cm.recv_msg(s)
    if response_bytes is None:
        print(f"Client: No response for chunk {chunk_idx + 1}")
        break

    response_enc = ts.ckks_vector_from(context, response_bytes)
    decrypted_val = round(response_enc.decrypt()[0])
    responses.append(decrypted_val)
    print(f"Client: Received response {chunk_idx + 1}")

s.close()

# Find non-zero result
result = next((val for val in responses if val != 0), None)

database_chunks = chunk_generator()

if result is not None:
    chunk_idx = desired_index // chunk_size
    offset = desired_index % chunk_size
    chunk = get_chunk_at_index(database_chunks, chunk_idx)
    if chunk is None:
        print("Error: chunk index out of range")
    elif result == chunk[offset]:
        print("Success! Retrieved value matches database.")
    else:
        print("Error! Value mismatch.")

    print("Decrypted response:", result)
