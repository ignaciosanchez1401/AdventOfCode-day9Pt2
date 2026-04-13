## Problem

🔗 [Advent of Code - Day 9](https://adventofcode.com/2025/day/9)  
*(Part 2 unlocks after completing Part 1)*

---

## Approach

The solution combines several algorithmic techniques:

### 1. Coordinate Compression
To reduce the size of the grid, I compress the coordinates and insert intermediate points when necessary.  
This allows efficient processing without losing geometric accuracy.

### 2. Point-in-Polygon (Ray Casting)
To determine whether a cell is inside or outside the polygon:
- Count intersections with vertical edges  
- Odd → inside  
- Even → outside  

### 3. Flood Fill (DFS)
I classify regions of the grid as:
- `"o"` → inside  
- `"-"` → outside  
- `"x"` → border  

This avoids recomputing point-in-polygon for every cell.

### 4. 2D Prefix Sum
I build a prefix sum matrix to efficiently check whether a rectangle contains any outside cells.

### 5. Brute Force with Optimization
I iterate over all pairs of points and:
- Map them to compressed coordinates  
- Check if the rectangle is valid using prefix sums  
- Compute its area  

---

## How to Run

1. Place your input in `input.txt`
2. Run:

```bash
python solution.py
