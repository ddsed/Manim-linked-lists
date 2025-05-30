# Tests for deletion from the class with overview of linked list representations

# Test parameters: 
# For list sizes from 3 to 30; 
# Head deletion at indices (0); 
# Tail deletion at indices (last_index); 
# Middle deletion for every position in the list of each size

# Add the project root directory to sys.path for imports to work correctly
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from unittest.mock import patch
from manim import tempconfig
from deletion_overview import OverviewScene

# Function to generate node values for a specific list size
def generate_node_values(size):
    return " ".join([chr(ord("A") + i) for i in range(size)])

# Parametrize the test so that it covers all possible linked list length
@pytest.mark.parametrize("size", range(3, 31)) # List sizes from 3 to 30

def test_overview_delete_all_positions(size):
    # Generate the node values for the current size
    node_values = generate_node_values(size)

    deletion_positions = list(range(size))
    
    # Inputs for the test
    for delete_idx in deletion_positions:
        inputs = [
            node_values,
            f"{delete_idx}",
            "Z"
        ]
    
        # Patch the input function to simulate user input during the test
        with patch("builtins.input", side_effect=inputs):
            with tempconfig({"quality": "low_quality", "disable_caching": True}):
                try:
                    # Scene for testing
                    scene = OverviewScene()
                    scene.render()
                except Exception as e:
                    pytest.fail(f"Rendering failed for size {size} with error: {e}")
