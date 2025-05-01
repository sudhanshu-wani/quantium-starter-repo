#!/bin/bash

# Activate the virtual environment (adjust path if needed)
source venv/Scripts/activate

# Run the test suite with pytest
pytest
exit_code=$?

# Return 0 if tests passed, 1 if any test failed
if [ $exit_code -eq 0 ]; then
    echo "All tests passed."
    exit 0
else
    echo "Some tests failed."
    exit 1
fi
