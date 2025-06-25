# Distributed Key-Value Store

A distributed, fault-tolerant key-value storage system implemented in Python with replication, persistence, and automatic failover capabilities.

## Features

### Core Functionality
- **Persistent Storage**: Write ahead logging ensures data durability across server restarts[1]
- **Distributed Architecture**: Multi-node setup with consistent hashing for data distribution[2]
- **Replication**: Configurable replication factor (default: 2) for high availability[2]
- **Fault Tolerance**: Automatic failover when nodes become unavailable[2]
- **Multi-threading**: Concurrent client connection handling[1]

### Supported Operations
- `PUT key value` - Store a key-value pair
- `GET key` - Retrieve value for a given key
- `DELETE key` - Remove a key-value pair

## Architecture

### Components

1. **Node Server** (`node_persist.py`)[1]
   - TCP socket based server
   - Write ahead logging to `store.log`
   - Automatic log replay on startup
   - Multi-threaded client handling

2. **Distributed Client** (`client_rep.py`)[2]
   - Consistent hashing for node selection
   - Replication management
   - Failover mechanism
   - Interactive command-line interface

3. **Test Suite** (`test_key_value.py`)[3]
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
- **Ports**: 5000, 5001, 5002[2]
- **Replication Factor**: 2[2]
- **Log File**: `store.log`[1]
- **Hash Algorithm**: SHA-1 for consistent hashing[2]

### Customization
Modify these variables in `client_rep.py` to adjust the cluster configuration[2]:
```python
NODES = [
    ('localhost', 5000),
    ('localhost', 5001),
    ('localhost', 5002)
]
REPLICATION_FACTOR = 2
```

## Technical Details

### Persistence Mechanism
The system uses write ahead logging where all operations are logged to `store.log` before being applied to the in memory store[1]. On startup, nodes replay the log to restore their state.

### Consistent Hashing
Keys are distributed across nodes using SHA-1 hashing, ensuring even distribution and allowing for easy scaling[2].

### Replication Strategy
Each key is replicated to multiple nodes based on the replication factor. The client automatically selects replica nodes using consistent hashing[2].

### Fault Tolerance
When a node fails, the client automatically tries replica nodes until it finds an available one, ensuring high availability[2].

## File Structure

```
project/
├── node_persist.py      # Main node server implementation
├── client_rep.py        # Distributed client with replication
├── test_key_value.py    # Automated test suite
└── store.log           # Persistent storage log file
```

## Error Handling

The system handles various error conditions:
- Node failures during operations
- Network timeouts
- Invalid commands
- Key not found scenarios

## Future Enhancements

Potential improvements for this key-value store:
- Data partitioning across nodes
- Leader election for write coordination
- REST API interface
- Monitoring and metrics
- Compression for log files
- Configurable consistency levels
