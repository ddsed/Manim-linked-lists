# Tests for transformation a chain representation of linked list into memory model representation

# Test parameters: 
# For list sizes from 1 to 5; 

# Add the project root directory to sys.path for imports to work correctly
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from unittest.mock import patch
from manim import tempconfig
from transformation import TransformationScene

# Function to generate node values for a specific list size
def generate_node_values(size):
    return " ".join([chr(ord("A") + i) for i in range(size)])

# Parametrize the test so that it covers all possible linked list length
@pytest.mark.parametrize("size", range(1, 6)) # List sizes from 1 to 5

def test_linked_list_static_insert_all_positions(size):
    # Generate the node values for the current size
    node_values = generate_node_values(size)

    # Simulate inputs
    inputs = [node_values]
    
    with patch("builtins.input", side_effect=inputs):
        with tempconfig({"quality": "low_quality", "disable_caching": True}):
            try:
                scene = TransformationScene()
                scene.render()
            except Exception as e:
                pytest.fail(f"Rendering failed for size {size} with error: {e}")
