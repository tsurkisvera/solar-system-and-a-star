# Stellar Flyby Simulation
A numerical simulation of the Solar System interacting with a passing star, written in Python.
The project models gravitational dynamics between the Sun, planets, and a flyby star using NumPy for computation and Matplotlib for visualization (2D & 3D animations).

## Features
<dl>
  <dd> N-body simulation (Sun + planets + flyby star)</dd>
  <dd> NumPy-based integration (Implicit Runge-Kutta method of Radau family, order 5), flexible </dd>
  <dd> 2D or 3D Matplotlib animations </dd>
</dl>

## Description 
`body.py` - class, which stores all bodies in the simulation and tracks position and velocities

`solve.py` - performes trajectories integration 

`test.ipynb` - creates and runs simulations, saves time ans positions history`

`animation.ipynb` and `animation_2D.ipynb` - perform animation and save `.mp4` visualizations
