from manim import *
from node_basic import LinkedListNodeBasic
from node_closeup import LinkedListNodeCloseup

class LinkedListShiftScene(MovingCameraScene):
    def construct(self):
        # Show animation without cropping
        scale_factor = 1.5
        self.camera.frame_width = 14 * scale_factor  # Default width is 14
        self.camera.frame_height = self.camera.frame_width / 1.78  # Keep 16:9 aspect ratio
        self.camera.frame_center = ORIGIN  # Keep centered

        # Get input from user
        node_values = input("Enter node letters separated by space (e.g., A B C D, min = 2, max = 29): ").split()
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

        # Animate nodes appearance
        self.animate_nodes(nodes, headtext, headarrow)

        self.wait(1)

        self.delete_node(nodes, delete_idx, headtext, headarrow)

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
        if len(nodes) in [10, 20, 30]:
            last_node.set_next(None, last_node.row, last_node.row + 1)
        else:
            last_node.set_next(None, last_node.row, last_node.row)
        self.play(FadeIn(last_node.next_arrow, run_time=0.1))

    def delete_node(self, nodes, delete_idx, headtext, headarrow):
        # Determines the correct method for inserting a node and calls it.
        self.delete_node_head(nodes, delete_idx, headtext, headarrow)

        # if (insert_idx1 == 9 or insert_idx1 == 19) and insert_idx1 != len(nodes) - 1:
        #     self.insert_node_inbetween_lines(nodes, insert_idx1, insert_idx2, new_letter, headtext, headarrow)
        # elif insert_idx2 == 0:
        #     self.insert_node_head(nodes, insert_idx2, new_letter, headtext, headarrow)
        # elif insert_idx1 == len(nodes) - 1:
        #     self.insert_node_tail(nodes, insert_idx1, new_letter, headtext, headarrow)
        # else:
        #     self.insert_node_row(nodes, insert_idx1, insert_idx2, new_letter, headtext, headarrow)

    def delete_node_head(self, nodes, idx, headtext, headarrow):
        # Find the reference nodes for insertion + color code them
            node_head = nodes[idx] 
            node_new_head = nodes[idx + 1] 
            node_for_zoom_arrow = nodes[idx + 2] 

            textfunc = Text(f"delete() from head position", font_size = 36)
            textfunc.to_edge(UP).shift(UP * 1)
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
            
            shifts = shift_nodes_to_the_left(nodes, idx)

            self.play(shifts)

            if len(nodes) < 10:
                shift_nodes_small(self, nodes, idx, headtext, headarrow)

            self.zoom_in_head(node_head, node_new_head, node_for_zoom_arrow)

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
 
def shift_nodes_to_the_left(nodes, idx2):
    shifts = []

    for i in range(idx2 + 1, len(nodes)):
        node_i = nodes[i]
        node_prev = nodes[i - 1]

        # Shift node_i to the previous node's position
        if i == len(nodes) - 1:
            if i == 10 or i == 20:
                shifts.append(node_i.animate.shift(UP * 3))
            elif node_i.row % 2 != 0:
                shifts.append(node_i.animate.shift(RIGHT * 2))
            else:
                shifts.append(node_i.animate.shift(LEFT * 2))
        else:
            shifts.append(node_i.animate.move_to(node_prev.get_center()))

        # Update the next_arrow
        if node_i.next_arrow:
            # Even lines without edge cases
            if node_i.row % 2 == 0 and i != 9 and i != 10 and i != 20 and i != 29:
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
