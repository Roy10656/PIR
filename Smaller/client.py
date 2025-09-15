import tenseal as ts
import socket
import Smaller.db as db
import Utils.comm as cm

# load database
database = db.create_database(db.database)

n = 14
database_size = 2**n
desired_index = 1023  # some index

# create TenSEAL context and encrypt query
context = ts.context(
    ts.SCHEME_TYPE.CKKS,
    poly_modulus_degree=32768,
    coeff_mod_bit_sizes=[60, 40, 40, 60]
)

context.global_scale = 2**40
context.generate_galois_keys()

# create query vector
query_vector = [0] * database_size
query_vector[desired_index] = 1
query_enc = ts.ckks_vector(context, query_vector)

# connect to server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(120.0)   # <-- set socket timeout (120s for large data)
s.connect(('localhost', 9990))
print("Connected to server")

# send context and query
cm.send_msg(s, context.serialize())
cm.send_msg(s, query_enc.serialize())
print("Query sent")

# receive and decrypt response
response_enc = cm.recv_msg(s)
response = ts.ckks_vector_from(context, response_enc)

decrypted_val = round(response.decrypt()[0])
print("Decrypted response:", decrypted_val)


print("Actual value:", database[desired_index])
if decrypted_val == database[desired_index]:
    print("Success: Retrieved correct value.")
else:
    print("Error: Incorrect value.")

s.close()
