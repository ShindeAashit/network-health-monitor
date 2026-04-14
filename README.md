# Network Health Monitor

A Python tool that monitors network host availability,
logs uptime metrics, and sends email alerts on outages.

## Features
- Multi-host ping monitoring with configurable interval
- CSV uptime logging with timestamps
- Email alerts with cooldown (anti-spam)
- Status change detection (UP/DOWN/RECOVERED)
- Cross-platform (Linux, Windows, macOS)

## How to run
```
git clone <your-repo>
cd network-health-monitor
python monitor.py
```
