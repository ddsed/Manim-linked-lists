from manim import *
import copy
from node_basic import LinkedListNodeBasic
from linked_list_vgroup import LinkedListVGroup
from memory_unit import MemoryUnit
from memory_units_vgroup import MemoryUnitsVGroup
import random

class DualScene(Scene):
    
    def construct(self):
        # Set camera settings
        scale_factor = 3
        self.camera.frame_width = 14 * scale_factor
        self.camera.frame_height = self.camera.frame_width / 1.78
        self.camera.frame_center = ORIGIN

        # Get input from user
        node_values = input("Enter node letters separated by space (e.g., A B C D, max = 29): ").split()
        last_index = len(node_values) - 1

        insert_idx1, insert_idx2 = map(int, input(
            f"Enter the two node indices where a new node should be inserted (0-based).\n"
            f"If you want to insert to the head – enter 0 0;\n"
            f"If you want to insert to the tail – enter the index of the last node (={last_index}) twice: "
        ).split())

        new_letter = input("Enter the new node letter: ")

        # Create the linked list groups and memory units
        linked_list = LinkedListVGroup(node_values)
        linked_list_shift = LinkedListVGroup(node_values)
        memory_line = MemoryUnitsVGroup(node_values)

        # Position the left linked list group to the left of the center
        linked_list.move_to(ORIGIN + LEFT * (self.camera.frame_width / 4) + LEFT * 0.2 + UP * 5.3)
        linked_list_shift.move_to(ORIGIN + RIGHT * (self.camera.frame_width / 4) + LEFT * 0.25 + UP * 5.3) 
        memory_line.move_to(ORIGIN + DOWN * 2.2)

        title = Text("Linked List: levels of abstraction", font_size=50)
        title.move_to(ORIGIN + UP * 10.9)
        self.play(FadeIn(title))

        # Animate node creation
        self.animate_nodes(linked_list.nodes, linked_list_shift.nodes)
        
        # Show the memory units
        self.play(FadeIn(memory_line, run_time=2))
        self.wait(1)

        # Show the memory units arrows
        arrows = self.create_arrows(memory_line)

        # Perform insertion animation
        self.insert_node(linked_list, insert_idx1, insert_idx2, new_letter)
        self.insert_node_shift(linked_list_shift, insert_idx1, insert_idx2, new_letter)

        if insert_idx2 == 0:
            updated_original_nodes = self.insert_memory_unit_head(memory_line, insert_idx2, new_letter, arrows)
        elif insert_idx1 == len(memory_line.original_nodes) - 1:
            updated_original_nodes = self.insert_memory_unit_tail(memory_line, insert_idx1, new_letter, arrows)
        else:
            updated_original_nodes = self.insert_memory_unit(memory_line, insert_idx1, insert_idx2, new_letter, arrows)

        self.transform_pointers(memory_line, updated_original_nodes)
    
    # Handles the animation for showing nodes
    def animate_nodes(self, nodes_left, nodes_right):
        # Text to show
        textfuncadd = Text("add()", font_size=42)
        textfuncarrow = Text("nodes[i-1].set_next(node[i])", font_size=42)

        # Positioning the text at the top of the screen
        textfuncadd.next_to(nodes_left[0], UP, buff=0.6)
        textfuncadd.align_to(nodes_left[0], LEFT)
        textfuncarrow.next_to(nodes_left[0], UP, buff=0.6)
        textfuncarrow.align_to(nodes_left[0], LEFT)

        # Loop through both left and right lists at the same time (since the length is the same)
        for i in range(len(nodes_left)):  
            left_node = nodes_left[i]
            right_node = nodes_right[i]

            # For the first 3 nodes, animate them simultaneously
            if i < 3:
                # both left and right nodes at the same time
                self.play(FadeIn(left_node, run_time=0.3), FadeIn(right_node, run_time=0.3), FadeIn(textfuncadd, run_time=0.4))
                self.play(FadeOut(textfuncadd, run_time=0.3))

                # Animate the set_next arrows for both sides (if i > 0)
                if i > 0:
                    arrow_left = nodes_left[i - 1].set_next(left_node, (i - 1) // 10, i // 10)
                    arrow_right = nodes_right[i - 1].set_next(right_node, (i - 1) // 10, i // 10)
                    self.play(FadeIn(arrow_left, run_time=0.3), FadeIn(arrow_right, run_time=0.3), FadeIn(textfuncarrow, run_time=0.4))

                    # FadeOut set_next text
                    self.play(FadeOut(textfuncarrow, run_time=0.3))

            else:
                # For nodes after the first 3, fade them in one by one
                self.play(FadeIn(left_node, run_time=0.1), FadeIn(right_node, run_time=0.1))

                # Animate the set_next arrows for both sides (if i > 0)
                if i > 0:
                    arrow_left = nodes_left[i - 1].set_next(left_node, (i - 1) // 10, i // 10)
                    arrow_right = nodes_right[i - 1].set_next(right_node, (i - 1) // 10, i // 10)
                    self.play(FadeIn(arrow_left, run_time=0.1), FadeIn(arrow_right, run_time=0.1))
        
        # Last null pointer logic
        last_node = nodes_left[-1]
        last_node_shift = nodes_right[-1]
        if len(nodes_left) in [10, 20]:
            last_node.set_next(None, last_node.row, last_node.row + 1)
            last_node_shift.set_next(None, last_node.row, last_node.row + 1)
        else:
            last_node.set_next(None, last_node.row, last_node.row)
            last_node_shift.set_next(None, last_node.row, last_node.row)
        self.play(
            FadeIn(last_node.next_arrow, run_time=0.1),
            FadeIn(last_node_shift.next_arrow, run_time=0.1)
        )
        
        self.wait(1)

    # Creates arrows for memory units
    def create_arrows(self, memory_line):
        arrows = VGroup()

        # Create arrows between the nodes for only non-empty nodes
        for i in range(len(memory_line.original_nodes) - 1):
            start_node = memory_line.original_nodes[i]   # Get node in original order
            next_node = memory_line.original_nodes[i + 1] # Next node in original order

            if start_node.value is not None and next_node.value is not None:
                # Set the next arrow
                arrow = start_node.set_next(next_node, arrow_type=CurvedArrow, color=WHITE)
                arrows.add(arrow)

        # Create a dot arrow for the last node
        last_node = memory_line.original_nodes[-1]
        dot_arrow = Circle(radius=0.1)
        dot_arrow.set_color(WHITE)
        dot_arrow.set_fill(WHITE, opacity=1)
        dot_arrow.move_to(last_node.get_bottom() + RIGHT * 0.25 + [0, 0.5, 0])
        arrows.add(dot_arrow)

        for i, arrow in enumerate(arrows):
        # Slower speed for the first 5 arrows
            if i < 5:
                self.play(FadeIn(arrow, run_time=0.5))
                self.wait(0.1)
            else:
                # Faster speed for the rest of the arrows
                self.play(FadeIn(arrow, run_time=0.2))
        return arrows
    
    # Determines the correct method for inserting a node
    def insert_node(self, linked_list, insert_idx1, insert_idx2, new_letter):
        if insert_idx1 == 9 and insert_idx1 != len(linked_list) - 1 or insert_idx1 == 19 and insert_idx1 != len(linked_list) - 1:
            self.insert_node_inbetween_lines(linked_list, insert_idx1, insert_idx2, new_letter)
        elif insert_idx2 == 0:
            self.insert_node_head(linked_list, insert_idx2, new_letter)
        elif insert_idx1 == len(linked_list) - 1:
            self.insert_node_tail(linked_list, insert_idx1, new_letter)
        else:
            self.insert_node_row(linked_list, insert_idx1, insert_idx2, new_letter)
    
    # Determines the correct method for inserting a node with shifting
    def insert_node_shift(self, linked_list_shift, insert_idx1, insert_idx2, new_letter):
        if insert_idx1 == 9 and insert_idx1 != len(linked_list_shift) - 1 or insert_idx1 == 19 and insert_idx1 != len(linked_list_shift) - 1:
            self.insert_node_inbetween_lines_shift(linked_list_shift, insert_idx1, insert_idx2, new_letter)
        elif insert_idx2 == 0:
            self.insert_node_head_shift(linked_list_shift, insert_idx2, new_letter)
        elif insert_idx1 == len(linked_list_shift) - 1:
            self.insert_node_tail_shift(linked_list_shift, insert_idx1, new_letter)
        else:
            self.insert_node_row_shift(linked_list_shift, insert_idx1, insert_idx2, new_letter)

    # Handles static head insertion 
    def insert_node_head(self, linked_list, idx2, new_value):
        # Find the reference nodes for insertion + color code them
            node2 = linked_list.nodes[idx2]     

            textfunc = Text(f"insert() to head position", font_size = 42)
            textfunc.next_to(linked_list.nodes[0], UP, buff=0.5)
            textfunc.align_to(linked_list.nodes[0], LEFT)
            self.play(
                node2.box.animate.set_fill(GREEN, opacity=0.35),
                FadeIn(textfunc)
            )

            self.play(FadeOut(textfunc))

            if not node2:
                print("Error: Specified nodes not found in the list.")
                return
            
            # Create the new node to insert
            new_node = LinkedListNodeBasic(new_value)
            initial_position = node2.get_left() + UP * 1.55
            new_node.move_to(initial_position)

            # Create an arrow
            new_node.next_arrow = CurvedArrow(
                start_point=new_node.get_bottom(), 
                end_point=node2.get_left(),
                tip_length=0.2
            )

            self.play(
                FadeIn(new_node),
                FadeIn(new_node.next_arrow),
                new_node.box.animate.set_fill(GREEN_E, opacity=1)
            )

    # Handles shifting head insertion 
    def insert_node_head_shift(self, linked_list_shift, idx2, new_value):
        # Find the reference nodes for insertion + color code them
            node2 = linked_list_shift.nodes[idx2]     

            textfunc = Text(f"insert() to head position", font_size = 42)
            textfunc.next_to(linked_list_shift.nodes[0], UP, buff=0.5)
            textfunc.align_to(linked_list_shift.nodes[0], LEFT)
            self.play(
                node2.box.animate.set_fill(GREEN, opacity=0.35),
                FadeIn(textfunc)
            )

            self.play(FadeOut(textfunc))

            if not node2:
                print("Error: Specified nodes not found in the list.")
                return
            
            # Create the new node to insert
            new_node = LinkedListNodeBasic(new_value)
            initial_position = node2.get_left() + UP * 1.55
            new_node.move_to(initial_position)

            new_node.next_arrow = CurvedArrow(
                start_point=new_node.get_bottom() + DOWN * 0.1, 
                end_point=node2.get_left() + LEFT * 0.1,
                tip_length=0.2
            )

            transformed_arrow = Arrow(
                start=new_node.get_right() + DOWN * 1.55 + RIGHT * 0.5, 
                end=node2.get_left() + RIGHT * 2,
                tip_length=0.2,
                buff=0.1
            )
            
            shifts = shift_nodes_to_the_right(linked_list_shift.nodes, idx2)

            self.play(
                FadeIn(new_node),
                FadeIn(new_node.next_arrow),
                new_node.box.animate.set_fill(GREEN_E, opacity=1)
            )
            self.play(
                *shifts,
                new_node.animate.move_to(node2.get_center()),
                Transform(new_node.next_arrow, transformed_arrow)
            )

            if len(linked_list_shift.nodes) < 10:
                # Shift simultaneously after manipulation
                shifts = []

                # Nodes shift left by 1 unit + their arrows
                for node in linked_list_shift.nodes: 
                    shifts.append(node.animate.shift(LEFT * 1))
                    if node.next_arrow:
                        shifts.append(node.next_arrow.animate.shift(LEFT * 1))
                 
                shifts.append(new_node.animate.shift(LEFT * 1))
                shifts.append(new_node.next_arrow.animate.shift(LEFT * 1))

                self.play(
                    *shifts 
                )

    # Handles static tail insertion 
    def insert_node_tail(self, linked_list, idx1, new_value):
        # Find the reference nodes for insertion + color code them
            node1 = linked_list.nodes[idx1]     

            textfunc = Text(f"insert() to tail position", font_size = 42)
            textfunc.next_to(linked_list.nodes[0], UP, buff=0.5)
            textfunc.align_to(linked_list.nodes[0], LEFT)
            self.play(
                node1.box.animate.set_fill(GREEN, opacity=0.35),
                FadeIn(textfunc)
            )

            self.play(FadeOut(textfunc))

            if not node1:
                print("Error: Specified nodes not found in the list.")
                return
            
            new_node = LinkedListNodeBasic(new_value)

            #if new_node will start a new line
            if idx1 == 9 or idx1 == 19:
                initial_position = node1.get_center() + DOWN * 3
                new_node.move_to(initial_position)
                new_node.set_next(None, node1.row + 1, node1.row + 1)

                basic_arrow = Arrow(
                    start = node1.get_bottom(),
                    end = new_node.get_top(),
                    tip_length = 0.2,
                    buff=0.1
                )
                self.play(
                    FadeIn(new_node),
                    FadeIn(new_node.next_arrow),
                    Transform(node1.next_arrow, basic_arrow),
                    new_node.box.animate.set_fill(GREEN_E, opacity=1)
                )
                
                shifts = []

                # Nodes shifts to center the structure
                for node in linked_list.nodes: 
                    shifts.append(node.animate.shift(UP * 1.5))
                    if node.next_arrow:
                        shifts.append(node.next_arrow.animate.shift(UP * 1.5))
                 
                shifts.append(new_node.animate.shift(UP * 1.5))
                shifts.append(new_node.next_arrow.animate.shift(UP * 1.5))

                self.play(
                    *shifts 
                )
            else:
                #if tail is odd row
                if node1.row % 2 != 0:
                    initial_position = node1.get_center() + LEFT * 2         
                    new_node.move_to(initial_position)
                    if idx1 == 18:
                        new_node.set_next(None, 0, 1)
                    else:
                        new_node.set_next(None, node1.row, node1.row)
                    basic_arrow = Arrow(
                        start = node1.get_left(),
                        end = new_node.get_right(),
                        tip_length = 0.2,
                        buff=0.1
                    )
                #if tail is even row
                else:
                    initial_position = node1.get_center() + RIGHT * 2
                    new_node.move_to(initial_position)
                    if idx1 == 8:
                        new_node.set_next(None, 0, 1)
                    else:
                        new_node.set_next(None, node1.row, node1.row)
                    basic_arrow = Arrow(
                        start = node1.get_right(),
                        end = new_node.get_left(),
                        tip_length = 0.2,
                        buff=0.1
                    )

                self.play(
                    FadeIn(new_node),
                    FadeIn(new_node.next_arrow),
                    Transform(node1.next_arrow, basic_arrow),
                    new_node.box.animate.set_fill(GREEN_E, opacity=1)
                )
            
            if len(linked_list.nodes) < 10:
                # Shift simultaneously
                shifts = []

                # Nodes shift left by 1 unit + their arrows
                for node in linked_list.nodes: 
                    shifts.append(node.animate.shift(LEFT * 1))
                    if node.next_arrow:
                        shifts.append(node.next_arrow.animate.shift(LEFT * 1))
                 
                shifts.append(new_node.animate.shift(LEFT * 1))
                shifts.append(new_node.next_arrow.animate.shift(LEFT * 1))

                self.play(
                    *shifts 
                )
    
    # Handles shifting tail insertion
    def insert_node_tail_shift(self, linked_list_shift, idx1, new_value):
        # Find the reference nodes for insertion + color code them
            node1 = linked_list_shift.nodes[idx1]     

            textfunc = Text(f"insert() to tail position", font_size = 42)
            textfunc.next_to(linked_list_shift.nodes[0], UP, buff=0.5)
            textfunc.align_to(linked_list_shift.nodes[0], LEFT)
            self.play(
                node1.box.animate.set_fill(GREEN, opacity=0.35),
                FadeIn(textfunc)
            )

            self.play(FadeOut(textfunc))

            if not node1:
                print("Error: Specified nodes not found in the list.")
                return
            
            new_node = LinkedListNodeBasic(new_value)

            #if new_node will start a new line
            if idx1 == 9 or idx1 == 19:
                initial_position = node1.get_center() + DOWN * 3
                new_node.move_to(initial_position)
                new_node.set_next(None, node1.row + 1, node1.row + 1)
                basic_arrow = Arrow (
                    start = node1.get_bottom(),
                    end = new_node.get_top(),
                    tip_length = 0.2,
                    buff=0.1
                )

                self.play(
                    FadeIn(new_node),
                    FadeIn(new_node.next_arrow),
                    Transform(node1.next_arrow, basic_arrow),
                    new_node.box.animate.set_fill(GREEN_E, opacity=1)
                )

                shifts = []

                # Nodes shift left by 1 unit + their arrows
                for node in linked_list_shift.nodes: 
                    shifts.append(node.animate.shift(UP * 1.5))
                    if node.next_arrow:
                        shifts.append(node.next_arrow.animate.shift(UP * 1.5))
                 
                shifts.append(new_node.animate.shift(UP * 1.5))
                shifts.append(new_node.next_arrow.animate.shift(UP * 1.5))
                
                self.play(
                    *shifts 
                )
            #if tail is odd row
            else:
                if node1.row % 2 != 0:
                    initial_position = node1.get_left() + DOWN * 1.55
                    new_node.move_to(initial_position)
                    new_node.set_next(None, node1.row, node1.row)

                    basic_arrow = CurvedArrow(
                        start_point=node1.get_bottom() + DOWN * 0.1, 
                        end_point=new_node.get_right() + RIGHT * 0.1,
                        angle=-TAU/4, 
                        tip_length=0.2
                    )

                    transformed_arrow = Arrow(
                        start=node1.get_left(), 
                        end=new_node.get_right() + LEFT * 1.5 + UP * 1.55,
                        tip_length=0.2,
                        buff=0.1
                    )

                    self.play(
                        FadeIn(new_node),
                        FadeIn(new_node.next_arrow),
                        Transform(node1.next_arrow, basic_arrow),
                        new_node.box.animate.set_fill(GREEN_E, opacity=1)
                    )
                    self.play(
                        new_node.animate.move_to(node1.get_center() + LEFT * 2),
                        new_node.next_arrow.animate.move_to(node1.get_left() + LEFT * 2.5),
                        Transform(node1.next_arrow, transformed_arrow)
                    )

                    if idx1 == 18:
                        new_last_arow = Arrow(
                            start = node1.get_bottom() + LEFT * 2, 
                            end = node1.get_bottom() + LEFT * 2 + DOWN * 1,
                            buff=0.1,
                            tip_length=0.2,
                            tip_shape=ArrowCircleFilledTip,
                            color=WHITE
                        )
                        self.play(
                            new_node.animate.move_to(node1.get_center() + LEFT * 2),
                            Transform(new_node.next_arrow, new_last_arow),
                            Transform(node1.next_arrow, transformed_arrow)
                        )
                    else:
                        self.play(
                            new_node.animate.move_to(node1.get_center() + LEFT * 2),
                            new_node.next_arrow.animate.move_to(node1.get_left() + LEFT * 2.5),
                            Transform(node1.next_arrow, transformed_arrow)
                        )
                #if tail is even row
                else:
                    initial_position = node1.get_right() + DOWN * 1.55
                    new_node.move_to(initial_position)
                    new_node.set_next(None, node1.row, node1.row)

                    basic_arrow = CurvedArrow(
                        start_point=node1.get_bottom() + DOWN * 0.1, 
                        end_point=new_node.get_left() + LEFT * 0.1,
                        tip_length=0.2
                    )

                    transformed_arrow = Arrow(
                        start=node1.get_right(), 
                        end=new_node.get_left() + RIGHT * 1.5 + UP * 1.55,
                        tip_length=0.2,
                        buff=0.1
                    )

                    self.play(
                        FadeIn(new_node),
                        FadeIn(new_node.next_arrow),
                        Transform(node1.next_arrow, basic_arrow),
                        new_node.box.animate.set_fill(GREEN_E, opacity=1)
                    )

                    if idx1 == 8:
                        new_last_arow = Arrow(
                            start = node1.get_bottom() + RIGHT * 2, 
                            end = node1.get_bottom() + RIGHT * 2 + DOWN * 1,
                            buff=0.1,
                            tip_length=0.2,
                            tip_shape=ArrowCircleFilledTip,
                            color=WHITE
                        )
                        self.play(
                            new_node.animate.move_to(node1.get_center() + RIGHT * 2),
                            Transform(new_node.next_arrow, new_last_arow),
                            Transform(node1.next_arrow, transformed_arrow)
                        )
                    else:
                        self.play(
                            new_node.animate.move_to(node1.get_center() + RIGHT * 2),
                            new_node.next_arrow.animate.move_to(node1.get_right() + RIGHT * 2.5),
                            Transform(node1.next_arrow, transformed_arrow)
                        )
                
            if len(linked_list_shift.nodes) < 10:
                if len(linked_list_shift.nodes) < 9:
                    shift = LEFT * 1
                else:
                    shift = LEFT * 0.5
                # Shift simultaneously before manipulation
                shifts = []

                # Nodes shift left by 1 unit + their arrows
                for node in linked_list_shift.nodes: 
                    shifts.append(node.animate.shift(shift))
                    if node.next_arrow:
                        shifts.append(node.next_arrow.animate.shift(shift))
                 
                shifts.append(new_node.animate.shift(shift))
                shifts.append(new_node.next_arrow.animate.shift(shift))
                
                self.play(
                    *shifts 
                )

    # Handles static basic insertion
    def insert_node_row(self, linked_list, idx1, idx2, new_value):
            # Find the reference nodes for insertion + color code them
            node1 = linked_list.nodes[idx1]
            node2 = linked_list.nodes[idx2]     

            textfunc = Text(f"insert({node1.text.text}, {node2.text.text})", font_size = 42)
            textfunc.next_to(linked_list.nodes[0], UP, buff=0.5)
            textfunc.align_to(linked_list.nodes[0], LEFT)
            self.play(
                node1.box.animate.set_fill(GREEN, opacity=0.35),
                node2.box.animate.set_fill(GREEN, opacity=0.35),
                FadeIn(textfunc)
            )

            self.play(FadeOut(textfunc))

            if not node1 or not node2:
                print("Error: Specified nodes not found in the list.")
                return

            # Create the new node to insert
            new_node = LinkedListNodeBasic(new_value)
            if idx1 == 10 or idx1 == 20:
                initial_position = (node1.get_right() + node2.get_left()) / 2 + DOWN * 1.5
            else:
                initial_position = (node1.get_right() + node2.get_left()) / 2 + UP * 1.5
            
            new_node.move_to(initial_position)

            self.play(
                FadeIn(new_node), 
                new_node.box.animate.set_fill(GREEN_E, opacity=1),
                run_time=0.8
            )

            # Create arrows to and from the new node for even rows
            if node1.row % 2 == 0:
                # for node right after the row switch
                if idx1 == 20:
                    arrow_to_new = Arrow(
                        start=node1.get_bottom(), 
                        end=new_node.get_left(),
                        tip_length=0.2,
                        buff=0.1 
                    )
                    new_node.next_arrow = Arrow(
                        start=new_node.get_right(), 
                        end=node2.get_bottom(),
                        tip_length=0.2,
                        buff=0.1 
                    )
                else:
                    arrow_to_new = Arrow(
                        start=node1.get_top(), 
                        end=new_node.get_left(),
                        tip_length=0.2,
                        buff=0.1 
                    )
                    new_node.next_arrow = Arrow(
                        start=new_node.get_right(), 
                        end=node2.get_top(),
                        tip_length=0.2,
                        buff=0.1 
                    )
            # for odd rows
            else:
                # for node right after the row switch
                if idx1 == 10:
                    arrow_to_new = Arrow(
                        start=node1.get_bottom(), 
                        end=new_node.get_right(),
                        tip_length=0.2,
                        buff=0.1 
                    )
                    new_node.next_arrow = Arrow(
                        start=new_node.get_left(), 
                        end=node2.get_bottom(),
                        tip_length=0.2,
                        buff=0.1 
                    )
                else:
                    arrow_to_new = Arrow(
                        start=node1.get_top(), 
                        end=new_node.get_right(),
                        tip_length=0.2,
                        buff=0.1 
                    )
                    new_node.next_arrow = Arrow(
                        start=new_node.get_left(), 
                        end=node2.get_top(),
                        tip_length=0.2,
                        buff=0.1 
                    )

            self.play(
                Transform(node1.next_arrow, arrow_to_new), 
                FadeIn(new_node.next_arrow),
                run_time=0.8
            )
    
    # Handles shifting basic insertion
    def insert_node_row_shift(self, linked_list_shift, idx1, idx2, new_value):
            # Find the reference nodes for insertion + color code them
            node1 = linked_list_shift.nodes[idx1]
            node2 = linked_list_shift.nodes[idx2]     

            textfunc = Text(f"insert({node1.text.text}, {node2.text.text})", font_size = 42)
            textfunc.next_to(linked_list_shift.nodes[0], UP, buff=0.5)
            textfunc.align_to(linked_list_shift.nodes[0], LEFT)
            self.play(
                node1.box.animate.set_fill(GREEN, opacity=0.35),
                node2.box.animate.set_fill(GREEN, opacity=0.35),
                FadeIn(textfunc)
            )

            self.play(FadeOut(textfunc))

            if not node1 or not node2:
                print("Error: Specified nodes not found in the list.")
                return

            if len(linked_list_shift.nodes) < 10:
                if len(linked_list_shift.nodes) < 9:
                    shift_left = LEFT * 1
                    shift_right = RIGHT * 1
                else:
                    shift_left = LEFT * 0.5
                    shift_right = RIGHT * 1.5
                # Shift simultaneously before manipulation
                shifts = []

                # Nodes from the first node to node1 left by 1 unit + their arrows
                for node in linked_list_shift.nodes[:linked_list_shift.nodes.index(node1) + 1]: 
                    shifts.append(node.animate.shift(shift_left))
                    if node.next_arrow:
                        shifts.append(node.next_arrow.animate.shift(shift_left)) 

                # Nodes from node2 to the last node right by 1 unit + their arrows
                for node in linked_list_shift.nodes[linked_list_shift.nodes.index(node2):]: 
                    shifts.append(node.animate.shift(shift_right))
                    if node.next_arrow:
                        if linked_list_shift.nodes.index(node) == 8:
                            shifts.append(node.next_arrow.animate.put_start_and_end_on(
                                node.get_bottom() + shift_right + DOWN * 0.1,
                                node.get_bottom() + shift_right + DOWN * 1
                            ))
                        else:
                            shifts.append(node.next_arrow.animate.shift(shift_right))
                # New stretched arrow
                long_arrow = Arrow (
                    start=node1.get_right() + shift_left, 
                    end=node2.get_left() + shift_right,
                    tip_length=0.2,
                    buff=0.1 
                )
            else:
                shifts = shift_nodes_to_the_right(linked_list_shift.nodes, idx2)
                # Checking what line we are inserting to
                if node2.row % 2 == 0:
                    if idx1 == 8:
                        long_arrow = node1.next_arrow
                    else:
                        # Stretch the existing arrow between node1 and node2 for even lines
                        long_arrow = Arrow(
                            start=node1.get_right(), 
                            end=node2.get_left() + RIGHT * 2,
                            tip_length=0.2,
                            buff=0.1
                        )
                else:
                    if idx1 == 18:
                        long_arrow = node1.next_arrow
                    else:
                        # Stretch the existing arrow between node1 and node2 for odd lines
                        long_arrow = Arrow(
                            start=node1.get_left(), 
                            end=node2.get_right() + LEFT * 2,
                            tip_length=0.2,
                            buff=0.1
                        )
            # Create the new node to insert
            new_node = LinkedListNodeBasic(new_value)
            
            if idx1 == 8:
                initial_position = node1.get_center() + RIGHT * 2
            elif idx1 == 18:
                initial_position = node1.get_center() + LEFT * 2
            else:
                pass
            
            if idx1 == 8 or idx1 == 18:
                new_node.move_to(initial_position)
                new_node.next_arrow = Arrow(
                    start=new_node.get_bottom(), 
                    end=new_node.get_bottom() + DOWN * 2,
                    tip_length=0.2,
                    buff=0.1
                )
                # Displaying stretching the arrow simultaneously with shifting + new node appears
                self.play(
                    *shifts, 
                    Transform(node1.next_arrow, long_arrow),
                    FadeIn(new_node.next_arrow),
                    FadeIn(new_node), 
                    new_node.box.animate.set_fill(GREEN_E, opacity=1),
                    run_time=1 
                )
            else:
                # Displaying stretching the arrow simultaneously with shifting
                self.play(
                    *shifts, 
                    Transform(node1.next_arrow, long_arrow),
                    run_time=1 
                )
                initial_position = (node1.get_right() + node2.get_left()) / 2 + UP * 1.5
                new_node.move_to(initial_position)
                self.play(
                    FadeIn(new_node), 
                    new_node.box.animate.set_fill(GREEN_E, opacity=1)
                )

            # Logic for either 1 line, or even lines 
            if len(linked_list_shift.nodes) < 10 or node2.row % 2 == 0:
                # Arrows to new node
                arrow_to_new = Arrow(
                    start=long_arrow.get_start(), 
                    end=new_node.get_left(),
                    tip_length=0.2,
                    buff=0.1 
                )
            # Logic for odd lines
            else:
                # Arrows to new node
                arrow_to_new = Arrow(
                    start=long_arrow.get_start(), 
                    end=new_node.get_right(),
                    tip_length=0.2,
                    buff=0.1 
                )

            if idx1 == 8 or idx1 == 18:
                pass
            else:
                new_node.next_arrow = new_node.set_next(node2, node1.row, node2.row)
                self.play(Transform(node1.next_arrow, arrow_to_new), FadeIn(new_node.next_arrow))

                #Position for a new node in line
                final_position = initial_position -  UP * 1.5

                # Updater for new node movement
                def update_node_position(node):
                    if not np.allclose(node.get_center(), final_position):
                        node.shift(DOWN * 0.05)
                    else:
                        node.remove_updater(update_node_position)

                if len(linked_list_shift.nodes) < 10 or node2.row % 2 == 0:
                    # Updater for arrow to new node
                    def update_arrow_to_new(arrow):
                        arrow.put_start_and_end_on(
                            node1.get_right() + RIGHT * 0.1,  
                            new_node.get_left() + LEFT * 0.1 
                        )

                    # Updater for arrow from new node
                    def update_arrow_from_new(arrow):
                        arrow.put_start_and_end_on(
                            new_node.get_right() + RIGHT * 0.1, 
                            node2.get_left() + LEFT * 0.1 
                        )
                else:
                    # Updater for arrow to new node
                    def update_arrow_to_new(arrow):
                        arrow.put_start_and_end_on(
                            node1.get_left() + LEFT * 0.1,  
                            new_node.get_right() + RIGHT * 0.1 
                        )

                    # Updater for arrow from new node
                    def update_arrow_from_new(arrow):
                        arrow.put_start_and_end_on(
                            new_node.get_left() + LEFT * 0.1, 
                            node2.get_right() + RIGHT * 0.1 
                        )
                
                # Add updaters
                new_node.add_updater(update_node_position)
                new_node.next_arrow.add_updater(update_arrow_from_new)
                node1.next_arrow.add_updater(update_arrow_to_new)

                # Animate the node and arrows moving to their final positions
                self.play(
                    new_node.animate.move_to(final_position),
                    run_time=1.5,
                )

                # Remove updaters
                new_node.remove_updater(update_node_position)
                new_node.next_arrow.remove_updater(update_arrow_from_new)
                node1.next_arrow.remove_updater(update_arrow_to_new)

    # Handles static insertion in between lines
    def insert_node_inbetween_lines(self, linked_list, idx1, idx2, new_value):
        # Find the reference nodes for insertion + color code them
        node1 = linked_list.nodes[idx1]
        node2 = linked_list.nodes[idx2]     

        textfunc = Text(f"insert({node1.text.text}, {node2.text.text})", font_size = 42)
        textfunc.next_to(linked_list.nodes[0], UP, buff=0.5)
        textfunc.align_to(linked_list.nodes[0], LEFT)
        self.play(
            node1.box.animate.set_fill(GREEN, opacity=0.35),
            node2.box.animate.set_fill(GREEN, opacity=0.35),
            FadeIn(textfunc)
        )

        self.play(FadeOut(textfunc))

        if not node1 or not node2:
            print("Error: Specified nodes not found in the list.")
            return
        
        # Create the new node to insert
        new_node = LinkedListNodeBasic(new_value)
        if idx1 == 9:
            initial_position = (node1.get_bottom() + node2.get_top()) / 2 + LEFT * 1.5
        else:
            initial_position = (node1.get_bottom() + node2.get_top()) / 2 + RIGHT * 1.5
        
        new_node.move_to(initial_position)

        self.play(
            FadeIn(new_node), 
            new_node.box.animate.set_fill(GREEN_E, opacity=1),
            run_time=0.8
        )
        
        # Arrows to new node
        arrow_to_new = Arrow(
            start=node1.get_bottom(), 
            end=new_node.get_top(),
            tip_length=0.2,
            buff=0.1 
        )

        new_node.next_arrow = new_node.set_next(node2, node1.row, node2.row)
        self.play(Transform(node1.next_arrow, arrow_to_new), FadeIn(new_node.next_arrow))

    # Handles shifting insertion in between lines
    def insert_node_inbetween_lines_shift(self, linked_list_shift, idx1, idx2, new_value):
        # Find the reference nodes for insertion + color code them
        node1 = linked_list_shift.nodes[idx1]
        node2 = linked_list_shift.nodes[idx2]     

        textfunc = Text(f"insert({node1.text.text}, {node2.text.text})", font_size = 42)
        textfunc.next_to(linked_list_shift.nodes[0], UP, buff=0.5)
        textfunc.align_to(linked_list_shift.nodes[0], LEFT)
        self.play(
            node1.box.animate.set_fill(GREEN, opacity=0.35),
            node2.box.animate.set_fill(GREEN, opacity=0.35),
            FadeIn(textfunc)
        )

        self.play(FadeOut(textfunc))

        if not node1 or not node2:
            print("Error: Specified nodes not found in the list.")
            return
        
        # Identify affected nodes for shifting to make space for insertion
        nodes_above = [n for n in linked_list_shift.nodes if n.row <= node1.row]  # Rows before insertion
        nodes_below = [n for n in linked_list_shift.nodes if n.row >= node2.row]  # Rows after insertion
        
        # Create the new node to insert
        new_node = LinkedListNodeBasic(new_value)
        if idx1 == 9:
            initial_position = (node1.get_bottom() + node2.get_top()) / 2 + LEFT * 1.5
        else:
            initial_position = (node1.get_bottom() + node2.get_top()) / 2 + RIGHT * 1.5
        
        new_node.move_to(initial_position)

        self.play(
            FadeIn(new_node), 
            new_node.box.animate.set_fill(GREEN_E, opacity=1),
            *[n.animate.shift(UP * 0.5) for n in nodes_above],
            *[n.animate.shift(DOWN * 0.5) for n in nodes_below],
            *[n.next_arrow.animate.shift(UP * 0.5) for n in nodes_above if n.next_arrow],
            *[n.next_arrow.animate.shift(DOWN * 0.5) for n in nodes_below if n.next_arrow],
            node1.next_arrow.animate.put_start_and_end_on(
                node1.get_bottom() + UP * 0.5 + DOWN * 0.1, 
                node2.get_top() + DOWN * 0.5 + UP * 0.1
            ),
            run_time=0.8
        )

        # Arrows to new node
        arrow_to_new = Arrow(
            start=node1.next_arrow.get_start(), 
            end=new_node.get_top(),
            tip_length=0.2,
            buff=0.1 
        )

        new_node.next_arrow = new_node.set_next(node2, node1.row, node2.row)
        self.play(Transform(node1.next_arrow, arrow_to_new), FadeIn(new_node.next_arrow))

        # Shift nodes from node2 onwards
        shifts = shift_nodes_to_the_right(linked_list_shift.nodes, idx2)
        
        # Updater for arrow to new node
        def update_arrow_to_new(arrow):
            arrow.put_start_and_end_on(
                node1.get_bottom() + DOWN * 0.1,  
                new_node.get_top() + UP * 0.1 
            )
            
        # Add updaters
        node1.next_arrow.add_updater(update_arrow_to_new)

        # Arrows to new node
        if idx1 == 9:
            arrow_from_new = Arrow(
                start=node2.get_left(), 
                end=node2.get_right() + LEFT * 2,
                tip_length=0.2,
                buff=0.1 
            )
        else:
            arrow_from_new = Arrow(
                start=node2.get_right(), 
                end=node2.get_left() + RIGHT * 2,
                tip_length=0.2,
                buff=0.1 
            )

        self.play(
            *shifts,
            Transform(new_node, new_node.copy().move_to(node2.get_center())),
            Transform(new_node.next_arrow, arrow_from_new),
            run_time=1.5
        )

        # Remove updaters
        node1.next_arrow.remove_updater(update_arrow_to_new)

        # Restore original positions of rows, new node and arrows 
        self.play(
            *[n.animate.shift(DOWN * 0.5) for n in nodes_above],
            *[n.animate.shift(UP * 0.5) for n in nodes_below],
            *[n.next_arrow.animate.shift(DOWN * 0.5) for n in nodes_above if n.next_arrow],
            *[n.next_arrow.animate.shift(UP * 0.5) for n in nodes_below if n.next_arrow],
            new_node.animate.shift(UP * 0.5),
            new_node.next_arrow.animate.shift(UP * 0.5),
            node1.next_arrow.animate.put_start_and_end_on(
                    node1.get_bottom() + DOWN * 0.5 + DOWN * 0.1, 
                    new_node.get_top() + UP * 0.5 + UP * 0.1
            ),
            run_time=0.8
        )

    # Handles insertion in memory unites line
    def insert_memory_unit(self, nodes, idx1, idx2, new_letter, arrows):
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
                if arrow is not new_node.next_arrow and arrow is not node1.next_arrow and not isinstance(arrow, Circle)
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

        self.wait(1)

        self.play(
            node1.next_arrow.animate.set_color(WHITE).set_stroke(width=4),
            node1.next_arrow.tip.animate.set_color(WHITE).set_stroke(width=0),
            new_node.next_arrow.animate.set_color(WHITE).set_stroke(width=4),
            new_node.next_arrow.tip.animate.set_color(WHITE).set_stroke(width=0),
            new_node.box.animate.set_fill(GREEN, opacity=0.35),
            *[
            AnimationGroup(
                arrow.animate.set_stroke(opacity=1), 
                arrow.tip.animate.set_fill(opacity=1)
            )
            for arrow in arrows 
                if arrow is not new_node.next_arrow and arrow is not node1.next_arrow and not isinstance(arrow, Circle)
            ]
        )

        # Update the list of original nodes
        nodes.original_nodes.insert(idx2, new_node)
        return nodes.original_nodes

    # Handles head insertion in memory unites line
    def insert_memory_unit_head(self, nodes, idx2, new_letter, arrows):
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
                if arrow is not new_node.next_arrow and not isinstance(arrow, Circle)
            ]
        )

        # Creating an arrow from a new node
        new_node.next_arrow = new_node.set_next(node_head, CurvedArrow, color=GREEN)
        new_node.next_arrow.set_stroke(width=10)
        self.play(FadeIn(new_node.next_arrow))

        self.wait(1)

        self.play(
            new_node.next_arrow.animate.set_color(WHITE).set_stroke(width=4),
            new_node.next_arrow.tip.animate.set_color(WHITE).set_stroke(width=0),
            new_node.box.animate.set_fill(GREEN, opacity=0.35),
            *[
            AnimationGroup(
                arrow.animate.set_stroke(opacity=1), 
                arrow.tip.animate.set_fill(opacity=1)
            )
            for arrow in arrows 
                if arrow is not new_node.next_arrow and not isinstance(arrow, Circle)
            ]
        )
        
        # Update the list of original nodes
        nodes.original_nodes.insert(idx2, new_node)
        return nodes.original_nodes

    # Handles tail insertion in memory unites line
    def insert_memory_unit_tail(self, nodes, idx1, new_letter, arrows):
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
                if arrow is not node_tail.next_arrow and not isinstance(arrow, Circle)
            ] 
        )

        # Creating an arrow to a new node and null pointer
        node_tail.next_arrow = node_tail.set_next(new_node, CurvedArrow, color=GREEN)
        node_tail.next_arrow.set_stroke(width=10)
        self.play(FadeOut(arrows[-1]), FadeIn(node_tail.next_arrow))
        arrows[-1].move_to(new_node.get_bottom() + RIGHT * 0.25 + [0, 0.5, 0])
        self.play(FadeIn(arrows[-1]))

        self.wait(1)

        self.play(
            node_tail.next_arrow.animate.set_color(WHITE).set_stroke(width=4),
            node_tail.next_arrow.tip.animate.set_color(WHITE).set_stroke(width=0),
            new_node.box.animate.set_fill(GREEN, opacity=0.35),
            *[
            AnimationGroup(
                arrow.animate.set_stroke(opacity=1), 
                arrow.tip.animate.set_fill(opacity=1)
            )
            for arrow in arrows 
                if arrow is not node_tail.next_arrow and not isinstance(arrow, Circle)
            ]
        )

        # Update the list of original nodes
        nodes.original_nodes.append(new_node)
        return nodes.original_nodes
    
    # Handles tranformation of arrow pointers into memory addresses pointers
    def transform_pointers(self, nodes, updated_original_nodes):
        memory_labels = nodes.memory_labels

        # Loop by indices of updated original nodes
        for i, node in enumerate(updated_original_nodes):
            # Avoid index error for the last node
            if i < len(updated_original_nodes) - 1:
                next_node = updated_original_nodes[i + 1]
                label = memory_labels[nodes.shuffled_nodes.index(next_node)]
                label_copy = copy.deepcopy(memory_labels[nodes.shuffled_nodes.index(next_node)])
                if node.next_arrow is not None and i < 5:
                    self.play(
                        FadeOut(label),
                        label_copy.animate.scale(1.5),
                        node.next_arrow.animate.set_color(ORANGE)
                    )
                    circle = Circle(radius=0.2)
                    circle.set_opacity(0) 
                    circle.move_to(node.next_arrow.get_start())
                    self.play(
                        FadeIn(label),
                        label_copy.animate.scale(1 / 1.5).rotate(PI / 2).move_to(node.get_bottom() + RIGHT * 0.25 + UP * 0.5),
                        Transform(node.next_arrow, circle)
                    )
                    self.wait(0.5)
                else:
                    self.play(
                        FadeOut(label),
                        label_copy.animate.scale(1.5),
                        node.next_arrow.animate.set_color(ORANGE),
                        run_time = 0.3
                    )
                    circle = Circle(radius=0.2)
                    circle.set_opacity(0) 
                    circle.move_to(node.next_arrow.get_start())
                    self.play(
                        FadeIn(label),
                        label_copy.animate.scale(1 / 1.5).rotate(PI / 2).move_to(node.get_bottom() + RIGHT * 0.25 + UP * 0.5),
                        Transform(node.next_arrow, circle),
                        run_time = 0.3
                    )
                    self.wait(0.2)

# Logic for shifting the nodes to the right
def shift_nodes_to_the_right(nodes, idx2):
    shifts = []

    # Iterate through the nodes starting from idx2
    for i in range(nodes.index(nodes[idx2]), len(nodes)):
        node_i = nodes[i]

        # Shift node_i to the position of node_i_next
        if i == len(nodes) - 1:
            if i == 9 or i == 19:
                shifts.append(node_i.animate.shift(DOWN * 3))
            elif node_i.row % 2 != 0:
                shifts.append(node_i.animate.shift(LEFT * 2))
            else:
                shifts.append(node_i.animate.shift(RIGHT * 2))
        else:
            node_i_next = nodes[i + 1]
            shifts.append(node_i.animate.move_to(node_i_next.get_center()))

        # If node_i has a next arrow, shift it accordingly
        if node_i.next_arrow:
            # Even lines without edge cases
            if node_i.row % 2 == 0 and i != 8 and i != 9 and i != 28 and i != 29:
                shifts.append(node_i.next_arrow.animate.shift(RIGHT * 2))
            # From even line to odd line to become long arrow
            elif i == 8 or i == 28:
                # Last node pointer
                if i == len(nodes) - 1:
                    shifts.append(node_i.next_arrow.animate.put_start_and_end_on(
                        node_i.get_bottom() + RIGHT * 2 + DOWN * 0.1,
                        node_i.get_bottom() + RIGHT * 2 + DOWN * 1
                    ))
                else:
                    shifts.append(node_i.next_arrow.animate.put_start_and_end_on(
                        node_i.get_bottom() + RIGHT * 2 + DOWN * 0.1,
                        node_i_next.get_top() + DOWN * 3 + UP * 0.1
                    ))
            # From even line to odd line to become short arrow
            elif i == 9 or i == 29:
                # Last node pointer
                if i == len(nodes) - 1:
                    shifts.append(node_i.next_arrow.animate.put_start_and_end_on(
                        node_i.get_left() + DOWN * 3 + LEFT * 0.1,
                        node_i.get_left() + DOWN * 3 + LEFT * 1
                    ))
                else:
                    shifts.append(node_i.next_arrow.animate.put_start_and_end_on(
                        node_i.get_left() + DOWN * 3 + LEFT * 0.1,
                        node_i_next.get_right() + LEFT * 2 + RIGHT * 0.1
                    ))
            # From odd line to even line to become long arrow
            elif i == 18:
                # Last node pointer
                if i == len(nodes) - 1:
                    shifts.append(node_i.next_arrow.animate.put_start_and_end_on(
                        node_i.get_bottom() + LEFT * 2 + DOWN * 0.1,
                        node_i.get_bottom() + LEFT * 2 + DOWN * 1
                    ))
                else:
                    shifts.append(node_i.next_arrow.animate.put_start_and_end_on(
                        node_i.get_bottom() + LEFT * 2 + DOWN * 0.1,
                        node_i_next.get_top() + DOWN * 3 + UP * 0.1
                    ))
            # From odd line to even line to become short arrow
            elif i == 19:
                # Last node pointer
                if i == len(nodes) - 1:
                    shifts.append(node_i.next_arrow.animate.put_start_and_end_on(
                        node_i.get_right() + DOWN * 3 + RIGHT * 0.1,
                        node_i.get_right() + DOWN * 3 + RIGHT * 1
                    ))
                else:
                    shifts.append(node_i.next_arrow.animate.put_start_and_end_on(
                        node_i.get_right() + DOWN * 3 + RIGHT * 0.1,
                        node_i_next.get_left() + RIGHT * 2 + LEFT * 0.1
                    ))
            # For odd lines
            else:
                shifts.append(node_i.next_arrow.animate.shift(LEFT * 2))
    return shifts
