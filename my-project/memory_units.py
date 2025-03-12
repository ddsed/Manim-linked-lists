from manim import *
from memory_units_vgroup import MemoryUnitsVGroup

class MemoryLineScene(Scene):
    def construct(self):
        # Show animation without cropping
        scale_factor = 3
        self.camera.frame_width = 14 * scale_factor  # Default width is 14
        self.camera.frame_height = self.camera.frame_width / 1.78  # Keep 16:9 aspect ratio
        self.camera.frame_center = ORIGIN  # Keep centered

        # Get input from user
        node_values = input("Enter distinctive node letters separated by space (e.g., A B C D, min = 5): ").split()

        # Create memory line with both values and empty units
        memory_line = MemoryUnitsVGroup(node_values)

        # Show the memory units
        self.play(FadeIn(memory_line, run_time=1))
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
                arrow = start_node.set_next(next_node, CurvedArrow, color=WHITE)
                arrows.add(arrow)

        for i, arrow in enumerate(arrows):
        # Slower speed for the first 5 arrows
            if i < 5:
                self.play(FadeIn(arrow, run_time=0.5))
                self.wait(0.1)
            else:
                # Faster speed for the rest of the arrows
                self.play(FadeIn(arrow, run_time=0.2))