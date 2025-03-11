from manim import *
from memory_unit import MemoryUnit
import random

class MemoryUnitsVGroup(VGroup):
    
    def __init__(self, node_values, node_spacing=0.15, **kwargs):
        super().__init__(**kwargs)
        
        # Create memory units without shuffling yet
        self.original_nodes = [MemoryUnit(value) for value in node_values]
        
        # Create a shuffled copy of nodes for display
        self.shuffled_nodes = self.original_nodes[:]  # Copy list
        random.shuffle(self.shuffled_nodes)  # Shuffle their positions

        # Convert to VGroup for arrangement
        self.nodes = VGroup(*self.shuffled_nodes)
        self.node_spacing = node_spacing

        self.construct_memory()
        self.center_list()
        self.create_index_labels() 

    # Positions memory units in a line
    def construct_memory(self):
        self.nodes.arrange(RIGHT, buff=self.node_spacing)
        self.add(self.nodes)

    # Centers the entire memory structure on the screen
    def center_list(self):
        self.move_to(ORIGIN)
    
    def create_index_labels(self):
        self.index_labels = VGroup()

        for idx, node in enumerate(self.original_nodes):
            shuffled_pos = self.shuffled_nodes.index(node)  # Find shuffled position

            # Create a circle for background
            circle = Circle(radius=0.2, color=PURPLE, fill_opacity=1)

            # Create index text (white)
            index_label = Text(str(idx), color=WHITE, font_size=24)

            # Position text in the center of the circle
            index_label.move_to(circle.get_center())

            # Group them together
            index_with_bg = VGroup(circle, index_label)
            index_with_bg.next_to(self.shuffled_nodes[shuffled_pos], UP, buff=0.2)  # Position above node

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

        memory_line = MemoryUnitsVGroup(node_values)

        self.play(FadeIn(memory_line, run_time=2))
        self.wait(1)

        self.create_arrows(memory_line)

    def create_arrows(self, memory_line):
            arrows = VGroup()

            # Create arrows between the nodes using set_next() method
            for i in range(len(memory_line.original_nodes) - 1):
                start_node = memory_line.original_nodes[i]   # Get node in original order
                next_node = memory_line.original_nodes[i + 1] # Next node in original order

                # Set the next arrow
                arrow = start_node.set_next(next_node, arrow_type=CurvedArrow, color=WHITE)

                # Add the arrow to the group of arrows
                arrows.add(arrow)

            # Animate the arrows appearing one by one
            for i, arrow in enumerate(arrows):
                self.play(FadeIn(arrow, run_time=0.5))
                self.wait(0.5) 