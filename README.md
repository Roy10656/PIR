CKKS PIR Python Demo

A research-driven Python project demonstrating Private Information Retrieval (PIR) based on the CKKS homomorphic encryption scheme using the TenSEAL library. This client-server system allows privacy-preserving queries over a massive, chunked database—each server-client interaction is conducted securely, ensuring the query and data remain private.
Features

    CKKS PIR Protocol: Query and retrieve database entries securely without disclosing the query index to the server.

    Chunked Database Model: Database entries (up to 232232) are divided into fixed-size chunks stored as .pkl files for efficient memory usage.

    Socket Communication: Length-prefixed messaging using custom helpers for robust transmission of serialized ciphertexts.

    Modular Structure: Separate modules for database generation, socket communication, and PIR client/server orchestration.

File Overview

File	        Purpose
client_max.py	PIR client: query construction, encryption, communication, decryption, response verification
server_max.py	PIR server: query reception, homomorphic processing, response encryption
db_pkl.py	    Database creation, chunking, loading utilities
comm.py	        Socket send/receive helpers (serialize, message framing)


Getting Started

Install Python & TenSEAL:

    pip install tenseal

Database Preparation:   
Run db_pkl.py to generate database chunks (default: 232232 entries, chunk size: 8192). Chunks will be saved in db_chunks/.

    python db_pkl.py

Start the Server:

    python server_max.py

Run the Client (in a new terminal):


    python client_max.py

Usage :     
Edit desired_index in client_max.py to retrieve a specific database entry.

Ensure both client and server use consistent parameters: database total size, chunk size, port, and polynomial modulus degree.

Output on client checks decrypted value against original database for correctness.

Project Structure


    PIR/
    ├── client_max.py      # PIR client logic
    ├── server_max.py      # PIR server logic
    ├── db_pkl.py          # Database creation & chunk utils
    ├── Utils/comm.py      # Socket communication helpers
    ├── db_chunks/(.pkl)   # Generated database chunk files 

In Development

    Improved performance and scalability for databases with up to 2^32 (429,49,67,296) entries. Chunked processing enables privacy-preserving queries on very large datasets using standard hardware resources.

    Multi-client support and advanced error handling.

    Separation of demo versus production configuration.

Future Development

Efficiency Enhancements: Current database creation (for 232232 entries) requires 2–3 hours; client-server data transmission typically takes 15+ hours on an Intel i5 (12th Gen) CPU with 8GB RAM—reflecting disk-based chunking and serialization bottlenecks.

Optimized Storage Utilization: The system intentionally uses disk storage for dataset chunking/loading, minimizing RAM consumption and enabling scaling on consumer hardware.

Planned Improvements:

Parallelized chunk generation and client-server communication to reduce database generation and query response times.

Batch PIR and query hoisting techniques to accelerate ciphertext operations and minimize communication overhead.

More efficient serialization and chunk loading, possibly using memory-mapped files or advanced database formats for storage.

Support for multi-threaded encryption/decryption and response aggregation for high-throughput scenarios.

Investigating sublinear PIR schemes and preprocessing optimizations specifically tailored for disk-based chunk architecture.

Detailed benchmarks for hardware resource usage (CPU, disk, RAM) and targeted bottleneck mitigation, with an aim to reduce runtimes by an order of magnitude.


Notes

    Chunk size and poly_modulus_degree must be carefully chosen to fit hardware constraints.

    Demo parameters can be adjusted for experimentation, while production should benchmark for large-scale PIR settings.
