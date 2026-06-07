# sys-metric-daemon

A modular, high-performance system metrics monitoring daemon designed to run with minimal overhead. It parses standard system metrics directly from `/proc` filesystems on Unix-like environments.

## Features
- Direct `/proc` parsing to eliminate heavy external dependencies.
- Modular class structure for easy expansion.
- Outputs structured JSON metrics to standard output.