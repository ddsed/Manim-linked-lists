# Improving Conceptual Understanding of Singly Linked Lists Using Manim-Driven Animations

## Introduction

Linked lists are a fundamental data structure in computer science and serve as the foundation for more advanced structures such as stacks, queues, and graphs. Unlike arrays, which require contiguous memory allocation, linked lists use pointers to dynamically connect nodes, enabling efficient insertion and deletion operations. This flexibility makes them particularly useful in scenarios where memory reallocation is frequent. However, traditional visual representations of linked lists often depict them as a continuous sequence of nodes, which can lead to misconceptions about their actual memory allocation and storage.  

Visualization is a powerful tool that is broadly implemented in an attempt to enhance learning and teaching experience across scientific fields, particularly in computer science, where abstract concepts can be difficult to grasp. In the context of this project, visual graphics and animated visualizations are used to facilitate the theoretical understanding of singly linked lists by creating more tangible representations of this data structure and illustrating its behavior in a more intuitive and accessible manner. However, creating visualizations in a way that would accurately convey technical details while maintaining clarity can be challenging and time-consuming. Most existing approaches simplify singly linked lists to a linear arrangement, overlooking their true non-contiguous nature in memory.  

To address this, the main goal of this project is to develop animated visualizations using the [Manim Community Library](https://docs.manim.community/) that represent more accurately how singly linked list nodes are allocated in memory. Unlike common representations, this animated visualization highlights the scattered storage of nodes and how pointers ensure navigation between them. In addition to visualizing memory allocation, more abstract linear representations of the singly linked lists are created to reflect higher-level abstractions of this data structure, thereby illustrating differences between conceptual representations and representations that are closer to implementation. By demonstrating this non-contiguous memory allocation and bridging multiple levels of abstraction, the animation aims to provide a clearer and more comprehensive understanding of singly linked lists and to clarify common misconceptions about this essential data structure.

This project contributes to computer science educational resources by developing numerous interactive Python classes that enable users to visualize insertion and deletion operations on a singly linked list at varying levels of abstraction based on dynamic user input. This adaptability will allow learners to customize their experience and gain a deeper understanding of singly linked lists. By ensuring learners' participation in the process of creating singly linked list visualizations, this work recognizes the fact that educational value is significantly enhanced when visualizations actively engage the learner. 

---

## Features

- Visualizes singly linked lists with accurate representation of non-contiguous memory allocation.
- Supports multiple abstraction levels: static chain, dynamic chain, and memory model representations.
- Interactive animations demonstrating insertion and deletion operations.
- Animated transformation between high and low levels of abstraction.
- User input-driven customization for tailored learning experiences.

---


## Repository Structure

```text
/singly-linked-list/                   # Main folder containing all source code
│
├── tests/                             # Folder containing unit tests
│
├── name-of-operation_static.py        # Scene classes for static chain representation
├── name-of-operation_shift.py         # Scene classes for dynamic chain representation
├── name-of-operation_memory_units.py  # Scene classes for non-contiguous memory model representation
├── name-of-operation_overview.py      # Scene classes for singly linked list representations overview
├── transformation.py                  # Scene class for animated transformation between abstraction levels
│
├── element-name_vgroup.py             # VGroup classes for individual visual components
```

---


## Getting Started

### Prerequisites

- Python
- Manim Community Library ([Installation guide](https://docs.manim.community/en/stable/installation.html))

### Installation and rendering

1. Clone the repository:
   ```bash
   git clone https://github.com/ddsed/Manim-linked-lists.git
2. Render an animation
   ```bash
   cd singly-linked-list
   manim -pql insertion_shift.py LinkedListShiftScene  # For low resolution animation
   manim -pqh insertion_shift.py LinkedListShiftScene  # For high resolution animation

---