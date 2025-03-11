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


class MemoryLineScene(Scene):
    def construct(self):
        # Show animation without cropping
        scale_factor = 1.5
        self.camera.frame_width = 14 * scale_factor  # Default width is 14
        self.camera.frame_height = self.camera.frame_width / 1.78  # Keep 16:9 aspect ratio
        self.camera.frame_center = ORIGIN  # Keep centered

        # Get input from user
        node_values = input("Enter distinctive node letters separated by space (e.g., A B C D, min = 5): ").split()

        # Create memory line with both values and empty units
        memory_line = MemoryUnitsVGroup(node_values)

        # Show the memory units
        self.play(FadeIn(memory_line, run_time=2))
        self.wait(1)

        # Show the memory units arrows
        self.create_arrows(memory_line)

    def create_arrows(self, memory_line):
        arrows = VGroup()

        # Create arrows between the nodes using set_next() for only non-empty nodes
        for i in range(len(memory_line.original_nodes) - 1):
            start_node = memory_line.original_nodes[i]   # Get node in original order
            next_node = memory_line.original_nodes[i + 1] # Next node in original order

            if start_node.value is not None and next_node.value is not None:
                # Set the next arrow
                arrow = start_node.set_next(next_node, arrow_type=CurvedArrow, color=WHITE)
                arrows.add(arrow)

        # Animate the arrows appearing one by one
        for i, arrow in enumerate(arrows):
            self.play(FadeIn(arrow, run_time=0.5))
            self.wait(0.5)
