import psutil
import logging
from typing import Dict
from butler import briefing

def report_status() -> None:
    """
    Gather system statistics and print a health report.
    """
    logging.info("🔎 Gathering system vitals...")

    # 1. CPU Usage
    # interval=1 means "measure for 1 second" to get an accurate average
    cpu_percent = psutil.cpu_percent(interval=1)

    # 2. Memory (RAM) Usage
    memory = psutil.virtual_memory()
    total_mem_gb = _bytes_to_gb(memory.total)
    used_mem_gb = _bytes_to_gb(memory.used)
    mem_percent = memory.percent

    # 3. Disk Usage
    disk = psutil.disk_usage('/')
    total_disk_gb = _bytes_to_gb(disk.total)
    free_disk_gb = _bytes_to_gb(disk.free)
    disk_percent = disk.percent

    # 4. The Output (The Dashboard)
    print("\n📊 --- SYSTEM HEALTH REPORT --- 📊")

    # CPU
    _print_bar("CPU Usage", cpu_percent)

    # Memory
    print(f"Memory:     {used_mem_gb:.2f} GB / {total_mem_gb:.2f} GB ({mem_percent}%)")
    _print_bar("RAM Usage", mem_percent)

    # Disk
    print(f"Disk (Main): {free_disk_gb:.2f} GB Free / {total_disk_gb:.2f} GB Total")
    _print_bar("Disk Usage", disk_percent)
    print("--------------------------------")

def _bytes_to_gb(bytes_value: int) -> float:
    """Helper to convert raw bytes to GB."""
    return bytes_value / (1024 ** 3)

def _print_bar(label: str, percent: float, width: int = 20) -> None:
    """
    Draws a simple ASCII progress bar.
    Example: CPU Usage [#####.......] 45.0%
    """
    # Calculate how many hashes (#) to draw based on percentage
    filled_length = int(width * percent // 100)
    bar = '█' * filled_length + '-' * (width - filled_length)

    # Determine color (conceptually) - generic print for now
    print(f"{label:<12} [{bar}] {percent}%")
