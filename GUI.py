# GUI3D.py
import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from Build import planewave
#c=3
class EM3DApp:
    def __init__(self, root):
        self.root = root
        root.title("E and M wave simulator app")

        #modelling time 
        self.model = planewave()           # default params
        self.t, self.dt = 0.0, 0.03
        self.running = False

        # the space / layout
        wrap = ttk.Frame(root, padding=8); wrap.grid(sticky="nsew")
        root.rowconfigure(0, weight=1); root.columnconfigure(0, weight=1)
        self.left = ttk.Frame(wrap); self.left.grid(row=0, column=0, sticky="nsw", padx=(0,10))
        self.right = ttk.Frame(wrap); self.right.grid(row=0, column=1, sticky="nsew")
        wrap.columnconfigure(1, weight=1); wrap.rowconfigure(0, weight=1)

        # all the controls
        self.vars = {
            "A": tk.DoubleVar(value=1.0),
            "lam": tk.DoubleVar(value=2.5),
            "c": tk.DoubleVar(value=1.0),
            "theta": tk.DoubleVar(value=20.0),
            "phi": tk.DoubleVar(value=35.0), #set to defaukt values
            "pol": tk.DoubleVar(value=0.0),
            "n": tk.IntVar(value=18),
            "extent": tk.DoubleVar(value=6.0),
            "showE": tk.BooleanVar(value=False),
            "showB": tk.BooleanVar(value=True),
            "planes": tk.BooleanVar(value=False),
        }

        def add_slider(label, v, a, b, step=0.1):
            ttk.Label(self.left, text=label).pack(anchor="w")
            s = ttk.Scale(self.left, from_=a, to=b, orient="horizontal", variable=v)
            s.pack(fill="x", padx=2, pady=2)
            e = ttk.Entry(self.left, textvariable=v, width=8); e.pack(anchor="w", padx=2, pady=(0,6))

        add_slider("Amplitude A", self.vars["A"], 0.0, 3.0)
        add_slider("Wavelength λ", self.vars["lam"], 0.5, 6.0)
        add_slider("Speed c", self.vars["c"], 0.2, 3.0)
        add_slider("Direction θ (deg) (Up/down)", self.vars["theta"],   0.0, 180.0)
        add_slider("Direction φ (deg) (Left/Right)", self.vars["phi"],     0.0, 360.0)
        add_slider("Polarization angle (deg) (offset)", self.vars["pol"], -180.0, 180.0)
        add_slider("Arrow count", self.vars["n"], 6, 40)
        add_slider("Extent", self.vars["extent"], 3.0, 12.0)

        #ttk.Checkbutton(self.left, text="Show E", variable=self.vars["showE"]).pack(anchor="w")
        #ttk.Checkbutton(self.left, text="Show B", variable=self.vars["showB"]).pack(anchor="w")
        ttk.Checkbutton(self.left, text="Show planes", variable=self.vars["planes"]).pack(anchor="w")

        btns = ttk.Frame(self.left); btns.pack(fill="x", pady=8)
        ttk.Button(btns, text="Apply", command=self.apply_params).pack(side="left", expand=True, fill="x", padx=2)
        self.run_btn = ttk.Button(btns, text="Run ▶", command=self.toggle_run)
        self.run_btn.pack(side="left", expand=True, fill="x", padx=2)
        ttk.Button(btns, text="Reset", command=self.reset).pack(side="left", expand=True, fill="x", padx=2)

        # ----- figure (3D) -----
        self.fig = plt.Figure(figsize=(8,6))
        self.ax = self.fig.add_subplot(111, projection="3d")
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.right)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        self.E_quiv = None
        self.B_quiv = None
        self.Eplane_coll = None; self.Bplane_coll = None
        self._init_axes()
        self.apply_params()
        self._animate()

        
    def _safe_remove(self, artist):
        if artist is None:
            return
        try:
            artist.remove()         # works if still attached
        except Exception:
            # Fallback: if it's a collection and still in ax.collections, pop it
            if hasattr(self.ax, "collections") and artist in self.ax.collections:
                self.ax.collections.remove(artist)
        # finally, forget it
    
    def _init_axes(self):
        ext = self.vars["extent"].get()
        ax = self.ax
        ax.clear()
        self.E_quiv = None
        self.B_quiv = None
        self.Eplane_coll = None
        self.Bplane_coll = None
        ax.set_xlim(-ext, ext); ax.set_ylim(-ext, ext); ax.set_zlim(-ext, ext)
        ax.set_xlabel("x"); ax.set_ylabel("y"); ax.set_zlabel("z")
        ax.set_title("E ⟂ B ⟂ k — 3D Plane Wave")

        # faint coordinate axes
        ax.plot([-ext, ext], [0,0], [0,0], color='0.85', linewidth=1)
        ax.plot([0,0], [-ext, ext], [0,0], color='0.85', linewidth=1)
        ax.plot([0,0], [0,0], [-ext, ext], color='0.85', linewidth=1)

        # k̂ arrow
        ax.quiver(0,0,0, *self.model.k_hat, length=ext*0.9, color='k', linewidth=2)
        ax.text(*(self.model.k_hat*ext*0.95), "k̂")

        # travel line
        P = self.model.line_pts
        ax.plot(P[:,0], P[:,1], P[:,2], '--', color='0.6', linewidth=1)

    def apply_params(self):
        # update model parameters & geometry from sliders
        self.model.set_params(
            A=self.vars["A"].get(),
            lam=self.vars["lam"].get(),
            c=self.vars["c"].get(),
            theta_deg=self.vars["theta"].get(),
            phi_deg=self.vars["phi"].get(),
            pol_angle_deg=self.vars["pol"].get()
        )
        self.model.set_geometry(self.vars["n"].get(), self.vars["extent"].get())
        self._init_axes()  # redraw axes/line with new geometry

        # planes
        if self.Eplane_coll: self.Eplane_coll.remove()
        if self.Bplane_coll: self.Bplane_coll.remove()
        Eplane, Bplane = self.model.planes()
        if self.vars["planes"].get():
            self.Eplane_coll = Poly3DCollection([Eplane], facecolor=(0.1,0.6,0.1,0.15), edgecolor='none')
            self.Bplane_coll = Poly3DCollection([Bplane], facecolor=(0.8,0.2,0.2,0.15), edgecolor='none')
            self.ax.add_collection3d(self.Eplane_coll)
            self.ax.add_collection3d(self.Bplane_coll)

        self.canvas.draw_idle()

    def toggle_run(self):
        self.running = not self.running
        self.run_btn.config(text="Pause ⏸" if self.running else "Run ▶")

    def reset(self):
        self.t = 0.0

    def _animate(self):
        # we need to remove old quivers
        if self.E_quiv: self.E_quiv.remove()
        if self.B_quiv: self.B_quiv.remove()

        P, E, B = self.model.fields_at(self.t)
        showE, showB = self.vars["showE"].get(), self.vars["showB"].get()

        self.E_quiv = self.ax.quiver(P[:,0], P[:,1], P[:,2],
                                         E[:,0], E[:,1], E[:,2],
                                         length=1.0, normalize=False, color='tab:green')
            
        self.B_quiv = self.ax.quiver(P[:,0], P[:,1], P[:,2],
                                         B[:,0], B[:,1], B[:,2],
                                         length=1.0, normalize=False, color='tab:red')

        self.canvas.draw_idle()
        if self.running:
            self.t += self.dt
        self.root.after(25, self._animate)  # 60 frames per secdond

def main():
    root = tk.Tk()
    EM3DApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
