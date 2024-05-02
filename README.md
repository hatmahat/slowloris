# Slowloris Simulation Script

This Python script simulates a Slowloris attack, a type of Denial of Service (DoS) attack where the attacker opens multiple connections to the web server and sends partial requests, which are never completed. The server keeps these connections open, which can exhaust its resources, potentially making the server unavailable to other legitimate users.

## Description

The script sets up multiple socket connections to a target server and sends HTTP headers in a slow manner to keep the connections open as long as possible without completing the HTTP request. This type of attack aims to test the resilience of servers to handle connections that are intentionally kept open.

## Features

- **HTTP Method Flexibility**: Supports specifying the HTTP method (e.g., GET, POST) for requests.
- **Custom Header Support**: Allows for custom headers to be included in the requests.
- **Connection Simulation**: Opens multiple connections and tries to maintain them by sending partial headers intermittently.

## Requirements

- Python 3.x
- Modules: `socket`, `time`, `argparse`, `shlex`, `urllib`

## Usage

To use the script, you need to pass a simulated `curl` command as an argument. The script parses this command to extract the URL, headers, and HTTP method if specified.

### Command-Line Syntax

```bash
python3 slowloris.py [-m METHOD] "curl COMMAND"
```

### Examples
```bash
python3 slowloris.py "curl --location 'http://localhost:9000/v1/test' --header 'X-App-Id: x-app'"
```
```bash
python3 slowloris.py -m POST "curl --location 'http://localhost:9000/v1/test' --header 'X-App-Id: x-app'"
```