import tenseal as ts
import socket
import db
import comm as cm

database = db.create_database(db.database)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.settimeout(120.0)   # <-- set timeout here too
server_socket.bind(('localhost', 9990))
server_socket.listen(1)
print("Server listening on port 9990...")

conn, addr = server_socket.accept()
print(f"Connected by {addr}")
conn.settimeout(120.0)   # <-- client connection timeout

# Receive context
context_bytes = cm.recv_msg(conn)
context = ts.context_from(context_bytes)
print("Context received")

# Receive query
query_bytes = cm.recv_msg(conn)
query = ts.ckks_vector_from(context, query_bytes)
print("Query received")

# PIR computation
db_vector = ts.plain_tensor(database)
response_enc = query * db_vector
dot_enc = response_enc.sum()

# Send result
cm.send_msg(conn, dot_enc.serialize())
print("Response sent")

conn.close()
server_socket.close()
