import os
import sys
import time
import json
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

class SystemMonitor:
    def __init__(self, interval=60):
        self.interval = interval
        self.running = True

    def get_cpu_usage(self):
        try:
            if os.path.exists('/proc/stat'):
                with open('/proc/stat', 'r') as f:
                    lines = f.readlines()
                for line in lines:
                    if line.startswith('cpu '):
                        fields = [float(column) for column in line.strip().split()[1:]]
                        idle_time = fields[3]
                        total_time = sum(fields)
                        return {"idle": idle_time, "total": total_time}
            return {}
        except Exception as e:
            logging.error(f"Error reading CPU usage: {e}")
            return {}

    def get_memory_usage(self):
        try:
            if os.path.exists('/proc/meminfo'):
                meminfo = {}
                with open('/proc/meminfo', 'r') as f:
                    for line in f:
                        parts = line.split(':')
                        if len(parts) == 2:
                            meminfo[parts[0].strip()] = int(parts[1].split()[0])
                if 'MemTotal' in meminfo and 'MemFree' in meminfo:
                    return {
                        "total_kb": meminfo['MemTotal'],
                        "free_kb": meminfo['MemFree'],
                        "available_kb": meminfo.get('MemAvailable', meminfo['MemFree'])
                    }
            return {}
        except Exception as e:
            logging.error(f"Error reading memory usage: {e}")
            return {}

    def collect_metrics(self):
        metrics = {
            "timestamp": time.time(),
            "cpu": self.get_cpu_usage(),
            "memory": self.get_memory_usage()
        }
        return metrics

    def run(self):
        logging.info("Starting System Monitor Daemon")
        while self.running:
            try:
                metrics = self.collect_metrics()
                print(json.dumps(metrics))
                time.sleep(self.interval)
            except KeyboardInterrupt:
                logging.info("Stopping System Monitor Daemon")
                self.running = False
            except Exception as e:
                logging.error(f"Daemon error: {e}")
                time.sleep(5)

if __name__ == '__main__':
    monitor = SystemMonitor(interval=10)
    monitor.run()