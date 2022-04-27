import numpy as np

class Ray:
    def __init__(self, i=[0.0,0.0,0.0], b=[0.0,0.0,0.0]):
        self._point = i
        self._direction = b
        self._vect = np.array([self._point, self._direction])
        self._v = []
        self._v.append(self._point)
    
    def p(self):
        return self._point
    
    def k(self):
        return self._direction
    
    def append(self, new_i, new_b):
        self._point = new_i
        self._direction = new_b
        self._vect = np.array([self._point, self._direction])
        self._v.append(self._point)

    def vertices(self):
        return self._v

'''
class OpticalElement:
    def propagate_ray(self,ray):
        "propagate a ray through the optical element"
        raise NotImplementedError()

class SphericalRefraction(OpticalElement):
    def __init__(self, z, r, n11, n22, ar):
        OpticalElement.__init__(self)
        self._z0 = z
        self._radius = r
        self._aradius = ar
        self._n1 = n11
        self._n2 = n22
        self._curvature = 1/r

    def intercept(self, ray):
        l1 = -1*np.inner(ray[0],ray[1]) + np.sqrt(np.inner(ray[0],ray[1])**2 - (np.linalg.norm(ray[0])**2 - self._radius**2))
        l2 = -1*np.inner(ray[0],ray[1]) - np.sqrt(np.inner(ray[0],ray[1])**2 - (np.linalg.norm(ray[0])**2 - self._radius**2))
        if self._curvature == 0:
            return None
        elif l1>l2:
            return np.array(ray[0] + l1*ray[1])
        elif l2<l1:
            return np.array(ray[0] + l2*ray[1])
        else:
            return None
        
'''

