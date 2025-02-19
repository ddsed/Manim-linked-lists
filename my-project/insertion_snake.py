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

    def set_next(self, next_node, row1, col1, row2, col2):
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


class LinkedListScene(Scene):
    def construct(self):
        # Show animation without cropping
        scale_factor = 1.5
        self.camera.frame_width = 14 * scale_factor  # Default width is 14
        self.camera.frame_height = self.camera.frame_width / 1.78  # Keep 16:9 aspect ratio
        self.camera.frame_center = ORIGIN  # Keep centered

        # Get input from user
        node_values = input("Enter distinctive node letters separated by space (e.g., A B C D, min = 5): ").split()
        insert_idx1, insert_idx2 = map(int, input("Enter the two node indices where a new node should be inserted (0-based): ").split())
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
            self.play(FadeIn(node, run_time=0.5), FadeIn(textfuncadd, run_time=0.6))
            self.play(FadeOut(textfuncadd, run_time=0.6))
            if i > 0:
                row1, col1 = (i - 1) // 10, (i - 1) % 10
                row2, col2 = i // 10, i % 10
                arrow = nodes[i - 1].set_next(node, row1, col1, row2, col2)
                self.play(FadeIn(arrow, run_time=0.5), FadeIn(textfuncarrow, run_time=0.6))
                self.play(FadeOut(textfuncarrow, run_time=0.6))

        self.wait(1)
        # Insert a new node
        self.insert_node_between(nodes, insert_idx1, insert_idx2, new_letter)

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
                # Shift nodes from node2 onwards
                shifts = []
        
                for i in range(nodes.index(node2), len(nodes)):
                    node_i = nodes[i]

                    # Shift node_i to the position of node_i_next
                    # The last node shift logic
                    if i == len(nodes) - 1:
                        if node_i.row % 2 != 0:
                            shifts.append(node_i.animate.shift(LEFT * 2))
                        else:
                            shifts.append(node_i.animate.shift(RIGHT * 2))
                    else:
                        node_i_next = nodes[i + 1]
                        shifts.append(node_i.animate.move_to(node_i_next.get_center()))
                    
                    # If node_i has a next arrow, shift it to node_i_next's arrow position
                    if node_i.next_arrow:
                        # Even lines without edge cases
                        if node_i.row % 2 == 0 and i != 8 and i != 9 and i != 28 and i != 29:
                            shifts.append(node_i.next_arrow.animate.shift((RIGHT * 2)))
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
                # Checking what line we are inserting to
                if node2.row % 2 == 0:
                    # Stretch the existing arrow between node1 and node2 for even lines
                    long_arrow = Arrow(
                        start=node1.get_right(), 
                        end=node2.get_left() + RIGHT * 2,
                        tip_length=0.2,
                        buff=0.1
                    )
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
            initial_position = (node1.get_right() + node2.get_left()) / 2 + UP * 1.5
            
            new_node.move_to(initial_position)

            self.play(
                FadeIn(new_node), 
                new_node.box.animate.set_fill(GREEN_E, opacity=1)
            )

            # Logic for either 1 l ine, or even lines 
            if len(nodes) < 10 or node2.row % 2 == 0:
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

            new_node.next_arrow = new_node.set_next(node2, node1.row, node1.col, node2.row, node2.col)

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
        