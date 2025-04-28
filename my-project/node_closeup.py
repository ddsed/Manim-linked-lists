from manim import *

class LinkedListNodeCloseup(VGroup):
    def __init__(self, value, row=None, col=None, **kwargs):
        super().__init__(**kwargs)
        self.box = Square(side_length=2, color=WHITE)
        self.line = Line(self.box.get_left(), self.box.get_right(), color=WHITE)
        self.text = Text(value, font_size=34).move_to(self.box.get_top() - [0, 0.5, 0])
        self.dot = Circle().scale(0.2)
        self.dot.set_fill(WHITE, opacity=1)
        self.dot.move_to(self.box.get_bottom() + [0 , 0.5, 0])
        self.dot.set_stroke(width=0) 
        self.add(self.box, self.text, self.line, self.dot)
        self.next_arrow = None
        self.row = row
        self.col = col

    def set_next(self, next_node, row1, row2):
        if self.next_arrow:
            self.remove(self.next_arrow)
        
        if row1 % 2 == 0:  # Even row (Left to Right)
            start, end = self.get_bottom() + [0, 0.3, 0], next_node.get_left() + [0, 0.3, 0]
        else:  # Odd row (Right to Left)
            start, end = self.get_bottom() + [0, 0.3, 0], next_node.get_right() + [0, 0.3, 0]
        self.next_arrow = Arrow(start, end, buff=0.1, tip_length = 0.2, color=WHITE)
        return self.next_arrow
