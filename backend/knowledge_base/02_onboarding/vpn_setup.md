# VPN Configuration Guide

## Overview
All remote access to Nexus AI Innovations's internal network **requires** an
active VPN connection. We use **WireGuard** as our VPN solution.

## Prerequisites
* Your `@nexusai.dev` credentials (provided by IT on Day 1).
* WireGuard client installed on your machine.

## Installation
```bash
# macOS
brew install wireguard-tools

# Ubuntu/Debian
sudo apt install wireguard

# Windows
# Download from https://www.wireguard.com/install/
```

## Configuration Steps
1. Request your configuration file from IT via `#it-support` on Slack.
2. Save the `.conf` file to a secure location:
   ```bash
   mkdir -p ~/.config/wireguard
   mv ~/Downloads/nexus-vpn.conf ~/.config/wireguard/
   ```
3. Import the configuration:
   ```bash
   sudo wg-quick up ~/.config/wireguard/nexus-vpn.conf
   ```
4. Verify the connection:
   ```bash
   curl -s https://internal.nexusai.dev/health
   # Expected: {"status": "ok", "network": "internal"}
   ```

## Troubleshooting
| Issue                          | Solution                          |
|--------------------------------|-----------------------------------|
| Handshake timeout              | Check firewall rules (port 51820) |
| DNS resolution failure         | Set DNS to `10.0.0.1`             |
| Connection drops after 5 min   | Update WireGuard to latest        |

## Security Notice
* **Never** share your VPN configuration file.
* Report lost/compromised configs to IT immediately.
* VPN sessions are logged for audit purposes.

---
*IT Operations — Nexus AI Innovations*
