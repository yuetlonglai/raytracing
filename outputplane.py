from raytracer import Ray
from opticalelement import OpticalElement
from refracting_surfaces import SphericalRefraction
import numpy as np

class OutputPlane(OpticalElement):
    def __init__(self,z1):
        self._outputz = z1
    
    def intercept(self,ray):
        #print(ray.p(),ray.k())
        l = (self._outputz - (ray.p())[2])/((ray.k()/np.linalg.norm(ray.k()))[2])
        return ray.p() + (ray.k()/np.linalg.norm(ray.k())) * l
    
    def propagate_ray(self, ray):
        ray.append(self.intercept(ray),ray.k())

        