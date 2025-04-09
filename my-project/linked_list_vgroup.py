from manim import *
from node_basic import LinkedListNodeBasic

class LinkedListVGroup(VGroup):
    
    def __init__(self, node_values, node_spacing=2, row_spacing=3, **kwargs):
        super().__init__(**kwargs)

        self.nodes = [LinkedListNodeBasic(value, row=i // 10, col=i % 10) for i, value in enumerate(node_values)]
        self.node_spacing = node_spacing
        self.row_spacing = row_spacing
        
        self.construct_list()

    # Positions the nodes in a structured grid layout
    def construct_list(self):
        for i, node in enumerate(self.nodes):
            row = i // 10
            col = i % 10

            if row % 2 == 0:  # Even row (left to right)
                x_pos = RIGHT * col * self.node_spacing
            else:  # Odd row (right to left)
                x_pos = RIGHT * (9 - col) * self.node_spacing

            y_pos = DOWN * row * self.row_spacing
            node.move_to(x_pos + y_pos)
            self.add(node)

        self.center_list()
            # Now that nodes are positioned, create the HEAD label and arrow
        self.headtext = Text("HEAD", font_size=26, color=YELLOW)
        self.headtext.next_to(self.nodes[0], UP, buff=1).align_to(self.nodes[0], LEFT)

        self.headarrow = Arrow(
            start=self.headtext.get_bottom(),
            end=self.nodes[0].get_top(),
            buff=0.1,
            tip_length=0.2,
            color=YELLOW
        )
        self.add(self.headarrow, self.headtext)
    # Centers the entire linked list structure on the screen.
    def center_list(self):
        if not self.nodes:
            return
        
        leftmost = min(node.get_left()[0] for node in self.nodes)
        rightmost = max(node.get_right()[0] for node in self.nodes)
        topmost = max(node.get_top()[1] for node in self.nodes)
        bottommost = min(node.get_bottom()[1] for node in self.nodes)

        structure_center = np.array([(leftmost + rightmost) / 2, (topmost + bottommost) / 2, 0])
        shift_amount = ORIGIN - structure_center

        for node in self.nodes:
            node.shift(shift_amount)