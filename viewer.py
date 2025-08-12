import numpy as np, matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.animation import FuncAnimation
from Build import planewave


model = planewave() #instance of planewave class
Eplane, Bplane = model.planes() #gives 2 rectangles E-plane and B-plane to show orientation
plt.ion()
fig = plt.figure(figsize=(8.5,6.5))
ax = fig.add_subplot(111, projection='3d')
ext = model.ext
ax.set_xlim(-ext,ext); ax.set_ylim(-ext,ext); ax.set_zlim(-ext,ext)
ax.set_xlabel('x'); ax.set_ylabel('y'); ax.set_zlabel('z')
ax.set_title('EM Wave — class-based (E ⟂ B ⟂ k)')

# k̂ arrow + travel line
ax.quiver(0,0,0, *model.khat, length=ext*0.9, color='k', linewidth=2)
s = model.s_coords; pts = model.line_pts
ax.plot(pts[:,0], pts[:,1], pts[:,2], '--', color='0.6', linewidth=1)

# translucent planes
Ecoll = Poly3DCollection([Eplane], facecolor=(0.1,0.6,0.1,0.15), edgecolor='none')
Bcoll = Poly3DCollection([Bplane], facecolor=(0.8,0.2,0.2,0.15), edgecolor='none')
ax.add_collection3d(Ecoll); ax.add_collection3d(Bcoll)

E_quiv = B_quiv = None
t, dt = 0.0, 0.03

def update(_):
    global E_quiv, B_quiv, t
    if E_quiv: E_quiv.remove()
    if B_quiv: B_quiv.remove()

    P, E, B = model.fields_at(t)
    E_quiv = ax.quiver(P[:,0],P[:,1],P[:,2], E[:,0],E[:,1],E[:,2],
                       length=1.0, normalize=False, color='tab:green')
    B_quiv = ax.quiver(P[:,0],P[:,1],P[:,2], B[:,0],B[:,1],B[:,2],
                       length=1.0, normalize=False, color='tab:red')
    t += dt
    return E_quiv, B_quiv

ani = FuncAnimation(fig, update, interval=30, blit=False)
plt.tight_layout(); plt.show()
