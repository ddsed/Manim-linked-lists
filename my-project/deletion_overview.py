from manim import *
import copy
from node_basic import LinkedListNodeBasic
from linked_list_vgroup import LinkedListVGroup
from memory_units_vgroup import MemoryUnitsVGroup

class OverviewScene(Scene):
    def construct(self):
        # Set camera settings
        scale_factor = 3
        self.camera.frame_width = 14 * scale_factor
        self.camera.frame_height = self.camera.frame_width / 1.78
        self.camera.frame_center = ORIGIN

        # Get and validate node values input from user
        while True:
            node_values = input("\033[0m\nEnter node letters separated by space (e.g., A B C D, min = 3, max = 30): ").strip().split()
            if len(node_values) < 3:
                print("\033[91mInvalid input: Must provide at least 3 nodes.")
            elif len(node_values) > 30:
                print("\033[91mInvalid input: Maximum allowed nodes is 30.")
            else:
                break  # if valid input

        last_index = len(node_values) - 1

        # Get and validate insert indices input from user
        while True:
            try:
                delete_idx = int(input(
                    f"\033[0m\nEnter the index of the node to delete (0-based).\n"
                    f"\033[0mValid range: 0 to {last_index}: "
                ))
                if not (0 <= delete_idx <= last_index):
                    print("\033[91mInvalid input: Index is out of range. Please, eneter valid index")
                else:
                    break
            except ValueError as e:
                print(f"\033[91mInvalid input: {e}")

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
        self.animate_nodes(linked_list.nodes, linked_list_shift.nodes, linked_list.headtext, linked_list_shift.headtext, linked_list.headarrow, linked_list_shift.headarrow)
        
        # Show the memory units
        self.play(FadeIn(memory_line, run_time=2))
        self.wait(1)

        # Show the memory units arrows
        arrows = self.create_arrows(memory_line)

        # Perform insertion animation
        self.delete_node(linked_list, delete_idx, linked_list.headtext, linked_list.headarrow)
        self.delete_node_shift(linked_list_shift, delete_idx, linked_list_shift.headtext, linked_list_shift.headarrow)

        if delete_idx == 0:
            updated_original_nodes = self.delete_memory_units_head(memory_line, delete_idx, arrows)
        elif delete_idx == len(memory_line.original_nodes) - 1:
            updated_original_nodes = self.delete_memory_units_tail(memory_line, delete_idx, arrows)
        else:
            updated_original_nodes = self.delete_memory_units(memory_line, delete_idx, arrows)

        self.transform_pointers(memory_line, updated_original_nodes)
    
    # Handles the animation for showing nodes
    def animate_nodes(self, nodes_left, nodes_right, nodes_left_head, nodes_right_head, nodes_left_headarrow, nodes_right_headarrow):

        self.play(FadeIn(nodes_left_head), FadeIn(nodes_right_head), FadeIn(nodes_left_headarrow), FadeIn(nodes_right_headarrow))
        # Loop through both left and right lists at the same time (since the length is the same)
        for i in range(len(nodes_left)):  
            left_node = nodes_left[i]
            right_node = nodes_right[i]

            # For the first 3 nodes, animate them simultaneously
            if i < 3:
                # both left and right nodes at the same time
                self.play(FadeIn(left_node, run_time=0.3), FadeIn(right_node, run_time=0.3))

                # Animate the set_next arrows for both sides (if i > 0)
                if i > 0:
                    arrow_left = nodes_left[i - 1].set_next(left_node, (i - 1) // 10, i // 10)
                    arrow_right = nodes_right[i - 1].set_next(right_node, (i - 1) // 10, i // 10)
                    self.play(FadeIn(arrow_left, run_time=0.3), FadeIn(arrow_right, run_time=0.3))

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
    
    # Determines the correct method for deleting a node
    def delete_node(self, linked_list, delete_idx, headtext, headarrow):
        if delete_idx == 0:
            self.delete_node_head(linked_list, delete_idx, headtext, headarrow)
        elif delete_idx == len(linked_list.nodes) - 1:
            self.delete_node_tail(linked_list, delete_idx)
        else:
            self.delete_node_row(linked_list, delete_idx)

    # Determines the correct method for deleting a node with shifting
    def delete_node_shift(self, linked_list_shift, delete_idx, headtext, headarrow):
        if delete_idx == 0:
            self.delete_node_head_shift(linked_list_shift, delete_idx, headtext, headarrow)
        elif delete_idx == len(linked_list_shift.nodes) - 1:
            self.delete_node_tail_shift(linked_list_shift, delete_idx, headtext, headarrow)
        else:
            self.delete_node_row_shift(linked_list_shift, delete_idx, headtext, headarrow)

    # Handles static head deletion 
    def delete_node_head(self, linked_list, delete_idx, headtext, headarrow):
        # Find the reference node for deletion + color code it
        node_head = linked_list.nodes[delete_idx]
        
        textfunc = Text(f"delete() from head position", font_size = 42)
        textfunc.move_to(ORIGIN + UP * 10.1)
        self.play(
            FadeIn(textfunc),
            node_head.box.animate.set_fill(GREEN, opacity=0.35),
        ) 
        self.play(FadeOut(textfunc))
        self.play(
            FadeOut(node_head.box),
            FadeOut(node_head.text),
            FadeOut(node_head.next_arrow),
            headtext.animate.shift(RIGHT * 2 + DOWN * 0.05),
            headarrow.animate.shift(RIGHT * 2 + DOWN * 0.05)
        )
        linked_list.nodes.pop(delete_idx)

    # Handles shifting head deletion 
    def delete_node_head_shift(self, linked_list_shift, idx, headtext, headarrow):
        # Find the reference nodes for insertion + color code them
            node_head = linked_list_shift.nodes[idx] 

            textfunc = Text(f"delete() from head position", font_size = 42)
            textfunc.move_to(ORIGIN + UP * 10.1)
            self.play(
                node_head.box.animate.set_fill(GREEN, opacity=0.35),
                FadeIn(textfunc)
            )

            self.play(
                FadeOut(textfunc),
                FadeOut(node_head.box),
                FadeOut(node_head.text),
                FadeOut(node_head.next_arrow),
            )
            
            shifts = shift_nodes_to_the_left(linked_list_shift.nodes, idx)

            self.play(shifts)

            if len(linked_list_shift.nodes) < 10:
                shift_nodes_small(self, linked_list_shift.nodes, idx, headtext, headarrow)

    # Handles static tail deletion 
    def delete_node_tail(self, linked_list, delete_idx):
        # Find the reference node for deletion + color code it
        node_tail = linked_list.nodes[delete_idx] 
        node_new_tail = linked_list.nodes[delete_idx - 1]    

        textfunc = Text(f"delete() from tail position", font_size = 42)
        textfunc.move_to(ORIGIN + UP * 10.1)

        self.play(
            node_tail.box.animate.set_fill(GREEN, opacity=0.35),
            FadeIn(textfunc)
        )

        self.play(FadeOut(textfunc))

        new_arrow = Arrow(
            start=node_new_tail.next_arrow.get_start(), 
            end=node_new_tail.next_arrow.get_end(), 
            tip_shape=ArrowCircleFilledTip,
            buff=0,
            tip_length=0.2,
        )

        self.play(
            FadeOut(node_tail.box),
            FadeOut(node_tail.text),
            FadeOut(node_tail.next_arrow),
            Transform(node_new_tail.next_arrow, new_arrow)
        )

        linked_list.nodes.pop(delete_idx)
    
    # Handles shifting tail deletion 
    def delete_node_tail_shift(self, linked_list_shift, idx, headtext, headarrow):
        # Find the reference node for deletion + color code it
        node_tail = linked_list_shift.nodes[idx] 
        node_new_tail = linked_list_shift.nodes[idx - 1]  

        textfunc = Text(f"delete() from tail position", font_size = 42)
        textfunc.move_to(ORIGIN + UP * 10.1)

        self.play(
            node_tail.box.animate.set_fill(GREEN, opacity=0.35),
            FadeIn(textfunc)
        )

        self.play(FadeOut(textfunc))

        new_arrow = Arrow(
            start=node_new_tail.next_arrow.get_start(), 
            end=node_new_tail.next_arrow.get_end(), 
            tip_shape=ArrowCircleFilledTip,
            buff=0,
            tip_length=0.2,
        )

        self.play(
            FadeOut(node_tail.box),
            FadeOut(node_tail.text),
            FadeOut(node_tail.next_arrow),
            Transform(node_new_tail.next_arrow, new_arrow)
        )

        # Shift if the amount of rows has chenged
        if idx == 10 or idx == 20:
            del linked_list_shift.nodes[idx]
            shifts = []

            shifts.append(headtext.animate.shift(DOWN * 1.5))
            shifts.append(headarrow.animate.shift(DOWN * 1.5))

            # Nodes shift up + their arrows to be centered
            for i, node in enumerate(linked_list_shift.nodes): 
                shifts.append(node.animate.shift(DOWN * 1.5))
                if i < len(linked_list_shift.nodes) - 1: 
                    shifts.append(node.next_arrow.animate.shift(DOWN * 1.5))
                else:
                    shifts.append(
                        node.next_arrow.animate.put_start_and_end_on(
                            linked_list_shift.nodes[idx - 1].get_bottom() + DOWN * 1.5 + DOWN * 0.1,
                            linked_list_shift.nodes[idx - 1].get_bottom()  + DOWN * 2.5 + UP * 0.1
                        )
                    )
                
            self.play(
                *shifts 
            )

        if len(linked_list_shift.nodes) < 10:
            shift_nodes_small(self, linked_list_shift.nodes, idx, headtext, headarrow)
    
    # Handles static row deletion 
    def delete_node_row(self, linked_list, delete_idx):
        # Find the reference node for deletion + color code it
        node_to_delete = linked_list.nodes[delete_idx] 
        node_before = linked_list.nodes[delete_idx - 1]
        node_after = linked_list.nodes[delete_idx + 1]
        
        textfunc = Text(f"delete({node_to_delete.text.text})", font_size = 42)
        textfunc.move_to(ORIGIN + UP * 10.1)

        self.play(
            FadeIn(textfunc),
            node_to_delete.box.animate.set_fill(GREEN, opacity=0.35),
        ) 

        self.play(FadeOut(textfunc))

        if node_to_delete.row % 2 == 0:
            if delete_idx == 9:
                long_arrow = CurvedArrow(
                    start_point=node_before.get_right() + RIGHT * 0.1, 
                    end_point=node_after.get_top() + UP * 0.1, 
                    angle=-TAU/4, 
                    tip_length=0.2
                )
            elif delete_idx == 20:
                long_arrow = CurvedArrow(
                    start_point=node_before.get_bottom() + DOWN * 0.1, 
                    end_point=node_after.get_left() + LEFT * 0.1, 
                    tip_length=0.2
                )
            else:
                long_arrow = Arrow(
                    start=node_before.get_right(), 
                    end=node_after.get_left(), 
                    buff=0.1,
                    tip_length=0.2,
                )
        else:
            if delete_idx == 10:
                long_arrow = CurvedArrow(
                    start_point=node_before.get_bottom() + DOWN * 0.1, 
                    end_point=node_after.get_right() + RIGHT * 0.1, 
                    angle=-TAU/4, 
                    tip_length=0.2
                )
            elif delete_idx == 19:
                long_arrow = CurvedArrow(
                    start_point=node_before.get_left() + LEFT * 0.1, 
                    end_point=node_after.get_top() + UP * 0.1, 
                    tip_length=0.2
                )
            else:
                long_arrow = Arrow(
                    start=node_before.get_left(), 
                    end=node_after.get_right(), 
                    buff=0.1,
                    tip_length=0.2,
                )

        self.play(
            FadeOut(node_to_delete.box),
            FadeOut(node_to_delete.text),
            FadeOut(node_to_delete.next_arrow),
            Transform(node_before.next_arrow, long_arrow)
        )

    # Handles shifting row deletion 
    def delete_node_row_shift(self, linked_list_shift, idx, headtext, headarrow):
        # Find the reference node for deletion + color code it
        node_to_delete = linked_list_shift.nodes[idx] 
        node_before = linked_list_shift.nodes[idx - 1]
        node_after = linked_list_shift.nodes[idx + 1]
        
        textfunc = Text(f"delete({node_to_delete.text.text})", font_size = 42)
        textfunc.move_to(ORIGIN + UP * 10.1)
        self.play(
            FadeIn(textfunc),
            node_to_delete.box.animate.set_fill(GREEN, opacity=0.35),
        ) 

        self.play(FadeOut(textfunc))

        if node_to_delete.row % 2 == 0:
            if idx == 9:
                long_arrow = CurvedArrow(
                    start_point=node_before.get_right() + RIGHT * 0.1, 
                    end_point=node_after.get_top() + UP * 0.1, 
                    angle=-TAU/4, 
                    tip_length=0.2
                )
            elif idx == 20:
                long_arrow = CurvedArrow(
                    start_point=node_before.get_bottom() + DOWN * 0.1, 
                    end_point=node_after.get_left() + LEFT * 0.1, 
                    tip_length=0.2
                )
            else:
                long_arrow = Arrow(
                    start=node_before.get_right(), 
                    end=node_after.get_left(), 
                    buff=0.1,
                    tip_length=0.2,
                )
        else:
            if idx == 10:
                long_arrow = CurvedArrow(
                    start_point=node_before.get_bottom() + DOWN * 0.1, 
                    end_point=node_after.get_right() + RIGHT * 0.1, 
                    angle=-TAU/4, 
                    tip_length=0.2
                )
            elif idx == 19:
                long_arrow = CurvedArrow(
                    start_point=node_before.get_left() + LEFT * 0.1, 
                    end_point=node_after.get_top() + UP * 0.1, 
                    tip_length=0.2
                )
            else:
                long_arrow = Arrow(
                    start=node_before.get_left(), 
                    end=node_after.get_right(), 
                    buff=0.1,
                    tip_length=0.2,
                )

        self.play(
            FadeOut(node_to_delete.box),
            FadeOut(node_to_delete.text),
            FadeOut(node_to_delete.next_arrow),
            Transform(node_before.next_arrow, long_arrow)
        )

        shifts = shift_nodes_to_the_left(linked_list_shift.nodes, idx)

        if node_to_delete.row % 2 == 0:
            if idx == 9:
                arrow_after_shift = Arrow(
                    start=node_before.get_right(), 
                    end=node_after.get_left() + UP * 3, 
                    buff=0.1,
                    tip_length=0.2
                )
            elif idx == 20:
                arrow_after_shift = Arrow(
                    start=node_before.get_bottom(), 
                    end=node_after.get_top() + LEFT * 2, 
                    buff=0.1,
                    tip_length=0.2
                )
            else:
                arrow_after_shift = Arrow(
                    start=node_before.get_right(), 
                    end=node_after.get_left() + LEFT * 2, 
                    buff=0.1,
                    tip_length=0.2,
                )
        else:
            if idx == 10:
                arrow_after_shift = Arrow(
                    start=node_before.get_bottom(), 
                    end=node_after.get_top() + RIGHT * 2,
                    buff=0.1,
                    tip_length=0.2
                )
            elif idx == 19:
                arrow_after_shift = Arrow(
                    start=node_before.get_left(), 
                    end=node_after.get_right() + UP * 3, 
                    buff=0.1,
                    tip_length=0.2
                )
            else:
                arrow_after_shift = Arrow(
                    start=node_before.get_left(), 
                    end=node_after.get_right() + RIGHT * 2, 
                    buff=0.1,
                    tip_length=0.2,
                )

        self.play(
            shifts,
            Transform(node_before.next_arrow, arrow_after_shift)
        )

        if len(linked_list_shift.nodes) < 10:
            shift_nodes_small(self, linked_list_shift.nodes, idx, headtext, headarrow)

    # Handles head deletion in memory unites line
    def delete_memory_units_head(self, nodes, idx, arrows):
        # Find head and new head nodes
        node_head = nodes.original_nodes[idx]
        node_new_head = nodes.original_nodes[idx + 1]
        headtext = nodes.headtext 
        headarrow = nodes.headarrow

        textfunc = Text(f"delete() from head position", font_size = 36)
        textfunc.next_to(nodes[0], UP, buff=2.75)
        textfunc.align_to(nodes[0]) 

        self.play(
            node_head.box.animate.set_fill(GREEN, opacity=0.35),
            nodes.index_labels[idx][0].animate.set_fill(GREEN, opacity=1).set_stroke(GREEN),
            node_head.next_arrow.animate.shift(DOWN * 0.01).set_color(GREEN).set_stroke(width=10),
            FadeIn(textfunc),
            *([
                AnimationGroup(
                    arrow.animate.set_stroke(opacity=0.35),
                    arrow.tip.animate.set_fill(opacity=0.35)
                )
                for arrow in arrows 
                if arrow is not node_new_head.next_arrow 
                and arrow is not node_head.next_arrow 
                and not isinstance(arrow, Circle)
            ] if len(nodes) > 3 else [])
        )

        self.play(FadeOut(textfunc))

        # Move the head pointer to a new head node + color code the transformation
        self.play(
            nodes.index_labels[idx][0].animate.set_fill(PURPLE, opacity=1).set_stroke(PURPLE),
            node_head.box.animate.set_fill(PURPLE, opacity=0),
            FadeOut(node_head.text), 
            FadeOut(node_head.next_arrow),
            headtext.animate.move_to(node_new_head.get_top() + UP * 2.1),
            headarrow.animate.move_to(node_new_head.get_top() + UP * 1.55),
            node_new_head.box.animate.set_fill(GREEN, opacity=0.35),
            nodes.index_labels[idx + 1][0].animate.set_fill(GREEN, opacity=1).set_stroke(GREEN),
        )

        if len(nodes) >= 4:
            animations = [
                AnimationGroup(
                    arrow.animate.set_stroke(opacity=1), 
                    arrow.tip.animate.set_fill(opacity=1)
                )
                for arrow in arrows 
                if arrow is not node_new_head.next_arrow 
                and arrow is not node_head.next_arrow 
                and not isinstance(arrow, Circle)
            ]
            if animations:
                self.play(*animations)

        # Update the list of original nodes
        del nodes.original_nodes[idx]
        return nodes.original_nodes
    
    # Handles head deletion in memory unites line
    def delete_memory_units(self, nodes, idx, arrows):
        # Find the memory units for insertion + color code them
        node = nodes.original_nodes[idx] 
        node_before = nodes.original_nodes[idx - 1]
        node_after = nodes.original_nodes[idx + 1]

        textfunc = Text(f"delete({node.text.text})", font_size = 36)
        textfunc.next_to(nodes[0], UP, buff=2.75)
        textfunc.align_to(nodes[0])

        self.play(
            node.box.animate.set_fill(GREEN, opacity=0.35),
            node.next_arrow.animate.shift(DOWN * 0.01).set_color(GREEN).set_stroke(width=10),
            nodes.index_labels[idx][0].animate.set_fill(GREEN, opacity=1).set_stroke(GREEN),
            FadeIn(textfunc)
        )

        self.play(FadeOut(textfunc))

        # Creating an arrow to a new node
        node_before_x = node_before.get_center()[0]
        node_after_x = node_after.get_center()[0]

        if node_before_x < node_after_x:
            arrow_new = CurvedArrow(
                start_point=node_before.next_arrow.get_start(),
                end_point=node_after.get_bottom() + LEFT * 0.25,
                angle=TAU/4
            )
        else:
            arrow_new = CurvedArrow(
                start_point=node_before.next_arrow.get_start(),
                end_point=node_after.get_bottom() + LEFT * 0.25,
                angle=-TAU/4
            )

        arrow_new.set_color(GREEN)
        arrow_new.set_stroke(width=10)

        self.play(
            FadeOut(node.text), 
            FadeOut(node.next_arrow),
            FadeOut(node.next_arrow.tip),
            node.box.animate.set_fill(PURPLE, opacity=0),
            nodes.index_labels[idx][0].animate.set_fill(PURPLE, opacity=1).set_stroke(PURPLE),
            node_before.box.animate.set_fill(GREEN, opacity=0.35),
            node_after.box.animate.set_fill(GREEN, opacity=0.35),
            nodes.index_labels[idx - 1][0].animate.set_fill(GREEN, opacity=1).set_stroke(GREEN),
            nodes.index_labels[idx + 1][0].animate.set_fill(GREEN, opacity=1).set_stroke(GREEN),
            Transform(node_before.next_arrow, arrow_new),
            *[
            AnimationGroup(
                arrow.animate.set_stroke(opacity=0.35),
                arrow.tip.animate.set_fill(opacity=0.35)
            )
            for arrow in arrows 
                if arrow is not node_before.next_arrow and arrow is not node.next_arrow and not isinstance(arrow, Circle)
            ]
        )

        self.wait(1)

        self.play(
            node_before.next_arrow.animate.set_color(WHITE).set_stroke(width=4),
            node_before.next_arrow.tip.animate.set_color(WHITE).set_stroke(width=0),
            *[
            AnimationGroup(
                arrow.animate.set_stroke(opacity=1), 
                arrow.tip.animate.set_fill(opacity=1)
            )
            for arrow in arrows 
                if arrow is not node_before.next_arrow and arrow is not node.next_arrow and not isinstance(arrow, Circle)
            ]
        )

        # Update the list of original nodes
        del nodes.original_nodes[idx]
        return nodes.original_nodes
    
    # Handles tail deletion in memory unites line
    def delete_memory_units_tail(self, nodes, idx, arrows):
        # Find the memory units for insertion + color code them
        node_tail = nodes.original_nodes[idx]  
        node_new_tail = nodes.original_nodes[idx - 1]  

        textfunc = Text(f"delete() from tail position", font_size = 36)
        textfunc.next_to(nodes[0], UP, buff=2.75)
        textfunc.align_to(nodes[0])

        self.play(
            node_tail.box.animate.set_fill(GREEN, opacity=0.35),
            nodes.index_labels[idx][0].animate.set_fill(GREEN, opacity=1).set_stroke(GREEN),
            FadeIn(textfunc),
            *[
                AnimationGroup(
                    arrow.animate.set_stroke(opacity=0.35),
                    arrow.tip.animate.set_fill(opacity=0.35)
                )
                for arrow in arrows 
                    if arrow is not node_new_tail.next_arrow and not isinstance(arrow, Circle)
            ]
        )

        self.play(FadeOut(textfunc))

        self.play(
            nodes.index_labels[idx][0].animate.set_fill(PURPLE, opacity=1).set_stroke(PURPLE),
            node_tail.box.animate.set_fill(PURPLE, opacity=0),
            FadeOut(node_tail.text), 
            FadeOut(arrows[-1])
        )

        arrows[-1].move_to(node_new_tail.get_bottom() + RIGHT * 0.25 + [0, 0.5, 0])
        
        self.play(
            node_new_tail.box.animate.set_fill(GREEN, opacity=0.35),
            nodes.index_labels[idx - 1][0].animate.set_fill(GREEN, opacity=1).set_stroke(GREEN),
            Transform(node_new_tail.next_arrow, arrows[-1]),
            *[
            AnimationGroup(
                arrow.animate.set_stroke(opacity=1), 
                arrow.tip.animate.set_fill(opacity=1)
            )
            for arrow in arrows 
                if arrow is not node_new_tail.next_arrow and not isinstance(arrow, Circle)
            ]
        )

        # Update the list of original nodes
        del nodes.original_nodes[idx]
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

def shift_nodes_small(scene, nodes, idx, headtext, headarrow):
    del nodes[idx]
    shift = RIGHT * 1 if len(nodes) < 9 else RIGHT * 0.5
    shifts = []

    shifts.append(headtext.animate.shift(shift))
    shifts.append(headarrow.animate.shift(shift))

    for node in nodes:
        shifts.append(node.animate.shift(shift))
        if node.next_arrow:
            shifts.append(node.next_arrow.animate.shift(shift))

    scene.play(*shifts)

def shift_nodes_to_the_left(nodes, idx):
    shifts = []

    for i in range(idx + 1, len(nodes)):
        node_i = nodes[i]
        node_prev = nodes[i - 1]

        # Shift node_i to the previous node's position
        shifts.append(node_i.animate.move_to(node_prev.get_center()))

        # Update the next_arrow
        if node_i.next_arrow:
            # Even lines without edge cases
            if node_i.row % 2 == 0 and i != 9 and i != 20 and i != 29:
                shifts.append(node_i.next_arrow.animate.shift(LEFT * 2))
            # From odd to even line — short arrow
            elif i == 9 or i == 29:
                # Last node pointer
                if i == len(nodes) - 1:
                    shifts.append(node_i.next_arrow.animate.put_start_and_end_on(
                        node_i.get_right() + LEFT * 2 + RIGHT * 0.1,
                        node_i.get_right() + + LEFT * 1 + LEFT * 0.1
                    ))
                else:
                    node_next = nodes[i + 1]
                    shifts.append(node_i.next_arrow.animate.put_start_and_end_on(
                        node_i.get_right() + LEFT * 2 + RIGHT * 0.1,
                        node_next.get_left() + UP * 3 + LEFT * 0.1
                    ))
            # From odd to even line — long arrow
            elif i == 10:
                # Last node pointer
                if i == len(nodes) - 1:
                    shifts.append(node_i.next_arrow.animate.put_start_and_end_on(
                        node_i.get_bottom() + UP * 3 + DOWN * 0.1,
                        node_i.get_bottom() + UP * 0.1 + UP * 2
                    ))
                else:
                    node_next = nodes[i + 1]
                    shifts.append(node_i.next_arrow.animate.put_start_and_end_on(
                        node_i.get_bottom() + UP * 3 + DOWN * 0.1,
                        node_next.get_top() + UP * 0.1 + RIGHT * 2
                    ))
            # From even to odd line — short arrow
            elif i == 19:
                if i == len(nodes) - 1:
                    shifts.append(node_i.next_arrow.animate.put_start_and_end_on(
                        node_i.get_left() + RIGHT * 2 + LEFT * 0.1,
                        node_i.get_right() + RIGHT * 0.1
                    ))
                else:
                    node_next = nodes[i + 1]
                    shifts.append(node_i.next_arrow.animate.put_start_and_end_on(
                        node_i.get_left() + RIGHT * 2 + LEFT * 0.1,
                        node_next.get_right() + UP * 3 + RIGHT * 0.1
                    ))
            # From even to odd line — long arrow
            elif i == 20:
                if i == len(nodes) - 1:
                    shifts.append(node_i.next_arrow.animate.put_start_and_end_on(
                        node_i.get_bottom() + UP * 3 + DOWN * 0.1,
                        node_i.get_bottom() + UP * 2 + UP * 0.1
                    ))
                else:
                    node_next = nodes[i + 1]
                    shifts.append(node_i.next_arrow.animate.put_start_and_end_on(
                        node_i.get_bottom() + UP * 3 + DOWN * 0.1,
                        node_next.get_top() + LEFT * 2 + UP * 0.1
                    ))
            else:
                shifts.append(node_i.next_arrow.animate.shift(RIGHT * 2))

    return shifts
