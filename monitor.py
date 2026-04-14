# monitor.py
import time
import config
from utils import ping_host, log_result
from alerter import send_alert

def load_hosts(filepath):
    """Load hosts from file. Format: IP/hostname   label"""
    hosts = []
    with open(filepath) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                parts = line.split(None, 1)
                ip = parts[0]
                label = parts[1] if len(parts) > 1 else ip
                hosts.append((ip, label))
    return hosts

def run_monitor():
    hosts = load_hosts(config.HOSTS_FILE)
    prev_status = {ip: True for ip, _ in hosts}  # assume all UP at start

    print(f"Starting monitor — tracking {len(hosts)} hosts")
    print(f"Ping interval: {config.PING_INTERVAL}s | Log: {config.LOG_FILE}")
    print("-" * 55)

    while True:
        for host, label in hosts:
            is_alive, latency = ping_host(host, config.PING_TIMEOUT)
            log_result(host, label, is_alive, latency, config.LOG_FILE)

            # Alert on status change
            if not is_alive and prev_status[host]:
                send_alert(host, label, "DOWN")
            elif is_alive and not prev_status[host]:
                send_alert(host, label, "RECOVERED")

            prev_status[host] = is_alive

        time.sleep(config.PING_INTERVAL)

if __name__ == "__main__":
    run_monitor()
