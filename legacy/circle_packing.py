import random
from typing import List
import matplotlib.pyplot as plt
from matplotlib.patches import Circle as CirclePatch
from ghdtimer import Timer

# Rules: 
#   - Rectangle grid of 1 by 1
REGION_N = 1 # 3 by 3 grid
NUM_REGIONS = REGION_N * REGION_N

#############################################################################
# Collision Detection #
def check_collisions(self, circles) -> bool:
    
    # boundary check
    if self.x+self.r>=1 or self.x-self.r<=0 or self.y+self.r>=1 or self.y-self.r<=0:
        return True

    for circle in circles:
        if circle != self:
            dist_squared = (self.x-circle.x)*(self.x-circle.x) + (self.y-circle.y)*(self.y-circle.y)

            # Collided with at least one circle
            if dist_squared < (self.r+circle.r)*(self.r+circle.r):
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
        self.frozen = False
        
    def is_valid(self, circles) -> bool:
        collided = check_collisions(self, circles)
        if collided:
            return False
        return True
    
    def grow(self, dr: float=0.1) -> None:
        self.r += dr
    
    def shrink(self, dr: float=0.1) -> None:
        self.r -= dr


#############################################################################
# Plotting #
def plot(circles):
    fig, ax = plt.subplots(dpi=200)

    # make sure the plot is square
    ax.axis('square')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    # Regions lines
    for i in range(REGION_N):
        ax.axvline(i/REGION_N, color='k', linestyle='--')
        ax.axhline(i/REGION_N, color='k', linestyle='--')
    
    # Circles
    for c in circles:
        # only border of circle
        ax.add_patch(CirclePatch((c.x, c.y), c.r, fill=False, color='k'))
    
    # Current timestamp
    import datetime
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
    plt.savefig(f"result_{timestamp}.png")
    # plt.show()


def propose_position(circles):
    # generate random x and y, if it collides with the circles discard and try again.
    is_ok = False
    x = 0
    y = 0
    while(not is_ok):
        x = random.random()
        y = random.random()
        is_ok = True
        for circle in circles:
            if circle.x-circle.r<x<circle.x+circle.r and circle.y-circle.r<y<circle.y+circle.r:
                is_ok = False
                break
    return x, y


#############################################################################
# Main #
def main():
    # set random seed
    # random.seed(34)
    timer = Timer()

    circles = []
    
    for iteration in range(300):
        # print(f"Iteration {iteration}:")
        # print("Generating 15 circles...")
        # timer.tick()
        # Generate 15 random circles
        for i in range(15):
            x, y = propose_position(circles)
            c = Circle(x, y)
            circles.append(c)
        # timer.tock()
        
        # Grow the circles until they collide upto 100 iterations
        # print("Growing for 100 iterations and doing collision checks...")
        # timer.tick()
        for i in range(200):
            for c in circles:
                if not c.frozen:
                    if c.is_valid(circles):
                        c.grow(dr=0.005)
                    else:
                        c.shrink(dr=0.005)
                        c.frozen = True
            # plot(circles)
        # timer.tock()
        # print()

    # plot(circles)

if __name__ == '__main__':
    main()
