from typing import List, Tuple, NamedTuple
import time
from evasdk import Eva
from grid3d import Grid3D, GridCorners, XYZPoint

# Define the x and y coordinates for 3 corners of the grid
grid_corners1: GridCorners = [
    XYZPoint(x = 0.25, y = 0.1, z=0.27), # Starting position
    XYZPoint(x = 0.41, y = 0.1, z=0.27), # Length of the grid
    XYZPoint(x = 0.41, y = 0.30, z=0.37), # width of the grid + maximal height of the grid
    XYZPoint(x = 0.41, y = 0.30, z=0.27), # minimum height of the grid (minimum z position)
]
# Symmetrical grid
grid_corners2: GridCorners = [
    XYZPoint(x = 0.25, y = -0.30, z=0.27),
    XYZPoint(x = 0.41, y = -0.30, z=0.27),
    XYZPoint(x = 0.41, y = -0.1, z=0.27),
    XYZPoint(x = 0.41, y = -0.1, z=0.37),# maximal height of the grid (maximum z position)
]

# Using the corners and an amount of rows and columns, make the Grid3D
my_test_grid1 = Grid3D(grid_corners1, rows = 3, columns = 3, rowsz=3)
my_test_grid2 = Grid3D(grid_corners2, rows = 3, columns = 3, rowsz=3)


# Connect to Eva
host_ip = "edit this-Eva's IP address" #IP address
token = "edit this-your token" #token
eva = Eva(host_ip, token)
count = 0
# Set some default poses and a default orientation
pose_home = [0.057526037, 0.7658633, -1.9867575, 0.026749607, -1.732109, -0.011505207]
end_effector_orientation = {'w': 0.0, 'x': 0.0, 'y': 1.0, 'z': 0.0} #quaternion values

print("Waiting for Robot lock")
with eva.lock():

    print('Eva moving to home position')
    eva.control_wait_for_ready()
    eva.control_go_to(pose_home, max_speed = 0.15, mode='teach')

    for grid_position in my_test_grid1:
        count +=1
        print (count)

        # Calculate joint angles for the grid position and goto those joint angles
        print('Eva going to grid position x={:f}, y={:f}, z={:f}'.format(grid_position.x, grid_position.y, grid_position.z))

        # Initial hover position
        hover_position1 = {'x': grid_position.x, 'y': grid_position.y, 'z': grid_position.z+0.11}
        position_hover_angles = eva.calc_inverse_kinematics(pose_home, hover_position1, end_effector_orientation)
        eva.control_go_to(position_hover_angles['ik']['joints'], max_speed = 0.15, mode='teach')

        # Target position on the grid
        target_position1 = {'x': grid_position.x, 'y': grid_position.y, 'z': grid_position.z}
        position_joint_angles = eva.calc_inverse_kinematics(pose_home, target_position1, end_effector_orientation)
        eva.control_go_to(position_joint_angles['ik']['joints'], max_speed = 0.15, mode='teach')

        # Perform an action on a gripper - pick up
        eva.gpio_set('d1', True)
        eva.gpio_set('d0', False)

        time.sleep(0.4)
        print('Eva performing action at grid waypoint')

        # Hover the end effector after the pick up
        hover_position1 = {'x': grid_position.x, 'y': grid_position.y, 'z': grid_position.z+0.11}
        position_hover_angles = eva.calc_inverse_kinematics(pose_home, hover_position1, end_effector_orientation)
        eva.control_go_to(position_hover_angles['ik']['joints'], max_speed = 0.15, mode='teach')
        eva.control_go_to(pose_home, max_speed = 0.15, mode='teach')


        for grid_position in my_test_grid2:
            additional_angle = 0.0523598776*count # angle value in radians - user defined, 3 degrees
            print(additional_angle)

            # Initial hover position on the second grid
            hover_position2 = {'x': grid_position.x, 'y': grid_position.y, 'z': grid_position.z+0.11}
            position_hover_angles = eva.calc_inverse_kinematics(pose_home, hover_position2, end_effector_orientation)
            eva.control_go_to(position_hover_angles['ik']['joints'], max_speed = 0.15, mode='teach')

            # Calculate joint angles for the grid position and goto those joint angles
            print('Eva going to grid position x={:f}, y={:f}, z={:f}'.format(grid_position.x, grid_position.y, grid_position.z))

            target_position2 = {'x': grid_position.x, 'y': grid_position.y, 'z': grid_position.z}

            position_joint_angles = eva.calc_inverse_kinematics(pose_home, target_position2,  end_effector_orientation)

            #TODO: rotation of each iteration
            #////////////////////////////////
            eva.control_go_to(position_joint_angles['ik']['joints'], max_speed = 0.15, mode='teach')

            # Perform an action on a gripper - drop
            eva.gpio_set('d0', True)
            eva.gpio_set('d1', False)
            time.sleep(0.4)
            print('Eva performing action at grid waypoint')

            # Hover the end effector
            hover_position2 = {'x': grid_position.x, 'y': grid_position.y, 'z': grid_position.z+0.11}
            position_hover_angles = eva.calc_inverse_kinematics(pose_home, hover_position2, end_effector_orientation)
            eva.control_go_to(position_hover_angles['ik']['joints'], max_speed = 0.15, mode='teach')
            eva.control_go_to(pose_home, max_speed = 0.15, mode='teach')
            break

print("Grid movement complete, lock released")
