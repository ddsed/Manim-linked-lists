# Improving Conceptual Understanding of Linked Lists Using Manim-Driven Animations

## Introduction

Linked lists are a fundamental data structure in computer science and serve as the foundation for more advanced structures such as stacks, queues, and graphs. Unlike arrays, which require contiguous memory allocation, linked lists use pointers to dynamically connect nodes, enabling efficient insertion and deletion operations. This flexibility makes them particularly useful in scenarios where memory reallocation is frequent. However, traditional visual representations of linked lists often depict them as a continuous sequence of nodes, which can lead to misconceptions about their actual memory allocation and storage.

Visualization is a powerful tool broadly implemented to enhance learning and teaching experiences across scientific fields, particularly in computer science, where abstract concepts can be difficult to grasp. Visual graphics and animated visualizations bridge this gap by illustrating how data structures operate in a more intuitive way. However, creating them in a way that accurately conveys technical details while maintaining clarity can be challenging and time-consuming. Many existing visualizations simplify linked lists to a linear arrangement, overlooking their true non-contiguous nature in memory.

To address this, the main goal of this project is to develop an animated visualization using the [Manim Community Library](https://docs.manim.community/) that more accurately represents how linked list nodes are allocated in memory. Unlike common representations, this animated visualization highlights the scattered storage of nodes and how pointers ensure navigation between them.

In addition to visualizing memory allocation, more abstract chained representations of the linked list are created to reflect higher-level abstractions of this data structure, illustrating the transformations and differences between conceptual and closer-to-implementation representations. By demonstrating this non-contiguous memory allocation and bridging multiple levels of abstraction, the animation aims to provide a clearer and more comprehensive understanding of linked lists and reduce common misconceptions about this essential data structure.

This project contributes to computer science educational resources by developing interactive Python classes that enable users to visualize insertion and deletion operations on a singly linked list at varying levels of abstraction based on dynamic user input. This adaptability allows learners to customize their experience and gain a deeper understanding of linked lists based on their specific needs.

---

## Features

- Visualizes linked lists with accurate representation of non-contiguous memory allocation.
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
├── name-of-operation_static.py        # Scene class for static chain representation
├── name-of-operation_shift.py         # Scene class for dynamic chain representation
├── name-of-operation_memory_units.py  # Scene class for non-contiguous memory model representation
├── transformation.py                  # Scene class for animated transformation between abstraction levels
│
├── element-name_vgroup.py             # VGroup classes for individual visual components
```

---


## Getting Started

### Prerequisites

- Python
- Manim Community Library ([Installation guide](https://docs.manim.community/en/stable/installation.html))

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/ddsed/Manim-linked-lists.git
2. Render an animation (the second command is an example)
   cd singly-linked-list
   manim -pql insertion_shift.py LinkedListShiftScene

---