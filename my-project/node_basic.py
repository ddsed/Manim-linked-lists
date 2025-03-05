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
            start, end = self.get_bottom(), next_node.get_top()

        self.next_arrow = Arrow(start, end, buff=0.1, tip_length=0.2, color=WHITE)
        return self.next_arrow
