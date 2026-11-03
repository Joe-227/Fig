import math
import numpy as np


#body 2 is the black hole (the one with the crazy mass duh)

def ray_sim(ray_start_pos,ray_vector,body_1_pos,body_2_pos):

    c=3*pow(10,8)
    start_pos = ray_start_pos#np.array([20.0, 2.0, 0.0], dtype=np.float64)#ray_start_pos #
    ray_vector = np.asarray(ray_vector, dtype=np.float64)
    ray_vector = ray_vector / np.linalg.norm(ray_vector)
    start_vel = ray_vector * c



    
    #MAKE SURE NUMPY ARRAYS ARE USED FOR DIFFERENCE FINDING

    #Force=G*((m1*m2)/r^2)
    time_step = 0.001
    steps = 10000
    pos_log = np.zeros((steps, 3), dtype=np.float64)
    G = 6.67 * pow(10,-11)

    mass_body_1 = 6 * pow(10, 24)
    mass_body_2 = 250 * pow(10, 31)
    mass_body_3 = 6 * pow(10, -22)


    event_horizon_radius=(2*G*mass_body_2)/(c**2)
    # print(event_horizon_radius)


    #for loop here for multi rays?

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

        force_on_ob_1 =  G * ((mass_body_3 * mass_body_1)/(distance_1**2))
        force_on_ob_2 =  2* G * ((mass_body_3 * mass_body_2)/(distance_2**2))

        force_vector = (unit_vector_1 * force_on_ob_1) + (unit_vector_2 * force_on_ob_2)

        accleration = (force_vector/mass_body_3)

        distance_step = (current_vel*time_step) + (0.5 * (accleration) * (time_step**2))

        current_pos += distance_step
        current_vel += (accleration) * time_step
        pos_log[i] = current_pos

        distance_to_blackhole = np.linalg.norm(current_pos - body_2_pos)

        if distance_to_blackhole <= event_horizon_radius:
            break

    return [pos_log[:i+1], event_horizon_radius]