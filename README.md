# KV Database Server

A simple in-memory key-value database implemented in Python with no third-party dependencies.

It supports only string keys and string values of arbitrary length.

## Usage

1. Start the server: `python main.py`. It'll listen at `127.0.0.1:4000`.
2. Set value: `curl http://localhost:4000/set?somekey=somevalue`
3. Get value: `curl http://localhost:4000/get?key=somekey`
