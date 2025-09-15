import tenseal as ts
import socket
import Utils.comm as cm
from db_pkl import chunk_generator

# Create server socket etc. as before

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 9901))
server_socket.listen(1)
print("Server listening on port 9901...")

conn, addr = server_socket.accept()
print(f"Connected by {addr}")

context_bytes = cm.recv_msg(conn)
context = ts.context_from(context_bytes)
print("Context received")

# Use your chunk generator to load chunks one by one from disk
db_chunk_iter = chunk_generator()

for i, db_chunk in enumerate(db_chunk_iter):
    query_bytes = cm.recv_msg(conn)
    query_enc = ts.ckks_vector_from(context, query_bytes)

    db_chunk_vector = ts.ckks_vector(context, db_chunk)
    response_enc = query_enc * db_chunk_vector

    dot_enc = response_enc.sum()

    cm.send_msg(conn, dot_enc.serialize())
    print(f"Response sent for chunk {i+1}")

conn.close()
server_socket.close()
