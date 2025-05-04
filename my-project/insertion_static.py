from manim import *
from linked_list_vgroup import LinkedListVGroup
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

        insert_idx1, insert_idx2 = map(int, input(
            f"Enter the two node indices where a new node should be inserted (0-based).\n"
            f"If you want to insert to the head – enter 0 0;\n"
            f"If you want to insert to the tail – enter the index of the last node (={last_index}) twice: "
        ).split())

        new_letter = input("Enter the new node letter: ")

        # Create and position nodes
        list = LinkedListVGroup(node_values)

        # Animate node appearance
        self.animate_nodes(list.nodes, list.headtext, list.headarrow)

        self.wait(1)

        # Insert function
        self.insert_node(list.nodes, insert_idx1, insert_idx2, new_letter, list.headtext, list.headarrow)

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
        
    def insert_node(self, nodes, insert_idx1, insert_idx2, new_letter, headtext, headarrow):
        #Determines the correct method for inserting a node and calls it.
        if (insert_idx1 == 9 or insert_idx1 == 19) and insert_idx1 != len(nodes) - 1:
            self.insert_node_inbetween_rows(nodes, insert_idx1, insert_idx2, new_letter)
        elif insert_idx2 == 0:
            self.insert_node_head(nodes, insert_idx2, new_letter, headtext, headarrow)
        elif insert_idx1 == len(nodes) - 1:
            self.insert_node_tail(nodes, insert_idx1, new_letter, headtext, headarrow)
        else:
            self.insert_node_row(nodes, insert_idx1, insert_idx2, new_letter)

    def insert_node_head(self, nodes, idx2, new_value, headtext, headarrow):
        # Find the reference nodes for insertion + color code them
            node2 = nodes[idx2]     

            textfunc = Text(f"insert() to head position", font_size = 36)
            textfunc.to_edge(UP).shift(UP * 1)
            self.play(
                node2.box.animate.set_fill(GREEN, opacity=0.35),
                FadeIn(textfunc)
            )

            self.play(FadeOut(textfunc))
            
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

            headarrow_updated = Arrow(
                start=headtext.get_left() + RIGHT * 2 + DOWN * 0.05,
                end=new_node.get_right(),
                tip_length=0.2,
                buff=0.1,
                color=YELLOW
            )

            self.play(
                FadeIn(new_node),
                FadeIn(new_node.next_arrow),
                new_node.box.animate.set_fill(GREEN_E, opacity=1),
                headtext.animate.shift(RIGHT * 2 + DOWN * 0.05),
                Transform(headarrow, headarrow_updated)
            )

            self.zoom_in_head(node2, new_node)

    def insert_node_tail(self, nodes, idx1, new_value, headtext, headarrow):
        # Find the reference nodes for insertion + color code them
        node1 = nodes[idx1]     

        textfunc = Text(f"insert() to tail position", font_size = 36)
        textfunc.to_edge(UP).shift(UP * 1)
        self.play(
            node1.box.animate.set_fill(GREEN, opacity=0.35),
            FadeIn(textfunc)
        )

        self.play(FadeOut(textfunc))
        
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

            shifts.append(headtext.animate.shift(UP * 1.5))
            shifts.append(headarrow.animate.shift(UP * 1.5))

            # Nodes shifts to center the structure
            for node in nodes: 
                shifts.append(node.animate.shift(UP * 1.5))
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
        
        if len(nodes) < 10:

            shift = LEFT * 1
            # Shift simultaneously
            shifts = []
            
            shifts.append(headtext.animate.shift(shift))
            shifts.append(headarrow.animate.shift(shift))
            
            # Nodes shift left by 1 unit + their arrows
            for node in nodes: 
                shifts.append(node.animate.shift(shift))
                shifts.append(node.next_arrow.animate.shift(shift))
                
            shifts.append(new_node.animate.shift(shift))
            shifts.append(new_node.next_arrow.animate.shift(shift))

            self.play(
                *shifts 
            )
        self.zoom_in_tail(idx1, node1, new_node)

    def insert_node_row(self, nodes, idx1, idx2, new_value):
        # Find the reference nodes for insertion + color code them
        node1 = nodes[idx1]
        node2 = nodes[idx2]     

        textfunc = Text(f"insert({node1.text.text}, {node2.text.text})", font_size = 36)
        textfunc.to_edge(UP).shift(UP * 1)
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
        if idx1 == 0 or idx1 == 10 or idx1 == 20:
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
            if idx1 == 0 or idx1 == 20:
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

        self.zoom_in_rows(idx1, node1, node2, new_node)

    def insert_node_inbetween_rows(self, nodes, idx1, idx2, new_value):
        # Find the reference nodes for insertion + color code them
        node1 = nodes[idx1]
        node2 = nodes[idx2]     

        textfunc = Text(f"insert({node1.text.text}, {node2.text.text})", font_size = 36)
        textfunc.to_edge(UP).shift(UP * 1)
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
        self.zoom_in_rows(idx1, node1, node2, new_node)

    def zoom_in_rows(self, idx1, node1, node2, new_node):

        position = (node1.get_center() + node2.get_center()) / 2
        background = Rectangle(
            width=self.camera.frame.get_width(),  
            height=self.camera.frame.get_height(),

        )
        background.set_fill(BLACK, opacity=1)
        background.set_stroke(opacity=0)
        node1_closeup = LinkedListNodeCloseup(node1.text.text, node1.row, node1.col).scale(0.6)
        node2_closeup = LinkedListNodeCloseup(node2.text.text, node2.row, node2.col).scale(0.6)

        # Positioning of nodes for in between rows
        if node1.row != node2.row:
            node1_closeup.shift(position + UP * 0.7)
            node2_closeup.shift(position + DOWN * 0.7)
            node1_closeup.next_arrow = Arrow(
                start=node1_closeup.get_bottom() + [0, 0.3, 0],
                end=node2_closeup.get_top(),
                tip_length=0.2,
                buff=0.04
            )
            node1_closeup.next_arrow.set_stroke(width=4)
        # Same row
        else:
            if node1.get_center()[0] < node2.get_center()[0]:
                node1_closeup.shift(position + LEFT * 2)
                node2_closeup.shift(position + RIGHT * 2)
            else:
                node1_closeup.shift(position + RIGHT * 2)
                node2_closeup.shift(position + LEFT * 2)
            node1_closeup.next_arrow = node1_closeup.set_next(node2_closeup, node1_closeup.row, node2_closeup.row)

        self.play(
            self.camera.frame.animate.move_to(position).set(width=node1.width*6),
            FadeIn(background),
            FadeIn(node1_closeup),
            FadeIn(node2_closeup),
            node1_closeup.box.animate.set_fill(GREEN, opacity=0.35),
            node2_closeup.box.animate.set_fill(GREEN, opacity=0.35),
        )

        self.play(FadeIn(node1_closeup.next_arrow))

        node_closeup = LinkedListNodeCloseup(new_node.text.text).scale(0.6)

        # Positioning for new node
        # Same row
        if node1.row == node2.row:
            if idx1 == 0 or idx1 == 10 or idx1 == 20:
                node_closeup.shift((node1_closeup.get_center() + node2_closeup.get_center()) / 2 + DOWN * 0.6)
            else:
                node_closeup.shift((node1_closeup.get_center() + node2_closeup.get_center()) / 2 + UP * 0.6)
        # From even row to odd
        else:
            if node1.row % 2 == 0:
                node_closeup.shift((node1_closeup.get_center() + node2_closeup.get_center()) / 2 + LEFT * 2)
            else:
                node_closeup.shift((node1_closeup.get_center() + node2_closeup.get_center()) / 2 + RIGHT * 2)
        
        node_closeup.next_arrow = node_closeup.set_next(node2_closeup, node1_closeup.row, node2_closeup.row)

        # Arrow to a new node
        # Same row right to left or from odd to even row
        if node1.get_center()[0] < node2.get_center()[0] or (node1.row != node2.row and node1.row == 1):
            arrow_to = Arrow(
                start=node1_closeup.get_bottom() + [0, 0.3, 0], 
                end=node_closeup.get_left() + [0, 0.3, 0],
                tip_length=0.2,
                buff=0.1 
            )
        else:
            arrow_to = Arrow(
                start=node1_closeup.get_bottom() + [0, 0.3, 0], 
                end=node_closeup.get_right() + [0, 0.3, 0],
                tip_length=0.2,
                buff=0.1 
            )
        
        self.play(
            FadeIn(node_closeup),
            node_closeup.box.animate.set_fill(GREEN, opacity=1),
            FadeIn(node_closeup.next_arrow),
            Transform(node1_closeup.next_arrow, arrow_to)
        )

        self.wait(1)

        self.play(
            self.camera.frame.animate.move_to(ORIGIN).set(width=14 * 1.5),
            FadeOut(background),
            FadeOut(node1_closeup),
            FadeOut(node2_closeup),
            FadeOut(node1_closeup.next_arrow),
            FadeOut(node_closeup),
            FadeOut(node_closeup.next_arrow),
        )

        self.wait(1)

    def zoom_in_head(self, node2, new_node):
        position = node2.get_center()
        background = Rectangle(
            width=self.camera.frame.get_width(),  
            height=self.camera.frame.get_height(),

        )
        background.set_fill(BLACK, opacity=1)
        background.set_stroke(opacity=0)
        node1_closeup = LinkedListNodeCloseup(node2.text.text, node2.row, node2.col).scale(0.6)
        node2_closeup = LinkedListNodeCloseup(node2.text.text, node2.row, node2.col).scale(0.6)
        node1_closeup.shift(position + DOWN * 0.8)
        node2_closeup.shift(position + RIGHT * 4 + DOWN * 0.8)
        node1_closeup.next_arrow = node1_closeup.set_next(node2_closeup, node1_closeup.row, node2_closeup.row)
        headtext = Text("HEAD", font_size=26, color=YELLOW)
        headtext.shift(position + UP * 1.2)
        headarrow = Arrow(
            start=headtext.get_bottom(), 
            end=node1_closeup.get_top(),
            buff=0.1,
            tip_length=0.2,
            color=YELLOW
        )

        self.play(
            self.camera.frame.animate.move_to(position).set(width=node2.width*6),
            FadeIn(background),
            FadeIn(node1_closeup),
            node1_closeup.box.animate.set_fill(GREEN, opacity=0.35),
            FadeIn(node1_closeup.next_arrow),
            FadeIn(headtext),
            FadeIn(headarrow)
        )

        node_closeup = LinkedListNodeCloseup(new_node.text.text).scale(0.6)
        node_closeup.shift(node1_closeup.get_left() + UP * 0.6 + LEFT * 1.5)
        node_closeup.next_arrow = node_closeup.set_next(node1_closeup, node1_closeup.row, node1_closeup.row)

        headarrow_updated = CurvedArrow(
            start_point=headtext.get_left() + LEFT * 0.1, 
            end_point=node_closeup.get_top() + UP * 0.1,
            tip_length=0.2,
            color=YELLOW
        )

        self.play(
            FadeIn(node_closeup),
            node_closeup.box.animate.set_fill(GREEN, opacity=1),
            Transform(headarrow, headarrow_updated)
        )

        self.play(FadeIn(node_closeup.next_arrow))

        self.wait(1)

        self.play(
            self.camera.frame.animate.move_to(ORIGIN).set(width=14 * 1.5),
            FadeOut(background),
            FadeOut(node1_closeup),
            FadeOut(node1_closeup.next_arrow),
            FadeOut(node_closeup),
            FadeOut(node_closeup.next_arrow),
            FadeOut(headtext),
            FadeOut(headarrow)
        )

        self.wait(1)

    def zoom_in_tail(self, idx1, node1, new_node):
        position = node1.get_center()
        background = Rectangle(
            width=self.camera.frame.get_width(),  
            height=self.camera.frame.get_height(),
        )
        background.set_fill(BLACK, opacity=1)
        background.set_stroke(opacity=0)
        node1_closeup = LinkedListNodeCloseup(node1.text.text, node1.row, node1.col).scale(0.6)
        node2_closeup = LinkedListNodeCloseup(node1.text.text, node1.row, node1.col).scale(0.6)
        
        # Positioning node2
        if idx1 == 9 or idx1 == 19:
            node2_closeup.shift(position + UP * 0.7)
        else:
            node2_closeup.shift(position)

        # Positioning the ingoing arrow to node2
        if idx1 == 10 or idx1 == 20:
            node1_closeup.shift(position + UP * 4)
            node1_closeup.next_arrow = Arrow(
                start=node1_closeup.get_bottom() + [0, 0.3, 0], 
                end=node2_closeup.get_top(),
                tip_length=0.2,
                buff=0.1 
            )
        else:
            if node1.row % 2 == 0:
                node1_closeup.shift(position + LEFT * 4)
            else:
                node1_closeup.shift(position + RIGHT * 4)
            
            node1_closeup.next_arrow = node1_closeup.set_next(node2_closeup, node1_closeup.row, node2_closeup.row)
        
        node_closeup = LinkedListNodeCloseup(new_node.text.text).scale(0.6)
        if idx1 == 9 or idx1 == 19:
            node_closeup.shift(node2_closeup.get_bottom() + DOWN * 1)
            node2_closeup.next_arrow = Arrow(
                start=node2_closeup.get_bottom() + [0, 0.3, 0], 
                end=node_closeup.get_top(),
                tip_length=0.2,
                buff=0.1 
            )
        else:  
            if node1.row % 2 == 0:
                node_closeup.shift(node2_closeup.get_right() + RIGHT * 1.5)
            else:
                node_closeup.shift(node2_closeup.get_left() + LEFT * 1.5)
            node2_closeup.next_arrow = node2_closeup.set_next(node_closeup, node2_closeup.row, node2_closeup.row)

        self.play(
            self.camera.frame.animate.move_to(position).set(width=node1.width*6),
            FadeIn(background),
            FadeIn(node2_closeup),
            FadeIn(node1_closeup.next_arrow),
            node2_closeup.box.animate.set_fill(GREEN, opacity=0.35)
        )

        self.play(
            FadeIn(node_closeup),
            node_closeup.box.animate.set_fill(GREEN, opacity=1)
        )

        self.play(FadeIn(node2_closeup.next_arrow))

        self.wait(1)

        self.play(
            self.camera.frame.animate.move_to(ORIGIN).set(width=14 * 1.5),
            FadeOut(background),
            FadeOut(node2_closeup),
            FadeOut(node2_closeup.next_arrow),
            FadeOut(node_closeup),
            FadeOut(node1_closeup.next_arrow)
        )

        self.wait(1)
