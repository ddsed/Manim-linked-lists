from manim import *
from memory_unit import MemoryUnit
import random

# the close up look => from 2 to 4 initial nodes 
class LinkedListNodeCloseup(VGroup):
    def __init__(self, value, **kwargs):
        super().__init__(**kwargs)
        self.box = Square(side_length=2, color=WHITE)
        self.line = Line(self.box.get_left(), self.box.get_right(), color=WHITE)
        self.text = Text(value, font_size=34).move_to(self.box.get_top() - [0, 0.5, 0])
        self.dot = Circle().scale(0.2)
        self.dot.set_fill(WHITE, opacity=1)
        self.dot.move_to(self.box.get_bottom() + [0 , 0.5, 0])
        self.dot.set_stroke(width=0) 
        self.add(self.box, self.text, self.line, self.dot)
        self.next_arrow = None

    def set_next(self, next_node):
        if self.next_arrow:
            self.remove(self.next_arrow)
        self.next_arrow = Arrow(self.get_bottom() + [0, 0.5, 0], next_node.get_left() + [0, 0.5, 0], buff=0.1, tip_length = 0.2, color=WHITE)
        return self.next_arrow

class LinkedListScene(Scene):
    def construct(self):
        # Show animation without cropping
        scale_factor = 1.5
        self.camera.frame_width = 14 * scale_factor  # Default width is 14
        self.camera.frame_height = self.camera.frame_width / 1.78  # Keep 16:9 aspect ratio
        self.camera.frame_center = ORIGIN  # Keep centered

        # Get input from user
        node_values = input("Enter node letters separated by space (e.g., A B C D, max = 5): ").split()
        last_index = len(node_values) - 1

        insert_idx1, insert_idx2 = map(int, input(
            f"Enter the two node indices where a new node should be inserted (0-based).\n"
            f"Valid range: 0 to {last_index}: "
        ).split())

        new_letter = input("Enter the new node letter: ")

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
            self.play(FadeIn(node, run_time=0.5), FadeIn(textfuncadd, run_time=0.6))
            self.play(FadeOut(textfuncadd, run_time=0.6))
            if i > 0:
                self.play(FadeIn(nodes[i - 1].set_next(node), run_time=0.5), FadeIn(textfuncarrow, run_time=0.6))
                self.play(FadeOut(textfuncarrow, run_time=0.6))
        
        self.wait(1)

        # Insert a new node
        updated_nodes = self.insert_node_between(nodes, insert_idx1, insert_idx2, new_letter)

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

        self.convert_to_memory_units(updated_nodes, memory_units, memory_labels, memory_text)



    def insert_node_between(self, nodes, idx1, idx2, new_value):
        # Find the reference nodes for insertion + color code them
        node1 = nodes[idx1]
        node2 = nodes[idx2]
        textfunc = Text(f"insert({node1.text.text}, {node2.text.text})", font_size = 36)
        textfunc.next_to(nodes[0], UP, buff=0.5)
        textfunc.align_to(nodes[0], LEFT)
        self.play(
            node1.box.animate.set_fill(GREEN, opacity=0.35),
            node2.box.animate.set_fill(GREEN, opacity=0.35),
            FadeIn(textfunc)
        )

        self.play(FadeOut(textfunc))

        if not node1 or not node2:
            print("Error: Specified nodes not found in the list.")
            return

        # Shift simultaneously before manipulation
        shifts = []

        # Nodes from the first node to node1 left by 1 unit + their arrows
        for node in nodes[:nodes.index(node1) + 1]: 
            shifts.append(node.animate.shift(LEFT * 2))
            if node.next_arrow:
                shifts.append(node.next_arrow.animate.shift(LEFT * 2)) 

        # Nodes from node2 to the last node right by 1 unit + their arrows
        for node in nodes[nodes.index(node2):]: 
            shifts.append(node.animate.shift(RIGHT * 2))
            if node.next_arrow:
                shifts.append(node.next_arrow.animate.shift(RIGHT * 2))

        # New stretched arrow
        long_arrow = Arrow (
            start=node1.get_bottom() + [0, 0.5, 0] + LEFT * 2, 
            end=node2.get_left() + [0, 0.5, 0] + RIGHT * 2,
            tip_length=0.2,
            buff=0.1 
        )

        # Displaying stretching the arrow simultaneously with shifting
        self.play(
            *shifts, 
            Transform(node1.next_arrow, long_arrow),
            run_time=1 
        )

        # Create the new node to insert
        new_node = LinkedListNodeCloseup(new_value)
        initial_position = (node1.get_right() + node2.get_left()) / 2 + UP * 2.5
        
        new_node.move_to(initial_position)

        self.play(
            FadeIn(new_node), 
            new_node.box.animate.set_fill(GREEN_E, opacity=1)
        )

        # Arrows to new node
        arrow_to_new = Arrow(
            start=long_arrow.get_start(), 
            end=new_node.get_left(),
            tip_length=0.2,
            buff=0.1 
        )

        new_node.next_arrow = new_node.set_next(node2)

        self.play(Transform(node1.next_arrow, arrow_to_new), FadeIn(new_node.next_arrow))

        #Position for a new node in line
        final_position = initial_position -  UP * 2.5

        # Updater for new node movement
        def update_node_position(node):
            if not np.allclose(node.get_center(), final_position):
                node.shift(DOWN * 0.05)
            else:
                node.remove_updater(update_node_position)

        # Update arrows to new node
        arrow_to_new_updated = Arrow(
            start=node1.get_bottom() + [0, 0.5, 0], 
            end=node2.get_left() + [-4, 0.5, 0],
            tip_length=0.2,
            buff=0.1 
        )

        # Updater for arrow from new node
        def update_arrow_from_new(arrow):
            arrow.put_start_and_end_on(
                new_node.get_bottom() + [0, 0.5, 0], 
                node2.get_left() + [0, 0.5, 0] + LEFT * 0.1 
            )
        
        # Add updaters
        new_node.add_updater(update_node_position)
        new_node.next_arrow.add_updater(update_arrow_from_new)

        # Animate the node and arrows moving to their final positions
        self.play(
            new_node.animate.move_to(final_position),
            Transform(node1.next_arrow, arrow_to_new_updated),
            run_time=1.5,
        )

        # Remove updaters
        new_node.remove_updater(update_node_position)
        new_node.next_arrow.remove_updater(update_arrow_from_new)

        shifts_final = []

        for node in nodes: 
            shifts_final.append(node.animate.shift(UP * 2.2))
            if node.next_arrow:
                shifts_final.append(node.next_arrow.animate.shift(UP * 2.2)) 
        
        shifts_final.append(new_node.next_arrow.animate.shift(UP * 2.2))
        shifts_final.append(new_node.animate.shift(UP * 2.2))

        self.play(shifts_final)
        self.play(
            node1.box.animate.set_fill(GREEN, opacity=0),
            node2.box.animate.set_fill(GREEN, opacity=0),
            new_node.box.animate.set_fill(GREEN, opacity=0),
        )

        # Find the position to insert
        insert_index = nodes.index(node1) + 1

        # Insert the new node into the list
        nodes.insert(insert_index, new_node)

        return nodes
    
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
        used_indices = set()
        node_texts_in_memory = []
        node_indices = []

        for i in range(len(nodes)):
            # Pick random memory slots
            while True:
                idx1 = random.randint(0, len(memory_units) - 1)
                if idx1 not in used_indices:
                    used_indices.add(idx1)
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
            self.wait(0.2)
        self.play(
            VGroup(*memory_units).animate.shift(UP * 3),
            VGroup(*node_texts_in_memory).animate.shift(UP * 3),
            VGroup(*node_indices).animate.shift(UP * 3),
            VGroup(*memory_labels).animate.shift(UP * 3),
            memory_text.animate.shift(UP * 3)
        )

        self.create_arrows(node_texts_in_memory)

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
