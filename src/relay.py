# Chasm EE2E Chat Relay Server

import asyncio
from datetime import datetime

from protocol import Type, decode, encode

async def client_handler(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    addr = writer.get_extra_info("peername")
    print(f"Connected: {addr}")
    
    buffer : bytes = b''
    try:
        while True: 
            # Read up to 1024 bytes from the client
            incoming = await reader.read(1024)
            
            if not incoming:
                # log buffer
                if len(buffer) != 0: 
                    print(f"truncated buffer frame from {addr} : {buffer}")
                break

            buffer += incoming

            while len(buffer) > 0:
                message = decode(buffer)
                if message is not None:
                    # Log (payload visible)
                    print(f"{addr} : {message[0].name} : {message[1]} : {datetime.now().isoformat()}")
                    writer.write(encode(payload = message[1], msg_type = message[0]))
                    await writer.drain()
                    buffer = message[2]
                else:
                    break

    except ConnectionResetError:
        print(f"Connection reset by {addr}")
    except ValueError as e:
        print(f"protocol violation from {addr}: {e}") 
    finally:
        print(f"Closing connection: {addr}")
        writer.close()
        await writer.wait_closed()

async def main():
    host = "127.0.0.1"
    port = 5928
    print(f"Starting Server on {host}:{port}")
    server = await asyncio.start_server(client_handler, host, port)

    # Keep the server running indefinitely
    async with server:
        await server.serve_forever()
    
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nServer stopped.")

