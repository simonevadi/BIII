#!/bin/bash

# Determine the directory where the script is located
SCRIPT_DIR=$(dirname "$(readlink -f "$0")")

# Change directory to where the scripts are located
cd "$SCRIPT_DIR"

source /home/simone/miniconda3/etc/profile.d/conda.sh
# conda init
# conda activate rp

# Loop to run the tasks every 15 minutes
while true; do
    # Start the block in the background
    (
        # Check and kill any running simulation Python processes
        pid=$(pgrep -f 'simulation_*.py' | grep -v $$ | grep -v $PPID)
        if [ ! -z "$pid" ]; then
            echo "Killing previous simulation Python processes with PID $pid"
            kill $pid
        fi

        # Check and kill any running instances of rayui.sh
        rayui_pids=$(pgrep -f rayui.sh)
        if [ ! -z "$rayui_pids" ]; then
            echo "Killing running rayui.sh processes with PIDs $rayui_pids"
            kill $rayui_pids
        fi

        # Run Python scripts that match the pattern
        for py_file in $(find . -maxdepth 1 -name '*simulation*.py' | sort -f)
        do
            echo "Running $py_file"
            python "$py_file"
        done
    ) &

    # Sleep for 15 minutes
    sleep 1800
done
