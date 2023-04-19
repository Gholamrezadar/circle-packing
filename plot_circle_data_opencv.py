import cv2
import numpy as np
import datetime

def plot(circles):
    W, H = 4096, 4096
    image = np.ones((W, H, 3), np.uint8)*255
    for circle in circles:
        x, y, r = circle
        x = int(circle[0]*W)
        y = int(circle[1]*H)
        r = int(circle[2]*W)
        cv2.circle(image, (x, y), r, (0, 0, 0), int(W*0.0015), cv2.LINE_AA)
    
    # Current timestamp
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
    cv2.imwrite(f"images/cv_result_{timestamp}.png", image)

import sys
def main():
    circles = []
    result_file = "result.txt"
    if len(sys.argv)>1:
        result_file = sys.argv[1]
    with open(result_file, 'r') as f:
        for line in f:
            x, y, r = line.split(", ")
            circles.append((float(x), float(y), float(r)))
    
    print("Number of circles:", len(circles))
    plot(circles)

if __name__ == '__main__':
    main()
