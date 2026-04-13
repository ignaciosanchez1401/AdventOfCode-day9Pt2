def point_inside_polygon(i, j, xs, ys, vertical_edges):
    cx = xs[i] + 0.5
    cy = ys[j] + 0.5
    count = 0
    for (bx, y0), (_, y1) in vertical_edges:
        if bx > cx and y0 <= cy <= y1:
            count += 1

    if count % 2 == 0:  # Outside the polygon
        return False
    
    return True


def flood_fill(grid, i, j, c, n, m):
    #DFS
    stack = [(i, j)]
    while stack:
        i, j = stack.pop()

        if i<0 or i>=n or j<0 or j>=m or grid[j][i] != ".":
            continue 
        
        grid[j][i] = c
        stack.append([i+1,j])
        stack.append([i,j+1])
        stack.append([i-1,j])
        stack.append([i,j-1])



def rectangle_inside_polygon(i1, j1, i2, j2, prefix_sum):
    
    if i2<i1:
        i1, i2 = i2, i1


    if j2<j1:
        j1, j2 = j2, j1

    total = prefix_sum[j2+1][i2+1]-prefix_sum[j1][i2+1]-prefix_sum[j2+1][i1]+prefix_sum[j1][i1]
    if total>0:
        return False
    
    return True



def main():
    with open("input.txt", "r") as f:
        txt = f.read().strip().splitlines()

    points = []
    for a in txt:
        x = a.rsplit(",")
        x[0] = int(x[0])
        x[1] = int(x[1])
        points.append(x)

    auxXs = sorted({x for x, _ in points}) 
    auxYs = sorted({y for _, y in points})


    #adding intermediate points

    xs = []
    for i in range(len(auxXs)-1):
        xs.append(auxXs[i])
        if auxXs[i+1] - auxXs[i] > 1:
            xs.append(auxXs[i] + 0.5)
    xs.append(auxXs[len(auxXs)-1])

    ys = []
    for i in range(len(auxYs)-1):
        ys.append(auxYs[i])
        if auxYs[i+1] - auxYs[i] > 1:
            ys.append(auxYs[i] + 0.5)
    ys.append(auxYs[len(auxYs)-1])

    n = len(xs)
    m = len(ys)

    #vertical edges

    vertical_edges = []
    for x in range(len(points)):
        i0 = points[x][0]
        j0 = points[x][1]

        xsig = x + 1
        if xsig == len(points):
            xsig = 0

        i1 = points[xsig][0]
        j1 = points[xsig][1]

        if i0==i1:
            if j0<=j1:
                vertical_edges.append([points[x],points[xsig]])
            else:
                vertical_edges.append([points[xsig],points[x]])


    vertical_edges.sort(key=lambda e: e[0][0])  # sort by x


    #index

    x_index = {v: i for i, v in enumerate(xs)}
    y_index = {v: i for i, v in enumerate(ys)}

    #grid[j][i] compressed grid

    grid = [["." for _ in range(n)] for _ in range(m)]

    #connecting borders
    for x in range(len(points)):
        i0 = points[x][0]
        j0 = points[x][1]

        x_next = x + 1
        if x_next == len(points):
            x_next = 0

        i1 = points[x_next][0]
        j1 = points[x_next][1]

        if i0==i1 and j0<=j1:
            #x_next is below x
            for k in range(y_index[j0] ,y_index[j1]+1,1):
                grid[k][x_index[i0]] = 'x'

        elif i0==i1 and j0>j1:
            #x_next is above x
            for k in range(y_index[j1],y_index[j0]+1,1):
                grid[k][x_index[i0]] = 'x'

        elif i0<=i1:
            #x_next is to the right of x
            for k in range(x_index[i0],x_index[i1]+1,1):
                grid[y_index[j0]][k] = 'x'

        else:
            #x_next is to the left of x
            for k in range(x_index[i1],x_index[i0]+1,1):
                grid[y_index[j0]][k] = 'x'


    #completing the grid

    for j in range(m):
        for i in range(n):
            if grid[j][i] != ".":
                continue
            if point_inside_polygon(i, j, xs, ys, vertical_edges):
                flood_fill(grid, i, j, "o", n, m) # inside
            else:
                flood_fill(grid, i, j, "-", n, m) # outside
                

    #(Optional)printing the grid
    #for x in grid:
    #    print(x)


    #prefix_sum[j][i] is the number of "-" in the rectangle from the origin to (i,j)

    prefix_sum = [[0 for _ in range(n+1)] for _ in range(m+1)]

    for i in range(1,n+1):
        for j in range(1,m+1):
            esAfuera = 0
            if grid[j-1][i-1] == "-":
                esAfuera = 1
            prefix_sum[j][i] = prefix_sum[j][i-1] + prefix_sum[j-1][i] - prefix_sum[j-1][i-1] + esAfuera


    #calculating max area

    max_area = 0
    for k in range(len(points)):
        x = points[k][0]
        y = points[k][1]

        i1 = x_index[x]
        j1 = y_index[y]

        for l in range(k+1,len(points)):
            x = points[l][0]
            y = points[l][1]

            i2 = x_index[x]
            j2 = y_index[y]

            if rectangle_inside_polygon(i1, j1, i2, j2, prefix_sum):
                area = (abs(xs[i2]-xs[i1])+1)*(abs(ys[j2]-ys[j1])+1)
                if area>max_area:
                    max_area = area


    print(max_area)





if __name__ == "__main__":
    main()
