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
        node_values = input("Enter node letters separated by space (e.g., A B C D, max = 29): ").split()
        last_index = len(node_values) - 1

        insert_idx1, insert_idx2 = map(int, input(
            f"Enter the two node indices where a new node should be inserted (0-based).\n"
            f"If you want to insert to the head – enter 0 0;\n"
            f"If you want to insert to the tail – enter the index of the last node (={last_index}) twice: "
        ).split())

        new_letter = input("Enter the new node letter: ")


        # Create memory line with both values and empty units
        memory_line = MemoryUnitsVGroup(node_values)

        # Show the memory units
        self.play(FadeIn(memory_line, run_time=1))
        self.wait(1)

        # Show the memory units arrows
        arrows = self.create_arrows(memory_line)
        self.wait(1)
        if insert_idx2 == 0:
            self.insert_head(memory_line, insert_idx2, new_letter, arrows)
        elif insert_idx1 == len(memory_line.original_nodes) - 1:
            self.insert_tail(memory_line, insert_idx1, new_letter, arrows)
        else:
            self.insert(memory_line, insert_idx1, insert_idx2, new_letter, arrows)

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

        return arrows

    def insert(self, nodes, idx1, idx2, new_letter, arrows):
        # Find the memory units for insertion + color code them
        node1 = nodes.original_nodes[idx1]
        node2 = nodes.original_nodes[idx2]     

        textfunc = Text(f"insert({node1.text.text}, {node2.text.text})", font_size = 36)
        textfunc.next_to(nodes[0], UP, buff=1.5)
        textfunc.align_to(nodes[0])

        self.play(
            node1.box.animate.set_fill(GREEN, opacity=0.35),
            node1.next_arrow.animate.shift(DOWN * 0.01).set_color(GREEN).set_stroke(width=10),
            node2.box.animate.set_fill(GREEN, opacity=0.35),
            nodes.index_labels[idx1][0].animate.set_fill(GREEN, opacity=1).set_stroke(GREEN),
            nodes.index_labels[idx2][0].animate.set_fill(GREEN, opacity=1).set_stroke(GREEN),
            FadeIn(textfunc)
        )

        self.play(FadeOut(textfunc), FadeOut(nodes.empty_nodes[0].text))

        # Creating new node on the place of an empty unit
        new_node = nodes.empty_nodes[0]
        new_node.value = new_letter
        new_node.text = Text(str(new_letter), font_size=24).move_to(new_node.box.get_left() + RIGHT * 0.25)

        self.play(
            new_node.box.animate.set_fill(GREEN, opacity=1),
            FadeIn(new_node.text),
            *[
            AnimationGroup(
                arrow.animate.set_stroke(opacity=0.35), 
                arrow.tip.animate.set_fill(opacity=0.35)
            )
            for arrow in arrows 
                if arrow is not new_node.next_arrow and arrow is not node1.next_arrow
            ]
        )

        # Creating an arrow to a new node
        node1_x = node1.get_center()[0]
        new_node_x = new_node.get_center()[0]

        if node1_x < new_node_x:
            arrow_to_new = CurvedArrow(
                start_point=node1.next_arrow.get_start(),
                end_point=new_node.get_bottom() + LEFT * 0.25,
                angle=TAU/4
            )
        else:
            arrow_to_new = CurvedArrow(
                start_point=node1.next_arrow.get_start(),
                end_point=new_node.get_bottom() + LEFT * 0.25,
                angle=-TAU/4
            )

        arrow_to_new.set_color(GREEN)
        arrow_to_new.set_stroke(width=10)

        # Creating an arrow from a new node
        new_node.next_arrow = new_node.set_next(node2, CurvedArrow, color=GREEN)
        new_node.next_arrow.set_stroke(width=10)

        self.play(
            Transform(node1.next_arrow, arrow_to_new), 
            FadeIn(new_node.next_arrow)
        )
    
    def insert_head(self, nodes, idx2, new_letter, arrows):
        node_head = nodes.original_nodes[idx2] 

        textfunc = Text(f"insert() to head position", font_size = 36)
        textfunc.next_to(nodes[0], UP, buff=1.5)
        textfunc.align_to(nodes[0]) 

        self.play(
            node_head.box.animate.set_fill(GREEN, opacity=0.35),
            nodes.index_labels[idx2][0].animate.set_fill(GREEN, opacity=1).set_stroke(GREEN),
            FadeIn(textfunc)
        )

        self.play(FadeOut(textfunc), FadeOut(nodes.empty_nodes[0].text))

        # Creating new node on the place of an empty unit
        new_node = nodes.empty_nodes[0]
        new_node.value = new_letter
        new_node.text = Text(str(new_letter), font_size=24).move_to(new_node.box.get_left() + RIGHT * 0.25)

        self.play(
            new_node.box.animate.set_fill(GREEN, opacity=1),
            FadeIn(new_node.text),
            *[
            AnimationGroup(
                arrow.animate.set_stroke(opacity=0.35),
                arrow.tip.animate.set_fill(opacity=0.35)
            )
            for arrow in arrows 
                if arrow is not new_node.next_arrow and arrow is not node_head.next_arrow
            ]
        )

        # Creating an arrow from a new node
        new_node.next_arrow = new_node.set_next(node_head, CurvedArrow, color=GREEN)
        new_node.next_arrow.set_stroke(width=10)
        self.play(FadeIn(new_node.next_arrow))

    def insert_tail(self, nodes, idx1, new_letter, arrows):
        # Find the memory units for insertion + color code them
        node_tail = nodes.original_nodes[idx1]  

        textfunc = Text(f"insert() to tail position", font_size = 36)
        textfunc.next_to(nodes[0], UP, buff=1.5)
        textfunc.align_to(nodes[0])

        self.play(
            node_tail.box.animate.set_fill(GREEN, opacity=0.35),
            nodes.index_labels[idx1][0].animate.set_fill(GREEN, opacity=1).set_stroke(GREEN),
            FadeIn(textfunc)
        )

        self.play(FadeOut(textfunc), FadeOut(nodes.empty_nodes[0].text))

         # Creating new node on the place of an empty unit
        new_node = nodes.empty_nodes[0]
        new_node.value = new_letter
        new_node.text = Text(str(new_letter), font_size=24).move_to(new_node.box.get_left() + RIGHT * 0.25)

        self.play(
            new_node.box.animate.set_fill(GREEN, opacity=1),
            FadeIn(new_node.text),
            *[
            AnimationGroup(
                arrow.animate.set_stroke(opacity=0.35),
                arrow.tip.animate.set_fill(opacity=0.35)
            )
            for arrow in arrows 
                if arrow is not node_tail.next_arrow
            ]
        )

        # Creating an arrow to a new node
        node_tail.next_arrow = node_tail.set_next(new_node, CurvedArrow, color=GREEN, stroke_width=10)
        self.play(FadeIn(node_tail.next_arrow))