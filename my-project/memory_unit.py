from manim import *

class MemoryUnit(VGroup):
    def __init__(self, value, **kwargs):
        super().__init__(**kwargs)
        self.value = value
        self.box = Square(side_length=1, color=WHITE)
        self.line = Line(self.box.get_top(), self.box.get_bottom(), color=WHITE)
        
        if value is None:
            self.text = Text("*", color=BLACK, font_size=24).move_to(self.box.get_left() + RIGHT * 0.25)
        else:
            self.box.set_fill(PURPLE, opacity=0.4)
            self.text = Text(str(value), font_size=24).move_to(self.box.get_left() + RIGHT * 0.25)

        self.add(self.box, self.line, self.text)
        self.next_arrow = None


    def set_next(self, next_node, arrow_type, **arrow_kwargs):
        if self.next_arrow:
            self.remove(self.next_arrow) 

        start = self.get_bottom()
        end = next_node.get_bottom()

        # Get the x-coordinate positions of the current node and next node
        current_x = self.get_center()[0]
        next_x = next_node.get_center()[0]

        if current_x < next_x:
            # Create an arrow (CurvedArrow by default)
            self.next_arrow = arrow_type(
                start_point=start + RIGHT * 0.25, 
                end_point=end + LEFT * 0.25,
                angle=TAU/4,
                **arrow_kwargs
            )
        else:
            # Create an arrow (CurvedArrow by default)
            self.next_arrow = arrow_type(
                start_point=start + RIGHT * 0.25, 
                end_point=end + LEFT * 0.25,
                angle=-TAU/4,
                **arrow_kwargs
            )

        return self.next_arrow