# Chasm EE2E Chat Relay Server

import asyncio
from datetime import datetime

from protocol import Type, decode, encode, split_frames

# Global peer dictionary:
clients = {}

async def client_handler(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    addr = writer.get_extra_info("peername")
    clients[addr] = writer
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
            
            frames, buffer = split_frames(buffer)
            
            # Send messages to peers
            for frame in frames:
                peers = clients.copy()
                peers.pop(addr, None)

                if not peers:
                    print(f"dropped CHAT from {addr}: no peer")
                else:
                    for k, w in peers.items():
                        try:
                            w.write(encode(payload = frame[1], msg_type = frame[0]))
                            await w.drain()
                        except OSError:
                            print(f"peer {k} gone")
                            clients.pop(k, None) 
                            

                    # Log (payload visible)
                    print(f"{addr} -> {peers.keys()} : {frame[0].name} : {frame[1]} : {datetime.now().isoformat()}")   

    except ConnectionResetError:
        print(f"Connection reset by {addr}")
    except ValueError as e:
        print(f"protocol violation from {addr}: {e}") 
    finally:
        print(f"Closing connection: {addr}")
        clients.pop(addr, None)
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

