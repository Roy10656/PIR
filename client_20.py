import tenseal as ts
import socket
import db_20
import comm as cm

database = db_20.create_database_chunks()

n = 25
chunk_size = 16384 // 2
num_chunks = 2**n // chunk_size  # Equals 128 for n=20, chunk_size=8192


desired_index = 1023  # your target index

context = ts.context(
    ts.SCHEME_TYPE.CKKS,
    poly_modulus_degree=32768 // 2,
    coeff_mod_bit_sizes=[60, 40, 40, 60]
)
context.global_scale = 2**40
context.generate_galois_keys()

# Create query chunks
query_chunks = []
for chunk_idx in range(num_chunks):
    query_chunk = [0] * chunk_size
    start_idx = chunk_idx * chunk_size
    if start_idx <= desired_index and desired_index < start_idx + chunk_size:
        query_chunk[desired_index - start_idx] = 1
    query_chunks.append(query_chunk)

query_enc_chunks = [ts.ckks_vector(context, chunk) for chunk in query_chunks]

# Connect and send context once
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('localhost', 9991))
cm.send_msg(s, context.serialize())
print("Client: Context sent")

# Receive and decrypt responses
responses = []
for idx, enc_chunk in enumerate(query_enc_chunks):
    print(f"Client: Sending chunk {idx+1}/{num_chunks}")
    cm.send_msg(s, enc_chunk.serialize())

    print(f"Client: Waiting for response {idx+1}/{num_chunks}")
    response_bytes = cm.recv_msg(s)
    if response_bytes is None:
        print(f"Client: No response received for chunk {idx+1}")
        break
    response_enc = ts.ckks_vector_from(context, response_bytes)
    decrypted_val = round(response_enc.decrypt()[0])
    responses.append(decrypted_val)
    print(f"Client: Received response {idx+1}")


# result = sum(responses)

s.close()

# Find non-zero result
result = next(val for val in responses if val != 0)
chunk_idx = desired_index // chunk_size
offset = desired_index % chunk_size

print("\n")
if result == database[chunk_idx][offset]:
    print("Success! Retrieved value matches database.")
else:
    print("Error! Retrieved value does not match database.")
print("\n")

print("Decrypted response:", result)
