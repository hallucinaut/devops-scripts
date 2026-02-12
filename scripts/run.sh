#!/bin/bash
# Quick start script for DevOps scripts

echo "DevOps Python Scripts - Quick Start"
echo "====================================="
echo ""

# Make script executable
chmod +x scripts/run.sh

# Show available commands
echo "Available scripts:"
ls -1 scripts/*.py | sed 's/scripts\///' | sed 's/\.py$//' | sed 's/_/ /g' | awk '{printf "  - %-20s %s\n", $1, $2}'
echo ""

# Example usage
echo "Example: Run a specific script"
echo "  python scripts/docker_manager.py --help"
echo ""
echo "For more information, see README.md"
