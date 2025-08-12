import numpy as np

pi_v = np.pi
#c = 3 speed of light in vaccum

class planewave:
    #create a class of wave using parameters of wave equation
    #we will create 2 instances - E wave and B wave
    # default parameters in constructor
    def __init__(self, A=1.0, lam=2.5, c=3, theta_deg=20, phi_deg=35, 
                 pol_angle_deg=0, n_arrows=18, extent=6.0): 
        #create helper methods
        self.set_params(A, lam, c, theta_deg, phi_deg, pol_angle_deg) #set physics parameters and calculate values of k and w
        self.set_geometry(n_arrows, extent)   # calc
    def set_params(self, A, lam, c, theta_deg, phi_deg, pol_angle_deg):
        self.A=float(A)
        self.lam=float(lam)
        self.c=float(c)
        self.k=2*pi_v/self.lam
        self.w = self.c * self.k
        #converting to spherical coordinates
        #convert degrees to radians to degrees
        th = np.deg2rad(theta_deg) #propogation direction angle
        ph = np.deg2rad(phi_deg)   #rotation around z axis in xy plane
# user enters direction in degrees, convert that to radians as numpy's trig func work only in radians and then convert to cartesian coordinates for vector math
        self.k_hat = np.array([np.sin(th)*np.cos(ph), #x componeny
                              np.sin(th)*np.sin(ph),   #y component
                              np.cos(th)])   #z component
        # spherical coordinates to cartesian coordinates
        # k hat is unit direction vector Ehat must be perp to khat and Bhat must be perp to Ehat
        # formula becomes E=Enaughtsin(k(khat dot r) - wt) instead of Enaughtsin(kx-wt) as we are building 3d wave simulator and wave can go in ANY direction not just x
        # (u, v, khat)
        # choose helper temporary vector NOT perp to khat
        tmp = np.array([0,0,1]) if abs(self.k_hat[2])<0.9 else np.array([1,0,0])
        # we can get u and v from cross product of temp with k
        # u is the direction in which E wave oscilates and v is the direction in which B wave oscilates and they both propogate along k hate
        # we have only k hat now so to find u and v we use a temp direction not parallel to k hat to fing orthogonal vector
        u = np.cross(self.k_hat, tmp) 
        u /= np.linalg.norm(u)
        v = np.cross(self.k_hat, u)
        v /= np.linalg.norm(v) #normalize the vectors

        ang = np.deg2rad(pol_angle_deg)
        self.E_hat = np.cos(ang)*u + np.sin(ang)*v
        self.E_hat /= np.linalg.norm(self.E_hat)
        self.B_hat = np.cross(self.k_hat, self.E_hat)

    def set_geometry(self, n_arrows, extent):
        self.n = int(n_arrows) # how many arrows in wave path
        self.ext = float(extent) #total length of wave section
        s = np.linspace(-self.ext*0.8, self.ext*0.8, self.n) # n evenly spaced numbers between a and b 80% of the space being utilized by the diagram animation
        self.line_pts = s[:,None] * self.k_hat[None,:] 
        self.line_pts = s[:,None] * self.k_hat[None,:]
        self.s_coords = s  

    def fields_at(self, t): #calculate E and B at a given t
        phase = self.k*self.s_coords - self.w*t         #ks - wt for each arrow position
        Et = self.A*np.sin(phase)                       # amplitudes
        Bt = (self.A/self.c)*np.sin(phase)              # B = E/c
# E = Enaughtsin(ks - wt)
        E = Et[:,None]*self.E_hat[None,:]                # (n,3) row vector
        B = Bt[:,None]*self.B_hat[None,:]                # (n,3)
        return self.line_pts, E, B
# planes on which waves will be drawn transulecnt
    def planes(self):
        def quad(center, a_hat, b_hat, ha, hb):
            p1 = center + ha*a_hat + hb*b_hat
            p2 = center - ha*a_hat + hb*b_hat
            p3 = center - ha*a_hat - hb*b_hat
            p4 = center + ha*a_hat - hb*b_hat
            return np.array([p1,p2,p3,p4])
        center = np.zeros(3)
        Eplane = quad(center, self.k_hat, self.E_hat, self.ext*0.7, self.ext*0.35)
        Bplane = quad(center, self.k_hat, self.B_hat, self.ext*0.7, self.ext*0.35)
        return Eplane, Bplane











