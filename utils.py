import subprocess
import platform
import time

def ping_host(host, timeout=5):
	system = platform.system().lower()
	if system == "windows":
		cmd = ["ping","-n","1","-w", str(timeout*100),host]
	else:
		cmd = ["ping", "-c", "1", "-W", str(timeout), host]
	start = time.time()
	try:
		result = subprocess.run(
		cmd,
		stdout = subprocess.DEVNULL,
		stderr = subprocess.DEVNULL,
		timeout = timeout + 2
		)
		latency = round((time.time() - start) * 1000, 2)
		is_alive = result.returncode == 0
		return is_alive, latency if is_alive else None
	except subprocess.TimeoutExpired:
		return False, None
import csv
import os
from datetime import datetime

def log_result(host, label, is_alive, latency, log_file):
    """Appends a single ping result row to the CSV log."""
    status = "UP" if is_alive else "DOWN"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lat_str = f"{latency} ms" if latency else "N/A"

    # Write header if file is new
    write_header = not os.path.exists(log_file)

    with open(log_file, "a", newline="") as f:
        writer = csv.writer(f)
        if write_header:
            writer.writerow(["timestamp", "host", "label",
                              "status", "latency_ms"])
        writer.writerow([timestamp, host, label, status, lat_str])

    print(f"[{timestamp}]  {label:<20} {host:<18} {status}  {lat_str}")
