
import math
import numpy as np
from vispy import app, scene


body_1_pos=np.array([-20000, 40000, 1000000], dtype=np.float64)
body_2_pos=np.array([10000, 900000, 30000], dtype=np.float64)

ray_start_pos=body_1_pos + 1000#assume body 1 emits the ray

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
    distance=1000000,
    translate_speed=100000
)

# Create first sphere
sphere1 = scene.visuals.Sphere(
    radius=100000,
    method='latitude',
    subdivisions=30,
    color=(1, 1, 1, 1),
    parent=view.scene
)

# Position first sphere
sphere1.transform = scene.transforms.STTransform(
    translate=(body_1_pos[0], body_1_pos[1], body_1_pos[2])
)

# Create second sphere
sphere2 = scene.visuals.Sphere(
    radius=100000,
    method='latitude',
    subdivisions=30,
    color=(1.0, 0.3, 0.2, 1.0),
    parent=view.scene
)

# Position second sphere
sphere2.transform = scene.transforms.STTransform(
    translate=(body_2_pos[0], body_2_pos[1], body_2_pos[2])
)


# # Generate helix coordinates
# t = np.linspace(0, 2*np.pi, 200)

# x = 2 * np.cos(t)
# y = 2 * np.sin(t)
# z = t / 2

start_pos = ray_start_pos#np.array([20.0, 2.0, 0.0], dtype=np.float64)#ray_start_pos #
start_vel = np.array([0.0,3*pow(10,8), 0.0], dtype=np.float64)
#MAKE SURE NUMPY ARRAYS ARE USED FOR DIFFERENCE FINDING

#Force=G*((m1*m2)/r^2)
time_step = 0.0001
steps = 10000
pos_log = np.zeros((steps, 3), dtype=np.float64)
G = 6.67 * pow(10,-11)

mass_body_1 = 6 * pow(10, 24)
mass_body_2 = 250 * pow(10, 31)
mass_body_3 = 6 * pow(10, -22)




current_pos = start_pos
pos_log[0] = current_pos
current_vel = start_vel





for i in range(1,steps):

    vector_1= body_1_pos - current_pos
    vector_2= body_2_pos - current_pos

    # distance_diff = math.sqrt((vector_1[0] ** 2) +(vector_1[1] ** 2) + (vector_1[2] ** 2))
    # Crazy they have this wowee numpy magic
    distance_1 = np.linalg.norm(vector_1)
    distance_2 = np.linalg.norm(vector_2)

    unit_vector_1 = vector_1 / distance_1
    unit_vector_2 = vector_2 / distance_2

    force_on_ob_1 = G * ((mass_body_3 * mass_body_1)/(distance_1**2))
    force_on_ob_2 = G * ((mass_body_3 * mass_body_2)/(distance_2**2))

    force_vector = (unit_vector_1 * force_on_ob_1) + (unit_vector_2 * force_on_ob_2)

    accleration = (force_vector/mass_body_3)

    distance_step = (current_vel*time_step) + (0.5 * (accleration) * (time_step**2))

    current_pos += distance_step
    current_vel += (accleration) * time_step
    pos_log[i] = current_pos
# distance = (force_vector/mass_body_3) * time^2
# print(pos_log)
print("Total displacement:", pos_log[-1] - pos_log[0])
#Force = Mass * Accleration
#Acceleartion = Velocity / time
#Velocity = distance / time


#Distance = (u*t) * 1/2 * ((force/mass) * time^2)

marker1 = scene.visuals.Sphere(
    radius=10000,
    method='latitude',
    subdivisions=30,
    color=(0.5, 0.5, 0.5, 1.0),
    parent=view.scene
)

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




# Combine coordinates into an N x 3 array
# pos = np.column_stack((x, y, z))

# Create curved line
curve = scene.visuals.Line(
    pos=pos_log,
    color='cyan',
    width=3,
    method='gl',
    parent=view.scene
)


# Add XYZ coordinate axes
axis = scene.visuals.XYZAxis(
    parent=view.scene
)

# Run application
if __name__ == '__main__':
    app.run()
