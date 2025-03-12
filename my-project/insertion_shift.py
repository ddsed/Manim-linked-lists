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
        node_values = input("Enter distinctive node letters separated by space (e.g., A B C D, min = 5): ").split()
        insert_idx1, insert_idx2 = map(int, input("Enter the two node indices where a new node should be inserted (0-based).\nIf you want to insert to the head – enter 0 0;\nIf you want to insert to the tail - enter the index of the last node twice: ").split())
        new_letter = input("Enter the new node letter: ")

        # Create and position nodes
        nodes = self.create_and_position_nodes(node_values)

        # Center the structure
        self.center_nodes(nodes)

        # Animate node appearance
        self.animate_nodes(nodes)

        self.wait(1)

        self.insert_node(nodes, insert_idx1, insert_idx2, new_letter)

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
        rightmost = max(node.get_right()[0] for node in nodes)
        topmost = max(node.get_top()[1] for node in nodes)
        bottommost = min(node.get_bottom()[1] for node in nodes)

        structure_center = np.array([(leftmost + rightmost) / 2, (topmost + bottommost) / 2, 0])
        shift_amount = ORIGIN - structure_center

        for node in nodes:
            node.shift(shift_amount)

    def animate_nodes(self, nodes):
        textfuncadd = Text("add()", font_size=36)
        textfuncarrow = Text("nodes[i - 1].set_next(node[i])", font_size=36)
        textfuncadd.next_to(nodes[0], UP, buff=0.5).align_to(nodes[0], LEFT)
        textfuncarrow.next_to(nodes[0], UP, buff=0.5).align_to(nodes[0], LEFT)

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

    def insert_node(self, nodes, insert_idx1, insert_idx2, new_letter):
        #Determines the correct method for inserting a node and calls it.
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
            
            shifts = shift_nodes_to_the_right(nodes, idx2)

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

            if len(nodes) < 10:
                # Shift simultaneously after manipulation
                shifts = []

                # Nodes shift left by 1 unit + their arrows
                for node in nodes: 
                    shifts.append(node.animate.shift(LEFT * 1))
                    if node.next_arrow:
                        shifts.append(node.next_arrow.animate.shift(LEFT * 1))
                 
                shifts.append(new_node.animate.shift(LEFT * 1))
                shifts.append(new_node.next_arrow.animate.shift(LEFT * 1))

                self.play(
                    *shifts 
                )

            self.zoom_in_head(node2, new_node)

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
                FadeIn(node1.next_arrow),
                new_node.box.animate.set_fill(GREEN_E, opacity=1)
            )

            shifts = []

            # Nodes shift left by 1 unit + their arrows
            for node in nodes: 
                shifts.append(node.animate.shift(UP * 1.5))
                if node.next_arrow:
                    shifts.append(node.next_arrow.animate.shift(UP * 1.5))
                
            shifts.append(new_node.animate.shift(UP * 1.5))

            self.play(
                *shifts 
            )
        #if tail is odd row
        else:
            if node1.row % 2 != 0:
                initial_position = node1.get_left() + DOWN * 1.55
                new_node.move_to(initial_position)

                node1.next_arrow = CurvedArrow(
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
                    FadeIn(node1.next_arrow),
                    new_node.box.animate.set_fill(GREEN_E, opacity=1)
                )
                self.play(
                    new_node.animate.move_to(node1.get_center() + LEFT * 2),
                    Transform(node1.next_arrow, transformed_arrow)
                )
            #if tail is even row
            else:
                initial_position = node1.get_right() + DOWN * 1.55
                new_node.move_to(initial_position)

                node1.next_arrow = CurvedArrow(
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
                    FadeIn(node1.next_arrow),
                    new_node.box.animate.set_fill(GREEN_E, opacity=1)
                )

                self.play(
                    new_node.animate.move_to(node1.get_center() + RIGHT * 2),
                    Transform(node1.next_arrow, transformed_arrow)
                )
            
        if len(nodes) < 10:
            # Shift simultaneously before manipulation
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
        
        self.zoom_in_tail(idx1, node1, new_node)

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

        if len(nodes) < 10:
            # Shift simultaneously before manipulation
            shifts = []

            # Nodes from the first node to node1 left by 1 unit + their arrows
            for node in nodes[:nodes.index(node1) + 1]: 
                shifts.append(node.animate.shift(LEFT * 1))
                if node.next_arrow:
                    shifts.append(node.next_arrow.animate.shift(LEFT * 1)) 

            # Nodes from node2 to the last node right by 1 unit + their arrows
            for node in nodes[nodes.index(node2):]: 
                shifts.append(node.animate.shift(RIGHT * 1))
                if node.next_arrow:
                    shifts.append(node.next_arrow.animate.shift(RIGHT * 1))
            
            # New stretched arrow
            long_arrow = Arrow (
                start=node1.get_right() + LEFT * 1, 
                end=node2.get_left() + RIGHT * 1,
                tip_length=0.2,
                buff=0.1 
            )
        else:
            shifts = shift_nodes_to_the_right(nodes, idx2)
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
        # Displaying stretching the arrow simultaneously with shifting
        self.play(
            *shifts, 
            Transform(node1.next_arrow, long_arrow),
            run_time=1 
        )

        # Create the new node to insert
        new_node = LinkedListNodeBasic(new_value)
        if idx1 == 8:
            initial_position = node1.get_center() + RIGHT * 2
        elif idx1 == 18:
            initial_position = node1.get_center() + LEFT * 2
        else:
            initial_position = (node1.get_right() + node2.get_left()) / 2 + UP * 1.5
        
        new_node.move_to(initial_position)
        
        if idx1 == 8 or idx1 == 18:
            new_node.next_arrow = new_node.set_next(node2, 1, 2)
            self.play(
                FadeIn(new_node.next_arrow),
                FadeIn(new_node), 
                new_node.box.animate.set_fill(GREEN_E, opacity=1)
            )
        else:
            self.play(
                FadeIn(new_node), 
                new_node.box.animate.set_fill(GREEN_E, opacity=1)
            )

        # Arrow to a new node
        # Logic for either 1 l ine, or even lines 
        if len(nodes) < 10 or node2.row % 2 == 0:
            arrow_to_new = Arrow(
                start=long_arrow.get_start(), 
                end=new_node.get_left(),
                tip_length=0.2,
                buff=0.1 
            )
        # Logic for odd lines
        else:   
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

            if len(nodes) < 10 or node2.row % 2 == 0:
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

        self.zoom_in_rows(idx1, node1, node2, new_node)
    
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
        
        # Identify affected nodes for shifting to make space for insertion
        nodes_above = [n for n in nodes if n.row <= node1.row]  # Rows before insertion
        nodes_below = [n for n in nodes if n.row >= node2.row]  # Rows after insertion
        
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
        shifts = shift_nodes_to_the_right(nodes, idx2)
        
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
            if node1.row % 2 == 0: # Moving down from even row (Right to Left next)
                node1_closeup.next_arrow = CurvedArrow(
                    start_point=node1_closeup.get_bottom() + [0, 0.3, 0], 
                    end_point=node2_closeup.get_left() + [0, 0.3, 0],
                    tip_length=0.2
                )
            else: # Moving down from odd row (Left to Right next)
                node1_closeup.next_arrow = CurvedArrow(
                    start_point=node1_closeup.get_bottom() + [0, 0.3, 0], 
                    end_point=node2_closeup.get_right() + [0, 0.3, 0],
                    angle=-TAU/4, 
                    tip_length=0.2
                )
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
            node_closeup.shift((node1_closeup.get_center() + node2_closeup.get_center()) / 2 + UP * 0.6)
        else:
            # From even row to odd
            if node1.row % 2 == 0:
                node_closeup.shift((node1_closeup.get_center() + node2_closeup.get_center()) / 2 + LEFT * 2)
            # From odd row to even
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

        if idx1 == 9 or idx1 == 19:
            pass
        # Shifting for even rows
        else:
            if node1.row % 2 == 0:
                new_arrow_to = Arrow(
                    start=arrow_to.get_start() + LEFT * 0.3 + [0, -0.1, 0], 
                    end=arrow_to.get_end() + DOWN * 0.6 + RIGHT * 0.1,
                    tip_length=0.2,
                    buff=0.1 
                )

                new_arrow_from = Arrow(
                    start=node_closeup.next_arrow.get_start() + DOWN * 0.6 + LEFT * 0.1, 
                    end=node_closeup.next_arrow.get_end() + RIGHT * 0.2,
                    tip_length=0.2,
                    buff=0.1 
                )

                self.play(
                    node_closeup.animate.shift(DOWN * 0.6),
                    node1_closeup.animate.shift(LEFT * 0.1),
                    node2_closeup.animate.shift(RIGHT * 0.1),
                    Transform(node1_closeup.next_arrow, new_arrow_to),
                    Transform(node_closeup.next_arrow, new_arrow_from)
                )
            # Shifting for odd rows
            else:
                new_arrow_to = Arrow(
                    start=arrow_to.get_start() + RIGHT * 0.3 + [0, -0.1, 0], 
                    end=arrow_to.get_end() + DOWN * 0.6 + LEFT * 0.1,
                    tip_length=0.2,
                    buff=0.1 
                )

                new_arrow_from = Arrow(
                    start=node_closeup.next_arrow.get_start() + DOWN * 0.6 + RIGHT * 0.1, 
                    end=node_closeup.next_arrow.get_end() + LEFT * 0.2,
                    tip_length=0.2,
                    buff=0.1 
                )

                self.play(
                    node_closeup.animate.shift(DOWN * 0.6),
                    node1_closeup.animate.shift(RIGHT * 0.1),
                    node2_closeup.animate.shift(LEFT * 0.1),
                    Transform(node1_closeup.next_arrow, new_arrow_to),
                    Transform(node_closeup.next_arrow, new_arrow_from)
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
        node1_closeup.shift(position)
        node2_closeup.shift(position + RIGHT * 4)
        node1_closeup.next_arrow = node1_closeup.set_next(node2_closeup, node1_closeup.row, node2_closeup.row)

        self.play(
            self.camera.frame.animate.move_to(position).set(width=node2.width*6),
            FadeIn(background),
            FadeIn(node1_closeup),
            node1_closeup.box.animate.set_fill(GREEN, opacity=0.35),
            FadeIn(node1_closeup.next_arrow)
        )

        node_closeup = LinkedListNodeCloseup(new_node.text.text).scale(0.6)
        node_closeup.shift(node1_closeup.get_left() + UP * 0.6 + LEFT * 1.5)
        node_closeup.next_arrow = node_closeup.set_next(node1_closeup, node1_closeup.row, node1_closeup.row)

        self.play(
            FadeIn(node_closeup),
            node_closeup.box.animate.set_fill(GREEN, opacity=1)
        )

        self.play(FadeIn(node_closeup.next_arrow))

        new_arrow_from_new_node = Arrow(
            start=node_closeup.next_arrow.get_start() + RIGHT * 0.7 + DOWN * 0.6,
            end=node_closeup.next_arrow.get_end() + RIGHT * 1.3, 
            tip_length=0.2,
            buff=0.1
        )

        new_arrow = Arrow(
            start=node1_closeup.next_arrow.get_start() + [0, -0.05, 0] + RIGHT * 1,
            end=node1_closeup.next_arrow.get_end() + RIGHT * 1.2, 
            tip_length=0.2,
            buff=0.1
        )

        self.play(
            node_closeup.animate.move_to(node1_closeup.get_left() + LEFT * 0.7),
            node1_closeup.animate.move_to(node1_closeup.get_center() + RIGHT * 1.2),
            Transform(node_closeup.next_arrow, new_arrow_from_new_node),
            Transform(node1_closeup.next_arrow, new_arrow)
        )

        self.wait(1)

        self.play(
            self.camera.frame.animate.move_to(ORIGIN).set(width=14 * 1.5),
            FadeOut(background),
            FadeOut(node1_closeup),
            FadeOut(node1_closeup.next_arrow),
            FadeOut(node_closeup),
            FadeOut(node_closeup.next_arrow)
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
                node_closeup.shift(node2_closeup.get_right() + DOWN * 0.6 + RIGHT * 1.5)
            else:
                node_closeup.shift(node2_closeup.get_left() + DOWN * 0.6 + LEFT * 1.5)
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
        
        if idx1 == 9 or idx1 == 19:
            pass
        else:
            if node1.row % 2 != 0:
                arrow_to_new = Arrow(
                    start=node2_closeup.next_arrow.get_start() + RIGHT * 1.3, 
                    end=node2_closeup.next_arrow.get_end() + RIGHT * 0.7 + [0, 0.6, 0],
                    tip_length=0.2,
                    buff=0.1 
                )

                self.play(
                    node_closeup.animate.move_to(node2_closeup.get_left() + LEFT * 0.7),
                    node2_closeup.animate.move_to(node2_closeup.get_center() + RIGHT * 1.2),
                    node1_closeup.next_arrow.animate.shift(RIGHT * 1.2),
                    Transform(node2_closeup.next_arrow, arrow_to_new)
                )
            else:
                arrow_to_new = Arrow(
                    start=node2_closeup.next_arrow.get_start() + LEFT * 1.3, 
                    end=node2_closeup.next_arrow.get_end() + LEFT * 0.7 + [0, 0.6, 0],
                    tip_length=0.2,
                    buff=0.1 
                )

                self.play(
                    node_closeup.animate.move_to(node2_closeup.get_right() + RIGHT * 0.7),
                    node2_closeup.animate.move_to(node2_closeup.get_center() + LEFT * 1.2),
                    node1_closeup.next_arrow.animate.shift(LEFT * 1.2),
                    Transform(node2_closeup.next_arrow, arrow_to_new)
                )

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
                shifts.append(node_i.next_arrow.animate.put_start_and_end_on(
                    node_i.get_bottom() + RIGHT * 2 + DOWN * 0.1,
                    node_i_next.get_top() + DOWN * 3 + UP * 0.1
                ))
            # From even line to odd line to become short arrow
            elif i == 9 or i == 29:
                shifts.append(node_i.next_arrow.animate.put_start_and_end_on(
                    node_i.get_left() + DOWN * 3 + LEFT * 0.1,
                    node_i_next.get_right() + LEFT * 2 + RIGHT * 0.1
                ))
            # From odd line to even line to become long arrow
            elif i == 18 or i == 38:
                shifts.append(node_i.next_arrow.animate.put_start_and_end_on(
                    node_i.get_bottom() + LEFT * 2 + DOWN * 0.1,
                    node_i_next.get_top() + DOWN * 3 + UP * 0.1
                ))
            # From odd line to even line to become short arrow
            elif i == 19 or i == 39:
                shifts.append(node_i.next_arrow.animate.put_start_and_end_on(
                    node_i.get_right() + DOWN * 3 + RIGHT * 0.1,
                    node_i_next.get_left() + RIGHT * 2 + LEFT * 0.1
                ))
            # For odd lines
            else:
                shifts.append(node_i.next_arrow.animate.put_start_and_end_on(
                    node_i.get_left() + LEFT * 2 + LEFT * 0.1,
                    node_i_next.get_right() + LEFT * 2 + RIGHT * 0.1
                ))
    return shifts
