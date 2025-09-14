CKKS PIR Python Demo

A research-driven Python project demonstrating Private Information Retrieval (PIR) using the CKKS homomorphic encryption scheme via the TenSEAL library. This client-server system enables privacy-preserving queries over large, chunked databases.
Features

    CKKS-based PIR: Secure query and retrieval without revealing query contents.

Chunked Database Model: Splits large databases (220220 entries) into manageable memory chunks.

Socket Communication: Length-prefixed messaging for robust data transfer.

Modular Structure: Separate modules for database, communication, client, and server logic.
File Overview
File	Purpose
client_20.py	Client: generates query, encrypts, sends, decrypts
server_20.py	Server: receives query, processes, returns result
db_20.py	Database: initializes and chunks database
comm.py	Communication: socket send/receive helpers
Getting Started

    Install Python & TenSEAL

bash
pip install tenseal

Start Server

bash
python server_20.py

Run Client (new terminal)

    bash
    python client_20.py

Usage

    Change the desired_index in client_20.py to retrieve different entries from the database.

    Both server and client must use the same chunk size/database size configuration for correct operation.

    Output confirms decryption and checks correctness against the database entry.

Project Structure

PIR
.
├── client_20.py   # PIR client logic
├── server_20.py   # PIR server logic
├── db_20.py       # Database creation & chunking
└── comm.py        # Socket utilities

In Development

    Performance optimizations for larger database sizes and parallel queries.

    Distinction between demo and production settings.

    Improved error handling and support for multi-client queries.
