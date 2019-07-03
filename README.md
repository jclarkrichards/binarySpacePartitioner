# binarySpacePartitioner
This is my implementation of a Binary Space Partioner in Python.

I draw the lines in the window and then the program divides up the area via BSP.  Seems simple enough.

I am making these assumptions (at least initially, when I get this working I'll relax these restrictions)
1. A Vertex is simply a point in space with a position as a Vector2.
2. A Segment connects 2 Vertices together
3. A Directed Segment connects 2 Vertices together, but only in one direction
4. Directed Segments connect together to form a loop.
5. The initial loop the user creates needs to be a clock-wise loop
6. There can only be 1 initial loop.
7. There cannot be any inner loops initially.