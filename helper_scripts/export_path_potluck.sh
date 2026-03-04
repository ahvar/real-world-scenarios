#!/bin/bash

# run this script to set PYTHONPATH of the python interpreter in your virtual environment

# Get the helper script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# cd from the 'helper_scripts' dir one level up to get the project root
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Construct PYTHONPATH dynamically based on the project root
# Only including directories that actually exist in your project
export PYTHONPATH="$PROJECT_ROOT:$PROJECT_ROOT/potluck:$PROJECT_ROOT/potluck/cs:$PROJECT_ROOT/potluck/utils:"
echo "PYTHONPATH set to: $PYTHONPATH"
echo ""
echo "Available custom modules:"
echo "  - potluck.cs (CodeSignal Potluck application)"
echo "  - potluck.utils (Potluck utils)"
