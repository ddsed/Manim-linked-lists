from manim import *

class Shapes(Scene):
    def construct(self):
        # Scene 1
        # Show animation without cropping
        scale_factor = 1.5
        self.camera.frame_width = 14 * scale_factor  # Default width is 14
        self.camera.frame_height = self.camera.frame_width / 1.78  # Keep 16:9 aspect ratio
        self.camera.frame_center = ORIGIN  # Keep centered

        # Square1
        square1 = Square()
        square1.set_fill(PINK, opacity=0.5) 
        
        # Create a vertical line inside the square
        line1 = Line(square1.get_left(), square1.get_right(), color=WHITE)
        
        # Create texts inside the square
        text1up = Text("Data", font_size = 36) 
        text1up.move_to(square1.get_top() - [0, 0.5, 0])
        text1down = Text("Pointer", font_size = 34)
        text1down.move_to(square1.get_bottom() + [0, 0.5, 0])
        
        # Group them together so they move as one
        square1_group = VGroup(square1, line1, text1up, text1down)

        # Square2
        square2 = Square()
        square2.set_fill(PINK, opacity=0.5) 
        square2.shift(RIGHT * 2)
        
        # Create a vertical line inside the square
        line2 = Line(square2.get_left(), square2.get_right(), color=WHITE)
        
        # Create text inside the square
        text2 = Text("Data", font_size = 36) 
        text2.move_to(square2.get_top() - [0, 0.5, 0])
        
        # Group them together so they move as one
        square2_group = VGroup(square2, line2, text2)
        
        # Create circles for abstraction
        circle1 = Circle()
        circle1.set_fill(PINK, opacity=0.5) 
        circle1.set_stroke(WHITE, width=2)

        circle2 = Circle()
        circle2.set_fill(PINK, opacity=0.5) 
        circle2.set_stroke(WHITE, width=2)

        # Display square1
        # Smooth Creation Effect
        self.play(
            AnimationGroup(
                FadeIn(square1),  
                Create(line1),  
                FadeIn(text1up), 
                FadeIn(text1down), 
                lag_ratio=0.05
            ),
            run_time=1.5
        )
        self.play(square1_group.animate.shift(LEFT * 2), run_time=1)

        # Preserve the position when transforming
        circle1.move_to(square1_group.get_center())
        circle2.move_to(square2_group.get_center())

        # Create an arrow starting from the right border of the square1
        arrow = Arrow(
            start=square1_group.get_bottom() + [-0.25, 0.4, 0], 
            end=square2_group.get_left() + [0, 0.5, 0],
            color=ORANGE
        )

        #Create a dot for arrow start
        dot = Circle().scale(0.15)
        dot.set_fill(ORANGE, opacity=1)
        dot.move_to(square1_group.get_bottom() + [0, 0.5, 0])

        # Display arrow and square2
        self.play(
            FadeOut(text1down), 
            Create(arrow), 
            Create(dot),
            Transform(text1down, dot),
            # Smooth Creation Effect
            AnimationGroup(
                FadeIn(square2),  
                Create(line2),  
                FadeIn(text2),  
                lag_ratio=0.5
            ),
            run_time=1.5
            )
        
        self.wait(0.8)

        # New arrow for transition
        new_arrow = Arrow(
            start=circle1.get_right(), 
            end=circle2.get_left(),
            color=ORANGE
        )

        # Transform the squares to circles simultaneously
        self.play(
            Transform(square1_group, circle1),
            Transform(square2_group, circle2),
            Transform(arrow, new_arrow),
            FadeOut(dot)
        )

        # Keep the final state for a moment
        self.wait(1)

        # Scene 2
        # Group circles together
        circles_group = VGroup(square1_group, square2_group, arrow)

        # Move circles down to free the space for memory blocks
        self.play(circles_group.animate.shift(DOWN * 2), run_time=1)

        # Create text for circles
        text1circle = Text("1", font_size = 44)
        text1circle.move_to(square1_group.get_center()) 
        text2circle = Text("2", font_size = 44) 
        text2circle.move_to(square2_group.get_center()) 

        # Create memory representation       
        memory_units = VGroup(*[Rectangle(width=0.8, height=1.5) for _ in range(18)])

        # Arrange them in a line, making sure they are perfectly adjacent
        memory_units.arrange(RIGHT, buff=0)

        # Center the whole group at the top
        memory_units.move_to(UP * 2)

        # Text for memory units
        textmemoryunits = Text("Memory Units", font_size = 36) 
        textmemoryunits.next_to(memory_units, UP, buff=0.5)
        textmemoryunits.align_to(memory_units, LEFT)
        
        # Display text and memory units
        self.play(
            FadeIn(text1circle),
            FadeIn(text2circle),
            FadeIn(memory_units),
            FadeIn(textmemoryunits),
        )

        self.wait(1)

        # Scene 3
        # Get references to squares at positions [3] and [12]
        memory_unit_3 = memory_units[3]
        memory_unit_12 = memory_units[12]

        self.play(
            FadeOut(arrow),
            Transform(square2_group, memory_unit_3),
            Transform(square1_group, memory_unit_12),
            text2circle.animate.move_to(memory_unit_3.get_center()).scale(0.6),
            text1circle.animate.move_to(memory_unit_12.get_center()).scale(0.6),
            memory_unit_3.animate.set_fill(PINK, opacity=0.5),
            memory_unit_12.animate.set_fill(PINK, opacity=0.5)
        )

        self.wait(2)