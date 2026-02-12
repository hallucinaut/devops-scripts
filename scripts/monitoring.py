#!/usr/bin/env python3
"""
Monitoring and Logging Script
Collects system metrics and logs
"""

import argparse
import json
import logging
import os
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import re


class SystemMonitor:
    """System resource monitor"""
    
    def __init__(self, output_dir: str = 'logs'):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.logger = self._setup_logger()
    
    def _setup_logger(self) -> logging.Logger:
        """Set up logger"""
        logger = logging.getLogger('monitoring')
        logger.setLevel(logging.INFO)
        
        # File handler
        file_handler = logging.FileHandler(
            self.output_dir / f'monitoring_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
        )
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        ))
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter(
            '%(levelname)s: %(message)s'
        ))
        
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        return logger
    
    def get_cpu_usage(self) -> Dict[str, float]:
        """Get CPU usage information"""
        try:
            result = subprocess.run(
                ['top', '-bn1', '-d', '1'],
                capture_output=True, text=True, check=True
            )
            
            # Parse CPU usage
            lines = result.stdout.split('\n')
            for line in lines:
                if line.startswith('%Cpu(s)'):
                    parts = re.findall(r'(\d+\.?\d*)', line)
                    if len(parts) >= 8:
                        return {
                            'user': float(parts[0]),
                            'nice': float(parts[1]),
                            'system': float(parts[2]),
                            'idle': float(parts[3]),
                            'iowait': float(parts[4]),
                            'irq': float(parts[5]),
                            'softirq': float(parts[6]),
                            'steal': float(parts[7]) if len(parts) > 7 else 0.0
                        }
        except subprocess.CalledProcessError:
            pass
        
        return {'error': 'Could not get CPU usage'}
    
    def get_memory_usage(self) -> Dict[str, any]:
        """Get memory usage information"""
        try:
            result = subprocess.run(
                ['free', '-m'],
                capture_output=True, text=True, check=True
            )
            
            lines = result.stdout.split('\n')
            if len(lines) >= 3:
                parts = lines[1].split()
                if len(parts) >= 7:
                    return {
                        'total_mb': int(parts[1]),
                        'used_mb': int(parts[2]),
                        'free_mb': int(parts[3]),
                        'shared_mb': int(parts[4]),
                        'buffers_mb': int(parts[5]),
                        'cache_mb': int(parts[6]),
                        'available_mb': int(parts[7]) if len(parts) > 7 else 0
                    }
        except subprocess.CalledProcessError:
            pass
        
        return {'error': 'Could not get memory usage'}
    
    def get_disk_usage(self) -> Dict[str, any]:
        """Get disk usage information"""
        try:
            result = subprocess.run(
                ['df', '-h'],
                capture_output=True, text=True, check=True
            )
            
            lines = result.stdout.split('\n')
            filesystems = []
            
            for line in lines[1:]:  # Skip header
                parts = line.split()
                if len(parts) >= 6:
                    filesystems.append({
                        'device': parts[0],
                        'size': parts[1],
                        'used': parts[2],
                        'available': parts[3],
                        'use_percent': parts[4],
                        'mountpoint': parts[5]
                    })
            
            return {'filesystems': filesystems}
        except subprocess.CalledProcessError:
            pass
        
        return {'error': 'Could not get disk usage'}
    
    def get_network_stats(self) -> Dict[str, any]:
        """Get network statistics"""
        try:
            result = subprocess.run(
                ['ip', 'addr'],
                capture_output=True, text=True, check=True
            )
            
            interfaces = {}
            
            for line in result.stdout.split('\n'):
                if line.startswith('2:'):
                    parts = line.split()
                    if len(parts) >= 2:
                        interface_name = parts[1]
                        interfaces[interface_name] = {
                            'address': parts[3].split('/')[0] if len(parts) > 3 else 'N/A',
                            'state': parts[4] if len(parts) > 4 else 'N/A'
                        }
            
            return {'interfaces': interfaces}
        except subprocess.CalledProcessError:
            pass
        
        return {'error': 'Could not get network stats'}
    
    def get_process_info(self, limit: int = 10) -> List[Dict[str, any]]:
        """Get top processes"""
        try:
            result = subprocess.run(
                ['ps', 'aux', '--sort=-pcpu'],
                capture_output=True, text=True, check=True
            )
            
            processes = []
            lines = result.stdout.split('\n')[1:limit+1]
            
            for line in lines:
                parts = line.split()
                if len(parts) >= 11:
                    processes.append({
                        'user': parts[0],
                        'pid': int(parts[1]),
                        'cpu_percent': float(parts[2]),
                        'mem_percent': float(parts[3]),
                        'vsz_kb': int(parts[4]),
                        'rss_kb': int(parts[5]),
                        'tty': parts[6],
                        'stat': parts[7],
                        'start': parts[8],
                        'time': parts[9],
                        'command': ' '.join(parts[10:])
                    })
            
            return processes
        except subprocess.CalledProcessError:
            return []
    
    def get_logs(self, log_path: str, tail: int = 100) -> str:
        """Read log file"""
        try:
            result = subprocess.run(
                ['tail', '-n', str(tail), log_path],
                capture_output=True, text=True, check=True
            )
            return result.stdout
        except subprocess.CalledProcessError:
            return f"Error: Could not read log file {log_path}"
    
    def get_container_logs(self, container_name: str, tail: int = 100) -> str:
        """Get logs from Docker container"""
        try:
            result = subprocess.run(
                ['docker', 'logs', '--tail', str(tail), container_name],
                capture_output=True, text=True, check=True
            )
            return result.stdout
        except subprocess.CalledProcessError:
            return f"Error: Could not get logs for container {container_name}"
    
    def save_metrics(self, metrics: Dict[str, any], filename: str = None):
        """Save metrics to file"""
        timestamp = datetime.now().isoformat()
        metrics_with_time = {
            'timestamp': timestamp,
            **metrics
        }
        
        if filename is None:
            filename = f'metrics_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        
        filepath = self.output_dir / filename
        
        with open(filepath, 'w') as f:
            json.dump(metrics_with_time, f, indent=2)
        
        print(f"✓ Metrics saved to: {filepath}")
        self.logger.info(f"Metrics saved: {filepath}")
    
    def monitor_loop(self, interval: int = 5, duration: Optional[int] = None):
        """Continuous monitoring loop"""
        self.logger.info(f"Starting monitoring (interval: {interval}s)")
        
        iterations = 0
        while True:
            print(f"\n--- Monitoring Cycle {iterations + 1} ---")
            
            metrics = {
                'cpu': self.get_cpu_usage(),
                'memory': self.get_memory_usage(),
                'disk': self.get_disk_usage(),
                'network': self.get_network_stats(),
                'top_processes': self.get_process_info()
            }
            
            self.save_metrics(metrics)
            self.logger.info("Metrics collected")
            
            iterations += 1
            if duration and iterations * interval >= duration:
                break
            
            time.sleep(interval)
        
        self.logger.info("Monitoring completed")


def main():
    parser = argparse.ArgumentParser(description='System Monitoring Script')
    parser.add_argument('--output', default='logs', help='Output directory')
    parser.add_argument('--log', type=str, help='System log file path')
    parser.add_argument('--container', type=str, help='Docker container name')
    parser.add_argument('--interval', type=int, default=5, help='Monitoring interval (seconds)')
    parser.add_argument('--duration', type=int, help='Monitoring duration (seconds)')
    parser.add_argument('--monitor', action='store_true', help='Start continuous monitoring')
    parser.add_argument('--save', action='store_true', help='Save metrics to file')
    
    args = parser.parse_args()
    
    monitor = SystemMonitor(args.output)
    
    if args.monitor:
        monitor.monitor_loop(args.interval, args.duration)
    else:
        metrics = {
            'cpu': monitor.get_cpu_usage(),
            'memory': monitor.get_memory_usage(),
            'disk': monitor.get_disk_usage(),
            'network': monitor.get_network_stats(),
            'top_processes': monitor.get_process_info()
        }
        
        if args.log:
            logs = monitor.get_logs(args.log)
            print(logs)
        
        if args.container:
            logs = monitor.get_container_logs(args.container)
            print(logs)
        
        if args.save:
            monitor.save_metrics(metrics)


if __name__ == '__main__':
    main()
