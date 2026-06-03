import unittest
import sys
from src.collector import SystemMetricsCollector

class TestSystemMetricsCollector(unittest.TestCase):
    def setUp(self):
        self.collector = SystemMetricsCollector()

    def test_cpu_usage_type(self):
        cpu = self.collector.get_cpu_usage()
        self.assertIsInstance(cpu, float)

    def test_memory_usage_structure(self):
        mem = self.collector.get_memory_usage()
        self.assertIn('total_mb', mem)
        self.assertIn('available_mb', mem)
        self.assertIn('percent_used', mem)

    def test_disk_usage_structure(self):
        disk = self.collector.get_disk_usage('/')
        self.assertIn('total_gb', disk)
        self.assertIn('used_gb', disk)
        self.assertIn('percent_used', disk)

    def test_collect_all_keys(self):
        data = self.collector.collect_all()
        self.assertIn('timestamp', data)
        self.assertIn('cpu_percent', data)
        self.assertIn('memory', data)
        self.assertIn('disk', data)

if __name__ == '__main__':
    unittest.main()