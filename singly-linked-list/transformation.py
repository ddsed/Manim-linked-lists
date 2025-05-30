from manim import *
from node_closeup_vgroup import LinkedListNodeCloseup
import random

class TransformationScene(Scene):
    def construct(self):
        # Show animation without cropping
        scale_factor = 1.5
        self.camera.frame_width = 14 * scale_factor  # Default width is 14
        self.camera.frame_height = self.camera.frame_width / 1.78  # Keep 16:9 aspect ratio
        self.camera.frame_center = ORIGIN  # Keep centered

        # Get input from user and validate it
        while True:
            node_values = input("\033[0m\nEnter node letters separated by space (e.g., A B C D, max = 5): ").split()
            if len(node_values) < 1:
                print("\033[91mInvalid input: Must provide at least 1 node.")
            elif len(node_values) > 5:
                print("\033[91mInvalid input: Maximum allowed nodes is 5.")
            else:
                break  # if valid input

        # Create nodes
        nodes = [LinkedListNodeCloseup(value) for value in node_values]
        for i, node in enumerate(nodes):
            node.move_to(RIGHT * i * 4)

        # Center the entire linked list
        linked_list_center = (nodes[0].get_left() + nodes[-1].get_right()) / 2
        shift_amount = ORIGIN - linked_list_center  # Calculate shift vector

        # Move all nodes to center
        for node in nodes:
            node.shift(shift_amount)

        # Texts for code commands
        textfuncadd = Text("add()", font_size = 36) 
        textfuncadd.next_to(nodes[0], UP, buff=0.5)
        textfuncadd.align_to(nodes[0], LEFT)
        textfuncarrow = Text("nodes[i - 1].set_next(node[i])", font_size = 36) 
        textfuncarrow.next_to(nodes[0], UP, buff=0.5)
        textfuncarrow.align_to(nodes[0], LEFT)

        # Add nodes to the scene
        for i, node in enumerate(nodes):
            self.play(FadeIn(node, run_time=0.4), FadeIn(textfuncadd, run_time=0.4))
            self.play(FadeOut(textfuncadd, run_time=0.4))
            if i > 0:
                self.play(FadeIn(nodes[i - 1].set_next(node, 0, 0), run_time=0.4), FadeIn(textfuncarrow, run_time=0.4), nodes[i-1].next_arrow.animate.shift(UP * 0.2))
                self.play(FadeOut(textfuncarrow, run_time=0.4))
        
        self.wait(1)

        animations=[]
        for node in nodes:
            animations.append(node.animate.shift(UP * 2))
            if node.next_arrow:
                animations.append(node.next_arrow.animate.shift(UP * 2))

        self.play(*animations)

        # Create memory units
        memory_units = []

        for i in range(10):
            box = Square(side_length=1.8, color=WHITE, fill_opacity=0.0)
            line = Line(box.get_top(), box.get_bottom(), color=WHITE)

            unit = VGroup(box, line)
            unit.move_to(RIGHT * i * 2)
            memory_units.append(unit)

        # Center the line on screen
        memory_line = VGroup(*memory_units).move_to(ORIGIN)
        memory_line.shift(DOWN * 3)

        # Explanation texts
        memory_text = Text("memory units", color=ORANGE, font_size=36)
        memory_text.next_to(memory_units[0], UP, buff=1.3)
        memory_text.align_to(memory_units[0], LEFT)
        memory_labels = self.create_memory_labels(memory_units)

        self.play(FadeIn(memory_line), FadeIn(memory_text), FadeIn(memory_labels))

        self.convert_to_memory_units(nodes, memory_units, memory_labels, memory_text)
    
    def create_memory_labels(self, memory_units, start_address=452):
        memory_labels = VGroup()

        current_number = start_address
        for unit in memory_units:
            # Create a memory unit number above each unit
            memory_label = Text(str(current_number), color=ORANGE, font_size=24)
            memory_label.next_to(unit, UP, buff=0.8)

            memory_labels.add(memory_label)
            current_number += 1

        return memory_labels

    def convert_to_memory_units(self, nodes, memory_units, memory_labels, memory_text):
        used_units = set()
        node_texts_in_memory = []
        node_indices = []
        node_index_to_label = {} 

        for i in range(len(nodes)):
            # Pick random memory slots
            while True:
                idx1 = random.randint(0, len(memory_units) - 1)
                if idx1 not in used_units:
                    used_units.add(idx1)
                    break

            target = memory_units[idx1].get_center() + LEFT * 0.45

            # Move the node text only (no more animations on the text after it's moved)
            node_text = nodes[i].text

            # Detach text from VGroups and animate to the memory unit positions
            node_text.generate_target()
            node_text.target.move_to(target)

            self.play(nodes[i].box.animate.set_fill(PURPLE, opacity=0.35))

            # Create an index label above the memory unit
            circle = Circle(radius=0.2, color=PURPLE, fill_opacity=1)
            index_label = Text(str(i), color=WHITE, font_size=24)
            index_label.move_to(circle.get_center())
            index_with_bg = VGroup(circle, index_label)
            index_with_bg.next_to(memory_units[idx1], UP, buff=0.2)

            
            # Move the text of node i to memory
            self.play(
                MoveToTarget(node_text),
                memory_units[idx1][0].animate.set_fill(PURPLE, opacity=0.35),
                FadeIn(index_with_bg),
                FadeOut(nodes[i].box),
                FadeOut(nodes[i].line),
                FadeOut(nodes[i].dot),
                FadeOut(nodes[i].next_arrow) if nodes[i].next_arrow else Wait(0),
            )
            node_texts_in_memory.append(node_text)
            node_indices.append(index_with_bg)
            node_index_to_label[i] = memory_labels[idx1] 
            self.wait(0.2)
        
        self.play(
            VGroup(*memory_units).animate.shift(UP * 3),
            VGroup(*node_texts_in_memory).animate.shift(UP * 3),
            VGroup(*node_indices).animate.shift(UP * 3),
            VGroup(*memory_labels).animate.shift(UP * 3),
            memory_text.animate.shift(UP * 3)
        )

        arrows = self.create_arrows(node_texts_in_memory)
        self.transform_pointers(arrows, node_index_to_label)
        
    def create_arrows(self, node_texts_in_memory):
        arrows = VGroup()

        for i in range(len(node_texts_in_memory) - 1):
            start_text = node_texts_in_memory[i].get_center() + RIGHT * 0.9 + DOWN * 0.9
            end_text = node_texts_in_memory[i + 1].get_center() + DOWN * 0.9

            # Get the x-coordinate positions of the current node and next node
            current_x = node_texts_in_memory[i].get_center()[0]
            next_x = node_texts_in_memory[i + 1].get_center()[0]

            if current_x < next_x:
                # Create an arrow
                arrow = CurvedArrow(
                    start_point=start_text, 
                    end_point=end_text,
                    angle=TAU/4,
                    tip_length=0.2
                )
            else:
                # Create an arrow
                arrow = CurvedArrow(
                    start_point=start_text, 
                    end_point=end_text,
                    angle=-TAU/4,
                    tip_length=0.2
                )
            arrows.add(arrow)

        # Optional: add a dot to the last one to indicate "end"
        end_dot = Circle(radius=0.15, color=WHITE, fill_opacity=1)
        end_dot.move_to(node_texts_in_memory[-1].get_center() + RIGHT * 0.9)
        arrows.add(end_dot)

        for i, arrow in enumerate(arrows):
            if i < 3:
                self.play(FadeIn(arrow, run_time=0.5))
                self.wait(0.1)
            else:
                self.play(FadeIn(arrow, run_time=0.2))

        return arrows
    
    def transform_pointers(self, arrows, pointer_targets):
        for i in range(len(arrows) - 1):  # Skip the last dot
            arrow = arrows[i]
            label = pointer_targets[i + 1]
            label_copy = label.copy()
            self.play(
                FadeOut(label),
                label_copy.animate.scale(1.5),
                arrow.animate.set_color(ORANGE)
            )
            circle = Circle(radius=0.2)
            circle.set_opacity(0) 
            circle.move_to(arrow.get_start())
            self.play(
                FadeIn(label),
                label_copy.animate.scale(1 / 1.5).rotate(PI / 2).move_to(circle.get_center() + UP * 0.9),
                Transform(arrow, circle)
            )
            self.wait(0.3)