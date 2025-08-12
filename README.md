#E&M Wave Simulator
>This is an interactive electromagnetic wave simulator built with Python with an intuitive GUI for visualizing electric E and magnetic B field components of plane waves.
>This project uses Matplotlib, NumPy, and Tkinter to provide a dynamic and customizable experience for exploring the fundamentals of wave propagation.

Features:
>Interactive GUI for adjusting wave parameters such as medium of propogation (adjusting speed of light option), amplitude, wavelength, frequency, propogation direction, orientation in space and phase.
>Real-time animated visualization of E and B field components.
>Simple and educational interface for learning maxwell's equations visually

Tech Stack: 
>Python, Matplotlib (for plotting and animation)
>NumPy (for numerical calculations)
>Tkinter (for GUI controls and parameter inputs)

How to use:
>Ensure that you have python 3 installed.
>Run the simulator: python GUI.py

Working Principle:
Physics involved -> Maxwell's equation, wave equation
E(s, t) = E₀ * sin(ks - ωt + φ) (electric field wave)
B(s, t) = B₀ * sin(ks - ωt + φ) (magnetic field wave)

Program structure:
> Build.py - Defines the planewave() class that calculates E and B from given parameters (θ, φ, polarization angle)
> viewer.py - visualizes the 3D EM waves
> GUI.py - handles the actual application user interface with tkinter


Enjoy!!!
