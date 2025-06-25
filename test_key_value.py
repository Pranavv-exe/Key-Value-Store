import subprocess
import time

def start_node(port):
    return subprocess.Popen(['python', 'node.py', str(port)])

def stop_node(proc):
    proc.terminate()
    proc.wait()

# Start nodes
node1 = start_node(5000)
node2 = start_node(5001)
node3 = start_node(5002)
time.sleep(1)  # Give nodes time to start

# Run tests using your client functions
assert put('foo', 'bar') == 'OK'
assert get('foo') == 'VALUE bar'

# Simulate node failure
stop_node(node1)
assert get('foo') == 'VALUE bar'  # Should still work via replica

# Clean up
stop_node(node2)
stop_node(node3)
