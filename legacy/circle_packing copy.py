import random
from typing import List
import matplotlib.pyplot as plt
from matplotlib.patches import Circle as CirclePatch
from ghdtimer import Timer

# timer = Timer()
# timer.tick()
# timer.tock()

# Rules: 
#   - Rectangle grid of 1 by 1
REGION_N = 1 # 3 by 3 grid
NUM_REGIONS = REGION_N * REGION_N

#############################################################################
# Collision Detection #
def check_collisions(x, y, r, circles) -> bool:
    for circle in circles:
        dist_squared = (x-circle.x)*(x-circle.x) + (y-circle.y)*(y-circle.y)

        # Collided with at least one circle
        if dist_squared < (r+circle.r)*(r+circle.r):
            return True
    
    # No collision
    return False


#############################################################################
# Circle Class #
class Circle():
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y
        self.r = 0
        self.regions = [False for i in range(NUM_REGIONS)]
        self.assign_region()
        
    def assign_region(self) -> None:
        self.regions = [False for i in range(NUM_REGIONS)]
        minx, miny, maxx, maxy = self.x-self.r, self.y-self.r, self.x+self.r, self.y+self.r
        for x, y in [(minx, miny), (minx, maxy), (maxx, miny), (maxx, maxy)]:
            # Boundary check
            if x < 0 or x >= 1 or y < 0 or y >= 1:
                continue

            region_x = int(x*REGION_N)
            region_y = int(y*REGION_N)
            self.regions[region_y*REGION_N+region_x] = True

    def is_valid(self, circles) -> bool:
        for i in range(len(circles)):
            if self.regions[i] == True:
                collided = check_collisions(self.x, self.y, self.r, circles[i])
                if collided:
                    return False
        return True
    
    def grow(self, dr: float=0.1) -> None:
        self.r += dr
        self.assign_region()
    
    def shrink(self, dr: float=0.1) -> None:
        self.r -= dr
        self.assign_region()


#############################################################################
# Plotting #
def plot(circles):
    fig, ax = plt.subplots()

    # make sure the plot is square
    ax.axis('square')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    # Regions lines
    for i in range(REGION_N):
        ax.axvline(i/REGION_N, color='k', linestyle='--')
        ax.axhline(i/REGION_N, color='k', linestyle='--')
    
    # Circles
    for circle in circles:
        for c in circle:
            # only border of circle
            ax.add_patch(CirclePatch((c.x, c.y), c.r, fill=False, color='k'))
            
    
    plt.show()


#############################################################################
# Main #
def main():
    # set random seed
    random.seed(34)

    circles = [[] for i in range(NUM_REGIONS)]
    
    # Generate 20 random circles
    for i in range(20):
        x = random.random()
        y = random.random()
        c = Circle(x, y)
        for j in range(NUM_REGIONS):
            if c.regions[j]==True:
                circles[j].append(c)
    
    # Grow the circles until they collide upto 100 iterations
    for i in range(100):
        for j in range(NUM_REGIONS):
            for c in circles[j]:
                if c.is_valid(circles):
                    c.grow(dr=0.1)

        circles = [[] for i in range(NUM_REGIONS)]
        for k in range(NUM_REGIONS):
            if c.regions[k]==True:
                circles[k].append(c)

                # else:
                #     c.shrink()

    plot(circles)


if __name__ == '__main__':
    main()