from manim import *

class LinkedListNodeBasic(VGroup):
    def __init__(self, value, row=None, col=None, **kwargs):
        super().__init__(**kwargs)
        self.box = Square(side_length=1, color=WHITE)
        self.text = Text(str(value), font_size=24).move_to(self.box.get_center())
        self.add(self.box, self.text)
        self.next_arrow = None
        self.row = row
        self.col = col

    def set_next(self, next_node, row1, row2):
        if self.next_arrow:
            self.remove(self.next_arrow)

        if row1 == row2:  # Same row connection
            if row1 % 2 == 0:  # Even row (Left to Right)
                start, end = self.get_right(), next_node.get_left()
            else:  # Odd row (Right to Left)
                start, end = self.get_left(), next_node.get_right()
        else:  # Connecting different rows
            if row1 % 2 == 0:  # Moving down from even row (Right to Left next)
                start, end = self.get_bottom(), next_node.get_top()
            else:  # Moving down from odd row (Left to Right next)
                start, end = self.get_bottom(), next_node.get_top()

        self.next_arrow = Arrow(start, end, buff=0.1, tip_length=0.2, color=WHITE)
        return self.next_arrow

class LinkedListStaticScene(Scene):
    def construct(self):
        # Show animation without cropping
        scale_factor = 1.5
        self.camera.frame_width = 14 * scale_factor  # Default width is 14
        self.camera.frame_height = self.camera.frame_width / 1.78  # Keep 16:9 aspect ratio
        self.camera.frame_center = ORIGIN  # Keep centered

        # Get input from user
        node_values = input("Enter distinctive node letters separated by space (e.g., A B C D, min = 5): ").split()
        insert_idx1, insert_idx2 = map(int, input("Enter the two node indices where a new node should be inserted (0-based).\nIf you want to insert to the head – enter 0 0;\nIf you want to insert to the tail - enter the index of the last node twice: ").split())
        new_letter = input("Enter the new node letter: ")

        # Constants
        NODE_SPACING = 2  # Horizontal spacing between nodes
        ROW_SPACING = 3   # Vertical spacing between rows

        # Create nodes
        nodes = [LinkedListNodeBasic(value, row=i//10, col=i%10) for i, value in enumerate(node_values)]

        # Place nodes in the correct position
        for i, node in enumerate(nodes):
            row = i // 10  # Determine the row index
            col = i % 10   # Determine the column index within the row

            if row % 2 == 0:  # Even row (left to right)
                x_pos = RIGHT * col * NODE_SPACING
            else:  # Odd row (right to left)
                x_pos = RIGHT * (9 - col) * NODE_SPACING

            y_pos = DOWN * row * ROW_SPACING  # Move downward for each new row
            node.move_to(x_pos + y_pos)  # Set final position

        # Center the whole structure
        if nodes:
            leftmost = min(node.get_left()[0] for node in nodes)  # X-coordinate of the leftmost node
            rightmost = max(node.get_right()[0] for node in nodes)  # X-coordinate of the rightmost node
            topmost = max(node.get_top()[1] for node in nodes)  # Y-coordinate of the topmost node
            bottommost = min(node.get_bottom()[1] for node in nodes)  # Y-coordinate of the bottommost node

            # Compute the center of the entire structure
            structure_center = np.array([(leftmost + rightmost) / 2, (topmost + bottommost) / 2, 0])

            # Compute shift vector to move structure center to ORIGIN
            shift_amount = ORIGIN - structure_center

            # Shift accordingly
            for node in nodes:
                node.shift(shift_amount)

        # Texts for code commands
        textfuncadd = Text("add()", font_size = 36) 
        textfuncadd.next_to(nodes[0], UP, buff=0.5)
        textfuncadd.align_to(nodes[0], LEFT)
        textfuncarrow = Text("nodes[i - 1].set_next(node[i])", font_size = 36) 
        textfuncarrow.next_to(nodes[0], UP, buff=0.5)
        textfuncarrow.align_to(nodes[0], LEFT)

        # Add nodes and create arrows
        for i, node in enumerate(nodes):
            if i < 3:
                # Full animation for the first three nodes
                self.play(FadeIn(node, run_time=0.3), FadeIn(textfuncadd, run_time=0.4))
                self.play(FadeOut(textfuncadd, run_time=0.3))
                if i > 0:
                    row1 = (i - 1) // 10
                    row2 = i // 10
                    arrow = nodes[i - 1].set_next(node, row1, row2)
                    self.play(FadeIn(arrow, run_time=0.3), FadeIn(textfuncarrow, run_time=0.4))
                    self.play(FadeOut(textfuncarrow, run_time=0.3))
            else:
                # Quick display for the rest of the nodes
                self.play(FadeIn(node, run_time=0.1))
                if i > 0:
                    row1 = (i - 1) // 10
                    row2 = i // 10
                    arrow = nodes[i - 1].set_next(node, row1, row2)
                    self.play(FadeIn(arrow, run_time=0.1))

        self.wait(1)

        # Call the refactored insert function
        self.insert_node(nodes, insert_idx1, insert_idx2, new_letter)
        
    def insert_node(self, nodes, insert_idx1, insert_idx2, new_letter):
        """Determines the correct method for inserting a node and calls it."""
        if insert_idx1 == 9 and insert_idx1 != len(nodes) - 1 or insert_idx1 == 19 and insert_idx1 != len(nodes) - 1:
            self.insert_node_inbetween_lines(nodes, insert_idx1, insert_idx2, new_letter)
        elif insert_idx2 == 0:
            self.insert_node_head(nodes, insert_idx2, new_letter)
        elif insert_idx1 == len(nodes) - 1:
            self.insert_node_tail(nodes, insert_idx1, new_letter)
        else:
            self.insert_node_row(nodes, insert_idx1, insert_idx2, new_letter)

    def insert_node_head(self, nodes, idx2, new_value):
        # Find the reference nodes for insertion + color code them
            node2 = nodes[idx2]     

            textfunc = Text(f"insert() to head position", font_size = 36)
            textfunc.next_to(nodes[0], UP, buff=0.5)
            textfunc.align_to(nodes[0], LEFT)
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

    def insert_node_tail(self, nodes, idx1, new_value):
        # Find the reference nodes for insertion + color code them
            node1 = nodes[idx1]     

            textfunc = Text(f"insert() to tail position", font_size = 36)
            textfunc.next_to(nodes[0], UP, buff=0.5)
            textfunc.align_to(nodes[0], LEFT)
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

                node1.next_arrow = node1.set_next(new_node, node1.row, new_node.row)

                self.play(
                    FadeIn(new_node),
                    new_node.box.animate.set_fill(GREEN_E, opacity=1)
                )

                self.play(FadeIn(node1.next_arrow))
                
                shifts = []

                # Nodes shifts to center the structure
                for node in nodes: 
                    shifts.append(node.animate.shift(UP * 1.5))
                    if node.next_arrow:
                        shifts.append(node.next_arrow.animate.shift(UP * 1.5))
                 
                shifts.append(new_node.animate.shift(UP * 1.5))

                self.play(
                    *shifts 
                )
            else:
                #if tail is odd row
                if node1.row % 2 != 0:
                    initial_position = node1.get_center() + LEFT * 2         
                    new_node.move_to(initial_position)
                    node1.next_arrow = node1.set_next(new_node, 1, 1)
                #if tail is even row
                else:
                    initial_position = node1.get_center() + RIGHT * 2
                    new_node.move_to(initial_position)
                    node1.next_arrow = node1.set_next(new_node, 0, 0)

                self.play(
                    FadeIn(new_node),
                    new_node.box.animate.set_fill(GREEN_E, opacity=1)
                )

                self.play(FadeIn(node1.next_arrow),)
            
            if len(nodes) < 10:
                # Shift simultaneously
                shifts = []

                # Nodes shift left by 1 unit + their arrows
                for node in nodes: 
                    shifts.append(node.animate.shift(LEFT * 1))
                    if node.next_arrow:
                        shifts.append(node.next_arrow.animate.shift(LEFT * 1))
                 
                shifts.append(new_node.animate.shift(LEFT * 1))

                self.play(
                    *shifts 
                )

    def insert_node_row(self, nodes, idx1, idx2, new_value):
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
    
    def insert_node_inbetween_lines(self, nodes, idx1, idx2, new_value):
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
