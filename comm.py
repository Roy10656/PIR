import struct

def send_msg(sock, obj_bytes):
    length = struct.pack("!I", len(obj_bytes))
    sock.sendall(length + obj_bytes)

def recvall(sock, n):
    data = b''
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data += packet
    return data

def recv_msg(sock):
    raw_len = recvall(sock, 4)
    if raw_len == None:
        return None
    msg_len = struct.unpack("!I", raw_len)[0]
    return recvall(sock, msg_len)