from manim import *
from memory_unit_vgroup import MemoryUnit
import random

class MemoryUnitsVGroup(VGroup):
    
    def __init__(self, node_values, node_spacing=0.15, **kwargs):
        super().__init__(**kwargs)
        
        # Create memory units with values (original input nodes)
        self.original_nodes = [MemoryUnit(value) for value in node_values]

        self.num_empty_units = max(5, 35 - len(self.original_nodes))
        
        # Create empty units
        self.empty_nodes = [MemoryUnit(None) for _ in range(self.num_empty_units)]
        
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
        self.create_memory_labels()

        # Explanation texts
        memory_text = Text("memory address", color=ORANGE, font_size=24)
        circle = Circle(radius=0.3, color=PURPLE, fill_opacity=1)
        index_text = Text("idx", color=WHITE, font_size=24)
        index_text.move_to(circle.get_center())
        index_text_bg = VGroup(circle, index_text)

        memory_text.next_to(self.shuffled_nodes[0], UP, buff=3.75)
        memory_text.align_to(self.shuffled_nodes[0], LEFT)
        index_text_bg.next_to(self.shuffled_nodes[0], UP, buff=3)
        index_text_bg.align_to(self.shuffled_nodes[0], LEFT)

        self.add(memory_text, index_text_bg)

        # Add HEAD pointer above the original node with index 0
        self.headtext = Text("HEAD", font_size=24, color=YELLOW)
        self.headtext.next_to(self.original_nodes[0], UP, buff=2)
        self.headarrow = Arrow(
            start=self.headtext.get_bottom(),
            end=self.original_nodes[0].get_top() + UP * 1.1,
            buff=0.1,
            tip_length=0.2,
            color=YELLOW
        )

        self.add(self.headtext, self.headarrow)

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

    def create_memory_labels(self):
        self.memory_labels = VGroup()

        current_number = 487
        for node in self.shuffled_nodes:
            # Create a memory unit number above each node
            memory_label = Text(str(current_number), color=ORANGE, font_size=24)
            memory_label.move_to(node.get_top() + UP * 1)
            
            # Add the label to the index_labels group
            self.memory_labels.add(memory_label)

            # Increment the number for the next label
            current_number += 1

        # Add all the index labels to the scene
        self.add(self.memory_labels)