import matplotlib.pyplot as plt
from matplotlib.patches import Circle as CirclePatch
from ghdtimer import Timer

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
        self.r = 0.0
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

    fig, ax = plt.subplots(dpi=300, figsize=(5, 5), constrained_layout=True)

    # make sure the plot is square
    ax.set_aspect('equal')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.axis('off')

    # Circles
    counter = 0
    for c in circles:
        # skip small circles
        if c.r <= 0.000000001:
            continue

        # only border of circle and change line width based on radius
        ax.add_patch(CirclePatch((c.x, c.y), c.r, fill=False, color='black',))# linewidth=max(c.r*12, 0.2)))
        counter += 1
    
    print("Number of plotted circles:", counter)
    
    # Current timestamp
    import datetime
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
    plt.savefig(f"images/result_{timestamp}.png")
    # plt.show()

#############################################################################
# Main #
def main():
    circles = []
    with open('result.txt', 'r') as f:
        for line in f:
            x, y, r = line.split(", ")
            c = Circle(float(x), float(y))
            c.r = float(r)
            circles.append(c)

    print("Number of circles:", len(circles))

    plot(circles)

if __name__ == '__main__':
    main()
