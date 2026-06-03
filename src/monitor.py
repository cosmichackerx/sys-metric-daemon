import asyncio
import json
import os
import time

class SystemMonitor:
    def __init__(self, interval=5.0):
        self.interval = interval
        self.running = False

    async def get_cpu_usage(self):
        if os.path.exists('/proc/stat'):
            with open('/proc/stat', 'r') as f:
                lines = f.readlines()
            for line in lines:
                if line.startswith('cpu '):
                    parts = [float(x) for x in line.split()[1:]]
                    idle_time = parts[3] + parts[4]
                    total_time = sum(parts)
                    return idle_time, total_time
        return 0.0, 0.0

    async def monitor_loop(self):
        self.running = True
        prev_idle, prev_total = await self.get_cpu_usage()
        while self.running:
            await asyncio.sleep(self.interval)
            curr_idle, curr_total = await self.get_cpu_usage()
            
            diff_idle = curr_idle - prev_idle
            diff_total = curr_total - prev_total
            
            cpu_pct = 0.0
            if diff_total > 0:
                cpu_pct = (1.0 - (diff_idle / diff_total)) * 100.0
            
            mem_total, mem_free = 0, 0
            if os.path.exists('/proc/meminfo'):
                with open('/proc/meminfo', 'r') as f:
                    for line in f:
                        if 'MemTotal' in line:
                            mem_total = int(line.split()[1])
                        elif 'MemFree' in line:
                            mem_free = int(line.split()[1])
            
            mem_used_pct = 0.0
            if mem_total > 0:
                mem_used_pct = ((mem_total - mem_free) / mem_total) * 100.0

            metrics = {
                'timestamp': time.time(),
                'cpu_percent': round(cpu_pct, 2),
                'memory_percent': round(mem_used_pct, 2)
            }
            print(json.dumps(metrics))
            prev_idle, prev_total = curr_idle, curr_total

if __name__ == '__main__':
    monitor = SystemMonitor(interval=2.0)
    try:
        asyncio.run(monitor.monitor_loop())
    except KeyboardInterrupt:
        pass