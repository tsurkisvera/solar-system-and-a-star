import numpy as np
from solve_motion import solve 
#from visualize_motion import visualize 

class Solar_system():
    def __init__(self, names=None, masses=None, initial_positions=None, initial_velocities=None,
                    time=None, time_step=None, history=-1, recalc=False, account_for='only_Sun', grid_size=32, grid_resolution=0.1):
        self.names = names
        self.initial_positions = initial_positions
        self.initial_velocities = initial_velocities
        self.history = history
        self.masses = masses 
        self.time = time
        self.time_step = time_step
        self.recalc = recalc
        self.account_for = account_for
        self.grid_size = grid_size
        self.grid_resolution = grid_resolution

    def add_body(self, name, mass, initial_position, initial_velocity):
        self.names = np.append(self.names, name)
        self.masses = np.append(self.masses, mass)
        self.initial_positions = np.append(self.initial_positions, initial_position, axis=0)
        self.initial_velocities = np.append(self.initial_velocities, initial_velocity, axis=0)
        self.recalc = True

    def do_calculations(self):
        if self.recalc or self.history==-1:
            solve(self)
            self.recalc = False
        else:
            pass
        # visualize(self)        