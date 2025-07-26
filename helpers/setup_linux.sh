#!/bin/bash

# Get the absolute path to the bot directory
BOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_DIR="$BOT_DIR/venv"

# Create systemd service file
cat << EOF | sudo tee /etc/systemd/system/jamtime.service
[Unit]
Description=Jamtime Discord Bot
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$BOT_DIR
Environment="PATH=$VENV_DIR/bin:$PATH"
ExecStart=$VENV_DIR/bin/python bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd daemon
sudo systemctl daemon-reload

# Enable and start the service
sudo systemctl enable jamtime
sudo systemctl start jamtime

echo "Jamtime bot has been installed as a systemd service"
echo "To check status: systemctl status jamtime"
echo "To view logs: journalctl -u jamtime"