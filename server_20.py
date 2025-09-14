import tenseal as ts
import socket
import db_20
import comm as cm

database_chunks = db_20.create_database_chunks()

# create server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 9991))
server_socket.listen(1)
print("Server listening on port 9991...")

# recieve client connection
conn, addr = server_socket.accept()
print(f"Connected by {addr}")

# 
context_bytes = cm.recv_msg(conn)
context = ts.context_from(context_bytes)
print("Context received")

num_chunks = len(database_chunks)



for i in range(num_chunks):
    query_bytes = cm.recv_msg(conn)
    query_enc = ts.ckks_vector_from(context, query_bytes)
    
    db_chunk_vector = ts.ckks_vector(context, database_chunks[i])
    response_enc = query_enc * db_chunk_vector
    dot_enc = response_enc.sum()
    
    cm.send_msg(conn, dot_enc.serialize())
    print(f"Response sent for chunk {i+1}/{num_chunks}")

conn.close()
server_socket.close()
