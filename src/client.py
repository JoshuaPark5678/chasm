# Chasm EE2E Chat Client

import argparse
import asyncio
from pathlib import Path

from protocol import Type, encode, split_frames


# Get the directory where this script is saved
BASE_DIR = Path(__file__).resolve().parent

async def receive(reader: asyncio.StreamReader): 
    buffer : bytes = b''
    while True: 
        incoming = await reader.read(1024)
        
        if not incoming:
            break

        buffer += incoming
        
        frames, buffer = split_frames(buffer)

        for frame in frames:
            try:
                match frame[0]:
                    case Type.CHAT:
                        print(f"Message: {frame[1].decode('utf-8')}")
                    case Type.IDENT:
                        print(f"{frame[1].decode('utf-8')} Joined")
                
            except UnicodeDecodeError:
                print(f"Failed to decode, binary: {frame[1]}")

async def transmit(writer: asyncio.StreamWriter, name: bytes):
    writer.write(encode(name, Type.IDENT))
    await writer.drain()

    while True:
        message : str = await asyncio.to_thread(input)
        try:
            payload : bytes  = message.encode('utf-8')
            
            writer.write(encode(payload, Type.CHAT))
            await writer.drain()

        except UnicodeEncodeError:
            print(f"Failed to encode: {message}")

async def client(host: str, port: int, name: bytes):
    reader, writer = await asyncio.open_connection(host, port)
    
    try:
        async with asyncio.TaskGroup() as tg:
            tg.create_task(receive(reader))
            
            await transmit(writer, name)
    finally:
        # Always close the connection cleanly
        writer.close()
        await writer.wait_closed()
        
def main():
    # Initialize the parser
    parser = argparse.ArgumentParser()
    
    # Define arguments and flags
    parser.add_argument(
        "--name", 
        type=str, 
        default="Anon", 
        help="The name of the person to greet."
    )
    parser.add_argument(
        "--relay",
        type=str,
        default="127.0.0.1",
        help="The relay address."
    )
    parser.add_argument(
        "--port",
        type=int,
        default=5928,
        help="The relay port"
    )
    
    #  Parse and use the arguments
    args = parser.parse_args()
    with open(BASE_DIR / "assets" / "chasm.txt", "r", encoding="utf-8") as file:
        logo = file.read()
        print(logo)

    try:
        name = args.name.encode('utf-8')
        asyncio.run(client(host=args.relay, port=args.port, name=name))
    except UnicodeEncodeError:
        print(f"\nError while encoding username: {args.name}")
    except EOFError:
        print("\nClient stopped.")
    except KeyboardInterrupt:
        print("\nClient stopped.")

if __name__ == "__main__":
    main()



