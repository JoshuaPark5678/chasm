# Test for src/protocol.py

from src.protocol import MAX_PAYLOAD, Type, decode, encode

# Tests:

def test_encode_full_message():
    # arrange 
    message : bytes = b"this is a test!"
    # act 
    result = encode(message)
    # assert
    assert result == b'\x00\x00\x0fthis is a test!', f"expected b'\x00\x00\x0fthis is a test!', got {result}."

def test_decode_full_message():
    encoded : bytes = b'\x00\x00\x0fthis is a test!'
    result = decode(encoded)
    assert result == (Type.CHAT, b'this is a test!', b''), \
    f"expected (<Type.CHAT: 0>, b'this is a test!', b''), got {result}."

def test_encode_oversize_raises():
    try:
        encode(b"x" * (MAX_PAYLOAD + 1))
    except ValueError:
        return          # exactly what we promised
    assert False, "encode accepted an oversize payload"

def test_decode_incomplete_header():
    encoded : bytes = b"\x00\x00"
    result = decode(encoded)
    assert result is None, f"expected None, got {result}."

def test_decode_leftover():
    encoded : bytes = b"\x00\x00\x01ab"
    result = decode(encoded)
    assert result == (Type.CHAT, b'a', b'b'), f"expected (<Type.CHAT: 0>, b'a', b'b'), got {result}."

def test_decode_incomplete_msg():
    encoded : bytes = b"\x00\x00\x03ab"
    result = decode(encoded)
    assert result is None, f"expected None, got {result}."

def test_decode_empty_payload():
    encoded : bytes = b"\x00\x00\x00"
    result = decode(encoded)
    assert result == (Type.CHAT, b'', b''), f"expected(<Type.CHAT: 0>, b'', b''), got {result}."

def test_decode_unknown_type():
    try:
        decode(b"\x64\x00\x02ab")
    except ValueError:
        return
    assert False, "decode accepted an unknown type"

def test_decode_two_frames():
    encoded : bytes = b'\x00\x00\x11this is message 1\x00\x00\rnow message 2'
    result1 = decode(encoded)
    assert result1 == (Type.CHAT, b'this is message 1', b'\x00\x00\rnow message 2'), \
    f"expected (<Type.CHAT : 0>, b'this is message 1', b'\x00\x00\rnow message 2'), got {result1}."
    if result1 is not None:
        result2 = decode(result1[2])
        assert result2 == (Type.CHAT, b'now message 2', b''), \
        f"expected (<Type.CHAT : 0>, b'now message 2', b''), got {result2}."




