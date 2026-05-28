import sapien.core as sapien
from sapien.utils import Viewer
import numpy as np

def main():
    # 1. Initialize Engine and Renderer
    engine = sapien.Engine()
    renderer = sapien.SapienRenderer()
    engine.set_renderer(renderer)

    # 2. Create Scene
    scene = engine.create_scene()
    scene.set_timestep(1 / 125)
    scene.add_ground(0)  # Add a ground plane

    # 3. Add Lighting
    scene.set_ambient_light([0.25, 0.25, 0.25])
    scene.add_directional_light([0, 1, -1], [0.5, 0.5, 0.5])

    # 4. Load URDF
    loader = scene.create_urdf_loader()
    loader.fix_root_link = True
    
    # Replace 'path/to/robot.urdf' with your actual URDF file path
    robot = loader.load("./dexmate-urdf/robots/humanoid/vega_1/vega_1_f5d6.urdf")
  
    joints = robot.get_joints()
    print("Robot Joint Names:")
    for joint in joints:
        print(f"- {joint.name}")
    
    # Set initial pose if needed
    if robot:
        robot.set_pose(sapien.Pose(p=[0, 0, 0.5]))

    # 5. Initialize Viewer
    viewer = Viewer(renderer)
    viewer.set_scene(scene)
    viewer.set_camera_xyz(x=2, y=0, z=1.5)
    viewer.set_camera_rpy(r=0, p=-0.5, y=3.14)

    active_joints = robot.get_active_joints()
    joint_names = [j.name for j in active_joints]
    
    joint_index = joint_names.index("R_arm_j1")
    target_joint = active_joints[joint_index]

    target_joint.set_drive_property(stiffness=1000.0, damping=100.0)
    target_position = 0.5
    target_joint.set_drive_target(target_position)

    # 6. Simulation Loop
    while not viewer.closed:
        scene.step()  # Physics step
        scene.update_render()  # Update renderer
        viewer.render()

if __name__ == "__main__":
    main()

