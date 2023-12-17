# Ambrocio Project
Hey, welcome to Ambrocio.

Link for the standard and realigned skull files: https://drive.google.com/drive/folders/1ZF87LsVM5wFYWkNBPbF12JSZAJvlF6oZ?usp=sharing

https://drive.google.com/drive/folders/1EVF9dfmyLoLZwhiFuIL9kGNNWUk-N6gN?usp=sharing

### The Projection Algorithm

This procedure is supposed to map models of damaged skulls onto a standard healthy skull surface in order to quantitatively analyze the distribution of size, location, curvature, and other parameters in the data set. It is necessary to align all skulls manually before the prjection can be computed.

The algorithm consists of two main steps:

#### Preparation of the reference skull

This initial step is only executed once and serves as a basis for the analysis.

1. The standard reference skull is converted into a convex hull. 
2. Its surface is resampled using triangles of fixed size and uniform distribution.
3. The geometric center of each triangle is computed, as well as its normal and anti-normal vectors.

#### Raycasting

These steps are repeated for each damaged skull model in the database. A global array counts the number of hits throughout the whole data set. Each entry of this array corresponds to one triangle of the reference skull, i.e. two rays (normal and anti-normal).

1. Originating from the geometric center of each triangle, an outward and inward facing ray is sent along the normal vector of the triangle.
2. The intersection between these rays and the damaged skulls are computed. 
3. If at least one ray intersects the damaged skull at least once and the distance of the triangle center to the intersection point is less than a user-defined margin, the corresponding hit count is incremented by one. This counting is strictly binary, meaning that it does not matter whether the normal or anti-normal ray intersects the damaged skull, nor is it relevant how often an intersection occurs. If any intersection within the given margin is computed, the count is always increased by 1.

Finally, the resulting array of hits per triangle is exported and saved as a csv file.