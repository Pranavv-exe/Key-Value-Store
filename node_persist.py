import socket
import threading
import os

LOG_FILE = 'store.log'

def append_to_log(entry):
    with open(LOG_FILE, 'a') as f:
        f.write(entry + '\n')

def replay_log():
    data_store = {}
    if not os.path.exists(LOG_FILE):
        return data_store
    with open(LOG_FILE, 'r') as f:
        for line in f:
            parts = line.strip().split(' ', 2)
            if not parts:
                continue
            cmd = parts[0]
            if cmd == 'PUT' and len(parts) == 3:
                key, value = parts[1], parts[2]
                data_store[key] = value
            elif cmd == 'DELETE' and len(parts) == 2:
                key = parts[1]
                if key in data_store:
                    del data_store[key]
    return data_store

# In-memory key-value store
data_store = replay_log()

def handle_client(conn, addr):
    """
    Accepts commands: PUT key value, GET key, DELETE key
    """
    with conn:
        while True:
            try:
                data = conn.recv(1024)
                if not data:
                    break
                command = data.decode().strip()
                response = process_command(command)
                conn.sendall((response + '\n').encode())
            except Exception as e:
                conn.sendall(f"ERROR {str(e)}\n".encode())
                break

def process_command(command):
    parts = command.split()
    if not parts:
        return "ERROR Empty command"
    cmd = parts[0].upper()
    if cmd == "PUT" and len(parts) == 3:
        key, value = parts[1], parts[2]
        append_to_log(f"PUT {key} {value}")
        data_store[key] = value
        return "OK"
    elif cmd == "GET" and len(parts) == 2:
        key = parts[1]
        if key in data_store:
            return f"VALUE {data_store[key]}"
        else:
            return "NOT_FOUND"
    elif cmd == "DELETE" and len(parts) == 2:
        key = parts[1]
        append_to_log(f"DELETE {key}")
        if key in data_store:
            del data_store[key]
            return "OK"
        else:
            return "NOT_FOUND"
    else:
        return "ERROR Invalid command"

def start_server(port):
    """
    Starts the key-value store node on the specified port.
    """
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', port))
    server.listen()
    print(f"Node started on port {port}. Waiting for connections...")
    try:
        while True:
            conn, addr = server.accept()
            threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()
    except KeyboardInterrupt:
        print("\nShutting down node.")
    finally:
        server.close()

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python node.py <port>")
        sys.exit(1)
    port = int(sys.argv[1])
    start_server(port)
