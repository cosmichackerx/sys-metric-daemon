import os
import sys
import json
import time
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

class SystemMetricsCollector:
    def __init__(self):
        self.is_linux = sys.platform.startswith('linux')

    def get_cpu_usage(self) -> float:
        if not self.is_linux:
            return 0.0
        try:
            with open('/proc/stat', 'r') as f:
                line = f.readline()
            parts = line.split()
            if len(parts) < 5:
                return 0.0
            vals = [float(x) for x in parts[1:5]]
            idle = vals[3]
            total = sum(vals)
            return round((1.0 - (idle / total)) * 100.0, 2)
        except Exception as e:
            logging.error(f'Failed to read CPU metrics: {e}')
            return 0.0

    def get_memory_usage(self) -> dict:
        metrics = {'total_mb': 0.0, 'available_mb': 0.0, 'percent_used': 0.0}
        if not self.is_linux:
            return metrics
        try:
            meminfo = {}
            with open('/proc/meminfo', 'r') as f:
                for line in f:
                    parts = line.split(':')
                    if len(parts) == 2:
                        meminfo[parts[0].strip()] = int(parts[1].replace('kB', '').strip())
            total = meminfo.get('MemTotal', 0) / 1024.0
            free = meminfo.get('MemFree', 0) / 1024.0
            buffers = meminfo.get('Buffers', 0) / 1024.0
            cached = meminfo.get('Cached', 0) / 1024.0
            available = free + buffers + cached
            used = total - available
            percent = (used / total) * 100.0 if total > 0 else 0.0
            metrics['total_mb'] = round(total, 2)
            metrics['available_mb'] = round(available, 2)
            metrics['percent_used'] = round(percent, 2)
        except Exception as e:
            logging.error(f'Failed to read Memory metrics: {e}')
        return metrics

    def get_disk_usage(self, path: str = '/') -> dict:
        metrics = {'total_gb': 0.0, 'used_gb': 0.0, 'percent_used': 0.0}
        try:
            stat = os.statvfs(path)
            total = (stat.f_blocks * stat.f_frsize) / (1024**3)
            free = (stat.f_bfree * stat.f_frsize) / (1024**3)
            used = total - free
            percent = (used / total) * 100.0 if total > 0 else 0.0
            metrics['total_gb'] = round(total, 2)
            metrics['used_gb'] = round(used, 2)
            metrics['percent_used'] = round(percent, 2)
        except Exception as e:
            logging.error(f'Failed to read Disk metrics: {e}')
        return metrics

    def collect_all(self) -> dict:
        return {
            'timestamp': int(time.time()),
            'cpu_percent': self.get_cpu_usage(),
            'memory': self.get_memory_usage(),
            'disk': self.get_disk_usage()
        }

if __name__ == '__main__':
    collector = SystemMetricsCollector()
    print(json.dumps(collector.collect_all(), indent=2))