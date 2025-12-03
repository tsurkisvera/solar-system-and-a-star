import numpy as np

def solve_from_scratch(solar_system):
    my_time = 0
    history = [[solar_system.initial_positions.copy()], [solar_system.initial_velocities.copy()]]
    print(history)
    my_positions = solar_system.initial_positions.copy()
    my_velocities = solar_system.initial_velocities.copy()
    my_masses = solar_system.masses.copy() 
    my_names = solar_system.names.copy()
    while my_time < solar_system.time:
        new_positions, new_velocities = step(solar_system, my_positions, my_velocities, my_masses)
        history[0].append(new_positions.copy())
        history[1].append(new_velocities.copy())
        my_positions, my_velocities = new_positions, new_velocities
        my_time += solar_system.time_step
    print(history)
    solar_system.history = history.copy()

def calculate_accelerations(my_positions, my_masses, my_names, my_account_for):
    if my_account_for=='only_Sun':
        solar_index = np.where(my_names=='Sun')
        mask = np.invert(solar_index)
        solar_mass = my_masses[solar_index][0]
        solar_position = my_positions[solar_index][0]
        relative_positions = my_positions-solar_position
        accelerations = np.array([-solar_mass*element/(element[0]**2+element[1]**2+element[2]**2)**(3/2) if i!=solar_index[0] else [0, 0, 0] for i, element in enumerate(relative_positions)])
        return accelerations

    elif my_account_for=='Sun_and_star':
        solar_index = np.where(my_names=='Sun')
        mask = np.invert(solar_index)
        solar_mass = my_masses[solar_index][0]
        solar_position = my_positions[solar_index][0]
        relative_positions = my_positions-solar_position
        accelerations_sun = np.array([-solar_mass*element/(element[0]**2+element[1]**2+element[2]**2)**(3/2) if i!=solar_index[0] else [0, 0, 0] for i, element in enumerate(relative_positions)])
        solar_index = np.where(my_names=='Star')
        mask = np.invert(solar_index)
        solar_mass = my_masses[solar_index][0]
        solar_position = my_positions[solar_index][0]
        relative_positions = my_positions-solar_position
        accelerations_star = np.array([-solar_mass*element/(element[0]**2+element[1]**2+element[2]**2)**(3/2) if i!=solar_index[0] else [0, 0, 0] for i, element in enumerate(relative_positions)])
        return accelerations_sun + accelerations_star
    else:
        error_msg = f'I cannot do it yet: account for {my_account_for}'
        raise ValueError(error_msg)

def step(solar_system, my_positions, my_velocities, my_masses):
    my_masses = solar_system.masses 
    my_names = solar_system.names 
    my_account_for = solar_system.account_for 
    my_accelerations = calculate_accelerations(my_positions, my_masses, my_names, my_account_for)
    my_positions += my_velocities*solar_system.time_step
    my_velocities += my_accelerations*solar_system.time_step
    return my_positions, my_velocities

########### From simple explicit scheme to Runge-Kutta (explicit OR implicit) ############

from scipy.integrate import solve_ivp 
def my_system(t, y, my_masses, my_names, my_account_for):
    n_bodies = my_names.shape[0]
    my_positions = np.array([y[0:n_bodies], y[n_bodies:2*n_bodies], y[2*n_bodies:3*n_bodies]]).T
    my_velocities = np.array([y[3*n_bodies:4*n_bodies], y[4*n_bodies:5*n_bodies], y[5*n_bodies:6*n_bodies]]).T
    my_accelerations = calculate_accelerations(my_positions, my_masses, my_names, my_account_for)
    return np.concatenate((my_velocities[:, 0], my_velocities[:, 1], my_velocities[:, 2],
                            my_accelerations[:, 0], my_accelerations[:, 1], my_accelerations[:, 2]), axis=None)

def run_model(system, y0, t_span, t_eval, vectorization, args):
    sol = solve_ivp(system, t_span=t_span, y0=y0, t_eval=t_eval, vectorized=vectorization, args=args, method='Radau')
    return sol

def solve(solar_system):
    my_positions = solar_system.initial_positions.copy()
    my_velocities = solar_system.initial_velocities.copy()
    evaluation_time = np.arange(0, solar_system.time, solar_system.time_step)
    solar_system.history = run_model(
                                    system=my_system,
                                    y0=list(np.concatenate((my_positions[:, 0], my_positions[:, 1], my_positions[:, 2],
                                                        my_velocities[:, 0], my_velocities[:, 1], my_velocities[:, 2]), axis=None)),
                                    t_span=[0., solar_system.time],
                                    t_eval=evaluation_time, 
                                    vectorization=False,
                                    args=(solar_system.masses.copy(), solar_system.names.copy(), solar_system.account_for)
                                    )