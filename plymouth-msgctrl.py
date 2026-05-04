#!/usr/bin/env python3

"""
Plymouth Message Controller
Version: 1.1beta
Author: NAZY-OS
License: GPL-3.0

This script sends messages to Plymouth with optional status formatting and includes a progress bar.
"""

import sys
import subprocess
import time

def plymouth_send(message, status=None):
    """
    Sends a message to Plymouth with optional status.
    """
    try:
        if status == 'warning':
            subprocess.run(['plymouth', 'update', '--status=warning'], check=True)
            subprocess.run(['plymouth', 'message', '--text={}'.format(message)], check=True)
            subprocess.run(['plymouth', 'update', '--status=normal'], check=True)
        elif status == 'failed':
            subprocess.run(['plymouth', 'update', '--status=failed'], check=True)
            subprocess.run(['plymouth', 'message', '--text={}'.format(message)], check=True)
            subprocess.run(['plymouth', 'update', '--status=normal'], check=True)
        else:
            subprocess.run(['plymouth', 'message', '--text={}'.format(message)], check=True)
    except Exception as e:
        print(f"Failed to send message to Plymouth: {e}", file=sys.stderr)

def show_progress_bar(percent):
    """
    Displays a progress bar for a specified percentage.
    """
    total_steps = 40
    steps = int(percent / 100 * total_steps)
    for step in range(total_steps + 1):
        bar = '#' * step + '-' * (total_steps - step)
        print(f'\r[{bar}] {step * 100 // total_steps}%', end='')
        time.sleep(0.1)  # Simulating progress update
    print()  # New line after completion

def show_help():
    print("Usage: {} <message> [-n | -w | -f | -p <percentage> | -h]".format(sys.argv[0]))
    print("Options:")
    print("  -n, --normal      Send a normal message.")
    print("  -w, --warning     Send a warning message.")
    print("  -f, --failed      Send a failed message.")
    print("  -p, --progress    Show a progress bar with a specified percentage (0-100).")
    print("  -h, --help        Display this help message.")

def main():
    if len(sys.argv) < 2:
        show_help()
        sys.exit(1)

    if sys.argv[1] in ['-h', '--help']:
        show_help()
        sys.exit(0)

    if len(sys.argv) >= 4 and sys.argv[1] in ['-p', '--progress']:
        try:
            percent = int(sys.argv[2])
            if 0 <= percent <= 100:
                show_progress_bar(percent)
            else:
                print("Error: Please provide a percentage between 0 and 100.")
        except ValueError:
            print("Error: Invalid percentage value. Please provide an integer between 0 and 100.")
        sys.exit(0)

    message = sys.argv[1]
    status = None

    if len(sys.argv) > 2:
        if sys.argv[2] in ['-n', '--normal']:
            status = 'normal'
        elif sys.argv[2] in ['-w', '--warning']:
            status = 'warning'
        elif sys.argv[2] in ['-f', '--failed']:
            status = 'failed'

    plymouth_send(message, status)

if __name__ == "__main__":
    main()
