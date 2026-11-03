
import math
import random
import numpy as np
from vispy import app, scene
from ray_simulation import ray_sim


# Currently this script generates random rays shooting out of the star, if they intersect the blackhole then they get swallowed

#Okay the plan for next time. I want to add an accrecian...accreshan? ackreeshain... a matter disk around the black hole
# and each time a light ray intersects the disk and line of sight to the camera is found and not swallowed up (this line of sight is also a ray affected by gravity which may
# vastily increase the ray count... perhaps relooking at some ray tracing tutorials and fundamentals should be looked at)






star_radius = 100000


body_1_pos=np.array([-2000000, 4000000, 10000000], dtype=np.float64)
body_2_pos=np.array([0, 0, 0], dtype=np.float64)




# Create the application
canvas = scene.SceneCanvas(
    keys='interactive',
    size=(1000, 700),
    show=True,
    title='VisPy - Two 3D Spheres'
)

# Create a 3D view
view = canvas.central_widget.add_view()

# Set 3D camera
view.camera = scene.TurntableCamera(
    fov=45,
    elevation=25,
    azimuth=45,
    distance=10000000,
    translate_speed=300000,
    center=(body_2_pos[0], body_2_pos[1], body_2_pos[2])
)




# # Generate helix coordinates
# t = np.linspace(0, 2*np.pi, 200)

# x = 2 * np.cos(t)
# y = 2 * np.sin(t)
# z = t / 2



for test_loop in range(100):

    x_angle= random.uniform(0,2*math.pi)
    y_angle= random.uniform(0,2*math.pi)

    # print(x_angle)

    x=math.cos(x_angle)
    y=math.sin(x_angle)
    z=math.sin(y_angle)

    # y=0
    # z=0

    # print(x)
    # print(y)
    # print(z)
 # np.linalg.norm(vector_1)?? use this for distance stuff of a vecotr?
    ray_vector=np.array([x, y, z], dtype=np.float64)
    ray_start_pos=body_1_pos + (ray_vector*star_radius)#assume body 1 emits the ray
    [pos_log,event_horizon_radius]=ray_sim(ray_start_pos,ray_vector,body_1_pos,body_2_pos)

    marker1 = scene.visuals.Sphere(
    radius=10000,
    method='latitude',
    subdivisions=30,
    color=(0.5, 0.5, 0.5, 1.0),
    parent=view.scene)

    # Position second sphere
    marker1.transform = scene.transforms.STTransform(
        translate=(pos_log[0])
    )
    marker2 = scene.visuals.Sphere(
        radius=10000,
        method='latitude',
        subdivisions=30,
        color=(0.5, 0.5, 0.5, 1.0),
        parent=view.scene
    )

    # Position second sphere
    marker2.transform = scene.transforms.STTransform(
        translate=(pos_log[-1])
    )

    curve = scene.visuals.Line(
        pos=pos_log,
        color='cyan',
        width=3,
        method='gl',
        parent=view.scene
    )



# Create first sphere
sphere1 = scene.visuals.Sphere(
    radius=star_radius,
    method='latitude',
    subdivisions=30,
    color=(1, 1, 1, 0.1),
    parent=view.scene
)

# Position first sphere
sphere1.transform = scene.transforms.STTransform(
    translate=(body_1_pos[0], body_1_pos[1], body_1_pos[2])
)

# # Create second sphere
# sphere2 = scene.visuals.Sphere(
#     radius=event_horizon_radius,
#     method='latitude',
#     subdivisions=30,
#     color=(1.0, 0.3, 0.2, 1),
#     parent=view.scene
# )

# # Position second sphere
# sphere2.transform = scene.transforms.STTransform(
#     translate=(body_2_pos[0], body_2_pos[1], body_2_pos[2])
# )





# Add XYZ coordinate axes
# axis = scene.visuals.XYZAxis(
#     parent=view.scene
# )

# Run application
if __name__ == '__main__':
    app.run()
