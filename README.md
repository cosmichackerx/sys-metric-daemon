# sys-metric-daemon

An asynchronous, dependency-free system resource monitoring daemon designed for lightweight profiling in performance-constrained environments.

## Features
- Asynchronous event loop (`asyncio`)
- No third-party library dependencies (reads `/proc` on Linux)
- Outputs structured JSON log data for easy log aggregation