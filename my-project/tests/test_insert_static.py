# Tests for insertion into static chain representation of linked list

# Test parameters: 
# For list sizes from 2 to 29; 
# Head insertion at indices (0, 0); 
# Tail insertion at indices (last_index, last_index); 
# Middle insertion for every pair of adjacent indices in the list of each size

# Add the project root directory to sys.path for imports to work correctly
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from unittest.mock import patch
from manim import tempconfig
from insertion_static import LinkedListStaticScene

# Function to generate node values for a specific list size
def generate_node_values(size):
    return " ".join([chr(ord("A") + i) for i in range(size)])

# Parametrize the test so that it covers all possible linked list length
@pytest.mark.parametrize("size", range(2, 30)) # List sizes from 2 to 29

def test_linked_list_static_insert_all_positions(size):
    # Generate the node values for the current size
    node_values = generate_node_values(size)

    insertion_positions = [
        (0, 0), # Head insertion (0, 0)
        (size - 1, size - 1), # Tail insertion (last_index, last_index)
    ] + [(i, i + 1) for i in range(size - 1)] # Middle insertions for all adjacent pairs
    
    # Inputs for the test
    for insert_idx1, insert_idx2 in insertion_positions:
        inputs = [
            node_values,
            f"{insert_idx1} {insert_idx2}",
            "Z"
        ]
    
        # Patch the input function to simulate user input during the test
        with patch("builtins.input", side_effect=inputs):
            with tempconfig({"quality": "low_quality", "disable_caching": True}):
                # Scene for testing
                scene = LinkedListStaticScene()
                scene.render()
