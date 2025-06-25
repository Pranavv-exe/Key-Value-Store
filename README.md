# Distributed Key-Value Store

## Overview

This project implements a **distributed key-value store** in Python, designed to demonstrate core distributed systems concepts such as partitioning, replication, and fault tolerance. The system supports multiple storage nodes running on different ports, uses consistent hashing for data distribution, and implements replication for high availability and durability. All networking is handled via a custom TCP protocol for efficiency and learning value.

---

## Features

- **Consistent Hashing:** Evenly distributes keys across nodes and allows seamless scaling.
- **Replication:** Each key is stored on multiple nodes (configurable replication factor) for fault tolerance.
- **Custom TCP Protocol:** Lightweight, non-HTTP communication between client and nodes.
- **Simple CLI Client:** Routes commands to the correct nodes using consistent hashing.
- **Easy Local Deployment:** All nodes and client can be run on a single laptop (macOS, Linux, or Windows).

---

## Architecture

```
+---------+           +---------------------+
|  Client | <-------> |  Node 1 (Port 5000) |
|         | <-------> |  Node 2 (Port 5001) |
|         | <-------> |  Node 3 (Port 5002) |
+---------+           +---------------------+
```

- **Client:** Accepts user commands, uses consistent hashing to pick nodes, and sends commands over TCP.
- **Nodes:** Each node is a separate process, stores a subset of the keyspace, and handles replication.

---

## How It Works

- **PUT/DELETE:** The client sends the command to both the primary and replica node(s) for the key.
- **GET:** The client queries the primary node for the key.
- **Replication:** If a primary node fails, data can still be retrieved from the replica.

---

## Getting Started

### **1. Clone the Repository**
```bash
git clone <your-repo-url>
cd distributed_kv_store
```

### **2. Start Node Servers**
Open three terminals and run:
```bash
python node.py 5000
python node.py 5001
python node.py 5002
```

### **3. Start the Client**
Open a fourth terminal:
```bash
python client.py
```

### **4. Example Commands**
```
PUT foo bar
GET foo
DELETE foo
GET foo
EXIT
```

---

## Design Decisions

- **Consistent Hashing:** Chosen for its scalability and even load distribution. Adding/removing nodes requires minimal data movement.
- **Replication:** Configurable for fault tolerance. The client handles replication logic for simplicity.
- **Custom Protocol:** Using TCP sockets keeps dependencies minimal and helps understand networking fundamentals.
- **Extensibility:** The system is designed to be easily extended (e.g., add persistence, web dashboard, or advanced failure handling).

---

## Possible Extensions

- **Node Failure Handling:** Detect and recover from node crashes automatically.
- **Persistence:** Store data on disk for durability across restarts.
- **Web Dashboard:** Visualize node status and key distribution.
- **Dynamic Membership:** Add or remove nodes without downtime.
- **Stronger Consistency:** Implement quorum-based reads/writes.

---

## Testing & Verification

- **Replication:** After a `PUT`, data is present on two nodes. If the primary node is stopped, the replica still serves the data.
- **Consistency:** After a `DELETE`, `GET` returns `NOT_FOUND` from all replicas.
- **Logs:** Each node logs incoming commands for transparency.
