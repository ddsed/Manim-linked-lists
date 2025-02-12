from manim import *
# basic look => 5 to 9 initial nodes in one line

class LinkedListNodeBasic(VGroup):
    def __init__(self, value, **kwargs):
        super().__init__(**kwargs)
        self.box = Square(side_length=1, color=WHITE)
        self.text = Text(str(value), font_size=24).move_to(self.box.get_center())
        self.add(self.box, self.text)
        self.next_arrow = None

    def set_next(self, next_node):
        if self.next_arrow:
            self.remove(self.next_arrow)
        self.next_arrow = Arrow(self.get_right(), next_node.get_left(), buff=0.1, tip_length = 0.2, color=WHITE)
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
        insert_letter1, insert_letter2 = input("Enter the two node letters where a new node should be inserted: ").split()
        new_letter = input("Enter the new node letter: ")

        # Create nodes
        nodes = [LinkedListNodeBasic(value) for value in node_values]
        for i, node in enumerate(nodes):
            node.move_to(RIGHT * i * 2)

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
        self.insert_node_between(nodes, insert_letter1, insert_letter2, new_letter)

    def insert_node_between(self, nodes, letter1, letter2, new_value):
        # Find the reference nodes for insertion + color code them
        node1 = next((node for node in nodes if node.text.text == letter1), None)
        node2 = next((node for node in nodes if node.text.text == letter2), None)
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
        final_position = initial_position -  UP * 1.5

        # Updater for new node movement
        def update_node_position(node):
            if not np.allclose(node.get_center(), final_position):
                node.shift(DOWN * 0.05)
            else:
                node.remove_updater(update_node_position)

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