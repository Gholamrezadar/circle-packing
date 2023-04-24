#include <cmath>
#include <iostream>
#include <random>
#include <vector>

class Circle {
public:
  float x, y, r;
  bool frozen;

  Circle(float x_, float y_) {
    x = x_;
    y = y_;
    r = 0.0;
    frozen = false;
  }

  bool is_valid(const std::vector<Circle> &circles) {
    bool collided = check_collisions(circles);
    if (collided) {
      return false;
    }
    return true;
  }

  void grow(float dr = 0.1) { r += dr; }

  void shrink(float dr = 0.1) { r -= dr; }

private:
  bool check_collisions(const std::vector<Circle> &circles) {
    // boundary check
    if (x + r >= 1 || x - r <= 0 || y + r >= 1 || y - r <= 0) {
      return true;
    }

    for (const Circle &circle : circles) {
      if (&circle != this) {
        if (circle.r < 0.00000001) {
          continue;
        }

        float dx = x - circle.x;
        float dy = y - circle.y;
        // float dist = sqrt(dx * dx + dy * dy);
        float dist_squared = dx * dx + dy * dy;

        // Collided with at least one circle
        if (dist_squared < (r + circle.r) * (r + circle.r)) {
          return true;
        }

        // if (dist < r + circle.r)
        // {
        //     return true;
        // }
      }
    }
    // No collision
    return false;
  }
};

std::pair<float, float> propose_position(const std::vector<Circle> &circles) {
  std::random_device rd;
  std::mt19937 gen(rd());
  std::uniform_real_distribution<> dis(0.0, 1.0);

  bool is_ok = false;
  float x = 0;
  float y = 0;
  while (!is_ok) {
    x = dis(gen);
    y = dis(gen);
    is_ok = true;
    for (const Circle &circle : circles) {
      if (circle.x - circle.r < x && x < circle.x + circle.r &&
          circle.y - circle.r < y && y < circle.y + circle.r) {
        is_ok = false;
        break;
      }
    }
  }
  return std::make_pair(x, y);
}

int main() {
  constexpr int ITERATIONS = 10 * 10000;
  constexpr int CIRCLES_PER_ITERATION = 20;
  constexpr int GROWTH_ITERATIONS = 1 * 10;
  constexpr float GROW_DELTA = 0.0015;

  std::vector<Circle> circles;

  // std::random_device rd;
  // std::mt19937 gen(rd());
  // std::uniform_real_distribution<> dis(0.0, 1.0);

  for (int iteration = 0; iteration < ITERATIONS; iteration++) {
    // progessbar
    if (iteration % 10000 == 0) {
      std::clog << iteration << "/" << ITERATIONS << " " << circles.size()
                << " circles"
                << "\n";
    }

    for (int i = 0; i < CIRCLES_PER_ITERATION; i++) {
      auto [x, y] = propose_position(circles);
      Circle c(x, y);
      circles.push_back(c);
    }

    for (int i = 0; i < GROWTH_ITERATIONS; i++) {
      for (Circle &c : circles) {
        // float delta = 0.005 + (dis(gen) - 0.5) / 200;
        const float grow_delta = GROW_DELTA;
        if (!c.frozen) {
          if (c.is_valid(circles)) {
            c.grow(grow_delta);
          } else {
            c.shrink(grow_delta);
            c.frozen = true;
          }
        }
      }
    }

    // House-cleaning: delete circles that are frozen and are below 0.00000001
    // radius
    for (std::size_t i = 0; i < circles.size(); i++) {
      if (circles[i].r < 0.003) {
        circles.erase(circles.begin() + i);
        // decrement i because we deleted an element
        i--;
      }
    }
  }

  // Print the positions and radii of the circles
  for (const Circle &c : circles) {
    if (c.r > 0.000000001) {
      std::cout << c.x << ", " << c.y << ", " << c.r << "\n";
    }
  }

  return 0;
}
