# Distributed Key-Value Store

A distributed, fault-tolerant key-value storage system implemented in Python with replication, persistence, and automatic failover capabilities.

## Features

### Core Functionality
- **Persistent Storage**: Write ahead logging ensures data durability across server restarts
- **Distributed Architecture**: Multi-node setup with consistent hashing for data distribution
- **Replication**: Configurable replication factor (default: 2) for high availability
- **Fault Tolerance**: Automatic failover when nodes become unavailable
- **Multi-threading**: Concurrent client connection handling

### Supported Operations
- `PUT key value` - Store a key-value pair
- `GET key` - Retrieve value for a given key
- `DELETE key` - Remove a key-value pair

## Architecture

### Components

1. **Node Server** (`node_persist.py`)
   - TCP socket based server
   - Write ahead logging to `store.log`
   - Automatic log replay on startup
   - Multi-threaded client handling

2. **Distributed Client** (`client_rep.py`)
   - Consistent hashing for node selection
   - Replication management
   - Failover mechanism
   - Interactive command-line interface

3. **Test Suite** (`test_key_value.py`)
   - Automated cluster setup
   - Fault tolerance testing
   - Node failure simulation

## Quick Start

### Prerequisites
- Python 3.x
- No external dependencies required

### Setup and Run

1. **Start the node cluster**:
   ```bash
   # Terminal 1
   python node_persist.py 5000
   
   # Terminal 2
   python node_persist.py 5001
   
   # Terminal 3
   python node_persist.py 5002
   ```

2. **Run the client**:
   ```bash
   python client_rep.py
   ```

3. **Use the interactive shell**:
   ```
   > PUT mykey myvalue
   [Node 5000] OK
   [Node 5001] OK
   
   > GET mykey
   [Node 5000] VALUE myvalue
   
   > DELETE mykey
   [Node 5000] OK
   [Node 5001] OK
   ```

### Running Tests

Execute the automated test suite:
```bash
python test_key_value.py
```

## Configuration

### Default Settings
- **Ports**: 5000, 5001, 5002
- **Replication Factor**: 2
- **Log File**: `store.log`
- **Hash Algorithm**: SHA-1 for consistent hashing

### Customization
Modify these variables in `client_rep.py` to adjust the cluster configuration:
```python
NODES = [
    ('localhost', 5000),
    ('localhost', 5001),
    ('localhost', 5002)
]
REPLICATION_FACTOR = 2
```
- Compression for log files
- Configurable consistency levels
