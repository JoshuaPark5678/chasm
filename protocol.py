# Chatting Protocols
# The Layout:
# [Msg Type 1 Byte] [Msg Length 2 Bytes] [Msg remaining Bytes]

from enum import IntEnum

MAX_PAYLOAD = 65535

class Type(IntEnum):
    CHAT = 0
    IDENT = 1
    HS = 2
    HSR = 3
    ENCRYPTED = 4
    ACK = 5
    PING = 6
    COVER = 7
    DISCONNECT = 8


def encode(payload: bytes, msg_type: Type = Type.CHAT) -> bytes:
    b_data = msg_type.to_bytes(1, "big")
    if (len(payload) > MAX_PAYLOAD):
        raise ValueError(f"payload too big: {len(payload)} > {MAX_PAYLOAD}")
    msg_length = len(payload).to_bytes(2, byteorder="big")
    b_data += msg_length
    b_data += payload
    return b_data

def decode(b_data: bytes) -> list(Type | bytes):
    if len(b_data) < 3:
        return None
    msg_type = int.from_bytes(b_data[:1], byteorder='big')
    msg_length = int.from_bytes(b_data[1:3], byteorder='big') 
    
    if (msg_length > len(b_data[3:])):
        return None

    payload = b_data[3:msg_length + 3]
    leftover = b_data[msg_length + 3:]
    return [Type(msg_type), payload, leftover]

if __name__ == "__main__":
    # quick self-check while developing
    print(decode(encode(b"hello", Type.CHAT)))
