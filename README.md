#  Drawing Robot ROS2 Simulation

A simulated XY plotter robot built with ROS2 and visualized in RViz. The robot can draw shapes automatically and trace outlines from real images using OpenCV edge detection.

---

##  What It Does

- Simulates a 2-axis (XY) drawing robot in RViz
- Moves joints automatically to draw a square path
- Processes any image using OpenCV and extracts contours
- Feeds those contours as joint positions — making the robot "draw" the image

---

##  Requirements

- Ubuntu (20.04 or 22.04)
- ROS2 Humble
- Python 3
- OpenCV:
  ```bash
  pip install opencv-python
  ```

---

##  Project Structure

```
drawing_robot_ws/
├── src/
│   ├── drawing_robot_description/       # URDF model, RViz config, launch files
│   │   ├── urdf/                        # Robot URDF definition
│   │   ├── launch/                      # display.launch.py
│   │   └── rviz/                        # RViz configuration
│   └── drawing_robot_controller/        # Controller nodes and image processor
│       └── drawing_robot_controller/
│           ├── draw_controller.py       # Draws a square automatically
│           ├── image_processor.py       # OpenCV edge detection + contour extraction
│           └── image_draw_controller.py # Feeds image contours to robot joints
```

---

##  Setup

```bash
git clone https://github.com/PES2UG23CS065/drawing_robot_ros2.git
cd drawing_robot_ros2
colcon build
source install/setup.bash
```

---

##  How to Run

### 1. Visualize the robot in RViz

Open **Terminal 1**:
```bash
cd ~/drawing_robot_ws
source install/setup.bash
ros2 launch drawing_robot_description display.launch.py
```

RViz will open showing the robot model.

---

### 2. Draw a square automatically

Open **Terminal 2** (keep Terminal 1 open):
```bash
cd ~/drawing_robot_ws
source install/setup.bash
ros2 run drawing_robot_controller draw_controller
```

The robot will move its joints to trace a square: `(-0.2,-0.2) → (0.2,-0.2) → (0.2,0.2) → (-0.2,0.2)`.

You'll see logs like:
```
Publishing: x=-0.2, y=-0.2
Publishing: x=0.2, y=-0.2
...
```

---

### 3. Draw from an image

First, make sure you have an image (PNG or JPG). Then run:

```bash
cd ~/drawing_robot_ws
source install/setup.bash
ros2 run drawing_robot_controller image_draw_controller /path/to/your/image.png
```

**What happens internally:**
1. Image is loaded and converted to grayscale
2. Gaussian blur is applied to reduce noise
3. Canny edge detection finds all edges
4. Contours are extracted as (x, y) coordinate lists
5. Each contour is published to `/joint_states` — the robot traces them one by one
6. The robot returns to `(0, 0)` between contours (pen lift)

---

##  How the Image Processing Works

File: `image_processor.py`

```
Image (any PNG/JPG)
  → Grayscale conversion
  → Resize to 200×200
  → Gaussian blur (5×5)
  → Canny edge detection (threshold 50–150)
  → Find contours
  → Normalize to robot range (-0.2 to +0.2 meters)
  → Return list of (x, y) waypoints per contour
```

Example output:
```
Found 50 contours
  Contour 1: 15 points
  Contour 50: 497 points
```

---

## 📡 ROS2 Topics Used

| Topic | Message Type | Purpose |
|-------|-------------|---------|
| `/joint_states` | `sensor_msgs/JointState` | Publishes x_joint and y_joint positions |

To monitor live joint data:
```bash
ros2 topic echo /joint_states
```

---

## 

| Node | File | What it does |
|------|------|-------------|
| `draw_controller` | `draw_controller.py` | Moves robot in a square path every 0.5s |
| `image_draw_controller` | `image_draw_controller.py` | Draws contours from an image at 20Hz |

---


