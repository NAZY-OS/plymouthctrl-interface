#!/bin/bash

# Plymouth Message Controller
# Version: 1.01beta
# Author: NAZY-OS
# License: GPL-3.0
#
# This script sends messages to Plymouth with optional status formatting and includes a progress bar.

PLYMOUTH_SCRIPT="/bin/plymouth-msgctrl.py"

plymouth_send() {
    local message="$1"
    local status="$2"
    
    if [ "$status" == "warning" ]; then
        /bin/plymouth update --status="warning"
        python3 "$PLYMOUTH_SCRIPT" "$message" -w
        /bin/plymouth update --status="normal"
    elif [ "$status" == "failed" ]; then
        /bin/plymouth update --status="failed"
        python3 "$PLYMOUTH_SCRIPT" "$message" -f
        /bin/plymouth update --status="normal"
    else
        python3 "$PLYMOUTH_SCRIPT" "$message"
    fi
}

show_progress_bar() {
    local percent="$1"
    local total_steps=40
    local steps=$((percent * total_steps / 100))
    for ((step=0; step<=total_steps; step++)); do
        bar=$(printf "%0.s#" $(seq 1 $step))
        bar+=$(printf "%0.s-" $(seq 1 $((total_steps - step))))
        printf "\r[%s] %d%%" "$bar" "$((step * 100 / total_steps))"
        sleep 0.1  # Simulating progress update
    done
    echo # New line after completion
}

show_help() {
    echo "Usage: $0 <message> [-n | -w | -f | -p <percentage> | -h]"
    echo "Options:"
    echo "  -n, --normal      Send a normal message."
    echo "  -w, --warning     Send a warning message."
    echo "  -f, --failed      Send a failed message."
    echo "  -p, --progress    Show a progress bar with a specified percentage (0-100)."
    echo "  -h, --help        Display this help message."
}

if [ "$#" -lt 1 ]; then
    show_help
    exit 1
fi

if [[ "$1" == "-h" || "$1" == "--help" ]]; then
    show_help
    exit 0
fi

if [[ "$1" == "-p" || "$1" == "--progress" ]]; then
    percent="$2"
    
    if ! [[ "$percent" =~ ^[0-9]{1,3}$ ]] || [ "$percent" -lt 0 ] || [ "$percent" -gt 100 ]; then
        echo "Error: Please provide a percentage between 0 and 100."
        exit 1
    fi

    show_progress_bar "$percent"
    exit 0
fi

message="$1"
status="normal"

if [ "$#" -gt 1 ]; then
    case "$2" in
        -n) status="normal";;
        --normal) status="normal";;
        -w) status="warning";;
        --warning) status="warning";;
        -f) status="failed";;
        --failed) status="failed";;
    esac
fi

plymouth_send "$message" "$status"
