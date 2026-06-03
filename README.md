# sys-metric-daemon

A high-performance, ultra-lightweight performance collection daemon engineered to consume minimal resources. Gathers OS-level execution metrics straight from `/proc` interfaces on Linux environments.

## Features

- Zero-dependency framework (pure Python standard library execution).
- Highly modular subsystem directory separation.
- Instant low-level system parsing metrics.

## Usage

Run the metrics collector natively:

```bash
python3 src/collector.py
```

## Configuration

Modify parameter keys located directly inside `config/config.json`.