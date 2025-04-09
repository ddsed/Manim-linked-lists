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

        # Animate node appearance
        self.animate_nodes(nodes, headtext, headarrow)

        self.wait(1)

        self.delete_head(nodes, delete_idx, headtext, headarrow)

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
        # Find the reference nodes for insertion + color code them
        node_head = nodes[delete_idx] 
        node_new_head = nodes[delete_idx + 1] 
        node_for_zoom_arrow = nodes[delete_idx + 2] 
        
        textfunc = Text(f"delete() from head position", font_size = 36)
        textfunc.to_edge(UP).shift(UP * 1)
        self.play(FadeIn(textfunc)) 
        self.play(
            node_head.box.animate.set_fill(GREEN, opacity=0.35),
            FadeOut(textfunc)
        )
        self.play(
            FadeOut(node_head.box),
            FadeOut(node_head.text),
            FadeOut(node_head.next_arrow),
            headtext.animate.shift(RIGHT * 2 + DOWN * 0.05),
            headarrow.animate.shift(RIGHT * 2 + DOWN * 0.05)
        )
        nodes.pop(delete_idx)

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
