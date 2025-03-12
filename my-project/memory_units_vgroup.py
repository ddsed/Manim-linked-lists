from manim import *
from memory_unit import MemoryUnit
import random

class MemoryUnitsVGroup(VGroup):
    
    def __init__(self, node_values, num_empty_units=5, node_spacing=0.15, **kwargs):
        super().__init__(**kwargs)
        
        # Create memory units with values (original input nodes)
        self.original_nodes = [MemoryUnit(value) for value in node_values]
        
        # Create empty units
        self.empty_nodes = [MemoryUnit(None) for _ in range(num_empty_units)]
        
        # Combine original nodes + empty nodes
        all_nodes = self.original_nodes + self.empty_nodes
        
        # Shuffle combined nodes for random placement
        self.shuffled_nodes = all_nodes[:]
        random.shuffle(self.shuffled_nodes)

        # Convert to VGroup for arrangement
        self.nodes = VGroup(*self.shuffled_nodes)
        self.node_spacing = node_spacing

        self.construct_memory()
        self.create_index_labels() 

    # Positions memory units in a line
    def construct_memory(self):
        self.nodes.arrange(RIGHT, buff=self.node_spacing)
        self.add(self.nodes)
        self.move_to(ORIGIN)
    
    def create_index_labels(self):
        self.index_labels = VGroup()

        for idx, node in enumerate(self.original_nodes):
            shuffled_pos = self.shuffled_nodes.index(node) # Find shuffled position

            if node.value is not None:  # Only create index labels for non-empty nodes
                circle = Circle(radius=0.2, color=PURPLE, fill_opacity=1)
                index_label = Text(str(idx), color=WHITE, font_size=24)
                index_label.move_to(circle.get_center())

                # Group them together
                index_with_bg = VGroup(circle, index_label)
                index_with_bg.next_to(self.shuffled_nodes[shuffled_pos], UP, buff=0.2)

                self.index_labels.add(index_with_bg)

        self.add(self.index_labels)