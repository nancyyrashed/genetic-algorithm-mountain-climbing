import pybullet as p
import pybullet_data
import time
import numpy as np
import random
import creature
import genome
import sys
import os
import math

def make_mountain(num_rocks=100, max_size=0.25, arena_size=10, mountain_height=5):
    def gaussian(x, y, sigma=arena_size/4):
        """Return the height of the mountain at position (x, y) using a Gaussian function."""
        return mountain_height * math.exp(-((x**2 + y**2) / (2 * sigma**2)))

    for _ in range(num_rocks):
        x = random.uniform(-arena_size/2, arena_size/2)
        y = random.uniform(-arena_size/2, arena_size/2)
        z = gaussian(x, y)  # Height determined by the Gaussian function

        size_factor = 1 - (z / mountain_height)
        size = random.uniform(0.1, max_size) * size_factor

        orientation = p.getQuaternionFromEuler([
            random.uniform(0, 3.14), random.uniform(0, 3.14), random.uniform(0, 3.14)
        ])
        rock_shape = p.createCollisionShape(p.GEOM_BOX, halfExtents=[size, size, size])
        rock_visual = p.createVisualShape(p.GEOM_BOX, halfExtents=[size, size, size], rgbaColor=[0.5, 0.5, 0.5, 1])
        p.createMultiBody(baseMass=0, baseCollisionShapeIndex=rock_shape, baseVisualShapeIndex=rock_visual,
                          basePosition=[x, y, z], baseOrientation=orientation)

def make_arena(arena_size=10, wall_height=1):
    wall_thickness = 0.5
    floor_collision_shape = p.createCollisionShape(shapeType=p.GEOM_BOX, halfExtents=[arena_size/2, arena_size/2, wall_thickness])
    floor_visual_shape = p.createVisualShape(shapeType=p.GEOM_BOX, halfExtents=[arena_size/2, arena_size/2, wall_thickness],
                                             rgbaColor=[1, 1, 0, 1])
    p.createMultiBody(baseMass=0, baseCollisionShapeIndex=floor_collision_shape,
                      baseVisualShapeIndex=floor_visual_shape, basePosition=[0, 0, -wall_thickness])

    wall_collision_shape = p.createCollisionShape(shapeType=p.GEOM_BOX, halfExtents=[arena_size/2, 0.25, wall_height/2])
    wall_visual_shape = p.createVisualShape(shapeType=p.GEOM_BOX, halfExtents=[arena_size/2, 0.25, wall_height/2],
                                            rgbaColor=[0.7, 0.7, 0.7, 1])
    # Create four walls
    p.createMultiBody(0, wall_collision_shape, wall_visual_shape, [0, arena_size/2, wall_height/2])
    p.createMultiBody(0, wall_collision_shape, wall_visual_shape, [0, -arena_size/2, wall_height/2])

    wall_collision_shape2 = p.createCollisionShape(shapeType=p.GEOM_BOX, halfExtents=[0.25, arena_size/2, wall_height/2])
    wall_visual_shape2 = p.createVisualShape(shapeType=p.GEOM_BOX, halfExtents=[0.25, arena_size/2, wall_height/2],
                                             rgbaColor=[0.7, 0.7, 0.7, 1])
    p.createMultiBody(0, wall_collision_shape2, wall_visual_shape2, [arena_size/2, 0, wall_height/2])
    p.createMultiBody(0, wall_collision_shape2, wall_visual_shape2, [-arena_size/2, 0, wall_height/2])

def main(csv_file):
    assert os.path.exists(csv_file), f"Tried to load {csv_file} but it does not exist"

    # Connect to PyBullet GUI only here!
    p.connect(p.GUI)
    p.setPhysicsEngineParameter(enableFileCaching=0)
    p.configureDebugVisualizer(p.COV_ENABLE_GUI, 0)
    p.setAdditionalSearchPath(pybullet_data.getDataPath())
    p.setGravity(0, 0, -10)

    p.resetDebugVisualizerCamera(
        cameraDistance=15,
        cameraYaw=45,
        cameraPitch=-45,
        cameraTargetPosition=[0, 0, 0]
    )


    arena_size = 20
    make_arena(arena_size=arena_size)

    mountain_position = (0, 0, 0)
    mountain_orientation = p.getQuaternionFromEuler((0, 0, -1))
    p.setAdditionalSearchPath('shapes/')
    mountain = p.loadURDF("gaussian_pyramid.urdf", mountain_position, mountain_orientation, useFixedBase=1)

    #p.setRealTimeSimulation(1)

    cr = creature.Creature(gene_count=1)
    dna = genome.Genome.from_csv(csv_file)
    cr.update_dna(dna)

    with open('test.urdf', 'w') as f:
        f.write(cr.to_xml())

    rob1 = p.loadURDF('test.urdf')
    p.resetBasePositionAndOrientation(rob1, [6, 6, 2], [0, 0, 0, 1])

    start_pos, orn = p.getBasePositionAndOrientation(rob1)

    elapsed_time = 0
    wait_time = 1.0 / 240
    total_time = 90
    step = 0

    while True:
        p.stepSimulation()
        step += 1
        if step % 24 == 0:
            motors = cr.get_motors()
            assert len(motors) == p.getNumJoints(rob1), "Something went wrong: joint count mismatch"
            for jid in range(p.getNumJoints(rob1)):
                vel = motors[jid].get_output()
                p.setJointMotorControl2(rob1, jid, controlMode=p.VELOCITY_CONTROL, targetVelocity=vel)
            new_pos, orn = p.getBasePositionAndOrientation(rob1)
            dist_moved = np.linalg.norm(np.asarray(start_pos) - np.asarray(new_pos))
            print(dist_moved)

        time.sleep(wait_time)
        elapsed_time += wait_time
        if elapsed_time > total_time:
            break

    print("TOTAL DISTANCE MOVED:", dist_moved)

if __name__ == "__main__":
    assert len(sys.argv) == 2, "Usage: python cw-envt.py csv_filename"
    main(sys.argv[1])
