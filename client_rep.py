# client.py (with replication)
import socket
import hashlib

NODES = [
    ('localhost', 5000),
    ('localhost', 5001),
    ('localhost', 5002)
]

REPLICATION_FACTOR = 2

def consistent_hash(key, nodes):
    h = int(hashlib.sha1(key.encode()).hexdigest(), 16)
    idx = h % len(nodes)
    return idx

def get_replica_nodes(key, nodes, replication_factor):
    """Returns a list of nodes for this key (primary + replicas)."""
    idx = consistent_hash(key, nodes)
    replica_nodes = []
    for i in range(replication_factor):
        replica_nodes.append(nodes[(idx + i) % len(nodes)])
    return replica_nodes

def send_command(node, command):
    host, port = node
    try:
        with socket.create_connection((host, port), timeout=2) as s:
            s.sendall((command.strip() + '\n').encode())
            response = s.recv(1024).decode().strip()
            return response
    except Exception as e:
        return f"ERROR {str(e)}"
    

def get_with_failover(key, nodes, replication_factor):
    replica_nodes = get_replica_nodes(key, nodes, replication_factor)
    for node in replica_nodes:
        response = send_command(node, f"GET {key}")
        if response.startswith("VALUE"):
            print(f"[Node {node[1]}] {response}")
            return
        elif "ERROR" not in response:  # NOT_FOUND is also a valid response
            print(f"[Node {node[1]}] {response}")
            return
    print(f"GET {key} failed on all replicas.")


def main():
    print("Distributed Key-Value Store Client (with Replication)")
    print("Commands: PUT key value | GET key | DELETE key | EXIT")
    while True:
        try:
            user_input = input("> ").strip()
            if not user_input:
                continue
            if user_input.upper() == "EXIT":
                print("Exiting client.")
                break
            parts = user_input.split()
            if parts[0].upper() in ("PUT", "DELETE"):
                key = parts[1]
                replica_nodes = get_replica_nodes(key, NODES, REPLICATION_FACTOR)
                for node in replica_nodes:
                    response = send_command(node, user_input)
                    print(f"[Node {node[1]}] {response}")
            elif parts[0].upper() == "GET":
                key = parts[1]
                replica_nodes = get_replica_nodes(key, NODES, REPLICATION_FACTOR)
                for node in replica_nodes:
                    response = send_command(node, user_input)
                    if response.startswith("VALUE"):
                        print(f"[Node {node[1]}] {response}")
                        break
                    elif "ERROR" not in response:  # NOT_FOUND is also a valid response
                        print(f"[Node {node[1]}] {response}")
                        break
                else:
                    print(f"GET {key} failed on all replicas.")
            else:
                print("Invalid command.")
        except KeyboardInterrupt:
            print("\nExiting client.")
            break

if __name__ == "__main__":
    main()
