from manim import *
from node_basic import LinkedListNodeBasic
from node_closeup import LinkedListNodeCloseup

class LinkedListStaticScene(MovingCameraScene):
    def construct(self):
        # Show animation without cropping
        scale_factor = 1.5
        self.camera.frame_width = 14 * scale_factor  # Default width is 14
        self.camera.frame_height = self.camera.frame_width / 1.78  # Keep 16:9 aspect ratio
        self.camera.frame_center = ORIGIN  # Keep centered

        # Get input from user
        node_values = input("Enter node letters separated by space (e.g., A B C D, min = 3, max = 30): ").split()
        last_index = len(node_values) - 1

        delete_idx = int(input(
            f"Enter the index of the node to delete (0-based).\n"
            f"Valid range: 0 to {last_index}: "
        ))

        # Create and position nodes
        nodes = self.create_and_position_nodes(node_values)

        # Center the structure
        self.center_nodes(nodes)

        # Create head pointer
        headtext = Text("HEAD", font_size=26, color=YELLOW)
        headtext.next_to(nodes[0], UP, buff=1).align_to(nodes[0], LEFT)
        headarrow = Arrow(
            start=headtext.get_bottom(), 
            end=nodes[0].get_top(),
            buff=0.1,
            tip_length=0.2,
            color=YELLOW
        )

        # Animate node appearance
        self.animate_nodes(nodes, headtext, headarrow)

        self.wait(1)

        if delete_idx == 0:
            self.delete_head(nodes, delete_idx, headtext, headarrow)
        elif delete_idx == len(nodes) - 1:
            self.delete_tail(nodes, delete_idx)
        elif (delete_idx == 9 or delete_idx == 10 or delete_idx == 19 or delete_idx == 20) and delete_idx != len(nodes) - 1:
            self.delete_inbetween_rows(nodes, delete_idx)
        else:
            self.delete_rows(nodes, delete_idx)

    def create_and_position_nodes(self, node_values):
        NODE_SPACING = 2
        ROW_SPACING = 3
        
        nodes = [LinkedListNodeBasic(value, row=i//10, col=i%10) for i, value in enumerate(node_values)]
        
        for i, node in enumerate(nodes):
            row = i // 10
            col = i % 10
            
            x_pos = RIGHT * col * NODE_SPACING if row % 2 == 0 else RIGHT * (9 - col) * NODE_SPACING
            y_pos = DOWN * row * ROW_SPACING
            
            node.move_to(x_pos + y_pos)
        
        return nodes

    def center_nodes(self, nodes):
        if not nodes:
            return
        
        leftmost = min(node.get_left()[0] for node in nodes)
        if len(nodes) < 10:
            rightmost = max(node.get_right()[0] + 1 for node in nodes)
        else:
            rightmost = max(node.get_right()[0] for node in nodes)
        topmost = max(node.get_top()[1] for node in nodes)
        bottommost = min(node.get_bottom()[1] for node in nodes)

        structure_center = np.array([(leftmost + rightmost) / 2, (topmost + bottommost) / 2, 0])
        shift_amount = ORIGIN - structure_center

        for node in nodes:
            node.shift(shift_amount)

    def animate_nodes(self, nodes, headtext, headarrow):
        textfuncadd = Text("add()", font_size=36)
        textfuncarrow = Text("nodes[i - 1].set_next(node[i])", font_size=36)
        textfuncadd.to_edge(UP).shift(UP * 1)
        textfuncarrow.to_edge(UP).shift(UP * 1)

        self.play(FadeIn(headtext), FadeIn(headarrow))

        for i, node in enumerate(nodes):
            if i < 3:
                self.play(FadeIn(node, run_time=0.3), FadeIn(textfuncadd, run_time=0.4))
                self.play(FadeOut(textfuncadd, run_time=0.3))
                if i > 0:
                    arrow = nodes[i - 1].set_next(node, (i - 1) // 10, i // 10)
                    self.play(FadeIn(arrow, run_time=0.3), FadeIn(textfuncarrow, run_time=0.4))
                    self.play(FadeOut(textfuncarrow, run_time=0.3))
            else:
                self.play(FadeIn(node, run_time=0.1))
                if i > 0:
                    arrow = nodes[i - 1].set_next(node, (i - 1) // 10, i // 10)
                    self.play(FadeIn(arrow, run_time=0.1))
        
        # Last null pointer logic
        last_node = nodes[-1]
        if len(nodes) in [10, 20]:
            last_node.set_next(None, last_node.row, last_node.row + 1)
        else:
            last_node.set_next(None, last_node.row, last_node.row)
        self.play(FadeIn(last_node.next_arrow, run_time=0.1))
    
    def delete_head(self, nodes, delete_idx, headtext, headarrow):
        # Find the reference node for deletion + color code it
        node_head = nodes[delete_idx] 
        node_new_head = nodes[delete_idx + 1] 
        node_for_zoom_arrow = nodes[delete_idx + 2] 
        
        textfunc = Text(f"delete() from head position", font_size = 36)
        textfunc.to_edge(UP).shift(UP * 1)
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
        nodes.pop(delete_idx)

        self.zoom_in_head(node_head, node_new_head, node_for_zoom_arrow)

    def delete_tail(self, nodes, delete_idx):
        # Find the reference node for deletion + color code it
        node_tail = nodes[delete_idx] 
        node_new_tail = nodes[delete_idx - 1] 
        node_for_zoom_arrow = nodes[delete_idx - 2]   

        textfunc = Text(f"delete() from tail position", font_size = 36)
        textfunc.to_edge(UP).shift(UP * 1)

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

        nodes.pop(delete_idx)

        self.zoom_in_tail(delete_idx, node_tail, node_new_tail, node_for_zoom_arrow)

    def delete_rows(self, nodes, delete_idx):
        # Find the reference node for deletion + color code it
        node_to_delete = nodes[delete_idx] 
        node_before = nodes[delete_idx - 1]
        node_after = nodes[delete_idx + 1]
        
        textfunc = Text(f"delete({node_to_delete.text.text})", font_size = 36)
        textfunc.to_edge(UP).shift(UP * 1)
        self.play(
            FadeIn(textfunc),
            node_to_delete.box.animate.set_fill(GREEN, opacity=0.35),
        ) 

        self.play(FadeOut(textfunc))

        if node_to_delete.row % 2 == 0:
            long_arrow = Arrow(
                start=node_before.get_right(), 
                end=node_after.get_left(), 
                buff=0.1,
                tip_length=0.2,
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

        self.zoom_in_rows(node_to_delete, node_before, node_after)

    def delete_inbetween_rows(self, nodes, delete_idx):
        # Find the reference node for deletion + color code it
        node_to_delete = nodes[delete_idx] 
        node_before = nodes[delete_idx - 1]
        node_after = nodes[delete_idx + 1]

        textfunc = Text(f"delete({node_to_delete.text.text})", font_size = 36)
        textfunc.to_edge(UP).shift(UP * 1)
        self.play(
            FadeIn(textfunc),
            node_to_delete.box.animate.set_fill(GREEN, opacity=0.35),
        ) 

        self.play(FadeOut(textfunc))

        if delete_idx == 9:
            long_arrow = CurvedArrow(
                start_point=node_before.get_right() + RIGHT * 0.1, 
                end_point=node_after.get_top() + UP * 0.1, 
                angle=-TAU/4, 
                tip_length=0.2
            )
        elif delete_idx == 10:
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
            long_arrow = CurvedArrow(
                start_point=node_before.get_bottom() + DOWN * 0.1, 
                end_point=node_after.get_left() + LEFT * 0.1, 
                tip_length=0.2
            )
        
        self.play(
            FadeOut(node_to_delete.box),
            FadeOut(node_to_delete.text),
            FadeOut(node_to_delete.next_arrow),
            Transform(node_before.next_arrow, long_arrow)
        )

    def zoom_in_head(self, node_head, node_new_head, node_for_zoom_arrow):
        position = (node_head.get_center() + node_new_head.get_center()) / 2
        background = Rectangle(
            width=self.camera.frame.get_width(),  
            height=self.camera.frame.get_height(),

        )
        background.set_fill(BLACK, opacity=1)
        background.set_stroke(opacity=0)
        
        # Create nodes
        node_head_closeup = LinkedListNodeCloseup(node_head.text.text, node_head.row, node_head.col).scale(0.6)
        node_new_head_closeup = LinkedListNodeCloseup(node_new_head.text.text, node_new_head.row, node_new_head.col).scale(0.6)
        node_for_zoom_arrow = LinkedListNodeCloseup(node_for_zoom_arrow.text.text, node_for_zoom_arrow.row, node_for_zoom_arrow.col).scale(0.6)
        
        # Arange nodes on the screen + arrows
        node_head_closeup.shift(position + LEFT * 2 + DOWN * 0.8)
        node_new_head_closeup.shift(position + RIGHT * 2 + DOWN * 0.8)
        node_for_zoom_arrow.shift(position + RIGHT * 6 + DOWN * 0.8)
        node_head_closeup.next_arrow = node_head_closeup.set_next(node_new_head_closeup, node_head_closeup.row, node_new_head_closeup.row)
        node_new_head_closeup.next_arrow = node_new_head_closeup.set_next(node_for_zoom_arrow,  node_new_head_closeup.row, node_for_zoom_arrow.row)

        # Head pointer
        headtext = Text("HEAD", font_size=26, color=YELLOW)
        headtext.shift(position + LEFT * 2 + UP * 1.2)
        headarrow = Arrow(
            start=headtext.get_bottom(), 
            end=node_head_closeup.get_top(),
            buff=0.1,
            tip_length=0.2,
            color=YELLOW
        )

        # Display initial state
        self.play(
            self.camera.frame.animate.move_to(position).set(width=node_head.width*6),
            FadeIn(background),
            FadeIn(node_head_closeup),
            node_head_closeup.box.animate.set_fill(GREEN, opacity=0.35),
            FadeIn(node_head_closeup.next_arrow),
            FadeIn(node_new_head_closeup),
            FadeIn(node_new_head_closeup.next_arrow),
            FadeIn(node_for_zoom_arrow),
            FadeIn(headtext),
            FadeIn(headarrow)
        )

        # Perform deletion
        self.play(
            headtext.animate.shift(RIGHT * 2),
            headarrow.animate.shift(RIGHT * 2),
            node_new_head_closeup.animate.shift(LEFT * 2),
            node_new_head_closeup.next_arrow.animate.shift(LEFT * 2),
            node_for_zoom_arrow.animate.shift(LEFT * 2),
            FadeOut(node_head_closeup),
            FadeOut(node_head_closeup.next_arrow),
        )

        self.wait(1)

        # Clear screen and zoom out
        self.play(
            self.camera.frame.animate.move_to(ORIGIN).set(width=14 * 1.5),
            FadeOut(background),
            FadeOut(node_new_head_closeup),
            FadeOut(node_new_head_closeup.next_arrow),
            FadeOut(node_for_zoom_arrow),
            FadeOut(headtext),
            FadeOut(headarrow)
        )

        self.wait(1)

    def zoom_in_tail(self, delete_idx, node_tail, node_new_tail, node_for_zoom_arrow):
        position = (node_tail.get_center() + node_new_tail.get_center()) / 2
        background = Rectangle(
            width=self.camera.frame.get_width(),  
            height=self.camera.frame.get_height(),

        )
        background.set_fill(BLACK, opacity=1)
        background.set_stroke(opacity=0)

        # Create nodes
        node_tail_closeup = LinkedListNodeCloseup(node_tail.text.text, node_tail.row, node_tail.col).scale(0.6)
        node_new_tail_closeup = LinkedListNodeCloseup(node_new_tail.text.text, node_new_tail.row, node_new_tail.col).scale(0.6)
        node_for_zoom_arrow = LinkedListNodeCloseup(node_for_zoom_arrow.text.text, node_for_zoom_arrow.row, node_for_zoom_arrow.col).scale(0.6)
        
        # Shift for even rows
        if node_tail.row % 2 == 0:
            if delete_idx == 20:
                shift_tail = DOWN * 1
                shift_tail_new = UP * 0.7
                shift_before_tail_new = RIGHT * 6
            elif delete_idx == 21:
                shift_tail = RIGHT * 2
                shift_tail_new = LEFT * 2
                shift_before_tail_new = LEFT * 2 + UP * 4
            else:
                shift_tail = RIGHT * 2
                shift_tail_new = LEFT * 2
                shift_before_tail_new = LEFT * 6
        # Shift for odd rows
        else:
            if delete_idx == 10:
                shift_tail = DOWN * 1
                shift_tail_new = UP * 0.7
                shift_before_tail_new = LEFT * 6
            elif delete_idx == 11:
                shift_tail = LEFT * 2
                shift_tail_new = RIGHT * 2
                shift_before_tail_new = RIGHT * 2 + UP * 4
            else:
                shift_tail = LEFT * 2
                shift_tail_new = RIGHT * 2
                shift_before_tail_new = RIGHT * 6

        # Arange nodes on the screen + arrows
        node_tail_closeup.shift(position + shift_tail)
        node_new_tail_closeup.shift(position + shift_tail_new)
        node_for_zoom_arrow.shift(position + shift_before_tail_new)
        
        if delete_idx == 10 or delete_idx == 20:
            node_new_tail_closeup.next_arrow = Arrow(
                start=node_new_tail_closeup.get_bottom() + [0, 0.3, 0], 
                end=node_tail_closeup.get_top(),
                tip_length=0.2,
                buff=0.1 
            )
        else:
            node_new_tail_closeup.next_arrow = node_new_tail_closeup.set_next(node_tail_closeup,  node_new_tail_closeup.row, node_tail_closeup.row)
        
        if delete_idx == 11 or delete_idx == 21:
            node_for_zoom_arrow.next_arrow = Arrow(
                start=node_for_zoom_arrow.get_bottom() + [0, 0.3, 0], 
                end=node_new_tail_closeup.get_top(),
                tip_length=0.2,
                buff=0.1 
            )
        else:
            node_for_zoom_arrow.next_arrow = node_for_zoom_arrow.set_next(node_new_tail_closeup,  node_for_zoom_arrow.row, node_new_tail_closeup.row)
        
        # Display initial state
        self.play(
            self.camera.frame.animate.move_to(position).set(width=node_tail.width*6),
            FadeIn(background),
            FadeIn(node_tail_closeup),
            node_tail_closeup.box.animate.set_fill(GREEN, opacity=0.35),
            FadeIn(node_tail_closeup.next_arrow),
            FadeIn(node_new_tail_closeup),
            FadeIn(node_new_tail_closeup.next_arrow),
            FadeIn(node_for_zoom_arrow),
            FadeIn(node_for_zoom_arrow.next_arrow)
        )

       
        if delete_idx == 10 or delete_idx == 20:
            shift_deletion = 0
        # Shift for even rows
        elif node_tail.row % 2 == 0:
            shift_deletion = RIGHT * 2
        # Shift for odd rows
        else:
            shift_deletion = LEFT * 2
        
        # Perform deletion
        self.play(
            FadeOut(node_tail_closeup),
            FadeOut(node_new_tail_closeup.next_arrow)
        )
        self.play(
            node_new_tail_closeup.animate.shift(shift_deletion),
            node_for_zoom_arrow.animate.shift(shift_deletion),
            node_for_zoom_arrow.next_arrow.animate.shift(shift_deletion)
        )

        # Clear screen and zoom out
        self.play(
            self.camera.frame.animate.move_to(ORIGIN).set(width=14 * 1.5),
            FadeOut(background),
            FadeOut(node_new_tail_closeup),
            FadeOut(node_for_zoom_arrow),
            FadeOut(node_for_zoom_arrow.next_arrow)
        )

        self.wait(1)

    def zoom_in_rows(self, node_to_delete, node_before, node_after):
        position = node_to_delete.get_center()
        background = Rectangle(
            width=self.camera.frame.get_width(),  
            height=self.camera.frame.get_height(),

        )
        background.set_fill(BLACK, opacity=1)
        background.set_stroke(opacity=0)

        # Create nodes
        node_to_delete_closeup = LinkedListNodeCloseup(node_to_delete.text.text, node_to_delete.row, node_to_delete.col).scale(0.6)
        node_before_closeup = LinkedListNodeCloseup(node_before.text.text, node_before.row, node_before.col).scale(0.6)
        node_after_closeup = LinkedListNodeCloseup(node_after.text.text, node_after.row, node_after.col).scale(0.6)

        node_to_delete_closeup.shift(position)
        if node_before.get_center()[0] < node_after.get_center()[0]:
            node_before_closeup.shift(position + LEFT * 2)
            node_after_closeup.shift(position + RIGHT * 2)
        else:
            node_before_closeup.shift(position + RIGHT * 2)
            node_after_closeup.shift(position + LEFT * 2)

        node_before_closeup.next_arrow = node_before_closeup.set_next(node_to_delete_closeup,  node_before_closeup.row, node_to_delete_closeup.row)
        node_to_delete_closeup.next_arrow = node_to_delete_closeup.set_next(node_after_closeup,  node_to_delete_closeup.row, node_after_closeup.row)
        
        self.play(
            self.camera.frame.animate.move_to(position).set(width=node_to_delete.width*6),
            FadeIn(background),
            FadeIn(node_to_delete_closeup),
            FadeIn(node_to_delete_closeup.next_arrow),
            FadeIn(node_before_closeup),
            FadeIn(node_after_closeup),
            FadeIn(node_before_closeup.next_arrow),
            node_to_delete_closeup.box.animate.set_fill(GREEN, opacity=0.35),
        )

        animations = [
            FadeOut(node_to_delete_closeup),
            FadeOut(node_to_delete_closeup.next_arrow)
        ]

        if node_before.get_center()[0] < node_after.get_center()[0]:
            animations.append(
                node_before_closeup.next_arrow.animate.put_start_and_end_on(
                    node_before_closeup.next_arrow.get_start(),
                    node_after_closeup.get_left() + [0, 0.3, 0] + LEFT * 0.1
                )
            )
        else:
            # Add alternative animation if needed
            animations.append(
                node_before_closeup.next_arrow.animate.put_start_and_end_on(
                    node_before_closeup.next_arrow.get_start(),
                    # Different end point for the else case
                    node_after_closeup.get_right() + [0, 0.3, 0] + RIGHT * 0.1
                )
            )

        # Play all animations together
        self.play(*animations)

        # Clear screen and zoom out
        self.play(
            self.camera.frame.animate.move_to(ORIGIN).set(width=14 * 1.5),
            FadeOut(background),
            FadeOut(node_after_closeup),
            FadeOut(node_before_closeup),
            FadeOut(node_before_closeup.next_arrow)
        )

        self.wait(1)